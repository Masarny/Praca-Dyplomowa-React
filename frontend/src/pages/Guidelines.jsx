import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

export default function Guidelines() {
  const [guidelines, setGuidelines] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("Ataki na Użytkowników");

  useEffect(() => {
    fetch("/api/guidelines")
      .then((res) => res.json())
      .then((data) => {
        setGuidelines(data);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container" style={{ textAlign: "center", marginTop: "40px" }}>
        <h2>Ładowanie wytycznych...</h2>
      </div>
    );
  }

  const categories = Object.keys(guidelines);

  return (
    <div className="container_guide" style={{ textAlign: "left", padding: "20px" }}>
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-2xl font-bold mb-4"
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
          >
            Powrót
          </button>
        </Link>
      </motion.div>
    </div>
  );
}
