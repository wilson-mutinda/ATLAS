<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Create your account</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Already have an account?
          <router-link to="/login" class="font-medium text-blue-600 hover:text-blue-500">Sign in</router-link>
        </p>
      </div>
      <form class="mt-8 space-y-4" @submit.prevent="handleSubmit">
        <div class="grid grid-cols-2 gap-4">
          <Input label="First name" type="text" v-model="form.first_name" required />
          <Input label="Last name" type="text" v-model="form.last_name" required />
        </div>
        <Input label="Email address" type="email" v-model="form.email" required />
        <Input label="Password" type="password" v-model="form.password" required />
        <Input label="Confirm password" type="password" v-model="form.confirm_password" required />
        <div v-if="error" class="text-sm text-red-500 text-center">{{ error }}</div>
        <button type="submit" class="w-full ...">Register</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import Input from '../components/Input.vue';

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  confirm_password: '',
});
const error = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleSubmit = async () => {
  error.value = '';
  if (form.password !== form.confirm_password) {
    error.value = 'Passwords do not match';
    return;
  }
  try {
    await authStore.register(form);
    router.push('/login');
  } catch {
    error.value = 'Registration failed. Please try again.';
  }
};
</script>
