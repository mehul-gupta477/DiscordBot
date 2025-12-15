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

/* ----------------- Additional Components ----------------- */

// Inventory Component
interface InventoryItem {
  id: number;
  name: string;
  icon: string;
  quantity: number;
}

interface InventoryProps {
  items: InventoryItem[];
  onItemClick?: (item: InventoryItem) => void;
}

export const Inventory: React.FC<InventoryProps> = ({ items, onItemClick }) => {
  return (
    <div style={styles.inventoryContainer}>
      <h3 style={styles.inventoryTitle}>Inventory</h3>
      <div style={styles.inventoryGrid}>
        {items.map((item) => (
          <div
            key={item.id}
            style={styles.inventorySlot}
            onClick={() => onItemClick?.(item)}
          >
            <div style={styles.itemIcon}>{item.icon}</div>
            <div style={styles.itemQuantity}>{item.quantity}</div>
            <div style={styles.itemName}>{item.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Minimap Component
interface MinimapProps {
  playerPosition: { x: number; y: number };
  enemies?: Array<{ x: number; y: number }>;
  objectives?: Array<{ x: number; y: number }>;
}

export const Minimap: React.FC<MinimapProps> = ({ 
  playerPosition, 
  enemies = [], 
  objectives = [] 
}) => {
  return (
    <div style={styles.minimapContainer}>
      <div style={styles.minimapTitle}>Map</div>
      <div style={styles.minimapCanvas}>
        {/* Player marker */}
        <div
          style={{
            ...styles.playerMarker,
            left: `${playerPosition.x}%`,
            top: `${playerPosition.y}%`,
          }}
        />
        
        {/* Enemy markers */}
        {enemies.map((enemy, idx) => (
          <div
            key={`enemy-${idx}`}
            style={{
              ...styles.enemyMarker,
              left: `${enemy.x}%`,
              top: `${enemy.y}%`,
            }}
          />
        ))}
        
        {/* Objective markers */}
        {objectives.map((obj, idx) => (
          <div
            key={`obj-${idx}`}
            style={{
              ...styles.objectiveMarker,
              left: `${obj.x}%`,
              top: `${obj.y}%`,
            }}
          />
        ))}
      </div>
    </div>
  );
};

// Quest Log Component
interface Quest {
  id: number;
  title: string;
  description: string;
  progress: number;
  maxProgress: number;
  completed: boolean;
}

interface QuestLogProps {
  quests: Quest[];
  onQuestClick?: (quest: Quest) => void;
}

export const QuestLog: React.FC<QuestLogProps> = ({ quests, onQuestClick }) => {
  return (
    <div style={styles.questLogContainer}>
      <h3 style={styles.questLogTitle}>Quests</h3>
      <div style={styles.questList}>
        {quests.map((quest) => (
          <div
            key={quest.id}
            style={{
              ...styles.questItem,
              opacity: quest.completed ? 0.6 : 1,
            }}
            onClick={() => onQuestClick?.(quest)}
          >
            <div style={styles.questHeader}>
              <span style={styles.questTitle}>{quest.title}</span>
              {quest.completed && <span style={styles.completedBadge}>✓</span>}
            </div>
            <div style={styles.questDescription}>{quest.description}</div>
            <div style={styles.questProgressBar}>
              <div
                style={{
                  ...styles.questProgressFill,
                  width: `${(quest.progress / quest.maxProgress) * 100}%`,
                }}
              />
            </div>
            <div style={styles.questProgressText}>
              {quest.progress}/{quest.maxProgress}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Notification Component
interface NotificationProps {
  message: string;
  type?: "info" | "success" | "warning" | "error";
  duration?: number;
  onClose?: () => void;
}

export const Notification: React.FC<NotificationProps> = ({ 
  message, 
  type = "info",
  onClose 
}) => {
  const getTypeColor = () => {
    switch (type) {
      case "success": return "#4caf50";
      case "warning": return "#ff9800";
      case "error": return "#f44336";
      default: return "#2196f3";
    }
  };

  return (
    <div style={{ ...styles.notification, borderLeftColor: getTypeColor() }}>
      <div style={styles.notificationMessage}>{message}</div>
      {onClose && (
        <button style={styles.notificationClose} onClick={onClose}>
          ×
        </button>
      )}
    </div>
  );
};

// Leaderboard Component
interface LeaderboardEntry {
  rank: number;
  playerName: string;
  score: number;
  isCurrentPlayer?: boolean;
}

interface LeaderboardProps {
  entries: LeaderboardEntry[];
}

export const Leaderboard: React.FC<LeaderboardProps> = ({ entries }) => {
  return (
    <div style={styles.leaderboardContainer}>
      <h3 style={styles.leaderboardTitle}>🏆 Leaderboard</h3>
      <div style={styles.leaderboardList}>
        {entries.map((entry) => (
          <div
            key={entry.rank}
            style={{
              ...styles.leaderboardEntry,
              background: entry.isCurrentPlayer ? "#444" : "#222",
              fontWeight: entry.isCurrentPlayer ? "bold" : "normal",
            }}
          >
            <span style={styles.leaderboardRank}>#{entry.rank}</span>
            <span style={styles.leaderboardName}>{entry.playerName}</span>
            <span style={styles.leaderboardScore}>{entry.score}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

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
  // Inventory styles
  inventoryContainer: {
    position: "absolute",
    bottom: 20,
    right: 20,
    width: "300px",
    background: "rgba(0,0,0,0.8)",
    borderRadius: "8px",
    padding: "15px",
    pointerEvents: "auto",
  },
  inventoryTitle: {
    color: "white",
    margin: "0 0 10px 0",
    fontSize: "18px",
  },
  inventoryGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "8px",
  },
  inventorySlot: {
    background: "#333",
    borderRadius: "6px",
    padding: "10px",
    textAlign: "center",
    cursor: "pointer",
    border: "2px solid #555",
    transition: "border-color 0.2s",
  },
  itemIcon: {
    fontSize: "24px",
    marginBottom: "5px",
  },
  itemQuantity: {
    fontSize: "12px",
    color: "#aaa",
  },
  itemName: {
    fontSize: "10px",
    color: "#ddd",
    marginTop: "5px",
  },
  // Minimap styles
  minimapContainer: {
    position: "absolute",
    top: 20,
    right: 20,
    width: "150px",
    height: "150px",
    background: "rgba(0,0,0,0.7)",
    borderRadius: "8px",
    padding: "10px",
    pointerEvents: "auto",
  },
  minimapTitle: {
    color: "white",
    fontSize: "12px",
    marginBottom: "5px",
    textAlign: "center",
  },
  minimapCanvas: {
    position: "relative",
    width: "100%",
    height: "120px",
    background: "#1a1a1a",
    borderRadius: "4px",
    border: "1px solid #444",
  },
  playerMarker: {
    position: "absolute",
    width: "8px",
    height: "8px",
    background: "lime",
    borderRadius: "50%",
    transform: "translate(-50%, -50%)",
  },
  enemyMarker: {
    position: "absolute",
    width: "6px",
    height: "6px",
    background: "red",
    borderRadius: "50%",
    transform: "translate(-50%, -50%)",
  },
  objectiveMarker: {
    position: "absolute",
    width: "6px",
    height: "6px",
    background: "gold",
    borderRadius: "50%",
    transform: "translate(-50%, -50%)",
  },
  // Quest Log styles
  questLogContainer: {
    position: "absolute",
    top: 200,
    right: 20,
    width: "280px",
    maxHeight: "400px",
    background: "rgba(0,0,0,0.8)",
    borderRadius: "8px",
    padding: "15px",
    pointerEvents: "auto",
    overflowY: "auto",
  },
  questLogTitle: {
    color: "white",
    margin: "0 0 10px 0",
    fontSize: "18px",
  },
  questList: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  questItem: {
    background: "#222",
    borderRadius: "6px",
    padding: "12px",
    cursor: "pointer",
    transition: "background 0.2s",
  },
  questHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "5px",
  },
  questTitle: {
    color: "white",
    fontSize: "14px",
    fontWeight: "bold",
  },
  completedBadge: {
    color: "lime",
    fontSize: "16px",
  },
  questDescription: {
    color: "#aaa",
    fontSize: "12px",
    marginBottom: "8px",
  },
  questProgressBar: {
    width: "100%",
    height: "6px",
    background: "#333",
    borderRadius: "3px",
    overflow: "hidden",
    marginBottom: "4px",
  },
  questProgressFill: {
    height: "100%",
    background: "#4caf50",
    transition: "width 0.3s ease",
  },
  questProgressText: {
    color: "#888",
    fontSize: "10px",
    textAlign: "right",
  },
  // Notification styles
  notification: {
    position: "fixed",
    top: "20px",
    left: "50%",
    transform: "translateX(-50%)",
    background: "#222",
    color: "white",
    padding: "15px 20px",
    borderRadius: "8px",
    borderLeft: "4px solid",
    boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
    display: "flex",
    alignItems: "center",
    gap: "10px",
    minWidth: "300px",
    pointerEvents: "auto",
  },
  notificationMessage: {
    flex: 1,
    fontSize: "14px",
  },
  notificationClose: {
    background: "transparent",
    border: "none",
    color: "white",
    fontSize: "24px",
    cursor: "pointer",
    padding: "0",
    lineHeight: "1",
  },
  // Leaderboard styles
  leaderboardContainer: {
    position: "absolute",
    top: 20,
    left: "50%",
    transform: "translateX(-50%)",
    width: "300px",
    background: "rgba(0,0,0,0.85)",
    borderRadius: "8px",
    padding: "15px",
    pointerEvents: "auto",
  },
  leaderboardTitle: {
    color: "white",
    margin: "0 0 15px 0",
    fontSize: "20px",
    textAlign: "center",
  },
  leaderboardList: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  leaderboardEntry: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 12px",
    background: "#222",
    borderRadius: "6px",
    color: "white",
    fontSize: "14px",
  },
  leaderboardRank: {
    color: "#ffd700",
    fontWeight: "bold",
    minWidth: "30px",
  },
  leaderboardName: {
    flex: 1,
    marginLeft: "10px",
  },
  leaderboardScore: {
    color: "#4caf50",
    fontWeight: "bold",
  },
};
