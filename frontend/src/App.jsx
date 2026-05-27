import { BrowserRouter, Routes, Route } from "react-router-dom";

// Pages
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import AddHouse from "./pages/AddHouse";
import Search from "./pages/Search";
<<<<<<< HEAD
import Admin from "./pages/Admin"; // ✅ Added
=======
import AddFurniture from "./pages/AddFurniture";
>>>>>>> 3e428f534d42f51947e19a872534a44a62a76dd8

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* 🔐 Auth Pages */}
<<<<<<< HEAD
        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        {/* 🏠 Main Pages */}
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/add-house"
          element={<AddHouse />}
        />

        <Route
          path="/search"
          element={<Search />}
        />

        {/* 👨‍💻 ADMIN PAGE */}
        <Route
          path="/admin"
          element={<Admin />}
        />
=======
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* 🏠 Main Pages */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/add-house" element={<AddHouse />} />
        <Route path="/search" element={<Search />} />
        
>>>>>>> 3e428f534d42f51947e19a872534a44a62a76dd8

      </Routes>
    </BrowserRouter>
  );
}

export default App;