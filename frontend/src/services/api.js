import axios from "axios";

const API = axios.create({
  baseURL: "https://rental-house-finder-47uv.onrender.com/api"
});

export default API;