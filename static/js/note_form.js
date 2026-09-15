/**
 * note_form.js
 * Shared logic for both the "Create Note" and "Edit Note" pages.
 * If <body data-note-id="..."> is set, we're editing an existing
 * note (pre-fill the form, PUT on submit, show the delete button).
 * Otherwise we're creating a new one (POST on submit).
 */

const noteId = document.body.dataset.noteId || null;
const noteForm = document.getElementById("noteForm");

document.addEventListener("DOMContentLoaded", async () => {
  await loadCategoryOptions();

  if (noteId) {
    await loadNoteIntoForm(noteId);

    const deleteBtn = document.getElementById("deleteBtn");
    if (deleteBtn) {
      deleteBtn.addEventListener("click", deleteCurrentNote);
    }
  }
});

async function loadCategoryOptions() {
  try {
    const data = await apiRequest("/categories");
    const select = document.getElementById("category");
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

async function loadNoteIntoForm(id) {
  try {
    const data = await apiRequest(`/notes/${id}`);
    document.getElementById("title").value = data.note.title;
    document.getElementById("content").value = data.note.content;
    if (data.note.category_id) {
      document.getElementById("category").value = data.note.category_id;
    }
  } catch (err) {
    showMessage("formMessage", "Could not load note: " + err.message, "error");
  }
}

noteForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideMessage("formMessage");

  const payload = {
    title: document.getElementById("title").value.trim(),
    content: document.getElementById("content").value,
    category_id: document.getElementById("category").value || null,
  };

  try {
    if (noteId) {
      await apiRequest(`/notes/${noteId}`, { method: "PUT", body: payload });
    } else {
      await apiRequest("/notes", { method: "POST", body: payload });
    }
    window.location.href = "/dashboard";
  } catch (err) {
    showMessage("formMessage", err.message, "error");
  }
});

async function deleteCurrentNote() {
  if (!confirm("Delete this note? This cannot be undone.")) return;
  try {
    await apiRequest(`/notes/${noteId}`, { method: "DELETE" });
    window.location.href = "/dashboard";
  } catch (err) {
    alert("Failed to delete note: " + err.message);
  }
}
