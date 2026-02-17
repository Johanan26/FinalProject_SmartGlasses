import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { auth } from "../config/firebase";
import axios from "axios";
import { onAuthStateChanged } from "firebase/auth";

interface MediaItem {
  _id: string;
  user_id: string;
  data: string;
}

interface GalleryData {
  photos: MediaItem[];
  videos: MediaItem[];
}

export default function Photo_video() {
  const navigate = useNavigate();
  const [gallery, setGallery] = useState<GalleryData>({
	photos: [],
	videos: []
  });

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
          const res = await axios.get("http://localhost:8000/gallery", {
            headers: { Authorization: `Bearer ${token}` },
          });

		  setGallery(res.data);
        } catch (e) {
          console.error("POLL ERROR:", e);
        }
      }, 3000);
    });

    return () => {
      unsub();
      if (interval) clearInterval(interval);
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <button
        className="flex absolute top-0 left-0 text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded text-sm px-4 py-2.5 text-center"
        onClick={() => navigate("/home")}
      >
        Back
      </button>

	  <h1 className="text-3xl font-bold text-center mb-10">My Gallery</h1>

	  <section className="mb-16">
		<h2 className="text-2xl font-semibold mb-6">Photos</h2>
		{gallery.photos.length === 0 ? (
			<p>No photos yet..</p>
		) : (
			<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
				{gallery.photos.map((photo, index) => (
					<div key={index} className="bg-gray-800 rounded-xl overflow-hidden shadow-lg p-2">
						<img src={`data:image/jpeg;base64,${photo.data}`} className="w-full h-64 object-cover"></img>
					</div>
				))}
			</div>
		)}
	  </section>

	  <section className="mb-16">
		<h2 className="text-2xl font-semibold mb-6">Videos</h2>
		{gallery.photos.length === 0 ? (
			<p>No videos yet..</p>
		) : (
			<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
				{gallery.videos.map((video, index) => (
					<div key={index} className="bg-gray-800 rounded-xl overflow-hidden shadow-lg p-2">
						<video controls className="w-full rounded-lg">
							<source src={`data:video/mp4;base64,${video.data}`}/>
						</video>
					</div>
				))}
			</div>
		)}
	  </section>
    </div>
  );
}
