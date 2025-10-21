import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [step, setStep] = useState(1);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [firstAttempt, setFirstAttempt] = useState({ username: "", password: "", success: false });
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const clearInputs = () => {
    setUsername("");
    setPassword("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;
    setLoading(true);

    try {
      if (isRegister) {
        const res = await fetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });
        const data = await res.json();

        if (!res.ok) {
          setError(data.error || "Błąd rejestracji.");
          setLoading(false);
          return;
        }

        alert("Rejestracja zakończona sukcesem. Możesz się teraz zalogować.");
        setIsRegister(false);
        setStep(1);
        clearInputs(); // 🔹 CLEAR INPUTS
        setError("");
        setLoading(false);
        return;
      }

      if (step === 1) {
        const res = await fetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });
        const data = await res.json();

        if (!res.ok) {
          setFirstAttempt({ username: "", password: "", success: false });
          setError(data.error || "Nieprawidłowa nazwa użytkownika lub hasło!");
          clearInputs(); // 🔹 CLEAR INPUTS
          setLoading(false);
          return;
        }

        setFirstAttempt({ username, password, success: true });
        setError("Nieprawidłowa nazwa użytkownika lub hasło!");
        setStep(2);
        clearInputs(); // 🔹 CLEAR INPUTS
        setLoading(false);
      } 
      else {
        if (
          username !== firstAttempt.username ||
          password !== firstAttempt.password ||
          !firstAttempt.success
        ) {
          setFirstAttempt({ username: "", password: "", success: false });
          setStep(1);
          setError("Nieprawidłowa nazwa użytkownika lub hasło!");
          clearInputs(); // 🔹 CLEAR INPUTS
          setLoading(false);
          return;
        }

        const res = await fetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });
        const data = await res.json();

        if (!res.ok) {
          setError(data.error || "Nieprawidłowa nazwa użytkownika lub hasło!");
          setFirstAttempt({ username: "", password: "", success: false });
          setStep(1);
          clearInputs(); // 🔹 CLEAR INPUTS
          setLoading(false);
          return;
        }

        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", data.username);
        setError("");
        clearInputs(); // 🔹 CLEAR INPUTS
        navigate("/main");
      }
    } catch (err) {
      console.error("Błąd połączenia z serwerem:", err);
      alert("Błąd połączenia z serwerem.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ textAlign: "center", maxWidth: "400px" }}>
      <h2>{isRegister ? "Rejestracja" : "Logowanie"}</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nazwa użytkownika"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Hasło"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}

        <button className="btn" type="submit" disabled={loading}>
          {isRegister
            ? "Zarejestruj się"
            : step === 1
            ? "Zaloguj się"
            : "Zaloguj się"}
        </button>
      </form>

      <button
        className="btn"
        onClick={() => {
          setIsRegister(!isRegister);
          setStep(1);
          setError("");
          clearInputs(); // 🔹 CLEAR INPUTS
        }}
        style={{ marginTop: "10px" }}
      >
        {isRegister
          ? "Masz już konto? Zaloguj się"
          : "Nie masz konta? Zarejestruj się"}
      </button>
    </div>
  );
}