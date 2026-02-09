import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Circle, Popup } from "react-leaflet";

export default function Last_location() {
  const navigate = useNavigate();


  const latitude = 53.227482;
  const longitude = -8.425962333333333;
  const radiusMeters = 50;

  const position: [number, number] = [latitude, longitude];

  return (
    <div className="w-full h-screen bg-slate-700 relative">
      
      <button
        className="absolute top-4 right-4 z-[1000] text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-red-300 font-medium rounded text-sm px-4 py-2.5 shadow-lg"
        onClick={() => navigate("/home")}
      >
        Back
      </button>

      <div className="w-full h-full p-4">
        <div className="w-full h-full rounded-xl overflow-hidden shadow-xl">
          <MapContainer
            center={position}
            zoom={14}
            className="w-full h-full"
          >
            <TileLayer
              attribution="© OpenStreetMap contributors"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            <Marker position={position}>
              <Popup>Last known location</Popup>
            </Marker>

            <Circle
              center={position}
              radius={radiusMeters}
              pathOptions={{
                color: "blue",
                fillColor: "#3f8efc",
                fillOpacity: 0.3,
              }}
            />
          </MapContainer>
        </div>
      </div>
    </div>
  );
}
