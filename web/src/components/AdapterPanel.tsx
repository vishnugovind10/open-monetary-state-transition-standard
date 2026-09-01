import { Cable } from "lucide-react";

const mappings = [
  ["OMST", "EXACT"],
  ["ISO 20022", "APPROXIMATED"],
  ["OTAS", "DERIVED"],
  ["CDM", "LOSSY"]
];

export function AdapterPanel() {
  return (
    <section className="panel adapter-panel">
      <div className="panel-title">
        <h2>Adapters</h2>
        <Cable size={18} aria-hidden />
      </div>
      <div className="adapter-grid">
        {mappings.map(([name, status]) => (
          <div key={name}>
            <strong>{name}</strong>
            <span>{status}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
