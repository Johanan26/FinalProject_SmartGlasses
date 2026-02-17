import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Circle, Popup } from "react-leaflet";
import { useEffect } from "react";
import { auth } from "../config/firebase";
import axios from "axios";
import { onAuthStateChanged } from "firebase/auth";

export default function Last_location() {
  const navigate = useNavigate();

 useEffect(() => {
  let interval: number | null = null;

  const unsub = onAuthStateChanged(auth, (user) => {
    if (!user) {
      if (interval) clearInterval(interval);
      interval = null;
      return;
    }

    if (interval) return;

    interval = window.setInterval(async () => {
      try {
        const token = await user.getIdToken();
        const res = await axios.get("http://localhost:8000/get_last_location", {
          headers: { Authorization: `Bearer ${token}` },
        });
        console.log("DATA:", res.data);
      } catch (e) {
        console.error("POLL ERROR:", e);
      }
    }, 1000);
  });

  return () => {
    unsub();
    if (interval) clearInterval(interval);
  };
}, []);


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
          <MapContainer center={position} zoom={14} className="w-full h-full">
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
