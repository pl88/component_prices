<template>
  <div class="components-page">
    <h1>Components</h1>

    <form class="controls" @submit.prevent="searchComponent">
      <input
        v-model="searchQuery"
        type="search"
        placeholder="Type component name (e.g. AMD Ryzen 9 5950X)"
        class="search-input"
      />
      <button class="btn btn-primary" type="submit" :disabled="isLoading">
        {{ isLoading ? "Searching..." : "Search" }}
      </button>
    </form>

    <div v-if="error" class="error-banner">
      {{ error }}
    </div>

    <div v-if="isLoading" class="loading">Loading prices...</div>

    <div v-else-if="!result" class="empty-state">
      Search for a component to see latest prices.
    </div>

    <div v-else class="result-card">
      <h2>{{ result.name }}</h2>
      <p class="category"><strong>Category:</strong> {{ result.category }}</p>

      <table v-if="result.latest_prices.length > 0" class="prices-table">
        <thead>
          <tr>
            <th>Shop</th>
            <th>Price</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in result.latest_prices" :key="`${entry.shop}-${entry.date}`">
            <td>{{ entry.shop }}</td>
            <td>{{ entry.price_pln }} {{ entry.currency }}</td>
            <td>{{ entry.date }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else class="empty-state small">No prices available for this component yet.</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { ref } from "vue";

import { componentsAPI, type ComponentPriceResponse } from "@/api";

const searchQuery = ref("");
const isLoading = ref(false);
const error = ref("");
const result = ref<ComponentPriceResponse | null>(null);

const searchComponent = async () => {
  const query = searchQuery.value.trim();
  if (!query) {
    error.value = "Please enter a component name.";
    result.value = null;
    return;
  }

  isLoading.value = true;
  error.value = "";
  try {
    const response = await componentsAPI.getByName(query);
    result.value = response.data;
  } catch (err) {
    result.value = null;
    if (axios.isAxiosError(err) && err.response?.status === 404) {
      error.value = `Component '${query}' not found.`;
    } else {
      error.value = "Failed to fetch component prices.";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.components-page {
  width: 100%;
  max-width: 960px;
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

.loading,
.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--color-secondary);
}

.empty-state.small {
  padding: 1rem;
}

.result-card {
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  padding: 1.5rem;
}

.result-card h2 {
  margin: 0 0 0.75rem;
  color: var(--color-primary);
}

.category {
  margin-bottom: 1rem;
}

.prices-table {
  width: 100%;
  border-collapse: collapse;
}

.prices-table th,
.prices-table td {
  border-bottom: 1px solid var(--color-border);
  padding: 0.75rem;
  text-align: left;
}

.prices-table th {
  background: #f8fafc;
}
</style>
