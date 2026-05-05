import { BrowserRouter, Routes, Route } from "react-router-dom";

// Pages
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import AddHouse from "./pages/AddHouse";
import Search from "./pages/Search";
import AddFurniture from "./pages/AddFurniture";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* 🔐 Auth Pages */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* 🏠 Main Pages */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/add-house" element={<AddHouse />} />
        <Route path="/search" element={<Search />} />
        

      </Routes>
    </BrowserRouter>
  );
}

export default App;