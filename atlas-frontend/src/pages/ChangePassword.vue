<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
    <div class="max-w-md w-full bg-white p-8 rounded-xl shadow-lg">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Change Password</h2>
      <form @submit.prevent="handleSubmit">
        <Input label="Current Password" type="password" v-model="current_password" required />
        <Input label="New Password" type="password" v-model="new_password" required />
        <Input label="Confirm New Password" type="password" v-model="new_password_confirm" required />
        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
        <div v-if="success" class="text-green-500 text-sm">{{ success }}</div>
        <div class="flex gap-4 mt-6">
          <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Change</button>
          <button type="button" @click="router.push('/profile')" class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Cancel</button>
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
const current_password = ref('');
const new_password = ref('');
const new_password_confirm = ref('');
const error = ref('');
const success = ref('');

const handleSubmit = async () => {
  error.value = '';
  success.value = '';
  try {
    await authStore.changePassword(current_password.value, new_password.value, new_password_confirm.value);
    success.value = 'Password changed successfully!';
    setTimeout(() => router.push('/profile'), 2000);
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.current_password?.[0] || 'Failed to change password.';
  }
};
</script>
