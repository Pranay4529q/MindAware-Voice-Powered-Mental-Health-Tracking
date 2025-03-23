// frontend/src/services/auth.js
import API from "./api";

const AuthService = {
  login: async (email, password) => {
    try {
      const response = await API.post("/auth/login", { email, password });
      return response.data;
    } catch (error) {
      throw error.response
        ? error.response.data
        : new Error("Authentication failed");
    }
  },

  register: async (userData) => {
    try {
      const response = await API.post("/auth/register", userData);
      return response.data;
    } catch (error) {
      throw error.response
        ? error.response.data
        : new Error("Registration failed");
    }
  },

  logout: () => {
    // Client-side logout only
    // The actual token invalidation should happen on the server side
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  },

  validateToken: async () => {
    try {
      const response = await API.get("/auth/validate");
      return response.data;
    } catch (error) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      throw new Error("Invalid token");
    }
  },
};

export default AuthService;
