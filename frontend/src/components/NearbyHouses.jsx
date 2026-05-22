import {useEffect,useState} from "react"
import {getNearbyHouses} from "../services/locationService"

function NearbyHouses(){

const [houses,setHouses]=useState([])

useEffect(()=>{

navigator.geolocation.getCurrentPosition(
async(position)=>{

const lat=position.coords.latitude
const lng=position.coords.longitude

const res=
await getNearbyHouses(
lat,
lng
)

setHouses(res.data)

}
)

},[])

return(

<div>

<h2>Nearby Houses</h2>

{
houses.map((house)=>(

<div key={house._id}>

<h3>{house.title}</h3>

<p>
{house.distance} km away
</p>

</div>

))
}

</div>

)

}

export default NearbyHouses