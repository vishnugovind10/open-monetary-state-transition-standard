import { Play } from "lucide-react";
import { instruments, stressScenarios } from "../data";

type Props = {
  amount: number;
  sourceCode: string;
  targetCode: string;
  scenarioId: string;
  onAmountChange: (value: number) => void;
  onSourceChange: (value: string) => void;
  onTargetChange: (value: string) => void;
  onScenarioChange: (value: string) => void;
};

export function EvaluatorPanel({
  amount,
  sourceCode,
  targetCode,
  scenarioId,
  onAmountChange,
  onSourceChange,
  onTargetChange,
  onScenarioChange
}: Props) {
  return (
    <section className="panel evaluator" aria-labelledby="settlement-title">
      <div className="panel-title">
        <h2 id="settlement-title">Settlement Compatibility</h2>
        <button className="primary-button" type="button">
          <Play size={16} aria-hidden />
          Evaluate Profile
        </button>
      </div>
      <div className="form-grid">
        <label>
          Amount
          <input
            aria-label="Settlement amount"
            min="1"
            step="1000000"
            type="number"
            value={amount}
            onChange={(event) => onAmountChange(Number(event.target.value))}
          />
        </label>
        <label>
          Candidate
          <select
            aria-label="Source instrument"
            value={sourceCode}
            onChange={(event) => onSourceChange(event.target.value)}
          >
            {instruments.map((item) => (
              <option key={item.code} value={item.code}>
                {item.code} - {item.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Settlement leg
          <select
            aria-label="Target instrument"
            value={targetCode}
            onChange={(event) => onTargetChange(event.target.value)}
          >
            {instruments.map((item) => (
              <option key={item.code} value={item.code}>
                {item.code} - {item.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Stress context
          <select
            aria-label="Stress context"
            value={scenarioId}
            onChange={(event) => onScenarioChange(event.target.value)}
          >
            {stressScenarios.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
              </option>
            ))}
          </select>
        </label>
      </div>
    </section>
  );
}
