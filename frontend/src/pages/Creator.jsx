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

  const generatePassword = async () => {
    setLoading(true);
    setError(null);
    setPassword("");
    setCopied(false);

    try {
      let url = "";
      if (method === "random") {
        url = `/api/generate?length=${length}`;
      } else if (method === "diceware") {
        url = `/api/generate_diceware?count=${length}&sep=${encodeURIComponent(separator)}`;
      }

      const res = await fetch(url);
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || `Status ${res.status}`);
      }

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

  const labelText = method === "random" ? "Password length:" : "Number of words:";
  const min = method === "random" ? 8 : 1;
  const max = method === "random" ? 128 : 32;

  return (
    <div className="container">
      <h2>Create your password</h2>

      <label>Choose generation method:</label>
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
        <option value="random">Random (letters, digits, symbols)</option>
        <option value="diceware">Diceware (random words)</option>
      </select>

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

      {method === "diceware" && (
        <div>
          <label>Separator:</label>
          <select
            value={separator}
            onChange={(e) => setSeparator(e.target.value)}
            style={{ marginTop: 8, padding: 6, width: "100%" }}
          >
            <option value="space">Space ( )</option>
            <option value="dash">Dash (-)</option>
            <option value="underscore">Underscore (_)</option>
            <option value="slash">Slash (/)</option>
            <option value="random">Random separator</option>
          </select>
          <small style={{ display: "block", marginTop: 6, color: "#666" }}>
            Choose how words are joined — or let the app pick a random one.
          </small>
        </div>
      )}

      <div>
        <button
          className="btn"
          onClick={generatePassword}
          disabled={loading}
          style={{ flex: 1 }}
        >
          {loading ? "Generating..." : "Generate password"}
        </button>

        <button
          className="btn"
          onClick={() => {
            setPassword("");
            setError(null);
            setCopied(false);
          }}
          style={{ flex: 1 }}
        >
          Reset
        </button>
      </div>

      <div id="generated-password-box">
        <p style={{ marginBottom: 8, fontWeight: 600 }}>Generated password:</p>
        <div
          style={{
            backgroundColor: "#f5f5f5",
            padding: 12,
            borderRadius: 8,
            wordBreak: "break-all",
          }}
        >
          <span id="generated-password">
            {password || <em style={{ color: "#666" }}>No password yet</em>}
          </span>
        </div>

        {error && <p style={{ color: "red", marginTop: 8 }}>{error}</p>}
      </div>

      <div>
        <button className="btn" onClick={copyToClipboard} disabled={!password}>
          {copied ? "Copied!" : "Copy to clipboard"}
        </button>
      </div>

      <div>
        <button className="btn" onClick={() => alert("Save placeholder - not implemented")}>
          Save password to database
        </button>
      </div>

      <Link to="/main"><button className="btn">Return</button></Link>

    </div>
  );
}