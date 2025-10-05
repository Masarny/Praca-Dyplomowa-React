import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login1() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!username || !password) {
      alert("Please enter both username and password.");
      return;
    }

    localStorage.setItem("firstLogin", JSON.stringify({ username, password }));

    localStorage.setItem("loginAttempts", "0");

    navigate("/login_2");
  };

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

      <button className="btn" onClick={handleLogin}>Log in</button>

    </div>
  );
}
