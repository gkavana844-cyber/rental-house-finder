import axios from "axios";

const API = "http://127.0.0.1:5000/api/houses";

// ✅ Get all houses
export const getHouses = async () => {
  try {
    const res = await axios.get(API);
    console.log("API RESPONSE:", res.data);
    return res.data;
  } catch (error) {
    console.error("GET ERROR:", error);
    return [];
  }
};

// ✅ Add house
export const addHouse = async (data) => {
  try {
    const res = await axios.post(`${API}/add`, data);
    return res.data;
  } catch (error) {
    console.error("ADD ERROR:", error.response?.data || error.message);
    return { error: "Failed to add house" };
  }
};

// ✅ Search houses (location + price)
export const searchHouses = async (filters) => {
  try {
    const params = new URLSearchParams(filters).toString();
    const res = await axios.get(`${API}?${params}`);
    return res.data;
  } catch (error) {
    console.error("SEARCH ERROR:", error);
    return [];
  }
};

// ✅ Get single house (details page)
export const getHouseById = async (id) => {
  try {
    const res = await axios.get(`${API}/${id}`);
    return res.data;
  } catch (error) {
    console.error("DETAIL ERROR:", error);
    return null;
  }
};  