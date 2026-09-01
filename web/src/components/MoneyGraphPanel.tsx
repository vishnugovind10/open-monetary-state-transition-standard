import { GitBranch } from "lucide-react";
import { instruments } from "../data";

type Props = {
  sourceCode: string;
  onSelect: (value: string) => void;
};

export function MoneyGraphPanel({ sourceCode, onSelect }: Props) {
  return (
    <section className="panel graph-panel">
      <div className="panel-title">
        <h2>Money Graph</h2>
        <GitBranch size={18} aria-hidden />
      </div>
      <div className="graph-canvas" aria-label="Money graph">
        {instruments.map((item, index) => (
          <button
            className={`graph-node node-${index} ${item.code === sourceCode ? "node-active" : ""}`}
            key={item.code}
            onClick={() => onSelect(item.code)}
            type="button"
          >
            {item.code}
          </button>
        ))}
        <svg aria-hidden viewBox="0 0 560 260" preserveAspectRatio="none">
          <path className="edge edge-high" d="M98 142 L236 92 L362 118" />
          <path className="edge edge-high" d="M236 92 L362 118 L462 70" />
          <path className="edge edge-medium" d="M98 142 L294 196 L462 70" />
          <path className="edge edge-low" d="M80 214 L362 118" />
        </svg>
      </div>
    </section>
  );
}
