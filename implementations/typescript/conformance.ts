import { runConformance } from "./compatibility";
import { verifyPackageFile } from "./verification";

const result = runConformance();
const verification = verifyPackageFile("examples/verification/valid-package.json");

if (result.vectors !== "PASS" || verification.status !== "VERIFIED") {
  throw new Error(JSON.stringify(result.failures));
}

export default { ...result, verification };
