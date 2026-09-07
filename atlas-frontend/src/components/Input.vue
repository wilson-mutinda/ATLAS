<template>
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-1">{{ label }}</label>
    <input
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
      :class="{ 'border-red-500': error }"
      :required="required"
    />
    <p v-if="error" class="mt-1 text-sm text-red-500">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string;
  type?: string;
  modelValue: string;
  error?: string;
  required?: boolean;
}>();
defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();
</script>
