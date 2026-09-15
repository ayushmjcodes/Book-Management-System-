/**
 * dashboard.js
 * Loads and renders the note grid, and wires up search, category
 * filtering, favorites-only filtering, pin/favorite/delete actions,
 * and creating new categories.
 */

const currentFilters = { search: "", categoryId: "", favoriteOnly: false };

document.addEventListener("DOMContentLoaded", () => {
  loadCategories();
  loadNotes();
  setupSearch();
  setupCategoryFilter();
  setupFavoriteFilter();
  setupCategoryModal();
});

function setupSearch() {
  const input = document.getElementById("searchInput");
  let debounceTimer;
  input.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      currentFilters.search = input.value.trim();
      loadNotes();
    }, 300); // wait for the user to stop typing before hitting the API
  });
}

function setupCategoryFilter() {
  const select = document.getElementById("categoryFilter");
  select.addEventListener("change", () => {
    currentFilters.categoryId = select.value;
    loadNotes();
  });
}

function setupFavoriteFilter() {
  const btn = document.getElementById("favoriteFilterBtn");
  btn.addEventListener("click", () => {
    currentFilters.favoriteOnly = !currentFilters.favoriteOnly;
    btn.classList.toggle("active", currentFilters.favoriteOnly);
    loadNotes();
  });
}

async function loadCategories() {
  try {
    const data = await apiRequest("/categories");
    const select = document.getElementById("categoryFilter");
    data.categories.forEach((cat) => {
      const option = document.createElement("option");
      option.value = cat.id;
      option.textContent = cat.name;
      select.appendChild(option);
    });
  } catch (err) {
    console.error("Failed to load categories:", err);
  }
}

async function loadNotes() {
  const params = new URLSearchParams();
  if (currentFilters.search) params.set("search", currentFilters.search);
  if (currentFilters.categoryId) params.set("category_id", currentFilters.categoryId);
  if (currentFilters.favoriteOnly) params.set("favorite", "true");

  try {
    const data = await apiRequest(`/notes?${params.toString()}`);
    renderNotes(data.notes);
  } catch (err) {
    console.error("Failed to load notes:", err);
  }
}

function renderNotes(notes) {
  const grid = document.getElementById("notesGrid");
  const emptyState = document.getElementById("emptyState");
  grid.innerHTML = "";

  if (notes.length === 0) {
    emptyState.classList.remove("hidden");
    return;
  }
  emptyState.classList.add("hidden");

  notes.forEach((note) => grid.appendChild(buildNoteCard(note)));
}

function buildNoteCard(note) {
  const card = document.createElement("div");
  card.className = "note-card" + (note.is_pinned ? " pinned" : "");

  const preview =
    note.content.length > 120 ? note.content.slice(0, 120) + "…" : note.content;

  card.innerHTML = `
    <div class="note-card-header">
      <h3>${escapeHtml(note.title)}</h3>
      ${note.is_pinned ? '<span class="pin-badge" title="Pinned">📌</span>' : ""}
    </div>
    <p class="note-preview">${preview ? escapeHtml(preview) : "<em>No content</em>"}</p>
    <div class="note-card-footer">
      <span class="note-category">${note.category_name ? escapeHtml(note.category_name) : "Uncategorized"}</span>
      <span class="note-date">${formatDate(note.updated_at)}</span>
    </div>
    <div class="note-card-actions">
      <button class="icon-btn fav-btn ${note.is_favorite ? "active" : ""}" title="Toggle favorite">⭐</button>
      <button class="icon-btn pin-btn ${note.is_pinned ? "active" : ""}" title="Toggle pin">📌</button>
      <a href="/notes/${note.id}" class="icon-btn" title="View note">👁</a>
      <a href="/notes/${note.id}/edit" class="icon-btn" title="Edit note">✏️</a>
      <button class="icon-btn delete-btn" title="Delete note">🗑</button>
    </div>
  `;

  card.querySelector(".fav-btn").addEventListener("click", () => toggleFavorite(note.id));
  card.querySelector(".pin-btn").addEventListener("click", () => togglePin(note.id));
  card.querySelector(".delete-btn").addEventListener("click", () => deleteNote(note.id, note.title));

  return card;
}

async function toggleFavorite(noteId) {
  try {
    await apiRequest(`/notes/${noteId}/favorite`, { method: "PATCH" });
    loadNotes();
  } catch (err) {
    alert("Failed to update favorite: " + err.message);
  }
}

async function togglePin(noteId) {
  try {
    await apiRequest(`/notes/${noteId}/pin`, { method: "PATCH" });
    loadNotes();
  } catch (err) {
    alert("Failed to update pin: " + err.message);
  }
}

async function deleteNote(noteId, title) {
  if (!confirm(`Delete "${title}"? This cannot be undone.`)) return;
  try {
    await apiRequest(`/notes/${noteId}`, { method: "DELETE" });
    loadNotes();
  } catch (err) {
    alert("Failed to delete note: " + err.message);
  }
}

function setupCategoryModal() {
  const modal = document.getElementById("categoryModal");
  const nameInput = document.getElementById("newCategoryName");

  document.getElementById("addCategoryBtn").addEventListener("click", () => {
    modal.classList.remove("hidden");
    nameInput.focus();
  });

  document.getElementById("cancelCategoryBtn").addEventListener("click", () => {
    modal.classList.add("hidden");
    nameInput.value = "";
  });

  document.getElementById("saveCategoryBtn").addEventListener("click", async () => {
    const name = nameInput.value.trim();
    if (!name) return;

    try {
      await apiRequest("/categories", { method: "POST", body: { name } });
      nameInput.value = "";
      modal.classList.add("hidden");

      // Refresh the filter dropdown so the new category shows up immediately.
      document.getElementById("categoryFilter").innerHTML =
        '<option value="">All Categories</option>';
      loadCategories();
    } catch (err) {
      alert("Failed to create category: " + err.message);
    }
  });
}
