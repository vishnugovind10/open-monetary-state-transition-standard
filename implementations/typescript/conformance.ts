import { runConformance } from "./compatibility";

const result = runConformance();

if (result.vectors !== "PASS") {
  throw new Error(JSON.stringify(result.failures));
}

export default result;
