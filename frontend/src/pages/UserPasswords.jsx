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
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({ site: "", login: "", password: "", notes: "" });
  const [visiblePasswords, setVisiblePasswords] = useState([]); // 👈 nowe

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

  const handleEditClick = (entry) => {
    setEditingId(entry.id);
    setEditData({
      site: entry.site,
      login: entry.login,
      password: entry.password,
      notes: entry.notes,
    });
  };

  const handleEditChange = (field, value) => {
    setEditData((prev) => ({ ...prev, [field]: value }));
  };

  const handleEditSave = async (id) => {
    try {
      const res = await fetch(`/api/passwords/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(editData),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Błąd aktualizacji hasła");

      setEditingId(null);
      fetchPasswords();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Czy na pewno chcesz usunąć to hasło?")) return;

    try {
      const res = await fetch(`/api/passwords/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Błąd usuwania hasła");

      fetchPasswords();
    } catch (err) {
      alert(err.message);
    }
  };

  const togglePasswordVisibility = (id) => {
    setVisiblePasswords((prev) =>
      prev.includes(id) ? prev.filter((v) => v !== id) : [...prev, id]
    );
  };

  const handleCopyPassword = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      alert("Hasło skopiowane do schowka!");
    } catch {
      alert("Nie udało się skopiować hasła.");
    }
  };

  return (
    <div className="container_db">
      <h2>Twoje zapisane hasła</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <table>
        <thead>
          <tr>
            <th>Strona</th>
            <th>Login</th>
            <th>Hasło</th>
            <th>Notatki</th>
            <th>Akcje</th>
          </tr>
        </thead>
        <tbody>
          {passwords.length > 0 ? (
            passwords.map((p) => (
              <tr key={p.id}>
                {editingId === p.id ? (
                  <>
                    <td>
                      <input
                        type="text"
                        value={editData.site}
                        onChange={(e) => handleEditChange("site", e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        value={editData.login}
                        onChange={(e) => handleEditChange("login", e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="text"
                        value={editData.password}
                        onChange={(e) => handleEditChange("password", e.target.value)}
                      />
                    </td>
                    <td>
                      <textarea
                        rows="2"
                        value={editData.notes}
                        onChange={(e) => handleEditChange("notes", e.target.value)}
                      />
                    </td>
                    <td>
                      <button onClick={() => handleEditSave(p.id)}>Zapisz</button>
                      <button onClick={() => setEditingId(null)}>Anuluj</button>
                    </td>
                  </>
                ) : (
                  <>
                    <td>{p.site}</td>
                    <td>{p.login}</td>
                    <td>
                      {visiblePasswords.includes(p.id)
                        ? p.password
                        : "••••••••"}
                      <button
                        className="btn-db"
                        onClick={() => togglePasswordVisibility(p.id)}
                      >
                        {visiblePasswords.includes(p.id) ? "Ukryj" : "Pokaż"}
                      </button>
                      <button
                        className="btn-db"
                        onClick={() => handleCopyPassword(p.password)}
                      >
                        Kopiuj
                      </button>
                    </td>
                    <td>{p.notes}</td>
                    <td>
                      <button className="btn-db" onClick={() => handleEditClick(p)}>
                        Edytuj
                      </button>
                      <button className="btn-db" onClick={() => handleDelete(p.id)}>
                        Usuń
                      </button>
                    </td>
                  </>
                )}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" style={{ textAlign: "center" }}>
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
          style={{ marginTop: "15px" }}
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
