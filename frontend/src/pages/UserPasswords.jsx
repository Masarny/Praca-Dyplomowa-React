import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function UserPasswords() {
  const [passwords, setPasswords] = useState([]);
  const [site, setSite] = useState("");
  const [username, setUsername] = useState("");
  const [pwd, setPwd] = useState("");
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");

  const fetchPasswords = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/passwords/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Nie udało się pobrać danych");
      const data = await res.json();
      setPasswords(data);
    } catch (e) {
      console.error(e);
      setPasswords([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPasswords();
  }, []);

  const handleAdd = async () => {
    if (!site || !username || !pwd) {
      alert("Wypełnij wszystkie pola.");
      return;
    }

    try {
      const res = await fetch("/api/passwords/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ site, login: username, password: pwd }),
      });
      if (!res.ok) throw new Error("Nie udało się dodać hasła.");
      setSite("");
      setUsername("");
      setPwd("");
      fetchPasswords();
    } catch (e) {
      console.error(e);
      alert(e.message);
    }
  };

  return (
    <div className="container">
      <h2>Hasła Użytkownika</h2>

      {loading ? (
        <p>Ładowanie...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Strona</th>
              <th>Login</th>
              <th>Hasło</th>
            </tr>
          </thead>
          <tbody>
            {passwords.length > 0 ? (
              passwords.map((p, i) => (
                <tr key={i}>
                  <td>{p.site}</td>
                  <td>{p.login}</td>
                  <td>{p.password}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3" style={{ textAlign: "center", color: "#777" }}>
                  Brak zapisanych haseł.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}

      {/* 🔹 Formularz dodawania nowego wpisu */}
      <div style={{ marginTop: 20 }}>
        <h3>Dodaj nowe hasło</h3>
        <input
          placeholder="Strona (np. gmail.com)"
          value={site}
          onChange={(e) => setSite(e.target.value)}
        />
        <input
          placeholder="Login / adres e-mail"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          placeholder="Hasło"
          value={pwd}
          onChange={(e) => setPwd(e.target.value)}
        />
        <button className="btn" onClick={handleAdd}>
          Dodaj
        </button>
      </div>

      <Link to="/main">
        <button className="btn">Powrót</button>
      </Link>
    </div>
  );
}
