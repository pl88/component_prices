import client from "./client";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export const authAPI = {
  login: (credentials: LoginRequest) =>
    client.post<LoginResponse>("/auth/login", credentials),

  register: (data: RegisterRequest) =>
    client.post<LoginResponse>("/auth/register", data),

  logout: () => client.post("/auth/logout"),

  getCurrentUser: () =>
    client.get("/auth/me"),
};
