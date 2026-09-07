import { defineStore } from "pinia";
import type { RegisterData, User } from "../services/AuthService";
import AuthService from "../services/AuthService";
import api from "../services/api";

interface AuthState {
    user: User | null;
    accessToken: string | null;
    refreshToken: string | null;
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        user: null,
        accessToken: localStorage.getItem('access_token') || null,
        refreshToken: localStorage.getItem('refresh_token') || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken,
    },
    actions: {
        async login(email: string, password: string) {
            const response = await AuthService.login(email, password);
            this.accessToken = response.access;
            this.refreshToken = response.refresh;
            localStorage.setItem('access_token', response.access);
            localStorage.setItem('refresh_token', response.refresh);
            this.user = response.user;
        },

        async register(data: RegisterData) {
            const response = await AuthService.register(data);
            return response;
        },

        async fetchUser() {
            if (!this.accessToken) return;
            const user = await AuthService.getCurrentUser();
            this.user = user;
        },

        async logout() {
            try {
                if (this.refreshToken) {
                    await AuthService.logout(this.refreshToken);
                }
            } catch {
                // ignore errors
            }
            this.user = null;
            this.accessToken = null;
            this.refreshToken = null;
            localStorage.clear();
        },

        async updateProfile(data: Partial<User>) {
            const updated = await AuthService.updateProfile(data);
            this.user = updated;
            return updated;
        },

        async changePassword(current_password: string, new_password: string, new_password_confirm: string): Promise<void> {
            await api.post('/password/change/', {
                current_password,
                new_password,
                new_password_confirm
            })
        },

        async requestPasswordReset(email: string) {
            await AuthService.requestPasswordReset(email);
        },

        async confirmPasswordReset(uid: number, token: string, new_password: string, new_password_confirm: string) {
            await AuthService.confirmPasswordReset(uid, token, new_password, new_password_confirm);
        }
    },
});
