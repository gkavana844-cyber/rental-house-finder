import { useEffect, useState } from "react";

function NearbyHouses() {

  const [houses, setHouses] = useState([]);

  useEffect(() => {

    const loadNearbyHouses = async () => {

      try {

        const response = await fetch(
          "https://rental-house-finder-47uv.onrender.com/api/external/houses"
        );

        const data = await response.json();

        setHouses(data);

      } catch (error) {

        console.log(
          "Nearby Houses Error:",
          error
        );

      }

    };

    loadNearbyHouses();

  }, []);

  return (

    <div className="nearby-container">

      <h2>📍 Nearby Houses</h2>

      {
        houses.length === 0 ? (

          <p>No nearby houses found</p>

        ) : (

          houses.map((house, index) => (

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

              {
                house.distance && (

                  <p>
                    📏 {house.distance} km away
                  </p>

                )
              }

            </div>

          ))

        )
      }

    </div>

  );

}

export default NearbyHouses;