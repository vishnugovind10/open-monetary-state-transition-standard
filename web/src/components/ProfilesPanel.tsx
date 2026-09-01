import { Braces } from "lucide-react";

const profiles = [
  ["MoneyProfile", "EUR-X", "PUBLISHED", "fingerprinted"],
  ["SettlementProfile", "Network A", "PUBLISHED", "24/7 DvP"],
  ["ParticipantProfile", "party-a", "SYNTHETIC", "non-PII"],
  ["InteroperabilityProfile", "ISO 20022", "EXPERIMENTAL", "approximated"]
];

export function ProfilesPanel() {
  return (
    <section className="panel profiles-panel">
      <div className="panel-title">
        <h2>Profiles</h2>
        <Braces size={18} aria-hidden />
      </div>
      <table>
        <thead>
          <tr>
            <th>Profile</th>
            <th>Subject</th>
            <th>Status</th>
            <th>Conformance</th>
          </tr>
        </thead>
        <tbody>
          {profiles.map(([profile, subject, status, conformance]) => (
            <tr key={profile}>
              <td>{profile}</td>
              <td>{subject}</td>
              <td>{status}</td>
              <td>{conformance}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
