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
      alert("Podaj najpierw hasło!");
      return;
    }

    try {
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
        alert(data.error || "Wystąpił błąd podczas testowania hasła.");
      }
    } catch (err) {
      console.error(err);
      alert("Błąd połączenia z serwerem.");
    }
  };

  return (
    <div className="container">
      <h2>Sprawdź siłę swojego hasła</h2>

      <input
        type="text"
        placeholder="Wpisz hasło do przetestowania"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button className="btn" onClick={testPassword}>
        Testuj hasło
      </button>

      {strength && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <p>
            <strong>Siła hasła:</strong> {strength}
          </p>

          <h3>Ostrzeżenia:</h3>
          <ul style={{ paddingLeft: "20px" }}>
            {warnings.length > 0 ? (
              warnings.map((w, i) => <li key={i}>{w}</li>)
            ) : (
              <li>Brak ostrzeżeń.</li>
            )}
          </ul>

          <h3>Sugestie:</h3>
          <ul style={{ paddingLeft: "20px" }}>
            {suggestions.length > 0 ? (
              suggestions.map((s, i) => <li key={i}>{s}</li>)
            ) : (
              <li>Brak sugestii.</li>
            )}
          </ul>

          <h3>Szacowany czas złamania:</h3>
          <p>{crackTime}</p>
        </div>
      )}

      <Link to="/main">
        <button className="btn" style={{ marginTop: "20px" }}>
          Powrót
        </button>
      </Link>
    </div>
  );
}
