import { respond } from "./_omst.js";

export default function handler(req, res) {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.end("Method Not Allowed");
    return;
  }
  respond(res, {
    status: "FUNCTIONALLY_EQUIVALENT",
    boundary: "Synthetic reference equivalence response."
  });
}
