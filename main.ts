// gta6-meme-x-01 entry program (Node 22, standard library only).
// Its only job: copy POST.json from the repository root into the
// output directory, where the grader reads the X post address.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

// Fail loudly with the source path named, so a missing or unreadable
// POST.json is easy to diagnose from the run log alone.
try {
  copyFileSync(join(botDir, "POST.json"), join(outputDir, "POST.json"));
} catch (err) {
  const reason = err instanceof Error ? err.message : String(err);
  console.error(`could not copy POST.json from ${botDir}: ${reason}`);
  process.exit(1);
}
