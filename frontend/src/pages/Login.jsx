import { useState } from "react";
import axios from "axios";

function Login() {

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const API_URL = "http://localhost:5000";

    async function login(e) {

        e.preventDefault();

        try {

            const res = await axios.post(

                `${API_URL}/login`,

                {
                    username,
                    password
                }

            );

            localStorage.setItem(
                "token",
                res.data.token
            );

            alert("Login successful!");

            window.location.href = "/";

        }

        catch {

            alert("Incorrect username or password.");

        }

    }

    return (

        <div className="login-page">

            <h1>Movie Compass</h1>

            <h2>Login</h2>

            <form onSubmit={login}>

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

                    Login

                </button>

            </form>

        </div>

    );

}

export default Login;