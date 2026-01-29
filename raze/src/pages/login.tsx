import { signInWithEmailAndPassword } from "firebase/auth";
import React, { useState } from "react";
import { auth } from "../config/firebase";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState<string | null>(null);
  const [password, setPassword] = useState<string | null>(null);

  const navigate = useNavigate();

  const Login = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      return;
    }

    try {
      await signInWithEmailAndPassword(auth, email, password);
    } catch (error: any) {
      return;
    }

    navigate("/", { replace: true })
  };

  return (
    <>
      <div className="flex min-h-screen items-center justify-center bg-gray-100">
        <form
          className="w-full max-w-sm bg-white border border-gray-200 rounded-lg p-6 shadow-sm"
          onSubmit={(e) => Login(e)}
        >
          <div className="flex items-center justify-center text-bold text-3xl py-2">
            Login
          </div>
          <div>
            <label
              className="block text-sm font-medium text-gray-700 mb-1"
              htmlFor="email"
            >
              {" "}
              Email{" "}
            </label>
            <input
              id="email"
              type="email"
              className="w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2"
              required
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label
              className="block text-sm font-medium text-gray-700 mb-1"
              htmlFor="password"
            >
              {" "}
              Password{" "}
            </label>
            <input
              id="password"
              name="password"
              type="password"
              className="w-full round-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2"
              required
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="flex justify-between">
            <button onClick={(_) => navigate("/register", { replace: true })}>
              {" "}
              Sign up
            </button>
            <button type="submit">Login</button>
          </div>
        </form>
      </div>
    </>
  );
}
