import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

export default function Guidelines() {
  const [guidelines, setGuidelines] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("Ataki na Użytkowników");
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();
    const cached = localStorage.getItem("guidelines");

    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        if (parsed && typeof parsed === "object") {
          setGuidelines(parsed);
          setLoading(false);
        }
      } catch {
        console.warn("Nie udało się odczytać cache guidelines.");
      }
    }

    fetch("/api/guidelines")
      .then((res) => {
        if (!res.ok) throw new Error("Błąd sieci");
        return res.json();
      })
      .then((data) => {
        if (data && typeof data === "object" && !Array.isArray(data)) {
          setGuidelines(data);
          localStorage.setItem("guidelines", JSON.stringify(data));
        } else {
          console.error("Niepoprawny format danych z backendu");
          setError("Niepoprawny format danych z serwera.");
          setGuidelines(null);
        }
        setLoading(false);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error("Błąd pobierania:", err);
          setError("Nie udało się pobrać danych z serwera.");
          setLoading(false);
          setGuidelines(null);
        }
      });

    return () => controller.abort();
  }, []);

  if (error) {
    return (
      <div style={{ textAlign: "center", marginTop: "40px" }}>
        <h3 role="alert" aria-live="assertive">{error}</h3>
        <Link to="/main">
          <button
            className="btn"
            style={{
              backgroundColor: "#007BFF",
              color: "white",
              padding: "10px 20px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              marginTop: "20px",
            }}
            aria-label="Powrót do strony głównej po błędzie"
          >
            Powrót
          </button>
        </Link>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container" style={{ textAlign: "center", marginTop: "40px" }}>
        <h2>Ładowanie wytycznych...</h2>
      </div>
    );
  }

if (!loading && !guidelines) {
    return (
      <div style={{ textAlign: "center", marginTop: "40px" }}>
        <h3 role="alert">Nie udało się pobrać wytycznych. Spróbuj ponownie później.</h3>
        <Link to="/main">
          <button
            className="btn"
            style={{
              backgroundColor: "#007BFF",
              color: "white",
              padding: "10px 20px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              marginTop: "20px",
            }}
          >
            Powrót
          </button>
        </Link>
      </div>
    );
  }

  const categories = Array.isArray(Object.keys(guidelines)) ? Object.keys(guidelines) : [];

  return (
    <div className="container_guide" style={{ textAlign: "left", padding: "20px" }}>
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-2xl font-bold mb-4"
        aria-label="Wytyczne dotyczące bezpieczeństwa"
      >
        <p style={{ textAlign: "center", fontSize: "1.8rem" }}>
          Wytyczne Dotyczące Bezpieczeństwa
        </p>
      </motion.h2>

      <div
        style={{
          display: "flex",
          gap: "10px",
          flexWrap: "wrap",
          justifyContent: "center",
          marginBottom: "25px",
        }}
        role="tablist"
        aria-label="Kategorie wytycznych"
      >
        {categories.map((cat) => (
          <motion.button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`btn ${selectedCategory === cat ? "btn-active" : ""}`}
            style={{
              backgroundColor: selectedCategory === cat ? "#007BFF" : "#e0e0e0",
              color: selectedCategory === cat ? "white" : "black",
              border: "none",
              padding: "10px 20px",
              borderRadius: "8px",
              cursor: "pointer",
              transition: "0.2s",
              fontWeight: "500",
            }}
            aria-selected={selectedCategory === cat}
            role="tab"
          >
            {cat}
          </motion.button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        {selectedCategory && (
          <motion.div
            key={selectedCategory}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -15 }}
            transition={{ duration: 0.3 }}
            className="guideline-card"
            style={{
              background: "#f9f9f9",
              borderRadius: "10px",
              padding: "25px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
              lineHeight: "1.6",
            }}
            role="tabpanel"
            aria-label={`Wytyczne dla kategorii ${selectedCategory}`}
          >
            <h3
              style={{
                color: "#007BFF",
                marginBottom: "15px",
                fontSize: "1.4rem",
                textAlign: "center",
              }}
            >
              {selectedCategory}
            </h3>

            <div style={{ color: "#333", fontSize: "1rem" }}>
              {guidelines[selectedCategory]?.map((tip, i) => (
                <motion.p
                  key={i}
                  whileHover={{ scale: 1.02, color: "#007BFF" }}
                  transition={{ type: "spring", stiffness: 200 }}
                  style={{
                    marginBottom: "14px",
                    padding: "8px 0",
                    borderBottom: "1px solid #e0e0e0",
                  }}
                  tabIndex={0}
                >
                  {tip}
                </motion.p>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        style={{ textAlign: "center", marginTop: "25px" }}
      >
        <Link to="/main">
          <button
            className="btn"
            style={{
              backgroundColor: "#007BFF",
              color: "white",
              padding: "10px 20px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
            }}
            aria-label="Powrót do strony głównej"
          >
            Powrót
          </button>
        </Link>
      </motion.div>
    </div>
  );
}
