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

  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);

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

  // ❌ REMOVE IMAGE
  const removeImage = () => {
    setImage(null);
    setPreview(null);
  };

  // 📤 SUBMIT
  const handleSubmit = async (e) => {
    e.preventDefault();

    const cleanNumber = form.contact.replace(/\D/g, "").slice(-10);

    if (!form.name || !form.price || !cleanNumber) {
      setMessage("❌ All fields required");
      return;
    }

    if (cleanNumber.length !== 10) {
      setMessage("❌ Enter valid phone number");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const formData = new FormData();

      formData.append("name", form.name);
      formData.append("price", form.price);
      formData.append("contact", cleanNumber);

      if (image) {
        formData.append("image", image);
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
        setMessage("✅ Furniture added successfully");

        setForm({ name: "", price: "", contact: "" });
        setImage(null);
        setPreview(null);

        setTimeout(() => {
          navigate("/dashboard");
        }, 1200);

      } else {
        setMessage(data.error || "❌ Failed to add furniture");
      }

    } catch (err) {
      console.error(err);
      setMessage("❌ Upload failed");
    }

    setLoading(false);
  };

  return (
    <div className="add-furniture-container">
      <div className="furniture-card">
        <h2>🪑 Add Furniture</h2>

        <form onSubmit={handleSubmit}>

          {/* ━━ NAME ━━ */}
          <div className="input-group">
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              required
              placeholder=" "
            />
            <label>Furniture Name (Bed, Sofa...)</label>
          </div>

          {/* ━━ PRICE ━━ */}
          <div className="input-group">
            <input
              name="price"
              type="number"
              value={form.price}
              onChange={handleChange}
              required
              placeholder=" "
            />
            <label>Price ₹</label>
          </div>

          {/* ━━ CONTACT ━━ */}
          <div className="input-group">
            <input
              name="contact"
              value={form.contact}
              onChange={handleChange}
              required
              placeholder=" "
            />
            <label>+91 77777 88888</label>
          </div>

          {/* 🔥 CUSTOM UPLOAD */}
          <label className="upload-box">
            📸 Add your furniture image
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              hidden
            />
          </label>

          {/* 🖼 PREVIEW */}
          {preview && (
            <div className="preview-container">
              <img src={preview} alt="preview" />
              <button type="button" onClick={removeImage}>❌</button>
            </div>
          )}

          <button type="submit" disabled={loading}>
            {loading ? "Uploading..." : "Add Furniture"}
          </button>

          {message && (
            <p className={message.includes("✅") ? "success" : "error"}>
              {message}
            </p>
          )}

        </form>
      </div>
    </div>
  );
}