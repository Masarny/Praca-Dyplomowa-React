import { useState } from "react";
import { Link } from "react-router-dom";

export default function Tester() {
  const [password, setPassword] = useState("");
  const [strength, setStrength] = useState("");
  const [warnings, setWarnings] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [crackTime, setCrackTime] = useState("");

  const testPassword = async () => {
    if (!password) {
      alert("Please enter a password first!");
      return;
    }

    const res = await fetch("/api/test_password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });

    const data = await res.json();

    if (res.ok) {
      setStrength(data.strength);
      setWarnings(data.warnings);
      setSuggestions(data.suggestions);
      setCrackTime(data.crack_time);
    } else {
      alert(data.error || "Error testing password.");
    }
  };

  return (
    <div className="container">
      <h2>Test the strength of your password</h2>

      <input
        type="text"
        placeholder="Input your password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button className="btn" onClick={testPassword}>Test</button>

      {strength && (
        <>
          <p>
            <strong>Strength:</strong> {strength}
          </p>
          <h3>Warnings:</h3>
          <ul>
            {warnings.map((w, i) => (
              <li key={i}>{w}</li>
            ))}
          </ul>
          <h3>Suggestions:</h3>
          <ul>
            {suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
          <h3>Estimated crack time:</h3>
          <p>{crackTime}</p>
        </>
      )}

      <Link to="/main"><button className="btn">Return</button></Link>
    </div>
  );
}
