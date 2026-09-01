import { Activity } from "lucide-react";
import { stressScenarios } from "../data";
import { statusClass } from "../evaluation";

type Props = {
  scenarioId: string;
  onSelect: (value: string) => void;
};

export function StressPanel({ scenarioId, onSelect }: Props) {
  return (
    <section className="panel stress-panel">
      <div className="panel-title">
        <h2>Stress Lab Scenarios</h2>
        <Activity size={18} aria-hidden />
      </div>
      <div className="scenario-strip">
        {stressScenarios.map((item) => (
          <button
            className={item.id === scenarioId ? "scenario selected" : "scenario"}
            key={item.id}
            onClick={() => onSelect(item.id)}
            type="button"
          >
            <strong>{item.name}</strong>
            <span>{item.condition}</span>
            <span className={statusClass(item.impact)}>{item.impact}</span>
            <span>{item.equivalenceRate.toFixed(2)}% equivalent</span>
          </button>
        ))}
      </div>
    </section>
  );
}
