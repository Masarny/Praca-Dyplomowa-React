import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [step, setStep] = useState(1);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [firstAttempt, setFirstAttempt] = useState({ username: "", password: "", success: false });
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");
  const [passwordStrength, setPasswordStrength] = useState("");
  const [passwordRequirements, setPasswordRequirements] = useState([]);
  const [loading, setLoading] = useState(false);
  const [totp, setTotp] = useState("");
  const [qrCode, setQrCode] = useState(""); // ✅ dodane tylko to
  const navigate = useNavigate();

  const clearInputs = () => {
    setUsername("");
    setPassword("");
    setPasswordStrength("");
    setPasswordRequirements([]);
  };

  const checkPasswordStrength = (password) => {
    let strength = 0;
    if (password.length >= 15) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[!@#$%^&*(),.?":{}|<>_\-+=]/.test(password)) strength++;
    if (strength <= 2) return "Słabe";
    if (strength === 3 || strength === 4) return "Średnie";
    if (strength === 5) return "Silne";
    return "";
  };

  const getPasswordRequirements = (password) => {
    const missing = [];
    if (password.length < 15) missing.push("co najmniej 15 znaków");
    if (!/[A-Z]/.test(password)) missing.push("wielką literę");
    if (!/[0-9]/.test(password)) missing.push("cyfrę");
    if (!/[-!@#$%^&*(),.?\":{}|<>_+=]/.test(password)) missing.push("znak specjalny");
    return missing;
  };

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setPassword(value);
    if (isRegister) {
      setPasswordStrength(checkPasswordStrength(value));
      setPasswordRequirements(getPasswordRequirements(value));
    }
  };

  const handleTotpSubmit = async (e) => {
    e.preventDefault();
    if (!totp) {
      setError("Wprowadź kod TOTP.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("/api/auth/verify_totp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: firstAttempt.username, totp }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Nieprawidłowy kod TOTP.");
        setLoading(false);
        return;
      }
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("username", data.username);
      setError("");
      clearInputs();
      navigate("/main");
    } catch (err) {
      console.error("Błąd połączenia z serwerem:", err);
      alert("Błąd połączenia z serwerem.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;
    setLoading(true);
    try {
      if (isRegister) {
        const missing = getPasswordRequirements(password);
        if (missing.length > 0) {
          setError(`Hasło musi zawierać: ${missing.join(", ")}.`);
          setLoading(false);
          return;
        }
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

        // ✅ Po rejestracji pokaż QR kod
        setQrCode(data.qr_code || "");
        alert("Zeskanuj ten kod QR w aplikacji Google Authenticator.");
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
          clearInputs();
          setLoading(false);
          return;
        }
        setFirstAttempt({ username, password, success: true });
        setError("Nieprawidłowa nazwa użytkownika lub hasło!");
        setStep(2);
        clearInputs();
        setLoading(false);
      } else if (step === 2) {
        if (
          username !== firstAttempt.username ||
          password !== firstAttempt.password ||
          !firstAttempt.success
        ) {
          setFirstAttempt({ username: "", password: "", success: false });
          setStep(1);
          setError("Nieprawidłowa nazwa użytkownika lub hasło!");
          clearInputs();
          setLoading(false);
          return;
        }
        setStep(3);
        setError("");
        clearInputs();
        setLoading(false);
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

      {/* ✅ QR kod po rejestracji */}
      {qrCode && (
        <div style={{ marginTop: 20 }}>
          <p>Zeskanuj ten kod QR w aplikacji Google Authenticator:</p>
          <img src={qrCode} alt="QR" style={{ width: "200px", margin: "auto" }} />
          <button
            className="btn"
            onClick={() => {
              setQrCode("");
              setIsRegister(false);
              setStep(1);
            }}
            style={{ marginTop: "10px" }}
          >
            Przejdź do logowania
          </button>
        </div>
      )}

      {!qrCode && step !== 3 ? (
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
            onChange={handlePasswordChange}
            required
          />
          {isRegister && password && passwordRequirements.length > 0 && (
            <div style={{ color: "red", marginTop: 5, fontSize: "0.9em" }}>
              Hasło musi zawierać:{" "}
              {passwordRequirements.map((req, idx) => (
                <span key={idx}>
                  {req}
                  {idx < passwordRequirements.length - 1 ? ", " : "."}
                </span>
              ))}
            </div>
          )}
          {isRegister && password && (
            <p
              style={{
                color:
                  passwordStrength === "Silne"
                    ? "green"
                    : passwordStrength === "Średnie"
                    ? "orange"
                    : "red",
                marginTop: 5,
                fontWeight: "bold",
              }}
            >
              Siła hasła: {passwordStrength}
            </p>
          )}
          {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}
          <button className="btn" type="submit" disabled={loading}>
            {isRegister ? "Zarejestruj się" : "Zaloguj się"}
          </button>
        </form>
      ) : null}

      {!qrCode && step === 3 && (
        <form onSubmit={handleTotpSubmit}>
          <input
            type="text"
            placeholder="Kod TOTP (Google Authenticator)"
            value={totp}
            onChange={(e) => setTotp(e.target.value)}
            required
          />
          {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}
          <button className="btn" type="submit" disabled={loading}>
            Zweryfikuj kod
          </button>
        </form>
      )}

      {!qrCode && (
        <button
          className="btn"
          onClick={() => {
            setIsRegister(!isRegister);
            setStep(1);
            setError("");
            clearInputs();
          }}
          style={{ marginTop: "10px" }}
        >
          {isRegister
            ? "Masz już konto? Zaloguj się"
            : "Nie masz konta? Zarejestruj się"}
        </button>
      )}
    </div>
  );
}
