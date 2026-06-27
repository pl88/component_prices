import { computed } from "vue";
import { useComponentsStore } from "@/stores";

export const useComponents = () => {
  const componentsStore = useComponentsStore();

  const components = computed(() => componentsStore.components);
  const isLoading = computed(() => componentsStore.isLoading);
  const error = computed(() => componentsStore.error);
  const currentPage = computed(() => componentsStore.currentPage);
  const totalPages = computed(() => componentsStore.totalPages);

  const fetchComponents = (page?: number) => componentsStore.fetchComponents(page);
  const createComponent = (data) => componentsStore.createComponent(data);
  const updateComponent = (id: string, data) => componentsStore.updateComponent(id, data);
  const deleteComponent = (id: string) => componentsStore.deleteComponent(id);
  const clearError = () => componentsStore.clearError();

  return {
    components,
    isLoading,
    error,
    currentPage,
    totalPages,
    fetchComponents,
    createComponent,
    updateComponent,
    deleteComponent,
    clearError,
  };
};
