const AUTH_STORAGE_KEY = 'mahanayakAuth';

const AuthService = {
  async login(username, password) {
    try {
      // Use the global api.js client
      const response = await window.api.request('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password })
      });

      if (response && response.status === 'success') {
        const user = response.data.user;
        const role = user.role.toLowerCase();
        
        // Ensure role is mapped for existing frontend logic if needed
        const mappedRole = role === 'admin' ? 'admin' : 'office';
        const redirectUrl = mappedRole === 'admin' ? 'admin/war-room.html' : 'user/dashboard.html';

        const userSession = {
          username: user.username,
          role: mappedRole,
          loggedIn: true,
          loginTimestamp: new Date().toISOString()
        };

        sessionStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(userSession));

        return {
          success: true,
          user: userSession,
          redirectUrl: redirectUrl
        };
      }
    } catch (error) {
      return {
        success: false,
        message: error.message || 'Invalid username or password.'
      };
    }
  },

  async logout() {
    try {
      await window.api.request('/auth/logout', { method: 'POST' });
    } catch (e) {
      console.warn("Logout request failed, proceeding to clear session");
    }
    
    sessionStorage.removeItem(AUTH_STORAGE_KEY);
    const isSubdir = window.location.pathname.includes('/user/') || window.location.pathname.includes('/admin/');
    const loginPath = isSubdir ? '../' : './';
    window.location.href = loginPath;
  },

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

  isAuthenticated() {
    const user = this.getCurrentUser();
    return Boolean(user && user.loggedIn);
  },

  hasRole(role) {
    const user = this.getCurrentUser();
    return Boolean(user && user.role === role);
  }
};

window.AuthService = AuthService;
