import { respond } from "./_omst.js";

export default function handler(req, res) {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.end("Method Not Allowed");
    return;
  }
  respond(res, {
    plan_id: "plan-tokenized-bond-dvp",
    status: "PLANNED",
    assumptions: ["synthetic data", "not issuer or regulatory evidence"]
  });
}
