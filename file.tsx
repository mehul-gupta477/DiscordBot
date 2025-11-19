import React, { useState } from "react";

interface GameUIProps {
  score: number;
  health: number;      // 0–100
  onPause?: () => void;
  onResume?: () => void;
}

const GameUI: React.FC<GameUIProps> = ({ score, health, onPause, onResume }) => {
  const [isPaused, setIsPaused] = useState(false);

  const handlePauseToggle = () => {
    const next = !isPaused;
    setIsPaused(next);
    next ? onPause?.() : onResume?.();
  };

  return (
    <div style={styles.container}>
      {/* Top HUD */}
      <div style={styles.topBar}>
        <div style={styles.score}>Score: {score}</div>

        {/* Health Bar */}
        <div style={styles.healthContainer}>
          <div style={{ ...styles.healthBar, width: `${health}%` }} />
        </div>

        <button style={styles.pauseButton} onClick={handlePauseToggle}>
          {isPaused ? "Resume" : "Pause"}
        </button>
      </div>

      {/* Pause Overlay */}
      {isPaused && (
        <div style={styles.pauseOverlay}>
          <div style={styles.pauseBox}>
            <h2>Game Paused</h2>
            <button style={styles.resumeButton} onClick={handlePauseToggle}>
              Resume
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameUI;

/* ----------------- Styles ----------------- */

const styles: Record<string, React.CSSProperties> = {
  container: {
    position: "relative",
    width: "100%",
    height: "100%",
    pointerEvents: "none",
  },
  topBar: {
    position: "absolute",
    top: 20,
    left: 20,
    right: 20,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    pointerEvents: "auto",
  },
  score: {
    fontSize: "24px",
    color: "white",
    fontWeight: "bold",
    textShadow: "0 0 6px black",
  },
  healthContainer: {
    width: "200px",
    height: "20px",
    background: "#333",
    borderRadius: "10px",
    overflow: "hidden",
    border: "2px solid #111",
  },
  healthBar: {
    height: "100%",
    background: "limegreen",
    transition: "width 0.2s ease",
  },
  pauseButton: {
    padding: "10px 20px",
    fontSize: "16px",
    background: "#222",
    color: "white",
    border: "1px solid #555",
    borderRadius: "6px",
    cursor: "pointer",
  },
  pauseOverlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: "rgba(0,0,0,0.6)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    pointerEvents: "auto",
  },
  pauseBox: {
    background: "#222",
    padding: "30px 40px",
    borderRadius: "12px",
    textAlign: "center",
    color: "white",
    boxShadow: "0 0 12px rgba(0,0,0,0.5)",
  },
  resumeButton: {
    marginTop: "20px",
    padding: "10px 25px",
    fontSize: "18px",
    background: "#444",
    color: "white",
    border: "1px solid #888",
    borderRadius: "8px",
    cursor: "pointer",
  },
};
