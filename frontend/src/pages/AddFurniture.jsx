import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/AddFurniture.css";

export default function AddFurniture() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    price: "",
    contact: ""
  });

  const [image, setImage] = useState(null); // ✅ NEW
  const [preview, setPreview] = useState(null); // ✅ NEW

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // 🔁 HANDLE INPUT
  const handleChange = (e) => {
    let { name, value } = e.target;

    if (name === "contact") {
      let digits = value.replace(/\D/g, "");

      if (digits.startsWith("91")) digits = digits.slice(2);

      digits = digits.slice(0, 10);

      if (digits.length > 5) {
        value = `+91 ${digits.slice(0, 5)} ${digits.slice(5)}`;
      } else if (digits.length > 0) {
        value = `+91 ${digits}`;
      } else {
        value = "";
      }
    }

    setForm({ ...form, [name]: value });
  };

  // 📸 IMAGE SELECT
  const handleImageChange = (e) => {
    const file = e.target.files[0];

    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  // 📤 SUBMIT
  const handleSubmit = async (e) => {
    e.preventDefault();

    const cleanNumber = form.contact.replace(/\D/g, "").slice(-10);

    if (!form.name || !form.price || !cleanNumber) {
      setMessage("❌ All fields required");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();

      formData.append("name", form.name);
      formData.append("price", form.price);
      formData.append("contact", cleanNumber);

      if (image) {
        formData.append("image", image); // 🔥 SEND IMAGE
      }

      const res = await fetch(
        "https://rental-house-finder-47uv.onrender.com/api/furniture/add",
        {
          method: "POST",
          body: formData
        }
      );

      const data = await res.json();

      if (data.success) {
        setMessage("✅ Furniture added");

        setTimeout(() => navigate("/"), 1000);
      } else {
        setMessage(data.error);
      }

    } catch (err) {
      setMessage("❌ Upload failed");
    }

    setLoading(false);
  };

  return (
    <div className="add-furniture-container">
      <div className="furniture-card">
        <h2>🪑 Add Furniture</h2>

        <form onSubmit={handleSubmit}>
          <input name="name" placeholder="Furniture Name" value={form.name} onChange={handleChange} />
          <input name="price" type="number" placeholder="Price ₹" value={form.price} onChange={handleChange} />

          <input
            name="contact"
            placeholder="+91 98765 43210"
            value={form.contact}
            onChange={handleChange}
          />

          {/* 📸 IMAGE INPUT */}
          <input type="file" accept="image/*" onChange={handleImageChange} />

          {/* PREVIEW */}
          {preview && <img src={preview} className="preview" alt="preview" />}

          <button disabled={loading}>
            {loading ? "Uploading..." : "Add Furniture"}
          </button>

          {message && <p className="msg">{message}</p>}
        </form>
      </div>
    </div>
  );
}