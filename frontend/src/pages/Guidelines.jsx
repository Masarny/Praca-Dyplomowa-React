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
      <div className="container">
        <h2>Ładowanie wytycznych...</h2>
      </div>
    );
  }

  const categories = Object.keys(guidelines);

  return (
    <div className="container_guide" style={{ textAlign: "left" }}>
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-2xl font-bold mb-4"
      >
        <p style={{ textAlign: "center" }}> Wytyczne Dotyczące Bezpieczeństwa </p>
      </motion.h2>

      <div
        style={{
          display: "flex",
          gap: "10px",
          flexWrap: "wrap",
          marginBottom: "20px",
        }}
      >
        {categories.map((cat) => (
          <motion.button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`btn ${
              selectedCategory === cat ? "btn-active" : ""
            }`}
            style={{
              backgroundColor:
                selectedCategory === cat ? "#007BFF" : "#e0e0e0",
              color: selectedCategory === cat ? "white" : "black",
              border: "none",
              padding: "10px 20px",
              borderRadius: "8px",
              cursor: "pointer",
              transition: "0.2s",
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
              padding: "20px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            }}
          >
            <h3 style={{ color: "#007BFF" }}>{selectedCategory}</h3>
            <ul style={{ paddingLeft: "20px" }}>
              {guidelines[selectedCategory]?.map((tip, i) => (
                <motion.li
                  key={i}
                  whileHover={{ scale: 1.05, color: "#007BFF" }}
                  transition={{ type: "spring", stiffness: 200 }}
                  style={{ marginBottom: "8px" }}
                >
                  {tip}
                </motion.li>
              ))}
            </ul>
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
          <button className="btn">Powrót</button>
        </Link>
      </motion.div>
    </div>
  );
}
