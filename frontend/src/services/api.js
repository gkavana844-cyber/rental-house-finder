import axios from "axios";

const API = axios.create({
  baseURL: "https://rental-house-finder-backend.onrender.com"
});

export default API;