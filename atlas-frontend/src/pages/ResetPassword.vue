<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
    <div class="max-w-md w-full bg-white p-8 rounded-xl shadow-lg">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Set New Password</h2>
      <form @submit.prevent="handleSubmit">
        <Input label="New Password" type="password" v-model="new_password" required />
        <Input label="Confirm New Password" type="password" v-model="new_password_confirm" required />
        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
        <div v-if="success" class="text-green-500 text-sm">{{ success }}</div>
        <button type="submit" class="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Reset Password</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter, useRoute } from 'vue-router';
import Input from '../components/Input.vue';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const new_password = ref('');
const new_password_confirm = ref('');
const error = ref('');
const success = ref('');
const uid = ref<number | null>(null);
const token = ref<string | null>(null);

onMounted(() => {
  uid.value = route.query.uid ? Number(route.query.uid) : null;
  token.value = route.query.token as string || null;
  if (!uid.value || !token.value) {
    error.value = 'Invalid reset link.';
  }
});

const handleSubmit = async () => {
  if (!uid.value || !token.value) {
    error.value = 'Invalid reset link.';
    return;
  }
  error.value = '';
  success.value = '';
  try {
    await authStore.confirmPasswordReset(uid.value, token.value, new_password.value, new_password_confirm.value);
    success.value = 'Password reset successful! Redirecting...';
    setTimeout(() => router.push('/login'), 2000);
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.new_password?.[0] || 'Failed to reset password.';
  }
};
</script>
