<template>
  <div class="not-found-page">
    <div class="not-found-container">
      <h1>404</h1>
      <p>Page not found</p>
      <router-link to="/" class="btn btn-primary">Go Home</router-link>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.not-found-container {
  text-align: center;
}

h1 {
  font-size: 5rem;
  margin-bottom: 1rem;
  color: var(--color-primary);
}

p {
  font-size: 1.5rem;
  color: var(--color-secondary);
  margin-bottom: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: var(--border-radius-lg);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-block;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;

  &:hover {
    background-color: var(--color-primary-dark);
  }
}
</style>
