import {
  respond,
  verificationPackage,
  verificationRecord,
  verificationResult,
  verificationTamper
} from "../_omst.js";

const actions = {
  package: verificationPackage,
  record: verificationRecord,
  tamper: verificationTamper,
  verify: verificationResult
};

export default function handler(req, res) {
  if (req.method !== "GET" && req.method !== "POST") {
    res.statusCode = 405;
    res.end("Method Not Allowed");
    return;
  }
  const action = Array.isArray(req.query.action) ? req.query.action[0] : req.query.action;
  const body = action && actions[action] ? actions[action]() : { status: "UNKNOWN_ENDPOINT", endpoint: action };
  return respond(res, body);
}
