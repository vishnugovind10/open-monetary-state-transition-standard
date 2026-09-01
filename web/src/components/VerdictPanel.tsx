import { CheckCircle2, ShieldAlert } from "lucide-react";
import { formatAmount } from "../evaluation";
import type { Instrument, SettlementVerdict } from "../types";

type Props = {
  source: Instrument;
  target: Instrument;
  amount: number;
  verdict: SettlementVerdict;
};

export function VerdictPanel({ source, target, amount, verdict }: Props) {
  const equivalent = verdict.status === "COMPATIBLE" && source.finality !== "redeemable-claim";

  return (
    <section className="panel verdict-panel" aria-live="polite">
      <div className="verdict-card">
        {verdict.status === "BLOCKED" ? (
          <ShieldAlert size={34} aria-hidden />
        ) : (
          <CheckCircle2 size={34} aria-hidden />
        )}
        <strong>{equivalent ? "EQUIVALENT" : verdict.status}</strong>
        <span>
          {source.code} to {target.code}
        </span>
      </div>
      <div className="verdict-details">
        <h2>Equivalence Verdict</h2>
        <p>{verdict.reason}</p>
        <dl>
          <div>
            <dt>Value checked</dt>
            <dd>{formatAmount.format(amount)}</dd>
          </div>
          <div>
            <dt>Latency</dt>
            <dd>{verdict.latencySeconds}s</dd>
          </div>
          <div>
            <dt>Cost</dt>
            <dd>{verdict.costBps} bps</dd>
          </div>
          <div>
            <dt>Route</dt>
            <dd>{verdict.route.length ? verdict.route.join(" -> ") : "No route"}</dd>
          </div>
        </dl>
      </div>
    </section>
  );
}
