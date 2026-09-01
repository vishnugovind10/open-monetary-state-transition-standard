import { GitCompareArrows } from "lucide-react";

const flow = [
  "Settlement Request",
  "Candidate Profile",
  "Compatibility",
  "Settlement Response"
];

export function ExchangePanel() {
  return (
    <section className="panel exchange-panel">
      <div className="panel-title">
        <h2>Settlement Exchange</h2>
        <GitCompareArrows size={18} aria-hidden />
      </div>
      <div className="flow-strip">
        {flow.map((item) => (
          <div key={item}>{item}</div>
        ))}
      </div>
      <dl className="compact-list">
        <div>
          <dt>Request</dt>
          <dd>EUR 50m DvP</dd>
        </div>
        <div>
          <dt>Response</dt>
          <dd>portable result</dd>
        </div>
        <div>
          <dt>Semantic parity</dt>
          <dd>Python / TypeScript PASS</dd>
        </div>
      </dl>
    </section>
  );
}
