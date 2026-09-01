import { AlertTriangle, CheckCircle2, ShieldAlert } from "lucide-react";
import { formatAmount } from "../evaluation";
import type { Instrument, SettlementVerdict } from "../types";

type Props = {
  source: Instrument;
  target: Instrument;
  amount: number;
  verdict: SettlementVerdict;
};

export function VerdictPanel({ source, target, amount, verdict }: Props) {
  const isCompatible = verdict.status === "COMPATIBLE";
  const isIncompatible = verdict.status === "INCOMPATIBLE";

  return (
    <section className="panel verdict-panel" aria-live="polite">
      <div className={`verdict-card verdict-${verdict.status.toLowerCase()}`}>
        {isIncompatible ? (
          <ShieldAlert size={34} aria-hidden />
        ) : isCompatible ? (
          <CheckCircle2 size={34} aria-hidden />
        ) : (
          <AlertTriangle size={34} aria-hidden />
        )}
        <strong>{verdict.status}</strong>
        <span>
          {source.code} against {target.code}
        </span>
      </div>
      <div className="verdict-details">
        <h2>Compatibility Profile</h2>
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
            <dt>Confidence</dt>
            <dd>{verdict.confidence}</dd>
          </div>
          <div>
            <dt>Route</dt>
            <dd>{verdict.route.length ? verdict.route.join(" -> ") : "No route"}</dd>
          </div>
        </dl>
        <div className="reason-list" aria-label="Reason codes">
          {verdict.reasons.length ? (
            verdict.reasons.map((reason) => <span key={reason}>{reason}</span>)
          ) : (
            <span>NO_BLOCKING_CONDITIONS</span>
          )}
        </div>
      </div>
    </section>
  );
}
