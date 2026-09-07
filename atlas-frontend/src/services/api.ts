import type { AxiosInstance } from "axios";
import axios from "axios";

class ApiClient {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: 'http://127.0.0.1:8000/api/v1/auth/',
            headers: { 
                'Content-Type': 'application/json'
            }
        });

        // Request interceptor to add access token
        this.client.interceptors.request.use((config) => {
            const token = localStorage.getItem('access_token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });

        // Response interceptor to refresh token on 401
        this.client.interceptors.response.use(
            (response) => response,
            async (error) => {
                const originalRequest = error.config;
                if (error.response?.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;
                    const refresh = localStorage.getItem('refresh_token');
                    if (refresh) {
                        try {
                            const res = await axios.post('http://127.0.0.1:8000/api/v1/auth/token/refresh/', {
                                refresh
                            });
                            localStorage.setItem('access_token', res.data.access);
                            originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
                            return this.client(originalRequest);
                        } catch {
                            // Refresh failed - log out
                            localStorage.clear();
                            window.location.href = '/login';
                        }
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    // Expose the client instance for direct use, or add wrapper methods
    public getClient(): AxiosInstance {
        return this.client;
    }
}

export default new ApiClient().getClient();
