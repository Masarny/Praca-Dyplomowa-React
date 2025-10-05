import { useState } from "react";
import { Link } from "react-router-dom";

export default function Creator() {
  const [length, setLength] = useState(24);
  const [password, setPassword] = useState("");
  const [method, setMethod] = useState("random");

  const generatePassword = async () => {
    let url = "";

    if (method === "random") {
      url = `/api/generate?length=${length}`;
    } else if (method === "diceware") {
      url = `/api/generate_diceware?count=${length}`;
    } 

    const res = await fetch(url);
    const data = await res.json();

    if (res.ok) {
      setPassword(data.password);
    } else {
      setPassword("Error generating password");
    }
  };

  const handleSave = () => {
    alert("Password saved (placeholder).");
  };

  const labelText =
    method === "random"
      ? "Password length:"
      : "Number of words:";

  const min = method === "random" ? 8 : 3;
  const max = method === "random" ? 128 : 32;

  return (
    <div className="container">
      <h2>Create your password</h2>

      <label>Choose generation method:</label>
      <select
        className="password_select"
        value={method}
        onChange={(e) => setMethod(e.target.value)}
      >
        <option value="random">Random</option>
        <option value="diceware">Diceware</option>
      </select>

      <label style={{ marginTop: "15px" }}>
        {labelText} <span>{length}</span>
      </label>

      <input
        type="range"
        min={min}
        max={max}
        value={length}
        onChange={(e) => setLength(Number(e.target.value))}
      />

      <button className="btn" onClick={generatePassword}>
        Generate password
      </button>

      <div id="generated-password-box">
        <p><strong>Generated password:</strong></p>
        <p id="generated-password">{password}</p>
      </div>

      <button className="btn" onClick={handleSave}>
        Save password to database
      </button>

      <Link to="/main"><button className="btn">Return</button></Link>

    </div>
  );
}