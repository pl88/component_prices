<template>
  <div class="component-card">
    <h3>{{ component.name }}</h3>
    <div class="card-details">
      <p><strong>Category:</strong> {{ component.category }}</p>
      <p><strong>Price:</strong> ${{ component.price.toFixed(2) }}</p>
      <p><strong>Last Updated:</strong> {{ formatDate(component.lastUpdated) }}</p>
    </div>
    <div class="card-actions">
      <button @click="$emit('edit', component.id)" class="btn btn-small btn-edit">
        Edit
      </button>
      <button
        @click="$emit('delete', component.id)"
        class="btn btn-small btn-delete"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Component } from "@/api";

defineProps<{
  component: Component;
}>();

defineEmits<{
  edit: [id: string];
  delete: [id: string];
}>();

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};
</script>

<style scoped>
.component-card {
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
}

h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--color-primary);
}

.card-details {
  margin-bottom: 1.5rem;
}

p {
  margin: 0.5rem 0;
  color: var(--color-text);
  font-size: 0.95rem;
}

.card-actions {
  display: flex;
  gap: 0.75rem;
}

.btn {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.85rem;
  font-weight: 500;
}

.btn-small {
  padding: 0.5rem 1rem;
}

.btn-edit {
  background-color: var(--color-primary);
  color: white;

  &:hover {
    background-color: var(--color-primary-dark);
  }
}

.btn-delete {
  background-color: var(--color-error);
  color: white;

  &:hover {
    background-color: #dc2626;
  }
}
</style>
