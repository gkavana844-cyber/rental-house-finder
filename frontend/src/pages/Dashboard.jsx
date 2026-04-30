import { useNavigate } from "react-router-dom";
import "../styles/Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard-container">
      <h1 className="title">🏠 Rental House Finder</h1>
      <p className="subtitle">
        Find your perfect home or list your property easily
      </p>

      <div className="card-container">
        {/* ADD HOUSE CARD */}
        <div
          className="card add"
          onClick={() => navigate("/add-house")}
        >
          <h2>➕ Add Your House</h2>
          <p>List your property and reach more customers</p>
        </div>

        {/* SEARCH HOUSE CARD */}
        <div
          className="card search"
          onClick={() => navigate("/search")}
        >
          <h2>🔍 Search House</h2>
          <p>Find houses based on your needs & location</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;