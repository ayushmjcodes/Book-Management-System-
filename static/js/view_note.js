/**
 * view_note.js
 * Loads a single note's details into the read-only view page and
 * wires up the pin, favorite, edit, and delete actions.
 */

const noteId = document.body.dataset.noteId;

document.addEventListener("DOMContentLoaded", () => {
  loadNote();
  document.getElementById("pinBtn").addEventListener("click", handlePinClick);
  document.getElementById("favBtn").addEventListener("click", handleFavClick);
  document.getElementById("deleteBtn").addEventListener("click", handleDeleteClick);
});

async function loadNote() {
  try {
    const data = await apiRequest(`/notes/${noteId}`);
    const note = data.note;

    document.getElementById("noteTitle").textContent = note.title;
    document.getElementById("noteContent").textContent = note.content || "(No content)";
    document.getElementById("noteMeta").textContent =
      `${note.category_name || "Uncategorized"} • Created ${formatDate(note.created_at)} • Updated ${formatDate(note.updated_at)}`;
    document.getElementById("editLink").href = `/notes/${noteId}/edit`;

    updatePinButton(note.is_pinned);
    updateFavButton(note.is_favorite);
  } catch (err) {
    alert("Could not load note: " + err.message);
    window.location.href = "/dashboard";
  }
}

function updatePinButton(isPinned) {
  const btn = document.getElementById("pinBtn");
  btn.textContent = isPinned ? "📌 Unpin" : "📌 Pin";
  btn.classList.toggle("active", isPinned);
}

function updateFavButton(isFavorite) {
  const btn = document.getElementById("favBtn");
  btn.textContent = isFavorite ? "⭐ Unfavorite" : "⭐ Favorite";
  btn.classList.toggle("active", isFavorite);
}

async function handlePinClick() {
  try {
    const data = await apiRequest(`/notes/${noteId}/pin`, { method: "PATCH" });
    updatePinButton(data.note.is_pinned);
  } catch (err) {
    alert("Failed to update pin: " + err.message);
  }
}

async function handleFavClick() {
  try {
    const data = await apiRequest(`/notes/${noteId}/favorite`, { method: "PATCH" });
    updateFavButton(data.note.is_favorite);
  } catch (err) {
    alert("Failed to update favorite: " + err.message);
  }
}

async function handleDeleteClick() {
  if (!confirm("Delete this note? This cannot be undone.")) return;
  try {
    await apiRequest(`/notes/${noteId}`, { method: "DELETE" });
    window.location.href = "/dashboard";
  } catch (err) {
    alert("Failed to delete note: " + err.message);
  }
}
