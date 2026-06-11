const API_URL = 'http://localhost:8000/api';

class ApiService {
    static getHeaders() {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    static async handleResponse(response) {
        if (response.status === 401) {
            // Token might be expired, clear and redirect
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            if (!window.location.pathname.includes('login.html')) {
                window.location.href = '/login.html';
            }
            throw new Error('Session expired');
        }

        const data = await response.json().catch(() => null);

        if (!response.ok) {
            const errorMsg = data && data.detail ? data.detail : 
                             data && data.error ? data.error : 
                             'An error occurred';
            throw new Error(errorMsg);
        }

        return data;
    }

    static async get(endpoint) {
        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                method: 'GET',
                headers: this.getHeaders(),
            });
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    static async post(endpoint, data) {
        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    static async put(endpoint, data) {
        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    static async delete(endpoint, data = null) {
        try {
            const options = {
                method: 'DELETE',
                headers: this.getHeaders(),
            };
            if (data) {
                options.body = JSON.stringify(data);
            }
            const response = await fetch(`${API_URL}${endpoint}`, options);
            if (response.status === 204) return true;
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    // Auth specific methods
    static async login(username, password) {
        const data = await this.post('/auth/login/', { username, password });
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            return true;
        }
        return false;
    }

    static async register(userData) {
        return await this.post('/auth/register/', userData);
    }

    static logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/index.html';
    }

    static isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }
}
