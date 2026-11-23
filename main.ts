// Entry point for the news-image-20261123 entry.
//
// The repository ships the finished front-page image as entry.png.
// This program's only job is to place that image where the harness
// expects it: /output/entry.png, or $MAKEFUN_OUTPUT_DIR/entry.png
// when the harness points the output somewhere else.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
