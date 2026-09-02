import { verifyPackageFile } from "./verification";

const path = process.argv[2] ?? "examples/verification/valid-package.json";
const result = verifyPackageFile(path);

console.log(JSON.stringify(result, null, 2));

if (result.status !== "VERIFIED") {
  process.exitCode = 1;
}
