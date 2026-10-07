// Gaussian-splat car viewer (BRIEF §6): three.js + Spark + OrbitControls.
// Only CarStage.astro imports it, through import(), so three.js and Spark stay out of the first page load.
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { SparkRenderer, SplatMesh } from '@sparkjsdev/spark';

type Vec3 = [number, number, number];
export interface Anchor {
  at: Vec3;
  normal: Vec3;
}

const deg = THREE.MathUtils.degToRad;
const RESUME_AFTER_MS = 3000;

// One download per file, shared by both stages (hero + Our Car), with progress for each stage's loader bar.
const downloads = new Map<string, { bytes: Promise<Uint8Array>; listeners: Set<(p: number) => void> }>();
function download(url: string, onProgress: (p: number) => void) {
  let d = downloads.get(url);
  if (!d) {
    const listeners = new Set<(p: number) => void>();
    const bytes = fetch(url).then(async (res) => {
      if (!res.ok || !res.body) throw new Error(`${url}: HTTP ${res.status}`);
      const total = Number(res.headers.get('content-length')) || 0;
      const chunks: Uint8Array[] = [];
      let loaded = 0;
      for (const reader = res.body.getReader(); ; ) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
        loaded += value.length;
        if (total) listeners.forEach((fn) => fn(loaded / total));
      }
      const out = new Uint8Array(loaded);
      chunks.reduce((at, c) => (out.set(c, at), at + c.length), 0);
      return out;
    });
    downloads.set(url, (d = { bytes, listeners }));
  }
  d.listeners.add(onProgress);
  return d.bytes;
}

/** Soft elliptical contact shadow under the car: a radial gradient on a flat plane, no light or shadow map needed. */
function contactShadow(width: number, depth: number) {
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const g = c.getContext('2d')!;
  const grad = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  grad.addColorStop(0, 'rgba(7,42,102,0.55)'); // royal-deep
  grad.addColorStop(0.6, 'rgba(7,42,102,0.25)');
  grad.addColorStop(1, 'rgba(7,42,102,0)');
  g.fillStyle = grad;
  g.fillRect(0, 0, 128, 128);
  const plane = new THREE.Mesh(
    new THREE.PlaneGeometry(width * 1.35, depth * 1.2),
    new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false }),
  );
  plane.rotation.x = -Math.PI / 2;
  plane.position.y = 0.003;
  plane.renderOrder = -1;
  return plane;
}

