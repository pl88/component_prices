<template>
  <div class="components-page">
    <h1>Components</h1>

    <div v-if="error" class="error-banner">
      {{ error }}
      <button @click="clearError" class="close-btn">&times;</button>
    </div>

    <div class="controls">
      <input
        type="search"
        placeholder="Search components..."
        class="search-input"
      />
      <button class="btn btn-primary">Add Component</button>
    </div>

    <div v-if="isLoading" class="loading">Loading components...</div>

    <div v-else-if="components.length === 0" class="empty-state">
      No components found. Create your first component!
    </div>

    <div v-else class="components-grid">
      <ComponentCard
        v-for="component in components"
        :key="component.id"
        :component="component"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button
        v-if="currentPage > 1"
        @click="fetchComponents(currentPage - 1)"
        class="btn btn-secondary"
      >
        Previous
      </button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button
        v-if="currentPage < totalPages"
        @click="fetchComponents(currentPage + 1)"
        class="btn btn-secondary"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useComponents } from "@/composables";
import ComponentCard from "@/components/domain/ComponentCard.vue";

const {
  components,
  isLoading,
  error,
  currentPage,
  totalPages,
  fetchComponents,
  clearError,
} = useComponents();

const handleEdit = (id: string) => {
  console.log("Edit component:", id);
};

const handleDelete = async (id: string) => {
  if (confirm("Are you sure?")) {
    console.log("Delete component:", id);
  }
};

onMounted(() => {
  fetchComponents();
});
</script>

<style scoped>
.components-page {
  width: 100%;
}

h1 {
  margin-bottom: 2rem;
  color: var(--color-primary);
}

.error-banner {
  background-color: #fee2e2;
  color: #991b1b;
  padding: 1rem;
  border-radius: var(--border-radius-lg);
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #991b1b;
}

.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  font-size: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: var(--border-radius-lg);
  border: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;

  &:hover {
    background-color: var(--color-primary-dark);
  }
}

.btn-secondary {
  background-color: var(--color-secondary);
  color: white;

  &:hover {
    background-color: #4b5563;
  }
}

.loading,
.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--color-secondary);
}

.components-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 1rem;
  align-items: center;
  margin-top: 2rem;
}

.page-info {
  color: var(--color-secondary);
}
</style>
