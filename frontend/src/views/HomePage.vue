<template>
  <div class="home-page">
    <h1>Welcome to Component Prices</h1>
    <p>Manage and track component pricing with ease.</p>
    <div class="cta-buttons">
      <router-link v-if="!isAuthenticated" to="/login" class="btn btn-primary">
        Login
      </router-link>
      <router-link v-if="isAuthenticated" to="/components" class="btn btn-primary">
        View Components
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useAuth } from "@/composables";

const { isAuthenticated } = useAuth();
</script>

<style scoped>
.home-page {
  text-align: center;
  padding: 3rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: var(--color-primary);
}

p {
  font-size: 1.125rem;
  color: var(--color-secondary);
  margin-bottom: 2rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: var(--border-radius-lg);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;

  &:hover {
    background-color: var(--color-primary-dark);
  }
}
</style>
