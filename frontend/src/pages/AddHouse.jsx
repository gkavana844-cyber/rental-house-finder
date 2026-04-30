import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { addHouse } from "../services/houseService";
import "../styles/AddHouse.css";

import {
  MapContainer,
  TileLayer,
  Marker,
  useMapEvents,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

/* 🔥 Fix marker */
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
});

/* 📍 Tumkur bounds */
const TUMKUR = {
  minLat: 13.10,
  maxLat: 13.60,
  minLng: 76.80,
  maxLng: 77.40,
};

const isInsideTumkur = (lat, lng) =>
  lat >= TUMKUR.minLat &&
  lat <= TUMKUR.maxLat &&
  lng >= TUMKUR.minLng &&
  lng <= TUMKUR.maxLng;

/* 📍 FORMAT PHONE */
const formatIndianNumber = (value) => {
  let digits = value.replace(/\D/g, "");

  if (digits.startsWith("91")) {
    digits = digits.slice(2);
  }

  digits = digits.slice(0, 10);

  if (digits.length > 5) {
    digits = digits.slice(0, 5) + " " + digits.slice(5);
  }

  return "+91 " + digits;
};

/* 📍 Click map */
function LocationPicker({ setCoords, fetchAddress }) {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;

      if (isInsideTumkur(lat, lng)) {
        setCoords({ lat, lng });
        fetchAddress(lat, lng);
      } else {
        alert("Only Tumkur allowed");
      }
    },
  });
  return null;
}

/* 🔥 Move map */
function ChangeMapView({ coords }) {
  const map = useMap();
  map.setView([coords.lat, coords.lng], 14);
  return null;
}

