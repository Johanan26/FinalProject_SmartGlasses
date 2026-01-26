// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDNN2g7zD42rWi53VyYNkyeTbmeC9mc8a0",
  authDomain: "raze-glasses.firebaseapp.com",
  projectId: "raze-glasses",
  storageBucket: "raze-glasses.firebasestorage.app",
  messagingSenderId: "293951487728",
  appId: "1:293951487728:web:48f31bb1bdc9ba2c8b0c35",
  measurementId: "G-YM22GBHGQV"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export default app;