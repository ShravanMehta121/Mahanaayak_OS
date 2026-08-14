const USE_MOCK_DATA = false;

const api = {
    async request(endpoint, options = {}) {
        if (USE_MOCK_DATA) {
            console.warn(`[MOCK MODE] Intercepted call to ${endpoint}`);
            return this.mockResponse(endpoint, options);
        }

        const url = endpoint.startsWith('/api/') ? endpoint : `/api/v1${endpoint}`;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            // Important for HttpOnly Cookies
            credentials: 'same-origin'
        };

        // For FormData, remove Content-Type so browser can set boundary automatically
        if (options.body instanceof FormData) {
            delete defaultOptions.headers['Content-Type'];
        }

        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            let response = await fetch(url, finalOptions);

            // Handle Unauthorized (Token Expired)
            if (response.status === 401) {
                console.log("Access token expired, attempting refresh...");
                const refreshed = await this.refreshToken();
                if (refreshed) {
                    // Retry original request
                    response = await fetch(url, finalOptions);
                } else {
                    window.location.href = '/login.html';
                    return null;
                }
            }

            // Global error handling
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                console.error("API Error:", errData);
                throw new Error(errData.message || `HTTP Error ${response.status}`);
            }

            // For reports (Blob)
            if (finalOptions.responseType === 'blob') {
                return await response.blob();
            }

            return await response.json();
        } catch (error) {
            console.error("Network Error:", error);
            // In a real app, trigger a global toast notification here
            throw error;
        }
    },

    async refreshToken() {
        try {
            const response = await fetch('/api/v1/auth/refresh', {
                method: 'POST',
                credentials: 'same-origin'
            });
            return response.ok;
        } catch (e) {
            return false;
        }
    },

    // Mock data fallback
    mockResponse(endpoint, options) {
        return new Promise((resolve) => {
            setTimeout(() => {
                if (endpoint.includes('/auth/login')) {
                    resolve({ status: "success", data: { user: { role: "ADMIN" } } });
                } else if (endpoint.includes('/analytics/admin-dashboard')) {
                    resolve({
                        status: "success",
                        data: {
                            total_complaints: 125,
                            status_counts: { open: 15, pending: 20, resolved: 80, closed: 10 },
                            time_trends: { today: 5, weekly: 30, monthly: 125 },
                            ai_insights: {
                                top_5_critical_wards: [{ ward: "Ward A", count: 12 }],
                                recent_10_complaints: []
                            }
                        }
                    });
                } else {
                    resolve({ status: "success", data: [] });
                }
            }, 300);
        });
    }
};

window.api = api;
