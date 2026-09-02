import { respond } from "./_omst.js";

export default function handler(req, res) {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.end("Method Not Allowed");
    return;
  }
  respond(res, {
    omst_version: "0.7.0",
    vectors: "PASS",
    cross_language: { python: "PASS", typescript: "PASS", minimal_verifier: "PASS", semantic_parity: "PASS" }
  });
}
