const API_URL =
"https://rental-house-finder-47uv.onrender.com/api";

export const getNearbyHouses = async (
  lat,
  lng
) => {

  try {

    const response = await fetch(
      `${API_URL}/nearby?lat=${lat}&lng=${lng}`
    );

    if (!response.ok) {
      throw new Error("Failed to fetch nearby houses");
    }

    const data = await response.json();

    return data;

  } catch (error) {

    console.log(
      "Nearby fetch error:",
      error
    );

    return [];

  }

};