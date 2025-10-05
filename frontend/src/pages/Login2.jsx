import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Login2() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("Incorrect username or password! Try again.");
  const navigate = useNavigate();

  const handleLogin = async () => {
    const stored = JSON.parse(localStorage.getItem("firstLogin"));

    let attempts = parseInt(localStorage.getItem("loginAttempts") || "0");

    if (!stored) {
      setMessage("Session expired. Please log in again.");
      setTimeout(() => navigate("/login_1"), 1500);
      return;
    }

    if (username === stored.username && password === stored.password) {
      localStorage.removeItem("firstLogin");
      localStorage.removeItem("loginAttempts");
      navigate("/main");
      } else {
      attempts += 1;
      localStorage.setItem("loginAttempts", attempts.toString());

      if (attempts >= 3) {
        setMessage("Too many failed attempts. Restarting login...");
        setTimeout(() => {
          localStorage.removeItem("firstLogin");
          localStorage.removeItem("loginAttempts");
          navigate("/login_1");
        }, 1500);
      } else {
        setMessage(`Incorrect username or password! Try again.`);
      }
    }
  };

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem("firstLogin"));

    if (!stored) {
      setMessage("You must complete step 1 first.");
      setTimeout(() => navigate("/login_1"), 1500);
    }

  }, [navigate]);

  return (
    <div className="container">

      <h2>Log in</h2>

      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Input username"
      />

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Input password"
      />

      <p style={{ color: "red" }}>{message}</p>

      <button className="btn" onClick={handleLogin}>Log in</button>

    </div>
  );
}
