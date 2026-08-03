import { useState } from "react";
import axios from "axios";
import "./Auth.css";

function Register() {

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const API_URL = "http://localhost:5000";

    async function register(e) {

        e.preventDefault();

        try {

            await axios.post(

                `${API_URL}/register`,

                {
                    username,
                    password
                }

            );

            alert("Account created!");

            window.location.href="/login";

        }

        catch(error){

            alert(error.response.data.message);

        }

    }

    return (

        <div className="auth-page">

            <div className="auth-card">

            <h1>Movie Compass</h1>

            <h2>Create Account</h2>

            <form className="auth-form" onSubmit={register}>

                <input

                    type="text"

                    placeholder="Username"

                    value={username}

                    onChange={(e)=>setUsername(e.target.value)}

                />

                <input

                    type="password"

                    placeholder="Password"

                    value={password}

                    onChange={(e)=>setPassword(e.target.value)}

                />

                <button>

                    Register

                </button>

            </form>

            </div>
        </div>

    );

}

export default Register;