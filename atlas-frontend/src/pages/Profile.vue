<template>
  <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <div class="bg-white p-8 rounded-xl shadow">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Edit Profile</h2>
        <div v-if="message" :class="['mb-4 p-3 rounded text-sm', message.includes('success') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">
          {{ message }}
        </div>
        <form @submit.prevent="handleSubmit">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input label="First name" type="text" v-model="form.first_name" required />
            <Input label="Last name" type="text" v-model="form.last_name" required />
          </div>
          <Input label="Email address" type="email" v-model="form.email" required />
          <div class="mt-6 flex gap-4">
            <router-link to="/change-password" class="px-4 py-2 text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700 rounded-md transition">Change password</router-link>
            <!-- ... existing buttons ... -->
         </div>
          <div class="flex gap-4 mt-6">
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition">Save Changes</button>
            <button type="button" @click="router.push('/dashboard')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-md transition">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import Input from '../components/Input.vue';

const authStore = useAuthStore();
const router = useRouter();

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
});
const message = ref('');

onMounted(() => {
  if (authStore.user) {
    form.first_name = authStore.user.first_name || '';
    form.last_name = authStore.user.last_name || '';
    form.email = authStore.user.email || '';
  }
});

const handleSubmit = async () => {
  try {
    await authStore.updateProfile(form);
    message.value = 'Profile updated successfully!';
    setTimeout(() => message.value = '', 3000);
  } catch {
    message.value = 'Update failed.';
  }
};
</script>
