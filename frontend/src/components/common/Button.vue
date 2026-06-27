<template>
  <button :class="['button', `button--${variant}`]">
    <slot />
  </button>
</template>

<script setup lang="ts">
defineProps<{
  variant?: "primary" | "secondary" | "error";
}>();
</script>

<style scoped>
.button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.button--primary {
  background-color: var(--color-primary);
  color: white;

  &:hover {
    background-color: var(--color-primary-dark);
  }
}

.button--secondary {
  background-color: var(--color-secondary);
  color: white;

  &:hover {
    background-color: #4b5563;
  }
}

.button--error {
  background-color: var(--color-error);
  color: white;

  &:hover {
    background-color: #dc2626;
  }
}
</style>
