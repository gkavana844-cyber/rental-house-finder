import axios from "axios";

const API = "https://rental-house-finder-47uv.onrender.com/api/furniture";

// ADD
export const addFurniture = async (data) => {
  try {
    const res = await axios.post(`${API}/add`, data);
    return res.data;
  } catch (err) {
    return { error: "Failed to add furniture" };
  }
};

// GET
export const getFurniture = async () => {
  try {
    const res = await axios.get(API);
    return res.data.data;
  } catch (err) {
    return [];
  }
};