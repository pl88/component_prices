<template>
  <footer class="footer">
    <div class="footer-container">
      <p>&copy; 2026 Component Prices. All rights reserved.</p>
      <nav class="footer-links">
        <a href="#" class="footer-link">Privacy</a>
        <a href="#" class="footer-link">Terms</a>
        <a href="#" class="footer-link">Contact</a>
      </nav>
    </div>
  </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
.footer {
  background-color: #f3f4f6;
  border-top: 1px solid var(--color-border);
  padding: 2rem 0;
  margin-top: 3rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

p {
  color: var(--color-secondary);
  margin: 0;
}

.footer-links {
  display: flex;
  gap: 2rem;
}

.footer-link {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.3s ease;

  &:hover {
    color: var(--color-primary-dark);
  }
}
</style>
