import { IndexComponent1 } from "@/typescript1/index_component_1";
import GameUI from "@/file";
import { useState } from "react";

export const IndexComponent1Parent = () => {
  const [score, setScore] = useState(0);
  const [health, setHealth] = useState(100);

  const handlePause = () => {
    console.log("Game paused");
  };

  const handleResume = () => {
    console.log("Game resumed");
  };

  return (
    <div>
      <IndexComponent1 />
      <GameUI 
        score={score} 
        health={health} 
        onPause={handlePause}
        onResume={handleResume}
      />
    </div>
  );
};