import { useState } from "react";
import { Link } from "react-router-dom";

export default function Creator() {
  const [length, setLength] = useState(24);
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generatePassword = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`/api/generate?length=${length}`);

      if (!res.ok) {
        throw new Error(`Error status ${res.status}`);
      }
      const data = await res.json();
      setPassword(data.password);
    } catch (err) {
      console.error("Error fetching password:", err);
      setError("Failed to generate password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">

      <h2>Create your password (random method)</h2>

      <label>
        Password length: <span>{length}</span>
      </label>

      <input
        type="range"
        min="8"
        max="128"
        value={length}
        onChange={(e) => setLength(Number(e.target.value))}
      />

      <button className="btn" onClick={generatePassword} disabled={loading}>
        {loading ? "Generating..." : "Generate password"}
      </button>

      <div id="generated-password-box">
        <p>Generated password: {password}</p>
      </div>
      
      {error && <p style={{ color: "red" }}>{error}</p>}

      <Link to="/main"><button className="btn">Return</button></Link>

    </div>
  );
}
