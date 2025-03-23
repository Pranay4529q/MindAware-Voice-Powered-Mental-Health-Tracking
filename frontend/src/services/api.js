// frontend/src/services/api.js
import axios from "axios";

// Create base API instance
const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:5000",
});

// Add token to request headers if it exists
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API endpoints
export const audioAPI = {
  analyzeAudio: (audioFile) => {
    const formData = new FormData();
    formData.append("audio", audioFile);
    return API.post("/predict", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
  getUserHistory: () => API.get("/history"),
};

export const userAPI = {
  getUserProfile: () => API.get("/profile"),
  updateUserProfile: (userData) => API.put("/profile", userData),
};

export default API;
