// Favicon set + social share image → public/. Run: npm run icons (again after replacing the car poster).
// [TBD: logo] The icon is the checkered taxi motif on royal blue until the client's logo file arrives.
import { writeFile } from 'node:fs/promises';
import sharp from 'sharp';

const ROYAL = '#0B3D91';
const TAXI = '#FFD400';
const INK = '#121826';

// 4×4 checkerboard, 36 units square, origin top-left.
const cells = [...Array(16).keys()]
  .filter((i) => (Math.floor(i / 4) + i) % 2 === 0)
  .map((i) => `<rect x="${(i % 4) * 9}" y="${Math.floor(i / 4) * 9}" width="9" height="9"/>`)
  .join('');
const checker = `<rect width="36" height="36" fill="${TAXI}"/><g fill="${INK}">${cells}</g>`;
const icon = (radius, scale) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="${radius}" fill="${ROYAL}"/>` +
  `<g transform="translate(32 32) scale(${scale}) translate(-18 -18)">${checker}</g></svg>`;

const rounded = icon(14, 1);
// Maskable: full bleed, motif inside the 80% safe circle that Android crops to.
const maskable = icon(0, 0.85);
const png = (svg, size) => sharp(Buffer.from(svg), { density: 72 * (size / 64) }).resize(size, size).png().toBuffer();

await writeFile('public/favicon.svg', rounded);
await writeFile('public/icon-192.png', await png(rounded, 192));
await writeFile('public/icon-512.png', await png(rounded, 512));
await writeFile('public/icon-maskable-512.png', await png(maskable, 512));
// iOS rounds the corners itself, so no transparent corners here.
await writeFile('public/apple-touch-icon.png', await png(icon(0, 1), 180));

// favicon.ico = one 32px PNG wrapped in an ICO header (every browser since IE11 reads PNG-in-ICO).
const ico32 = await png(rounded, 32);
const header = Buffer.alloc(22);
header.writeUInt16LE(1, 2); // type: icon
header.writeUInt16LE(1, 4); // one image
header.writeUInt8(32, 6); // width
header.writeUInt8(32, 7); // height
header.writeUInt16LE(1, 10); // colour planes
header.writeUInt16LE(32, 12); // bits per pixel
header.writeUInt32LE(ico32.length, 14);
header.writeUInt32LE(22, 18); // image data offset
await writeFile('public/favicon.ico', Buffer.concat([header, ico32]));

// og:image: the car photo poster (npm run car:poster) with a taxi-yellow strip, 1200×630 JPEG (the size and format every share preview accepts).
const strip = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="12"><rect width="1200" height="12" fill="${TAXI}"/></svg>`;
await sharp('public/car-3d/dzire-poster-1200.webp')
  .resize(1200, 630, { fit: 'cover', position: 'centre' })
  .composite([{ input: Buffer.from(strip), gravity: 'south' }])
  .jpeg({ quality: 82, mozjpeg: true })
  .toFile('public/og-image.jpg');

console.log('✓ favicon.svg, favicon.ico, apple-touch-icon.png, icon-192/512.png, icon-maskable-512.png, og-image.jpg');
