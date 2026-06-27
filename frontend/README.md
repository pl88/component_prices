# Frontend

Vue 3 + TypeScript + Vite frontend application for Component Prices.

## Project Setup

### Install Dependencies

```bash
pnpm install
```

### Development

```bash
pnpm run dev
```

The dev server will start at `http://localhost:5173` with API proxy to `http://localhost:8000`.

### Build

```bash
pnpm run build
```

### Preview

```bash
pnpm run preview
```

## Code Quality

### Linting

```bash
pnpm run lint          # Lint and fix
pnpm run lint:check    # Check only
```

### Formatting

```bash
pnpm run format        # Format code
pnpm run format:check  # Check formatting
```

### Type Checking

```bash
pnpm run type-check
```

### Testing

```bash
pnpm run test           # Run tests
pnpm run test:ui        # Interactive UI
pnpm run test:coverage  # Coverage report
```

## Architecture

### Directory Structure

- **`src/api/`** — HTTP client and endpoint modules
- **`src/stores/`** — Pinia state management stores (domain-scoped)
- **`src/composables/`** — Reusable Vue composables
- **`src/router/`** — Vue Router configuration and guards
- **`src/views/`** — Page-level components (route views)
- **`src/components/`** — Reusable Vue components
  - `common/` — Generic UI components
  - `layout/` — Layout components
  - `domain/` — Domain-specific components
- **`src/types/`** — TypeScript type definitions
- **`src/utils/`** — Utility functions
- **`src/assets/`** — Static assets (styles, images)

### State Management

- **Pinia stores** are domain-scoped and hold server-derived state
- Store methods call into `src/api/` modules, never `fetch` or `axios` directly
- Local UI state (modals, form drafts) lives in component composables

### API Integration

- `src/api/client.ts` — Base HTTP client with auth interceptors
- `src/api/auth.ts` — Authentication endpoints
- `src/api/components.ts` — Component endpoints
- All API calls go through stores, not directly from components

### Routing

- Route-level code splitting for lazy loading pages
- Route guards in `src/router/guards.ts` handle auth
- `requiresAuth` meta field controls access

## Environment Variables

Create a `.env.local` file:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

## Browser Support

Modern browsers (Chrome, Firefox, Safari, Edge) with ES2020 support.
