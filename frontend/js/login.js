/**
 * MAHANAYAK OS — Login Page Controller
 * Handles user interactions, form validation, loading states, and inline error handling.
 */

document.addEventListener('DOMContentLoaded', () => {
  // If user is already logged in, auto-redirect to their role home page
  if (window.AuthService && window.AuthService.isAuthenticated()) {
    const user = window.AuthService.getCurrentUser();
    if (user.role === 'admin') {
      window.location.href = './admin/war-room.html';
      return;
    } else if (user.role === 'office') {
      window.location.href = './user/dashboard.html';
      return;
    }
  }

  const form = document.querySelector('[data-login-form]');
  if (!form) return;

  const userInput = document.getElementById('userId');
  const passInput = document.getElementById('password');
  const submitBtn = form.querySelector('button[type="submit"]');
  const errorContainer = document.getElementById('loginError');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = userInput ? userInput.value : '';
    const password = passInput ? passInput.value : '';

    if (errorContainer) {
      errorContainer.textContent = '';
      errorContainer.style.display = 'none';
    }

    if (!username.trim() || !password.trim()) {
      showError('Please enter both User ID and Password.');
      return;
    }

    // Set loading state
    const originalBtnContent = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Logging in...`;

    try {
      const result = await window.AuthService.login(username, password);

      if (result.success) {
        window.location.href = result.redirectUrl;
      } else {
        showError(result.message || 'Invalid username or password.');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnContent;
      }
    } catch (err) {
      showError('An unexpected authentication error occurred.');
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnContent;
    }
  });

  function showError(msg) {
    if (errorContainer) {
      errorContainer.textContent = msg;
      errorContainer.style.display = 'block';
    }
  }
});
