import { Database } from "lucide-react";
import { useMemo, useState } from "react";
import { ConformancePanel } from "./components/ConformancePanel";
import { EvaluatorPanel } from "./components/EvaluatorPanel";
import { InstrumentPanel } from "./components/InstrumentPanel";
import { MoneyGraphPanel } from "./components/MoneyGraphPanel";
import { StressPanel } from "./components/StressPanel";
import { VerdictPanel } from "./components/VerdictPanel";
import { instruments, stressScenarios } from "./data";
import { evaluateSettlement } from "./evaluation";

const navItems = [
  "Overview",
  "Money",
  "Compare",
  "Settlement",
  "Plans",
  "Graph",
  "Stress Lab",
  "Conformance",
  "Specification",
  "Research"
];

export function App() {
  const [activeTab, setActiveTab] = useState("Overview");
  const [query, setQuery] = useState("");
  const [sourceCode, setSourceCode] = useState("EUR-X");
  const [targetCode, setTargetCode] = useState("EUR-X");
  const [amount, setAmount] = useState(50_000_000);
  const [scenarioId, setScenarioId] = useState("baseline");

  const source = instruments.find((item) => item.code === sourceCode) ?? instruments[0];
  const target = instruments.find((item) => item.code === targetCode) ?? instruments[1];
  const scenario = stressScenarios.find((item) => item.id === scenarioId) ?? stressScenarios[0];
  const verdict = useMemo(
    () => evaluateSettlement(source, target, amount, scenario),
    [source, target, amount, scenario]
  );

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <h1>OMST Explorer</h1>
          <p>Settlement-compatibility profiles for digital money</p>
        </div>
        <nav aria-label="Explorer sections">
          {navItems.map((item) => (
            <button
              className={activeTab === item ? "nav-active" : ""}
              key={item}
              onClick={() => setActiveTab(item)}
              type="button"
            >
              {item}
            </button>
          ))}
        </nav>
        <div className="dataset-pill">
          <Database size={16} aria-hidden />
          <span>Dataset: synthetic v0.5</span>
        </div>
      </header>

      <section className="workspace" aria-label={`${activeTab} workspace`}>
        <InstrumentPanel
          query={query}
          selectedCode={sourceCode}
          onQueryChange={setQuery}
          onSelect={setSourceCode}
        />
        <section className="main-grid">
          <EvaluatorPanel
            amount={amount}
            sourceCode={sourceCode}
            targetCode={targetCode}
            scenarioId={scenarioId}
            onAmountChange={setAmount}
            onSourceChange={setSourceCode}
            onTargetChange={setTargetCode}
            onScenarioChange={setScenarioId}
          />
          <VerdictPanel source={source} target={target} amount={amount} verdict={verdict} />
          <MoneyGraphPanel sourceCode={sourceCode} onSelect={setSourceCode} />
          <ConformancePanel />
          <StressPanel scenarioId={scenarioId} onSelect={setScenarioId} />
        </section>
      </section>

      <footer>
        <span>All examples are synthetic.</span>
        <span>Not issuer, regulatory or market-condition evidence.</span>
        <span>OMST v0.5.0</span>
      </footer>
    </main>
  );
}
