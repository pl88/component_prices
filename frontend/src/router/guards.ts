import { useAuthStore } from "@/stores";

export const requireAuth = () => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) {
    throw new Error("Not authenticated");
  }
};

export const requireGuest = () => {
  const authStore = useAuthStore();

  if (authStore.isAuthenticated) {
    throw new Error("Already authenticated");
  }
};
