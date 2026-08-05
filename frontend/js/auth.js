/**
 * MAHANAYAK OS — Modular Authentication Service
 * Serves as a mock authentication layer that can be easily replaced by backend API endpoints.
 */

const AUTH_STORAGE_KEY = 'mahanayakAuth';

const DEMO_ACCOUNTS = {
  admin: {
    password: 'admin123',
    role: 'admin',
    redirectUrl: 'admin/war-room.html'
  },
  office: {
    password: 'office123',
    role: 'office',
    redirectUrl: 'user/dashboard.html'
  }
};

const AuthService = {
  /**
   * Authenticates user against demo credentials with a 300ms simulated network delay.
   * @param {string} username 
   * @param {string} password 
   * @returns {Promise<{success: boolean, user?: object, redirectUrl?: string, message?: string}>}
   */
  login(username, password) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const cleanUser = (username || '').trim();
        const cleanPass = (password || '').trim();

        const account = DEMO_ACCOUNTS[cleanUser];

        if (account && account.password === cleanPass) {
          const userSession = {
            username: cleanUser,
            role: account.role,
            loggedIn: true,
            loginTimestamp: new Date().toISOString()
          };

          sessionStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(userSession));

          resolve({
            success: true,
            user: userSession,
            redirectUrl: account.redirectUrl
          });
        } else {
          resolve({
            success: false,
            message: 'Invalid username or password.'
          });
        }
      }, 300);
    });
  },

  /**
   * Clears session storage and redirects user to login.html
   */
  logout() {
    sessionStorage.removeItem(AUTH_STORAGE_KEY);
    const isSubdir = window.location.pathname.includes('/user/') || window.location.pathname.includes('/admin/');
    const loginPath = isSubdir ? '../login.html' : './login.html';
    window.location.href = loginPath;
  },

  /**
   * Retrieves currently logged in user object or null.
   * @returns {{username: string, role: string, loggedIn: boolean}|null}
   */
  getCurrentUser() {
    try {
      const data = sessionStorage.getItem(AUTH_STORAGE_KEY);
      if (!data) return null;
      const parsed = JSON.parse(data);
      return parsed && parsed.loggedIn ? parsed : null;
    } catch (e) {
      return null;
    }
  },

  /**
   * Returns true if user is logged in.
   * @returns {boolean}
   */
  isAuthenticated() {
    const user = this.getCurrentUser();
    return Boolean(user && user.loggedIn);
  },

  /**
   * Checks if active user has the specified role.
   * @param {string} role 
   * @returns {boolean}
   */
  hasRole(role) {
    const user = this.getCurrentUser();
    return Boolean(user && user.role === role);
  }
};

window.AuthService = AuthService;
