// Driver photo pipeline: assets/drivers-original/* → public/drivers/<name>-<width>.{avif,webp}
// Auto-rotates from EXIF, then strips ALL metadata (EXIF, GPS, XMP). Run: npm run drivers
import { mkdir, readdir, rm } from 'node:fs/promises';
import { extname, basename } from 'node:path';
import sharp from 'sharp';
import { driverPhotoWidths } from '../src/content/site.ts';

const SRC = 'assets/drivers-original';
const OUT = 'public/drivers';
const formats = { avif: { quality: 50 }, webp: { quality: 75 } };

const photos = (await readdir(SRC)).filter((f) => /\.(jpe?g|png|webp|avif|tiff?)$/i.test(f));
await rm(OUT, { recursive: true, force: true }); // rebuild from scratch: removed originals don't linger online
await mkdir(OUT, { recursive: true });

for (const file of photos) {
  const name = basename(file, extname(file));
  for (const width of driverPhotoWidths) {
    for (const [format, options] of Object.entries(formats)) {
      const out = `${OUT}/${name}-${width}.${format}`;
      // rotate() bakes in the EXIF orientation. sharp drops metadata unless asked to keep it.
      // withoutEnlargement: small originals get same-size files at the larger widths (harmless).
      await sharp(`${SRC}/${file}`).rotate().resize({ width, withoutEnlargement: true })[format](options).toFile(out);
      const meta = await sharp(out).metadata();
      if (meta.exif || meta.xmp || meta.iptc) throw new Error(`${out} still has metadata — not publishing it.`);
    }
  }
  console.log(`✓ ${file}`);
}
console.log(`${photos.length} photo(s) → ${OUT}/ (no EXIF/GPS)`);
