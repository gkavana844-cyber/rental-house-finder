<<<<<<< HEAD
import { useNavigate } from "react-router-dom";
import "../styles/Dashboard.css";

function Dashboard() {

  const navigate = useNavigate();

  return (

    <div className="dashboard-container">

      <h1 className="title">
        🏠 Rental House Finder
      </h1>

      <p className="subtitle">
        Find your perfect home or list your property easily
      </p>

      <div className="card-container">

        {/* ➕ ADD HOUSE */}
        <div
          className="card add"
          onClick={() => navigate("/add-house")}
        >
          <h2>
            ➕ Add Your House
          </h2>

          <p>
            List your property and reach more customers
          </p>
        </div>


        {/* 🔍 SEARCH + FURNITURE */}
        <div
          className="card search"
          onClick={() => navigate("/search")}
        >
          <h2>
            🔍 Search House & View Furniture
          </h2>

          <p>
            Find houses and furniture in one place
          </p>
        </div>


        {/* 👨‍💻 ADMIN */}
        <div
          className="card admin"
          onClick={() => navigate("/admin")}
        >
          <h2>
            👨‍💻 Admin Panel
          </h2>

          <p>
            View user activities and analytics
          </p>
        </div>

      </div>

    </div>

  );

}

=======
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

        {/* ➕ ADD HOUSE */}
        <div
          className="card add"
          onClick={() => navigate("/add-house")}
        >
          <h2> Add Your House</h2>
          <p>List your property and reach more customers</p>
        </div>

        {/* 🔍 SEARCH HOUSE */}
        <div
          className="card search"
          onClick={() => navigate("/search")}
        >
          <h2>🔍 Search House And View Furniture </h2>
          <p>Find houses & furniture in one place</p>
        </div>

        {/* 🪑 ADD FURNITURE */}
        <div
          className="card furniture"
          onClick={() => navigate("/add-furniture")}
        >
          <h2>🪑 Add Furniture</h2>
          <p>Add furniture like bed, sofa, table</p>
        </div>

      </div>
    </div>
  );
}

>>>>>>> 3e428f534d42f51947e19a872534a44a62a76dd8
export default Dashboard;