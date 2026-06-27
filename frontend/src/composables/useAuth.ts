import { computed } from "vue";
import { useAuthStore } from "@/stores";

export const useAuth = () => {
  const authStore = useAuthStore();

  const isAuthenticated = computed(() => authStore.isAuthenticated);
  const currentUser = computed(() => authStore.user);
  const isLoading = computed(() => authStore.isLoading);

  const login = async (email: string, password: string) => {
    return authStore.login({ email, password });
  };

  const logout = async () => {
    return authStore.logout();
  };

  return {
    isAuthenticated,
    currentUser,
    isLoading,
    login,
    logout,
  };
};
