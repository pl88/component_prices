import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { componentsAPI, type Component } from "@/api";

export const useComponentsStore = defineStore("components", () => {
  const components = ref<Component[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const pageSize = ref(20);
  const total = ref(0);

  const totalPages = computed(() => Math.ceil(total.value / pageSize.value));

  const fetchComponents = async (page = 1) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await componentsAPI.getAll(page, pageSize.value);
      components.value = response.data.data;
      total.value = response.data.total;
      currentPage.value = page;
    } catch (err) {
      error.value = (err as Error).message || "Failed to fetch components";
    } finally {
      isLoading.value = false;
    }
  };

  const createComponent = async (data: Omit<Component, "id" | "lastUpdated">) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await componentsAPI.create(data);
      components.value.unshift(response.data);
      return response.data;
    } catch (err) {
      error.value = (err as Error).message || "Failed to create component";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateComponent = async (
    id: string,
    data: Partial<Component>
  ) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await componentsAPI.update(id, data);
      const index = components.value.findIndex((c) => c.id === id);
      if (index !== -1) {
        components.value[index] = response.data;
      }
      return response.data;
    } catch (err) {
      error.value = (err as Error).message || "Failed to update component";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const deleteComponent = async (id: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      await componentsAPI.delete(id);
      components.value = components.value.filter((c) => c.id !== id);
    } catch (err) {
      error.value = (err as Error).message || "Failed to delete component";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const clearError = () => {
    error.value = null;
  };

  return {
    components,
    isLoading,
    error,
    currentPage,
    pageSize,
    total,
    totalPages,
    fetchComponents,
    createComponent,
    updateComponent,
    deleteComponent,
    clearError,
  };
});
