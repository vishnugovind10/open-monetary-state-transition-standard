import { Search, SlidersHorizontal } from "lucide-react";
import { instruments } from "../data";
import { statusClass } from "../evaluation";
import type { Instrument } from "../types";

type Props = {
  query: string;
  selectedCode: string;
  onQueryChange: (value: string) => void;
  onSelect: (value: string) => void;
};

export function InstrumentPanel({ query, selectedCode, onQueryChange, onSelect }: Props) {
  const filteredInstruments = instruments.filter((item) =>
    `${item.code} ${item.name} ${item.type}`.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <aside className="panel instruments-panel">
      <div className="panel-title">
        <h2>Money Instruments</h2>
        <button aria-label="Filter instruments" className="icon-button" type="button">
          <SlidersHorizontal size={17} />
        </button>
      </div>
      <label className="search-box">
        <Search size={16} aria-hidden />
        <input
          aria-label="Search instruments"
          placeholder="Search instruments..."
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
        />
      </label>
      <div className="instrument-list" role="list">
        {filteredInstruments.map((item) => (
          <InstrumentRow
            instrument={item}
            key={item.code}
            selected={item.code === selectedCode}
            onSelect={onSelect}
          />
        ))}
      </div>
      <dl className="summary-list">
        <div>
          <dt>Total instruments</dt>
          <dd>{instruments.length}</dd>
        </div>
        <div>
          <dt>Active</dt>
          <dd>{instruments.filter((item) => item.status === "active").length}</dd>
        </div>
        <div>
          <dt>Settlement domains</dt>
          <dd>4</dd>
        </div>
        <div>
          <dt>Evidence status</dt>
          <dd>Synthetic</dd>
        </div>
      </dl>
    </aside>
  );
}

function InstrumentRow({
  instrument,
  selected,
  onSelect
}: {
  instrument: Instrument;
  selected: boolean;
  onSelect: (value: string) => void;
}) {
  return (
    <button
      className={selected ? "instrument-row selected" : "instrument-row"}
      onClick={() => onSelect(instrument.code)}
      type="button"
    >
      <span className="code">{instrument.code}</span>
      <span>{instrument.name}</span>
      <span className={statusClass(instrument.status)}>{instrument.status}</span>
    </button>
  );
}
