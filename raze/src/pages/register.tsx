import { createUserWithEmailAndPassword } from "firebase/auth";
import React, { useState } from "react";
import { auth } from "../config/firebase";
import { redirect } from "react-router-dom";

export default function Register() {
    const [email, setEmail] = useState<string | null>(null);
    const [password, setPassword] = useState<string | null>(null);
    
    const Signup = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!email || !password) {
            return;
        }

        try {
            await createUserWithEmailAndPassword(auth, email, password);
        } catch(error: any) {
            return;
        }

        redirect("/");
    }

    return (
        <>
            <form onSubmit={(e) => Signup(e)}>
                <div>
                    <label htmlFor="email"> Email </label>
                    <input id="email" type="email" required onChange={(e) => setEmail(e.target.value)} />
                </div>

                <div>
                    <label htmlFor="password"> Password </label>
                    <input id="password" name="password" type="password" required onChange={(e) => setPassword(e.target.value)}/>
                </div>
                <button type="submit">
                    Sign in
                </button>
            </form>
        </>
    )
}