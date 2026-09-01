import { respond } from "./_omst.js";

export default function handler(req, res) {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.end("Method Not Allowed");
    return;
  }
  respond(res, {
    status: "ROUTE_FOUND",
    snapshot_id: "graph-snapshot-v06-tokenized-bond-dvp",
    primary: ["EUR-X", "CBM", "EUR-Y"],
    fallback: ["EUR-X", "REDEMPTION", "BANK_MONEY", "EUR-Y"]
  });
}
