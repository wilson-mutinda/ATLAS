import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import Dashboard from "../pages/Dashboard.vue";
import Profile from "../pages/Profile.vue";
import ChangePassword from "../pages/ChangePassword.vue";
import ForgotPassword from "../pages/ForgotPassword.vue";
import ResetPassword from "../pages/ResetPassword.vue";

const routes = [
    {
        path: '/login', component: Login, meta: { requiresAuth: false }
    },
    {
        path: '/register', component: Register, meta: { requiresAuth: false }
    },
    {
        path: '/dashboard', component: Dashboard, meta: { requiresAuth: true }
    },
    {
        path: '/profile', component: Profile, meta: { requiresAuth: true }
    },
    {
        path: '/', redirect: '/dashboard'
    },
    {
        path: '/change-password', component: ChangePassword, meta: { requiresAuth: true }
    },
    {
        path: '/forgot-password', component: ForgotPassword, meta: { requiresAuth: false }
    },
    {
        path: '/reset-password', component: ResetPassword, meta: { requiresAuth: false }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, _from, next) => {
    const authStore = useAuthStore();
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login');
    } else {
        next();
    }
});

export default router;
