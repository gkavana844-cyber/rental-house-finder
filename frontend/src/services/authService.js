import axios from "axios";

// 🔥 UPDATED (LIVE BACKEND)
const API = "https://rental-house-finder-47uv.onrender.com/api/auth";

// ✅ REGISTER
export const registerUser = async (data) => {
  try {
    const res = await axios.post(`${API}/register`, data);
    return res.data;
  } catch (error) {
    console.error("REGISTER ERROR:", error);
    return { error: "Registration failed" };
  }
};

// ✅ LOGIN
export const loginUser = async (data) => {
  try {
    const res = await axios.post(`${API}/login`, data);
    console.log("LOGIN RESPONSE:", res.data);
    return res.data;
  } catch (error) {
    console.error("LOGIN ERROR:", error);
    return { error: "Login failed" };
  }
};