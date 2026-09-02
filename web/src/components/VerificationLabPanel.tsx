import { ShieldCheck } from "lucide-react";
import { useState } from "react";
import { tamperCases, verificationChecks } from "../data";

export function VerificationLabPanel() {
  const [selectedTamper, setSelectedTamper] = useState("liquidity");
  const tamper = tamperCases.find((item) => item.id === selectedTamper) ?? tamperCases[0];

  return (
    <section className="panel verification-panel">
      <div className="panel-title">
        <h2>Verification Lab</h2>
        <ShieldCheck size={18} aria-hidden />
      </div>
      <div className="verification-grid">
        <div className="verification-status">
          <span>Package</span>
          <strong>VERIFIED</strong>
          <small>pkg-tokenized-bond-dvp-eur-x-v07</small>
        </div>
        <div className="fingerprint-block">
          <span>Package fingerprint</span>
          <code>75ed62b3db676808ca7bf915046f381177fba931023f0995778f46d44bf6ce9f</code>
        </div>
        <div className="fingerprint-block">
          <span>Evaluation fingerprint</span>
          <code>cb7849ecba0d4afbbcbbf71d49b5220a2e6a410b1b3fc3a24107ac1f133b5252</code>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Layer</th>
            <th>Status</th>
            <th>Detail</th>
          </tr>
        </thead>
        <tbody>
          {verificationChecks.map((check) => (
            <tr key={check.layer}>
              <td>{check.layer}</td>
              <td>
                <span className={`status status-${check.status.toLowerCase()}`}>{check.status}</span>
              </td>
              <td>{check.detail}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="tamper-controls" aria-label="Tamper cases">
        {tamperCases.map((item) => (
          <button
            className={item.id === selectedTamper ? "selected" : ""}
            key={item.id}
            onClick={() => setSelectedTamper(item.id)}
            type="button"
          >
            {item.label}
          </button>
        ))}
      </div>
      <div className="tamper-result">
        <span>Tamper result</span>
        <strong>{tamper.status}</strong>
        <small>{tamper.reason}</small>
      </div>
    </section>
  );
}
