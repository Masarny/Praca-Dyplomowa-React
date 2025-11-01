import { useState, useRef  } from "react";
import { Link } from "react-router-dom";

export default function Tester() {
  const [password, setPassword] = useState("");
  const [strength, setStrength] = useState("");
  const [warnings, setWarnings] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [crackTime, setCrackTime] = useState("");
  const [improvedPassword, setImprovedPassword] = useState("");
  const [loadingImprove, setLoadingImprove] = useState(false);
  const [loadingTest, setLoadingTest] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const abortRef = useRef(null);

  const fetchWithTimeout = async (url, options, timeout = 8000) => {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    try {
      const res = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(id);
      return res;
    } catch (err) {
      clearTimeout(id);
      throw err;
    }
  };

  const testPassword = async () => {
    if (!password) {
      alert("Podaj najpierw hasło!");
      return;
    }

    setLoadingTest(true);
    setError("");
    try {
      abortRef.current?.abort();
      abortRef.current = new AbortController();

      const res = await fetch("/api/test_password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
        signal: abortRef.current.signal,
      });

      const data = await res.json().catch(() => ({}));

      if (res.ok && data) {
        setStrength(data.strength || "Nieznana");
        setWarnings(data.warnings || []);
        setSuggestions(data.suggestions || []);
        setCrackTime(data.crack_time || "");
        setImprovedPassword("");
      } else {
        setError(data.error || "Wystąpił błąd podczas testowania hasła.");
      }
    } catch (err) {
      console.error("Błąd połączenia:", err);
      if (err.name === "AbortError") setError("Przerwano żądanie (timeout).");
      else setError("Błąd połączenia z serwerem.");
    } finally {
      setLoadingTest(false);
    }
  };

  const improvePassword = async () => {
    if (!password.trim()) {
      alert("Najpierw przetestuj hasło!");
      return;
    }
    setLoadingImprove(true);
    setError("");
    try {
      const res = await fetch("/api/improve_password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });

      const data = await res.json().catch(() => ({}));
      if (res.ok && data.improved_password) {
        setImprovedPassword(data.improved_password);
      } else {
        setError(data.error || "Nie udało się ulepszyć hasła.");
      }
    } catch (err) {
      console.error(err);
      setError("Błąd połączenia z serwerem.");
    } finally {
      setLoadingImprove(false);
    }
  };

  const copyImproved = async () => {
    if (!improvedPassword) return;
    try {
      await navigator.clipboard.writeText(improvedPassword);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (err) {
      console.error("Copy failed", err);
      setError("Nie udało się skopiować hasła.");
    }
  };

  return (
    <div className="container" style={{ marginTop: "150px" }}>
      <h2>Sprawdź siłę swojego hasła</h2>

      <input
        type="text"
        placeholder="Wpisz hasło do przetestowania"
        aria-label="Wpisz hasło do przetestowania"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button
        className="btn"
        onClick={testPassword}
        disabled={loadingTest}
        aria-busy={loadingTest}
      >
        {loadingTest ? "Testuję..." : "Testuj hasło"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: 10, fontWeight: "bold" }}>{error}</p>
      )}
  
      {strength && !error && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <p>
            <strong>Siła hasła:</strong> {strength}
          </p>

          <div style={{ background: "#f8f8f8", padding: "10px", borderRadius: "8px" }}>
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
          </div>

          <h3>Szacowany czas złamania:</h3>
          <p style={{ textAlign: "center" }}>{crackTime}</p>

          <div style={{ marginTop: "25px" }}>
            <h3>Propozycja silniejszego hasła:</h3>
            <button className="btn" onClick={improvePassword} disabled={loadingImprove}>
              {loadingImprove ? "Generowanie..." : "Zaproponuj silniejsze hasło"}
            </button>

            {improvedPassword && (
              <div
                style={{
                  marginTop: "10px",
                  backgroundColor: "#f5f5f5",
                  padding: "10px",
                  borderRadius: "8px",
                  wordBreak: "break-all",
                }}
              >
                <strong>{improvedPassword}</strong>
                <div style={{ marginTop: "8px" }}>
                  <button className="btn" onClick={copyImproved}>
                    {copied ? "Skopiowano!" : "Kopiuj"}
                  </button>
                </div>
              </div>
            )}
          </div>
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
