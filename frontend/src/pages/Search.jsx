import { useState, useEffect } from "react";
import { getHouses } from "../services/houseService";
import { getFurniture } from "../services/furnitureService";
import "../styles/Search.css";

/*  Distance formula */
const getDistance = (lat1, lon1, lat2, lon2) => {
  const toRad = (v) => (v * Math.PI) / 180;
  const R = 6371;

  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);

  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) *
      Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) ** 2;

  return R * (2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)));
};

/* 📞 FORMAT PHONE */
const formatPhone = (num) => {
  if (!num) return null;

  let digits = num.toString().replace(/\D/g, "");

  if (digits.length === 10) {
    return `+91 ${digits.slice(0, 5)} ${digits.slice(5)}`;
  }

  return num;
};

function Search() {
  const [houses, setHouses] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [furniture, setFurniture] = useState([]);

  const [filters, setFilters] = useState({
    location: "",
    min: "",
    max: "",
    type: "all",
  });

  const [userCoords, setUserCoords] = useState(null);

  /* 🔥 LIVE LOCATION TRACKING */
  useEffect(() => {
    fetchHouses();

    const loadFurniture = async () => {
      const data = await getFurniture();
      setFurniture(data);
    };

    loadFurniture();

    const watchId = navigator.geolocation.watchPosition(
      (pos) => {
        const coords = {
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        };

        setUserCoords(coords);
      },
      (err) => console.log(err),
      {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 10000,
      }
    );

    return () => navigator.geolocation.clearWatch(watchId);
  }, []);

  /* 🔥 FIXED FETCH */
  const fetchHouses = async () => {
    try {
      const res = await getHouses();

      console.log("API RESPONSE:", res); // debug

      // 🔥 FIX: support both formats
      const data = res?.data || res || [];

      setHouses(data);
      setFiltered(data);
    } catch (err) {
      console.error("FETCH ERROR:", err);
    }
  };

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  /* 🔥 SEARCH + SORT */
  const handleSearch = () => {
    let result = [...houses];

    if (filters.location) {
      result = result.filter((h) =>
        h.location.toLowerCase().includes(filters.location.toLowerCase())
      );
    }

    if (filters.min) {
      result = result.filter((h) => (h.price || 0) >= Number(filters.min));
    }

    if (filters.max) {
      result = result.filter((h) => (h.price || 0) <= Number(filters.max));
    }

    if (filters.type !== "all") {
      result = result.filter((h) => h.type === filters.type);
    }

    /* 🔥 SORT BY NEAREST */
    if (userCoords) {
      result.sort((a, b) => {
        const d1 = getDistance(
          userCoords.lat,
          userCoords.lng,
          a.latitude,
          a.longitude
        );

        const d2 = getDistance(
          userCoords.lat,
          userCoords.lng,
          b.latitude,
          b.longitude
        );

        return d1 - d2;
      });
    }

    setFiltered(result);
  };

  return (
    <div className="search-container">
      <h1> Find Your Dream House</h1>

      {/* 🔍 SEARCH BAR */}
      <div className="search-bar">
        <input name="location" placeholder="📍 Location" onChange={handleChange} />
        <input name="min" type="number" placeholder="💰 Min Price" onChange={handleChange} />
        <input name="max" type="number" placeholder="💰 Max Price" onChange={handleChange} />

        <select name="type" onChange={handleChange}>
          <option value="all">🏠 All</option>
          <option value="rent">🏠 Rent</option>
          <option value="lease">📜 Lease</option>
        </select>

        <button onClick={handleSearch}>Search</button>
      </div>

      {/* ❗ EMPTY STATE FIX */}
      {filtered.length === 0 && (
        <p className="no-data">❌ No houses found</p>
      )}

      {/* 🏡 HOUSES */}
      <div className="house-grid">
        {filtered.map((h, i) => {
          let distance = null;

          if (userCoords && h.latitude && h.longitude) {
            const d = getDistance(
              userCoords.lat,
              userCoords.lng,
              Number(h.latitude),
              Number(h.longitude)
            );

            if (d && d < 50) distance = d.toFixed(2);
          }

          return (
            <div className="house-card" key={i}>
              <div className="type-badge">
                {h.type === "rent" ? "🏠 Rent" : "📜 Lease"}
              </div>

              <img
                src={h.images?.[0] || "https://via.placeholder.com/300x200"}
                alt=""
              />

              <div className="card-body">
                <h3>{h.title}</h3>

                <p>📍 {h.location}</p>

                {/* 🔥 ADDED AMENITIES */}
                {h.amenities && h.amenities.length > 0 && (
                  <p className="amenities">
                    🧾 {h.amenities.join(", ")}
                  </p>
                )}

                {h.type === "rent" && (
                  <p className="price">₹{h.price}/month</p>
                )}

                {h.type === "lease" && (
                  <>
                    <p className="price">₹{h.price}</p>
                    <p>⏳ {h.lease_duration} years</p>
                  </>
                )}

                {distance && (
                  <p className="distance">📏 {distance} km away</p>
                )}

                {h.phone && (
                  <p className="contact">
                    📞 {formatPhone(h.phone)}
                  </p>
                )}

                {h.whatsapp && (
                  <a
                    href={`https://wa.me/91${h.whatsapp}`}
                    target="_blank"
                    rel="noreferrer"
                    className="whatsapp-btn"
                  >
                    💬 WhatsApp
                  </a>
                )}

                <a
                  href={`https://www.google.com/maps/dir/?api=1&destination=${h.latitude},${h.longitude}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  🚗 Get Directions
                </a>
              </div>
            </div>
          );
        })}
      </div>

      {/* ✅ FURNITURE SECTION (UPDATED UI) */}
      <h2 className="furniture-title"> Available Furniture</h2>

      <div className="furniture-grid">
        {furniture.map((f, i) => (
          <div key={i} className="furniture-card">

            {/* 🖼 IMAGE */}
            <img
              src={f.image || "https://via.placeholder.com/300x200"}
              alt={f.name}
              className="furniture-image"
            />

            <div className="furniture-body">
              <h3 className="furniture-name">{f.name}</h3>

              <p className="furniture-price">₹{f.price}</p>

              {f.contact && (
                <p className="furniture-contact">📞 {formatPhone(f.contact)}</p>
              )}

              <div className="furniture-buttons">
                <a
                  href={`https://wa.me/91${f.contact}`}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-whatsapp"
                >
                  💬 WhatsApp
                </a>

                <a
                  href={`tel:${f.contact}`}
                  className="btn-call"
                >
                  📞 Call
                </a>
              </div>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}

export default Search;