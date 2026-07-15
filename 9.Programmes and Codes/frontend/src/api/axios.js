// src/api/axios.js
// Central Axios instance. Attaches the JWT access token to every request
// and clears the session automatically on a 401 response, matching the
// "Frontend communicates with FastAPI" story's Axios interceptor pattern.

import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("finrelief_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("finrelief_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
