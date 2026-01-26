import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import Register from "./pages/register";
import { auth } from "./config/firebase";

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
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
