import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Guidelines() {
  const [guidelines, setGuidelines] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/guidelines")
      .then((res) => res.json())
      .then((data) => {
        setGuidelines(data);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container">
        <h2>Loading guidelines...</h2>
      </div>
    );
  }

  return (
    <div className="container_guide" style={{ textAlign: "left" }}>
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        Wytyczne Dotyczące Bezpieczeństwa
      </motion.h2>

      {Object.entries(guidelines).map(([category, tips], idx) => (
        <motion.div
          key={category}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.2 }}
          className="guideline-card"
        >
          <h3>{category}</h3>
          <ul>
            {tips.map((tip, i) => (
              <motion.li
                key={i}
                whileHover={{ scale: 1.05, color: "#007BFF" }}
                transition={{ type: "spring", stiffness: 200 }}
              >
                {tip}
              </motion.li>
            ))}
          </ul>
        </motion.div>
      ))}

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        style={{ textAlign: "center", marginTop: "20px" }}
      >
        <Link to="/main">
          <button className="btn">Powrót</button>
        </Link>
      </motion.div>
    </div>
  );
}
