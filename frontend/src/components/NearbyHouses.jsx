import { useEffect, useState } from "react";

function NearbyHouses() {

  const [houses, setHouses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const loadNearbyHouses = async () => {

      try {

        const response = await fetch(
          "https://rental-house-finder-47uv.onrender.com/api/external/houses"
        );

        if (!response.ok) {
          throw new Error(
            "Failed to fetch houses"
          );
        }

        const data = await response.json();

        setHouses(data);

      } catch (error) {

        console.log(
          "Nearby Houses Error:",
          error
        );

      } finally {

        setLoading(false);

      }

    };

    loadNearbyHouses();

  }, []);

  return (

    <div className="nearby-container">

      <h2>📍 Nearby Houses</h2>

      {
        loading ? (
          <p>Loading houses...</p>
        ) : houses.length === 0 ? (
          <p>No nearby houses found</p>
        ) : (

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "20px"
            }}
          >

            {houses.map((house, index) => (

              <div
                key={house._id || index}
                className="nearby-card"
              >

                <h3>
                  {house.title}
                </h3>

                <p>
                  📍 {house.location}
                </p>

                <p>
                  💰 ₹{house.price}
                </p>

                {house.distance && (

                  <p>
                    📏 {house.distance} away
                  </p>

                )}

              </div>

            ))}

          </div>

        )
      }

    </div>

  );

}

export default NearbyHouses;