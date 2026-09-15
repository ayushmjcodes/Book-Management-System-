/**
 * auth.js
 * Handles the login and registration forms. Only one of these two
 * forms exists on any given page, so we simply check for each before
 * attaching a listener.
 */

const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideMessage("formMessage");

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
      await apiRequest("/auth/login", { method: "POST", body: { email, password } });
      window.location.href = "/dashboard";
    } catch (err) {
      showMessage("formMessage", err.message, "error");
    }
  });
}

const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideMessage("formMessage");

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
      showMessage("formMessage", "Passwords do not match.", "error");
      return;
    }

    try {
      await apiRequest("/auth/register", {
        method: "POST",
        body: { username, email, password },
      });
      showMessage("formMessage", "Account created! Redirecting to login...", "success");
      setTimeout(() => (window.location.href = "/login"), 1200);
    } catch (err) {
      showMessage("formMessage", err.message, "error");
    }
  });
}
