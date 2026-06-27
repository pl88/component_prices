import { createRouter, createWebHistory, Router } from "vue-router";
import { useAuthStore } from "@/stores";
import { routes } from "./routes";

const router: Router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.meta.requiresAuth as boolean | undefined;

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: "Login", query: { redirect: to.fullPath } });
  } else if (
    to.name === "Login" &&
    authStore.isAuthenticated
  ) {
    next({ name: "Home" });
  } else {
    next();
  }
});

export default router;
