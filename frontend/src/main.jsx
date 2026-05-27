import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// 🌍 Global styles
import "./index.css";

// 🗺️ Leaflet styles (REQUIRED)
import "leaflet/dist/leaflet.css";

// 🚀 Render App
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);