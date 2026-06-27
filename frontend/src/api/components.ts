import client from "./client";

export interface Component {
  id: string;
  name: string;
  price: number;
  category: string;
  lastUpdated: string;
}

export interface ComponentsResponse {
  data: Component[];
  total: number;
  page: number;
  pageSize: number;
}

export const componentsAPI = {
  getAll: (page = 1, pageSize = 20) =>
    client.get<ComponentsResponse>("/components", { params: { page, pageSize } }),

  getById: (id: string) =>
    client.get<Component>(`/components/${id}`),

  create: (data: Omit<Component, "id" | "lastUpdated">) =>
    client.post<Component>("/components", data),

  update: (id: string, data: Partial<Component>) =>
    client.put<Component>(`/components/${id}`, data),

  delete: (id: string) =>
    client.delete(`/components/${id}`),
};
