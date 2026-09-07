import api from "./api";

export interface User {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
}

export interface LoginResponse {
    access: string;
    refresh: string;
    user: User;
}

export interface RegisterData {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
    confirm_password: string;
}

class AuthService {
    async login(email: string, password: string): Promise<LoginResponse> {
        const response = await api.post('/login/', {
            email,
            password
        });
        return response.data;
    }

    async register(data: RegisterData): Promise<{
        message: string;
        user: User
    }> {
        const response = await api.post('/register/', data);
        return response.data;
    }

    async logout(refresh: string): Promise<{
        access: string
    }> {
        const response = await api.post('/token/refresh/', {
            refresh
        });
        return response.data;
    }

    async getCurrentUser(): Promise<User> {
        const response = await api.get('/me/');
        return response.data;
    }

    async updateProfile(data: Partial<User>): Promise<User> {
        const response = await api.patch('/me/', data);
        return response.data;
    }

    async changePassword(oldPassword: string, newPassword: string): Promise<void> {
        await api.post('/password/change/', {
            old_password: oldPassword,
            new_password: newPassword
        });
    }

    async resetPassword(email: string): Promise<void> {
        await api.post('/password/reset/', {
            email
        });
    }

    async resetPasswordConfirm(uid: string, token: string, newPassword: string): Promise<void> {
        await api.post('/password/reset/confirm/', {
            uid,
            token,
            new_password: newPassword
        });
    }

    async requestPasswordReset(email: string): Promise<void> {
        await api.post('/password/reset/', {
            email
        });
    }

    async confirmPasswordReset(uid: number, token: string, new_password: string, new_password_confirm: string): Promise<void> {
        await api.post('/password/reset/confirm/', {
            uid,
            token,
            new_password,
            new_password_confirm
        });
    }
}

export default new AuthService();
