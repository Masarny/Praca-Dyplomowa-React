import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function UserPasswords() {
  const [passwords, setPasswords] = useState([]);
  const [site, setSite] = useState("");
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const token = localStorage.getItem("token");

  const fetchPasswords = async () => {
    try {
      const res = await fetch("/api/passwords/", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        const msg = await res.text();
        console.error("Błąd backendu:", res.status, msg);
        throw new Error("Błąd pobierania danych lub autoryzacji.");
      }

      const data = await res.json();
      setPasswords(data);
    } catch (e) {
      console.error("fetchPasswords error:", e);
      alert("Błąd połączenia z serwerem lub brak autoryzacji.");
    }
  };

  useEffect(() => {
    if (token) fetchPasswords();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await fetch("/api/passwords/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ site, login, password, notes }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Błąd zapisu hasła");

      setSite("");
      setLogin("");
      setPassword("");
      setNotes("");
      fetchPasswords();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Twoje zapisane hasła</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <table>
        <thead>
          <tr>
            <th>Strona</th>
            <th>Login</th>
            <th>Hasło</th>
            <th>Notatki</th>
          </tr>
        </thead>
        <tbody>
          {passwords.length > 0 ? (
            passwords.map((p) => (
              <tr key={p.id}>
                <td>{p.site}</td>
                <td>{p.login}</td>
                <td>{p.password}</td>
                <td>{p.notes}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" style={{ textAlign: "center" }}>
                Brak zapisanych haseł.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <h3>Dodaj nowe hasło</h3>
      <form onSubmit={handleSave}>
        <input
          type="text"
          placeholder="Strona (np. gmail.com)"
          value={site}
          onChange={(e) => setSite(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Login"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Hasło"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <textarea
          placeholder="Notatki (opcjonalne)"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows="2"
        />
        <button className="btn" type="submit" disabled={loading}>
          {loading ? "Zapisywanie..." : "Zapisz hasło"}
        </button>
      </form>

      <Link to="/main">
        <button className="btn" style={{ marginTop: "20px" }}>
          Powrót
        </button>
      </Link>
    </div>
  );
}
