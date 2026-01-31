import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import Register from "./pages/register";
import { auth } from "./config/firebase";
import Login from "./pages/login";
import Ai_questions from "./pages/ai_questions";
import Last_location from "./pages/last_location";
import Photo_video from "./pages/photo_video";

function App() {
  auth.onAuthStateChanged(function(user) {
      if (user) {
          console.log('This is the user: ', user)
      } else {
          console.log('There is no logged in user');
      }
  });

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/ai_question" element={<Ai_questions/>} />
        <Route path="/photo_video" element={<Photo_video />} />
        <Route path="/last_location" element={<Last_location />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
