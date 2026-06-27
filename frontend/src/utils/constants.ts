export const COMPONENT_CATEGORIES = [
  "CPU",
  "GPU",
  "RAM",
  "Storage",
  "Motherboard",
  "PSU",
  "Cooling",
  "Other",
] as const;

export const API_ENDPOINTS = {
  AUTH: "/auth",
  COMPONENTS: "/components",
} as const;

export const PAGINATION_DEFAULTS = {
  PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
} as const;
