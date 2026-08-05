/**
 * MAHANAYAK OS — Route Guard & User Session Binding
 * Protects routes based on user role and updates header session information.
 */

(function () {
  function enforceRouteGuard() {
    if (!window.AuthService) return;

    const path = window.location.pathname;
    const isSubdir = path.includes('/user/') || path.includes('/admin/');
    const loginRedirect = isSubdir ? '../login.html' : './login.html';

    const isAuthenticated = window.AuthService.isAuthenticated();
    const currentUser = window.AuthService.getCurrentUser();

    // Determine required role from URL path
    let requiredRole = null;
    if (path.includes('/admin/')) {
      requiredRole = 'admin';
    } else if (path.includes('/user/')) {
      requiredRole = 'office';
    }

    if (!isAuthenticated || !currentUser) {
      window.location.href = loginRedirect;
      return;
    }

    if (requiredRole && currentUser.role !== requiredRole) {
      // User is logged in but does not have the required role for this section
      window.location.href = loginRedirect;
      return;
    }

    // Update Welcome Header with current username
    document.addEventListener('DOMContentLoaded', () => {
      updateWelcomeHeader(currentUser.username);
      bindLogoutAction();
    });
  }

  function updateWelcomeHeader(username) {
    const headerTitle = document.querySelector('.page-header-title');
    if (headerTitle) {
      headerTitle.innerHTML = `Welcome, <span class="brand-accent">${escapeHtml(username)}</span>`;
    }
  }

  function bindLogoutAction() {
    const logoutLinks = document.querySelectorAll('.sidebar-link.logout');
    logoutLinks.forEach((link) => {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        if (window.AuthService) {
          window.AuthService.logout();
        }
      });
    });
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  enforceRouteGuard();
})();
