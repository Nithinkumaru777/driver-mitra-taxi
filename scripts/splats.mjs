// Compresses the Dzire Gaussian-splat scan for the web (BRIEF §6, Phase 3 splat change).
//   npm run splats                      # reads assets/car-3d/dzire.ply
//   npm run splats -- path/to/scan.spz  # any format splat-transform reads (.ply, .spz, .splat, .ksplat, .sog)
//   npm run splats -- scan.ply -r 180,0,0 -B -2,-0.1,-3,2,2,3
//     Extra splat-transform actions after the file run first: the viewer expects the car facing +z, roof up (+y),
//     so rotate an upside-down scan here, and crop away the room around the car with a box (-B).
// Writes public/car-3d/dzire.sog (desktop, <= 10 MB) and public/car-3d/dzire-mobile.sog (<= 5 MB).
// Each file walks the quality ladder below and keeps the first step that fits its budget:
// view-dependent colour (SH bands) goes first, then splats are thinned out.
import { execFileSync } from 'node:child_process';
import { statSync, rmSync, mkdirSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const MB = 1024 * 1024;
const targets = [
  { out: 'public/car-3d/dzire.sog', budget: 10 * MB },
  { out: 'public/car-3d/dzire-mobile.sog', budget: 5 * MB },
];
const ladder = [
  { sh: 3, keep: 100 },
  { sh: 2, keep: 100 },
  { sh: 1, keep: 100 },
  { sh: 0, keep: 100 },
  { sh: 0, keep: 75 },
  { sh: 0, keep: 50 },
  { sh: 0, keep: 35 },
  { sh: 0, keep: 25 },
];

const [input = 'assets/car-3d/dzire.ply', ...actions] = process.argv.slice(2);
if (!existsSync(input)) {
  console.error(`No splat scan at ${input}. Put the scan there or pass its path: npm run splats -- <file>`);
  process.exit(1);
}

const cli = 'node_modules/@playcanvas/splat-transform/bin/cli.mjs'; // package exports don't expose it; npm scripts run from the root
const run = (...args) => execFileSync(process.execPath, [cli, '-w', '-q', ...args], { stdio: 'inherit' });
const decimated = join(tmpdir(), 'dzire-decimated.ply');
mkdirSync('public/car-3d', { recursive: true });

let start = 0; // the mobile file never needs a richer step than the desktop one
for (const { out, budget } of targets) {
  const fit = ladder.slice(start).findIndex(({ sh, keep }) => {
    if (keep < 100) {
      // --decimate must be the last action and write a .ply, so it's a separate pass (splat-transform README).
      run(input, ...actions, '-N', '-d', `${keep}%`, decimated);
      run(decimated, '-H', String(sh), out);
    } else {
      run(input, ...actions, '-N', '-H', String(sh), out);
    }
    const size = statSync(out).size;
    console.log(`${out}: ${sh} SH bands, ${keep}% of splats → ${(size / MB).toFixed(2)} MB`);
    return size <= budget;
  });
  rmSync(decimated, { force: true });
  if (fit < 0) {
    console.error(`${out} is still over ${budget / MB} MB at the lowest quality step. Crop the scan (-B box filter) or rescan with fewer splats.`);
    process.exit(1);
  }
  start += fit;
}
