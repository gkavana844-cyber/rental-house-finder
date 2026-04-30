import axios from "axios";

const API = "http://127.0.0.1:5000/api/auth";

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
    console.log("LOGIN RESPONSE:", res.data); // 🔥 debug
    return res.data;
  } catch (error) {
    console.error("LOGIN ERROR:", error);
    return { error: "Login failed" };
  }
};