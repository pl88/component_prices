import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authAPI, type LoginRequest, type LoginResponse } from "@/api";

interface User {
  id: string;
  email: string;
  name: string;
}

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null);
  const token = ref<string>(localStorage.getItem("auth_token") || "");
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => !!token.value && !!user.value);

  const login = async (credentials: LoginRequest) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await authAPI.login(credentials);
      token.value = response.data.token;
      user.value = response.data.user;
      localStorage.setItem("auth_token", response.data.token);
    } catch (err) {
      error.value = (err as Error).message || "Login failed";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } finally {
      token.value = "";
      user.value = null;
      localStorage.removeItem("auth_token");
    }
  };

  const clearError = () => {
    error.value = null;
  };

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    login,
    logout,
    clearError,
  };
});
