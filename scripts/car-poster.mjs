// Crops the instant poster for the car stage from the real photo (BRIEF §6): npm run car:poster
// Shown before the splat loads and as the fallback (no WebGL2, low-end device, load error). Also feeds og-image (npm run icons).
import sharp from 'sharp';

const src = 'reference/dzire-3d/photos/02-front-three-quarter-left.jpg';
// Crop box as fractions of the photo: the car with a little showroom on each side, ~1.4:1 so it covers
// both the 4:3 hero stage and the 16:11 Our Car stage without losing the bumpers.
const crop = { left: 0.1, top: 0, width: 0.72, height: 1 };

const img = sharp(src).rotate();
const { width, height } = await img.metadata();
const region = {
  left: Math.round(crop.left * width),
  top: Math.round(crop.top * height),
  width: Math.round(crop.width * width),
  height: Math.round(crop.height * height),
};
for (const w of [640, 1200]) {
  const out = `public/car-3d/dzire-poster-${w}.webp`;
  const info = await img.clone().extract(region).resize({ width: w }).webp({ quality: 78 }).toFile(out);
  console.log(`${out}: ${info.width}×${info.height}, ${(info.size / 1024).toFixed(0)} KB`);
}
