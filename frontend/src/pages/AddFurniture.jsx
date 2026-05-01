import { useState } from "react";
import { addFurniture } from "../services/furnitureService";

export default function AddFurniture() {
  const [form, setForm] = useState({
    name: "",
    price: "",
    contact: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await addFurniture(form);

    if (res.success) {
      alert("Furniture added ✅");
      setForm({ name: "", price: "", contact: "" });
    } else {
      alert(res.error);
    }
  };

  return (
    <div className="form-container">
      <h2>🪑 Add Furniture</h2>

      <form onSubmit={handleSubmit}>
        <input
          name="name"
          placeholder="Furniture Name"
          value={form.name}
          onChange={handleChange}
        />

        <input
          name="price"
          type="number"
          placeholder="Price ₹"
          value={form.price}
          onChange={handleChange}
        />

        <input
          name="contact"
          placeholder="Contact Number"
          value={form.contact}
          onChange={handleChange}
        />

        <button type="submit">Add Furniture</button>
      </form>
    </div>
  );
}