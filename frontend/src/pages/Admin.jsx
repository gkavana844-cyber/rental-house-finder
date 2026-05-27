import { useEffect, useState } from "react";
import "../styles/Admin.css";

function Admin() {

  const [stats, setStats] = useState({
    users: 0,
    houses: 0,
    searches: 0,
    location: "Tumakuru"
  });

  const [activities, setActivities] = useState([]);

  useEffect(() => {

    // Temporary data
    setStats({
      users: 23,
      houses: 15,
      searches: 127,
      location: "Tumakuru"
    });

    setActivities([
      "👤 User registered",
      "🏠 House added",
      "🔍 User searched Tumakuru",
      "🪑 Furniture selected",
      "📍 User viewed nearby houses"
    ]);

  }, []);

  return (

    <div className="admin-container">

      <h1>
        👨‍💻 Admin Dashboard
      </h1>

      <div className="stats-container">

        <div className="stat-card">
          <h2>{stats.users}</h2>
          <p>👤 Total Users</p>
        </div>

        <div className="stat-card">
          <h2>{stats.houses}</h2>
          <p>🏠 Houses Added</p>
        </div>

        <div className="stat-card">
          <h2>{stats.searches}</h2>
          <p>🔍 Total Searches</p>
        </div>

        <div className="stat-card">
          <h2>{stats.location}</h2>
          <p>📍 Top Location</p>
        </div>

      </div>

      <div className="activity-box">

        <h2>
          📈 Recent Activity
        </h2>

        {
          activities.map((item,index)=>(

            <div
              key={index}
              className="activity-item"
            >
              {item}
            </div>

          ))
        }

      </div>

    </div>

  );

}

export default Admin;