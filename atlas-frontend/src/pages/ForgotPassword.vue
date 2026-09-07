<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
    <div class="max-w-md w-full bg-white p-8 rounded-xl shadow-lg">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Reset Password</h2>
      <p class="text-gray-600 mb-4">Enter your email address and we'll send you a link to reset your password.</p>
      <form @submit.prevent="handleSubmit">
        <Input label="Email" type="email" v-model="email" required />
        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
        <div v-if="success" class="text-green-500 text-sm">{{ success }}</div>
        <div class="flex gap-4 mt-6">
          <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Send Reset Link</button>
          <button type="button" @click="router.push('/login')" class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import Input from '../components/Input.vue';

const authStore = useAuthStore();
const router = useRouter();
const email = ref('');
const error = ref('');
const success = ref('');

const handleSubmit = async () => {
  error.value = '';
  success.value = '';
  try {
    await authStore.requestPasswordReset(email.value);
    success.value = 'If that email exists, we\'ve sent a reset link.';
    setTimeout(() => router.push('/login'), 3000);
  } catch {
    error.value = 'Failed to send reset email. Please try again.';
  }
};
</script>
