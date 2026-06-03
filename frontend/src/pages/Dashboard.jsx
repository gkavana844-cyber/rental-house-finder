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
          onClick={async () => {

            const password = prompt(
              "🔐 Only Admin can access this panel.\n\nPlease enter password:"
            );

            if (!password) return;

            try {

              const res = await fetch(
                "https://rental-house-finder-backend.onrender.com/api/admin/login",
                {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                    password
                  })
                }
              );

              const data = await res.json();

              if (data.success) {

                localStorage.setItem(
                  "adminToken",
                  data.token
                );

                navigate("/admin");

              } else {

                alert("❌ Incorrect Password");

              }

            } catch (err) {

              alert("❌ Server Error");

            }

          }}
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

export default Dashboard;