function AddHouse() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    details: "",
    location: "",
    type: "rent",
    rent_price: "",
    lease_amount: "",
    lease_duration: "",
    amenities: "",
    phone: "",
    whatsapp: "",
  });

  const [coords, setCoords] = useState({
    lat: 13.3409,
    lng: 77.101,
  });

  const [suggestions, setSuggestions] = useState([]);
  const [images, setImages] = useState([]);
  const [previews, setPreviews] = useState([]);

  const fetchAddress = async (lat, lng) => {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
    );
    const data = await res.json();

    if (data?.display_name?.toLowerCase().includes("tumkur")) {
      setForm((prev) => ({
        ...prev,
        location: data.display_name,
      }));
    }
  };

  const getCurrentLocation = () => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;

        if (isInsideTumkur(latitude, longitude)) {
          setCoords({ lat: latitude, lng: longitude });
          fetchAddress(latitude, longitude);
        } else {
          alert("Outside Tumkur");
        }
      },
      () => alert("Permission denied"),
      { enableHighAccuracy: true }
    );
  };

  const fetchSuggestions = async (query) => {
    if (!query) return setSuggestions([]);

    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${query}, Tumkur`
    );

    const data = await res.json();

    const filtered = data.filter((i) =>
      i.display_name.toLowerCase().includes("tumkur")
    );

    setSuggestions(filtered.slice(0, 5));
  };

  const handleChange = (e) => {
    let { name, value } = e.target;

    if (name === "phone" || name === "whatsapp") {
      value = formatIndianNumber(value);
    }

    setForm({ ...form, [name]: value });

    if (name === "location") {
      fetchSuggestions(value);
    }
  };

  const selectSuggestion = (item) => {
    const lat = parseFloat(item.lat);
    const lng = parseFloat(item.lon);

    setForm({ ...form, location: item.display_name });
    setCoords({ lat, lng });
    setSuggestions([]);
  };

  const handleImageChange = (e) => {
    const files = Array.from(e.target.files);
    setImages(files);
    setPreviews(files.map((f) => URL.createObjectURL(f)));
  };

  const removeImage = (i) => {
    setImages(images.filter((_, idx) => idx !== i));
    setPreviews(previews.filter((_, idx) => idx !== i));
  };

  /* 🔥 FIXED VALIDATION */
  const validatePhone = (num) => {
    let digits = num.replace(/\D/g, "");

    if (digits.startsWith("91")) {
      digits = digits.slice(2);
    }

    return digits.length === 10;
  };

  /* 🚀 UPDATED SUBMIT — uses FormData + real image file uploads */
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validatePhone(form.phone)) {
      alert("Enter valid phone number");
      return;
    }

    if (form.whatsapp && !validatePhone(form.whatsapp)) {
      alert("Enter valid WhatsApp number");
      return;
    }

    try {
      const formData = new FormData();

      formData.append("title", form.details);
      formData.append("location", form.location);
      formData.append("type", form.type);
      formData.append(
        "price",
        form.type === "rent" ? form.rent_price : form.lease_amount
      );
      formData.append(
        "lease_duration",
        form.type === "lease" ? form.lease_duration : ""
      );
      formData.append("amenities", form.amenities);
      formData.append("latitude", coords.lat);
      formData.append("longitude", coords.lng);

      // 🔥 Clean phone numbers — strip formatting, keep last 10 digits
      formData.append(
        "phone",
        form.phone.replace(/\D/g, "").slice(-10)
      );
      formData.append(
        "whatsapp",
        form.whatsapp ? form.whatsapp.replace(/\D/g, "").slice(-10) : ""
      );

      // 🔥 Append actual image files (not blob URLs)
      images.forEach((img) => {
        formData.append("images", img);
      });

      const res = await fetch(
        "https://rental-house-finder-47uv.onrender.com/api/houses/add",
        {
          method: "POST",
          body: formData,
          // ⚠️ Do NOT set Content-Type manually — browser sets it with boundary automatically
        }
      );

      const data = await res.json();

      if (data.error) {
        alert(data.error);
      } else {
        alert("House added successfully ✅");

        setForm({
          details: "",
          location: "",
          type: "rent",
          rent_price: "",
          lease_amount: "",
          lease_duration: "",
          amenities: "",
          phone: "",
          whatsapp: "",
        });
        setImages([]);
        setPreviews([]);

        navigate("/dashboard");
      }
    } catch (err) {
      console.error(err);
      alert("❌ Error adding house");
    }
  };

  return (
    <div className="add-container">
      <div className="add-card">
        <h2>🏡 Add New House</h2>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <input name="details" value={form.details} placeholder=" " onChange={handleChange} />
            <label>House Details</label>
          </div>

          <div className="input-group">
            <input name="location" value={form.location} placeholder=" " onChange={handleChange} />
            <label>Location</label>

            {suggestions.length > 0 && (
              <div className="dropdown-options">
                {suggestions.map((s, i) => (
                  <div key={i} onClick={() => selectSuggestion(s)}>
                    📍 {s.display_name}
                  </div>
                ))}
              </div>
            )}
          </div>

          <button type="button" onClick={getCurrentLocation}>
            📍 Use My Current Location
          </button>

          <div className="input-group">
            <input
              name="phone"
              value={form.phone}
              placeholder=" "
              onFocus={() => {
                if (!form.phone) setForm({ ...form, phone: "+91 " });
              }}
              onChange={handleChange}
            />
            <label>Phone Number 📞</label>
          </div>

          <div className="input-group">
            <input
              name="whatsapp"
              value={form.whatsapp}
              placeholder=" "
              onFocus={() => {
                if (!form.whatsapp) setForm({ ...form, whatsapp: "+91 " });
              }}
              onChange={handleChange}
            />
            <label>WhatsApp Number 💬</label>
          </div>

          <div className="input-group">
            <select name="type" value={form.type} onChange={handleChange}>
              <option value="rent">🏠 Rent</option>
              <option value="lease">📜 Lease</option>
            </select>
            <label>Property Type</label>
          </div>

          {form.type === "rent" && (
            <div className="input-group">
              <input
                type="number"
                name="rent_price"
                value={form.rent_price}
                onChange={handleChange}
                placeholder=" "
              />
              <label>Monthly Rent ₹</label>
            </div>
          )}

          {form.type === "lease" && (
            <>
              <div className="input-group">
                <input
                  type="number"
                  name="lease_duration"
                  value={form.lease_duration}
                  onChange={handleChange}
                  placeholder=" "
                />
                <label>Lease Duration</label>
              </div>
              <div className="input-group">
                <input
                  type="number"
                  name="lease_amount"
                  value={form.lease_amount}
                  onChange={handleChange}
                  placeholder=" "
                />
                <label>Lease Amount ₹</label>
              </div>
            </>
          )}

          <div className="map-container">
            <MapContainer center={[coords.lat, coords.lng]} zoom={12}>
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              <ChangeMapView coords={coords} />
              <LocationPicker setCoords={setCoords} fetchAddress={fetchAddress} />
              <Marker position={[coords.lat, coords.lng]} />
            </MapContainer>
          </div>

          <div className="input-group file-upload">
            <input
              type="file"
              multiple
              accept="image/*"
              onChange={handleImageChange}
            />
            <span className="upload-text">📸 Upload Your Home Images</span>
          </div>

          <div className="preview-grid">
            {previews.map((img, i) => (
              <div key={i} className="preview-box">
                <img src={img} alt="" />
                <span onClick={() => removeImage(i)}>❌</span>
              </div>
            ))}
          </div>

          <div className="input-group">
            <input
              name="amenities"
              value={form.amenities}
              onChange={handleChange}
              placeholder=" "
            />
            <label>Amenities</label>
          </div>

          <button type="submit">Add House</button>
        </form>
      </div>
    </div>
  );
}

export default AddHouse;