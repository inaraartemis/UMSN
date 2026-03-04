// Abode API Configuration
const API_CONFIG = {
    // Automatically detect environment
    getBaseUrl: function () {
        const hostname = window.location.hostname;

        // If running locally as a file or on localhost, default to local backend
        if (hostname === "127.0.0.1" || hostname === "localhost" || !hostname) {
            return "http://127.0.0.1:8000";
        }

        // In production, the backend is assumed to be at the same origin or a specific Render URL
        // You can hardcode your Render URL here after deployment, e.g., "https://umsn.onrender.com"
        // For now, we'll return the same origin as a fallback
        return window.location.origin;
    }
};

const BASE_URL = API_CONFIG.getBaseUrl();
