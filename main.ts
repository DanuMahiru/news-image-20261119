import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry for news-image-20261119: the whole program is one image.
// Copy it to the output directory, byte for byte, deterministically.
// v6: "The Daily Globe", 40 stories (Trump-Xi-Putin Shenzhen summit lead),
// rendered by render.py; this file only moves entry.png into place.
const root = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(root, "entry.png"), join(outDir, "entry.png"));
