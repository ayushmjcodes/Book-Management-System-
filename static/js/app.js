/**
 * app.js
 * Shared helper functions used across every page: an API request
 * wrapper, message/date helpers, and the logout button handler
 * (since the header - and its logout button - appears on every
 * authenticated page).
 */

const API_BASE = "/api";

/**
 * Wrapper around fetch() that always sends/receives JSON, includes
 * the session cookie, and throws a readable Error on failure so
 * calling code can just try/catch it.
 */
async function apiRequest(path, { method = "GET", body = null } = {}) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin", // makes sure the session cookie is sent
  };
  if (body !== null) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong. Please try again.");
  }
  return data;
}

/** Displays a message (success or error) inside a #<id> element. */
function showMessage(elementId, message, type = "error") {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.textContent = message;
  el.className = `form-message ${type}`;
  el.classList.remove("hidden");
}

function hideMessage(elementId) {
  const el = document.getElementById(elementId);
  if (el) el.classList.add("hidden");
}

/** Formats an ISO date string (from the API) into something readable. */
function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/** Escapes text before inserting it into innerHTML, to prevent XSS. */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text ?? "";
  return div.innerHTML;
}

/** Wires up the logout button that appears in the shared header partial. */
function setupLogout() {
  const logoutBtn = document.getElementById("logoutBtn");
  if (!logoutBtn) return;
  logoutBtn.addEventListener("click", async () => {
    try {
      await apiRequest("/auth/logout", { method: "POST" });
      window.location.href = "/login";
    } catch (err) {
      alert("Failed to log out: " + err.message);
    }
  });
}

document.addEventListener("DOMContentLoaded", setupLogout);
