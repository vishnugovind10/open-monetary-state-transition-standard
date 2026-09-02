import { respond, verificationRecord } from "../_omst.js";

export default function handler(req, res) {
  if (req.method !== "GET" && req.method !== "POST") {
    res.statusCode = 405;
    return res.end("Method Not Allowed");
  }
  return respond(res, verificationRecord());
}
