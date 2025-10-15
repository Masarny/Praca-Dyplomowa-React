import { useState } from "react";
import { Link } from "react-router-dom";

export default function Creator() {
  const [method, setMethod] = useState("random");
  const [length, setLength] = useState(24);
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [separator, setSeparator] = useState("dash");
  const [copied, setCopied] = useState(false);
  const [site, setSite] = useState("");
  const [login, setLogin] = useState("");
  const [saving, setSaving] = useState(false);
  const [phrase, setPhrase] = useState("");

  const token = localStorage.getItem("token");

  const generatePassword = async () => {
    setLoading(true);
    setError(null);
    setPassword("");
    setCopied(false);

    try {
      let url = "";
      let options = {};

      if (method === "random") {
        url = `/api/generate?length=${length}`;
      } else if (method === "diceware") {
        url = `/api/generate_diceware?count=${length}&sep=${encodeURIComponent(separator)}`;
      } else if (method === "phrase") {
        url = `/api/generate_from_phrase`;
        options = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ phrase }),
        };
      }

      const res = await fetch(url, options);
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || `Status ${res.status}`);

      setPassword(data.password);
    } catch (err) {
      console.error("Generate error:", err);
      setError(err.message || "Failed to generate password");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async () => {
    if (!password) return;
    try {
      await navigator.clipboard.writeText(password);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch (e) {
      console.error("Copy failed", e);
      setError("Copy failed");
    }
  };

  const handleSavePassword = async () => {
    if (!token) {
      alert("Musisz się zalogować, aby zapisać hasło.");
      return;
    }
    if (!site || !login || !password) {
      alert("Podaj stronę, login i wygeneruj hasło przed zapisaniem.");
      return;
    }

    setSaving(true);
    try {
      const res = await fetch("/api/passwords/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          site: site.trim(),
          login: login.trim(),
          password: password.trim(),
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Błąd zapisu hasła.");

      alert("Hasło zapisane pomyślnie!");
      setSite("");
      setLogin("");
      setPassword("");
    } catch (err) {
      console.error(err);
      alert(err.message || "Nie udało się zapisać hasła.");
    } finally {
      setSaving(false);
    }
  };

  const labelText = method === "random" ? "Password length:" : "Number of words:";
  const min = method === "random" ? 8 : 1;
  const max = method === "random" ? 128 : 32;

  return (
    <div className="container">
      <h2>Stwórz Swoje hasło</h2>

      <label>Wybierz Metodę Generowania Hasła:</label>
      <select
        className="password_select"
        value={method}
        onChange={(e) => {
          setMethod(e.target.value);
          setLength(e.target.value === "random" ? 24 : 6);
          setPassword("");
          setError(null);
        }}
      >
        <option value="random">Random (Litery, Cyfry, Symbole)</option>
        <option value="diceware">Diceware (Losowe Słowa)</option>
        <option value="phrase">From phrase (Na podstawie zdania)</option>
      </select>

      {method === "phrase" ? (
        <div style={{ marginTop: 10 }}>
          <label>Wprowadź swoje zdanie:</label>
          <textarea
            placeholder="Np. Mój kot lubi spać na słońcu w maju."
            value={phrase}
            onChange={(e) => setPhrase(e.target.value)}
            rows="3"
            style={{ width: "100%", marginTop: 6 }}
          />
          <small style={{ color: "#666" }}>
            Z twojego zdania zostanie utworzone silne hasło (z wielkimi literami, cyframi, znakami specjalnymi).
          </small>
        </div>
      ) : (
        <div>
          <label>
            {labelText} <span style={{ fontWeight: 700 }}>{length}</span>
          </label>
          <input
            type="range"
            min={min}
            max={max}
            value={length}
            onChange={(e) => setLength(Number(e.target.value))}
            style={{ width: "100%", marginTop: 8 }}
          />
        </div>
      )}

      {method === "diceware" && (
        <div>
          <label>Separator:</label>
          <select
            value={separator}
            onChange={(e) => setSeparator(e.target.value)}
            style={{ marginTop: 8, padding: 6, width: "100%" }}
          >
            <option value="space">Spacja ( )</option>
            <option value="dash">Myślnik (-)</option>
            <option value="underscore">Podkreślenie (_)</option>
            <option value="slash">Ukośnik (/)</option>
            <option value="random">Losowy Separator</option>
          </select>
          <small style={{ display: "block", marginTop: 6, color: "#666" }}>
            Wybierz sposób łączenia słów - lub pozwól aplikacji wybrać słowo losowo.
          </small>
        </div>
      )}

      <div>
        <button className="btn" onClick={generatePassword} disabled={loading}>
          {loading ? "Tworzenie hasła..." : "Utwórz hasło"}
        </button>
        <button
          className="btn"
          onClick={() => {
            setPassword("");
            setError(null);
            setCopied(false);
            setPhrase("");
          }}
        >
          Resetuj
        </button>
      </div>

      <div id="generated-password-box">
        <p style={{ marginBottom: 8, fontWeight: 600 }}>Utworzone hasło:</p>
        <div
          style={{
            backgroundColor: "#f5f5f5",
            padding: 12,
            borderRadius: 8,
            wordBreak: "break-all",
          }}
        >
          <span id="generated-password">
            {password || <em style={{ color: "#666" }}>Brak Hasła</em>}
          </span>
        </div>

        {error && <p style={{ color: "red", marginTop: 8 }}>{error}</p>}
      </div>

      <div>
        <button className="btn" onClick={copyToClipboard} disabled={!password}>
          {copied ? "Skopiowano!" : "Kopiuj do schowka"}
        </button>
      </div>

      <div style={{ marginTop: 20 }}>
        <input
          placeholder="Strona (np. gmail.com)"
          value={site}
          onChange={(e) => setSite(e.target.value)}
        />
        <input
          placeholder="Login / adres e-mail"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
        />
        <button className="btn" onClick={handleSavePassword} disabled={saving}>
          {saving ? "Zapisywanie..." : "Zapisz Hasło"}
        </button>
      </div>

      <Link to="/main">
        <button className="btn">Powrót</button>
      </Link>
    </div>
  );
}