export async function mountCar(opts: {
  stage: HTMLElement;
  url: string;
  autoRotate: boolean;
  anchors: Anchor[];
  onProgress: (p: number) => void;
  onFirstInteraction: () => void;
  /** GPU dropped the context (driver reset, memory pressure on phones): the stage falls back to the poster. */
  onContextLost: () => void;
}) {
  const { stage, url, anchors } = opts;
  const bytes = await download(url, opts.onProgress);

  const canvas = document.createElement('canvas');
  canvas.className = 'absolute inset-0 size-full opacity-0 transition-opacity duration-500 group-data-[state=ready]:opacity-100';
  canvas.setAttribute('data-lenis-prevent', ''); // wheel over the car zooms instead of smooth-scrolling the page
  let lost = false;
  canvas.addEventListener('webglcontextlost', () => {
    lost = true;
    renderer.setAnimationLoop(null);
    opts.onContextLost();
  });
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false }); // Spark recommends no MSAA
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5)); // ponytail: fixed cap; splats are fill-rate bound, adapt to fps if phones stutter
  const scene = new THREE.Scene();
  scene.add(new SparkRenderer({ renderer }));
  const camera = new THREE.PerspectiveCamera(35, 1, 0.05, 100);

  const car = new SplatMesh({ fileBytes: bytes.slice(), fileName: url }); // Spark picks the format from the extension; copy since it may transfer the buffer to its worker
  await car.initialized;

  // Stand the car on the floor at the origin. The scan must already face +z with +y up (npm run splats -- … -r x,y,z).
  const box = car.getBoundingBox();
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  car.position.set(-center.x, -box.min.y, -center.z);
  const pivot = new THREE.Group(); // turned by the scroll-linked orbit; holds the car, its shadow and the hotspot anchors
  pivot.add(car, contactShadow(size.x, size.z));
  scene.add(pivot);

  const controls = new OrbitControls(camera, canvas);
  controls.target.set(0, size.y * 0.42, 0);
  controls.enablePan = false;
  controls.enableDamping = true;
  controls.minPolarAngle = deg(40); // never under the floor or straight down on the roof
  controls.maxPolarAngle = deg(88);
  controls.autoRotate = opts.autoRotate;
  controls.autoRotateSpeed = 25 / 6; // OrbitControls: 1 = 6°/s when update() gets a delta → 25°/s
  canvas.style.touchAction = 'pan-y'; // vertical swipes still scroll the page on phones; sideways drags turn the car

  const radius = size.length() / 2;
  const fit = () => {
    const { clientWidth: w, clientHeight: h } = stage;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    // Distance that fits the car's bounding sphere in the narrower field of view.
    const halfV = deg(camera.fov / 2);
    const halfH = Math.atan(Math.tan(halfV) * camera.aspect);
    const dist = (radius / Math.sin(Math.min(halfV, halfH))) * 0.9;
    controls.minDistance = dist * 0.6;
    controls.maxDistance = dist * 1.4;
    return dist;
  };
  // Opening view = the poster's angle (front-left three-quarter, photo 02), slightly above.
  camera.position.setFromSphericalCoords(fit() ?? radius * 3, deg(76), deg(35)).add(controls.target);
  new ResizeObserver(fit).observe(stage);

  // Pause while the visitor drags/zooms; resume ~3 s after they let go (unless paused with the button).
  let paused = !opts.autoRotate;
  let resumeTimer = 0;
  let touched = false;
  controls.addEventListener('start', () => {
    clearTimeout(resumeTimer);
    controls.autoRotate = false;
    if (touched) return;
    touched = true;
    opts.onFirstInteraction();
  });
  controls.addEventListener('end', () => {
    resumeTimer = window.setTimeout(() => (controls.autoRotate = !paused), RESUME_AFTER_MS);
  });

  // 3D-anchored hotspots: anchor in car-box units → screen pixels every frame; hidden when their side faces away.
  const spots = [...stage.querySelectorAll<HTMLElement>('[data-hotspot]')].map((el) => {
    const a = anchors[Number(el.dataset.hotspot)];
    return {
      el,
      local: new THREE.Vector3(a.at[0] * size.x * 0.5, a.at[1] * size.y, a.at[2] * size.z * 0.5),
      normal: new THREE.Vector3(...a.normal).normalize(),
    };
  });
  const p = new THREE.Vector3();
  const n = new THREE.Vector3();
  const toCamera = new THREE.Vector3();
  const placeSpots = () => {
    for (const s of spots) {
      pivot.localToWorld(p.copy(s.local));
      n.copy(s.normal).applyQuaternion(pivot.quaternion);
      const facing = n.dot(toCamera.subVectors(camera.position, p)) > 0;
      p.project(camera);
      const x = ((p.x + 1) / 2) * stage.clientWidth;
      s.el.style.transform = `translate(${x}px, ${((1 - p.y) / 2) * stage.clientHeight}px)`;
      s.el.toggleAttribute('data-away', !facing);
      s.el.toggleAttribute('data-flip', x > stage.clientWidth / 2);
    }
  };

  // Render only while the stage is on screen (rAF already stops in background tabs).
  let last = 0;
  const tick = (time: number) => {
    controls.update(last ? (time - last) / 1000 : 0);
    last = time;
    renderer.render(scene, camera);
    placeSpots();
  };
  new IntersectionObserver(([e]) => {
    last = 0; // no jump after being off screen
    renderer.setAnimationLoop(e.isIntersecting && !lost ? tick : null);
  }).observe(stage);

  stage.append(canvas);
  return {
    canvas,
    /** Pause/resume button. */
    setPaused(value: boolean) {
      paused = value;
      clearTimeout(resumeTimer);
      controls.autoRotate = !value;
    },
    /** Scroll-linked turn, in degrees (turns the car, so it adds to the visitor's own orbit). */
    setTurn(degrees: number) {
      pivot.rotation.y = -deg(degrees);
    },
  };
}
