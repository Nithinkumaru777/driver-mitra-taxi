// Shared motion setup (BRIEF §7). The tier is set before first paint by the inline script in Base.astro:
//   full    = everything
//   lite    = low-end device or Save-Data: no smooth scroll, tilt, float or scroll-linked 3D
//   reduced = prefers-reduced-motion: no movement, content shown as-is
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export const tier = (document.documentElement.dataset.motion ?? 'full') as 'full' | 'lite' | 'reduced';
export { gsap, ScrollTrigger };

/**
 * Calls fn once per element when its top reaches 90% of the viewport, including elements the page
 * loads already scrolled past. (`once: true` triggers skip those, and throw if created past their end.)
 */
export function onceVisible(targets: string | Element[] | NodeListOf<Element>, fn: (els: Element[]) => void) {
  const done = new WeakSet<Element>();
  ScrollTrigger.batch(targets, {
    start: 'top 90%',
    end: 'max',
    onEnter: (els) => {
      const fresh = els.filter((el) => !done.has(el));
      fresh.forEach((el) => done.add(el));
      if (fresh.length) fn(fresh);
    },
  });
}

/** Counts the element's number up from 0 when it scrolls into view. Non-numbers (e.g. [TBD]) are left as they are. */
export function countUp(el: HTMLElement) {
  const end = Number(el.textContent);
  if (tier === 'reduced' || !Number.isInteger(end) || end <= 0) return;
  // Fixed width + tabular digits: the box never changes size while counting.
  el.style.minWidth = `${String(end).length}ch`;
  el.style.fontVariantNumeric = 'tabular-nums';
  el.style.display = 'inline-block';
  const n = { v: 0 };
  el.textContent = '0';
  onceVisible([el], () =>
    gsap.to(n, { v: end, duration: 0.9, ease: 'power2.out', snap: { v: 1 }, onUpdate: () => void (el.textContent = String(n.v)) }),
  );
}
