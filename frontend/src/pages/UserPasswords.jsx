import { useEffect, useState, useCallback } from "react";
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
  const [visiblePasswords, setVisiblePasswords] = useState([]);

  const token = localStorage.getItem("token");

  const sanitizeInput = (text) => text.replace(/[<>]/g, "");

  const fetchPasswords = useCallback(async () => {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    try {
      const res = await fetch("/api/passwords/", {
        headers: { Authorization: `Bearer ${token}` },
        signal: controller.signal,
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
      setError("Błąd połączenia z serwerem lub brak autoryzacji.");
    } finally {
      clearTimeout(timeout);
    }
  }, [token]);

  useEffect(() => {
    if (token) fetchPasswords();
  }, [token, fetchPasswords]);

  const handleSave = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const cleanSite = sanitizeInput(site.trim());
    const cleanLogin = sanitizeInput(login.trim());
    const cleanPassword = sanitizeInput(password.trim());
    const cleanNotes = sanitizeInput(notes.trim());

    if (!cleanSite || !cleanLogin || !cleanPassword) {
      setError("Wszystkie pola (poza notatkami) są wymagane.");
      setLoading(false);
      return;
    }

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
      console.error("handleSave error:", err);
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

  const handleEditChange = useCallback((field, value) => {
    setEditData((prev) => ({ ...prev, [field]: value }));
  }, []);

  const handleEditSave = async (id) => {
    try {
      const res = await fetch(`/api/passwords/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          site: sanitizeInput(editData.site.trim()),
          login: sanitizeInput(editData.login.trim()),
          password: sanitizeInput(editData.password.trim()),
          notes: sanitizeInput(editData.notes.trim()),
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Błąd aktualizacji hasła");

      setEditingId(null);
      fetchPasswords();
    } catch (err) {
      console.error("handleEditSave error:", err);
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
      console.error("handleDelete error:", err);
      alert(err.message);
    }
  };

  const togglePasswordVisibility = useCallback((id) => {
    setTimeout(() => {
      setVisiblePasswords((prev) =>
        prev.includes(id) ? prev.filter((v) => v !== id) : [...prev, id]
      );
    }, 300);
  }, []);

  const handleCopyPassword = useCallback(async (text) => {
    try {
      if (!document.hasFocus()) throw new Error("Brak fokusu okna.");
      await navigator.clipboard.writeText(text);
      alert("Hasło skopiowane do schowka!");
    } catch {
      alert("Nie udało się skopiować hasła.");
    }
  }, []);

  return (
    <div className="container_db">
      <h2>Twoje zapisane hasła</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div className="table-wrapper">
        <table className="responsive-table" style={{ width: "100%" }}>
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
                          className="table-input"
                          value={editData.site}
                          onChange={(e) => handleEditChange("site", e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          className="table-input"
                          value={editData.login}
                          onChange={(e) => handleEditChange("login", e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          className="table-input"
                          value={editData.password}
                          onChange={(e) => handleEditChange("password", e.target.value)}
                        />
                      </td>
                      <td>
                        <textarea
                          className="table-textarea"
                          value={editData.notes}
                          onChange={(e) => handleEditChange("notes", e.target.value)}
                        />
                      </td>
                      <td className="table-actions">
                        <button className="table-btn" onClick={() => handleEditSave(p.id)}>Zapisz</button>
                        <button className="table-btn" onClick={() => setEditingId(null)}>Anuluj</button>
                      </td>
                    </>
                  ) : (
                    <>
                      <td>
                        <a
                          href={
                            p.site.startsWith("http://") || p.site.startsWith("https://")
                              ? p.site
                              : `https://${p.site}`
                          }
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{ color: "#0077cc", textDecoration: "none", fontWeight: "bold" }}
                        >
                          {p.site}
                        </a>
                      </td>
                      <td>{p.login}</td>
                      <td>
                        {visiblePasswords.includes(p.id)
                          ? p.password
                          : "••••••••"}
                        <button className="btn-db" onClick={() => togglePasswordVisibility(p.id)}>
                          {visiblePasswords.includes(p.id) ? "Ukryj" : "Pokaż"}
                        </button>
                        <button className="btn-db" onClick={() => handleCopyPassword(p.password)}>
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
      </div>

      <h3>Dodaj nowe hasło</h3>

      <form onSubmit={handleSave}>
        <div className="form-group">
          <input
            type="text"
            placeholder="Strona (np. gmail.com)"
            value={site}
            onChange={(e) => setSite(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <input
            type="text"
            placeholder="Login"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <input
            type="text"
            placeholder="Hasło"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <textarea
            style={{ marginTop: "15px" }}
            placeholder="Notatki (opcjonalne)"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            rows="2"
          />
        </div>

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
