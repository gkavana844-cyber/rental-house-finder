import axios from "./api"

export const getNearbyHouses=async(
lat,
lng
)=>{

return await axios.get(
`/nearby?lat=${lat}&lng=${lng}`
)

}