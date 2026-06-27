<template>
  <header class="header">
    <div class="header-container">
      <router-link to="/" class="logo">Component Prices</router-link>
      <nav class="nav">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link
          v-if="isAuthenticated"
          to="/components"
          class="nav-link"
        >
          Components
        </router-link>
      </nav>
      <div class="user-menu">
        <span v-if="currentUser" class="user-name">{{ currentUser.name }}</span>
        <button
          v-if="isAuthenticated"
          @click="handleLogout"
          class="btn btn-secondary"
        >
          Logout
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuth } from "@/composables";

const router = useRouter();
const { isAuthenticated, currentUser, logout } = useAuth();

const handleLogout = async () => {
  await logout();
  router.push({ name: "Home" });
};
</script>

<style scoped>
.header {
  background-color: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;

  &:hover {
    color: #e0e7ff;
  }
}

.nav {
  display: flex;
  gap: 2rem;
  flex: 1;
  margin-left: 3rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  transition: color 0.3s ease;

  &:hover {
    color: #e0e7ff;
  }

  &.router-link-active {
    font-weight: bold;
    border-bottom: 2px solid white;
  }
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  color: white;
  font-size: 0.9rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-secondary {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;

  &:hover {
    background-color: rgba(255, 255, 255, 0.3);
  }
}
</style>
