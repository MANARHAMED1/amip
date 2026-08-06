import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("amip_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("amip_token");
      localStorage.removeItem("amip_user");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export async function login(username: string, password: string) {
  const { data } = await api.post("/auth/login", { username, password });
  localStorage.setItem("amip_token", data.token);
  localStorage.setItem("amip_user", JSON.stringify(data.user));
  return data;
}

export async function getMe() {
  const { data } = await api.get("/auth/me");
  return data;
}

export async function getJSON<T = unknown>(path: string, params?: Record<string, string | number | undefined>): Promise<T> {
  const cleaned = Object.fromEntries(
    Object.entries(params || {}).filter(([_, v]) => v !== undefined && v !== "")
  );
  const { data } = await api.get<T>(path, { params: cleaned });
  return data;
}

export default api;
