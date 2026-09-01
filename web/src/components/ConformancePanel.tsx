import { FileCheck2 } from "lucide-react";
import { conformanceRows } from "../data";

export function ConformancePanel() {
  return (
    <section className="panel conformance-panel">
      <div className="panel-title">
        <h2>Conformance Status</h2>
        <FileCheck2 size={18} aria-hidden />
      </div>
      <table>
        <thead>
          <tr>
            <th>Instrument</th>
            <th>Core</th>
            <th>Value</th>
            <th>Settlement</th>
            <th>Jurisdiction</th>
            <th>Overall</th>
          </tr>
        </thead>
        <tbody>
          {conformanceRows.map((row) => (
            <tr key={row[0]}>
              {row.map((cell, index) => (
                <td key={cell + index} className={cell === "warn" ? "warn-cell" : ""}>
                  {cell === "pass" ? "Pass" : cell === "warn" ? "Review" : cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
