<template>
  <div :class="['card', `card--${variant}`]">
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  variant?: "default" | "elevated" | "outlined";
}>();
</script>

<style scoped>
.card {
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.card--default {
  background: white;
  border: 1px solid var(--color-border);
}

.card--elevated {
  background: white;
  box-shadow: var(--shadow-md);
}

.card--outlined {
  background: transparent;
  border: 2px solid var(--color-border);
}
</style>
