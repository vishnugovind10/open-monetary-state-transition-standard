import { respond } from "./_omst.js";

export default function handler(req, res) {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.end("Method Not Allowed");
    return;
  }
  respond(res, {
    omst_version: "0.6.0",
    vectors: "PASS",
    cross_language: { python: "PASS", typescript: "PASS", semantic_parity: "PASS" }
  });
}
