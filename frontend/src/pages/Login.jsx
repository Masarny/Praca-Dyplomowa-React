import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [step, setStep] = useState(1);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [firstAttempt, setFirstAttempt] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (step === 1) {
      // Save first login attempt
      if (!username || !password) {
        setError("Proszę wypełnić oba pola.");
        return;
      }
      setFirstAttempt({ username, password });
      setUsername("");
      setPassword("");
      setError("Nieprawidłowa nazwa użytkownika lub hasło! Spróbuj ponownie.");
      setStep(2);
    } else {
       if (!username || !password) {
        setError("Proszę wypełnić oba pola.");
        return;
      }

      if (username === firstAttempt.username && password === firstAttempt.password) {
        // Successful second login
        setError("");
        navigate("/main");
      } else {
        // Mismatch
        setError("Nieprawidłowa nazwa użytkownika lub hasło! Spróbuj ponownie.");
        setUsername("");
        setPassword("");
      }
    }
  };

  return (
    <div className="container">
      <h2>Zaloguj się</h2>

      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Nazwa Użytkownika"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Hasło"
      />

      {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}

      <button className="btn" onClick={handleLogin}>
        {step === 1 ? "Zaloguj się" : "Potwierdź ponownie"}
      </button>
    </div>
  );
}
