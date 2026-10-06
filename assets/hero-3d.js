/* GP METHOD: real gym equipment (cut-out photos) floating without gravity over the hero photo.
   Flat photos on planes: they turn only around Z (±25°) and sway a little on X/Y (±6°), never a full turn.
   Drift around a home point, a free zone around the hero copy, a push from pointer/finger, collisions.
   Paused when the hero is off screen or the tab is hidden; reduced motion = still scene. */

(() => {
  const hero = document.querySelector('.hero');
  const canvas = hero && hero.querySelector('.hero-scene');
  if (!canvas) return;

  // Three.js (≈600 KB) is fetched only after the page has loaded, so it never competes with the photo and the fonts
  const THREE_URL = 'https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js';
  const start = () => {
    const probe = document.createElement('canvas');
    if (!(probe.getContext('webgl2') || probe.getContext('webgl'))) return; // no WebGL: the photo alone is the hero
    const run = () => { if (window.THREE) { try { init(window.THREE); } catch (e) { canvas.remove(); } } };
    if (window.THREE) { run(); return; }
    const script = document.createElement('script');
    script.src = THREE_URL; script.async = true;
    script.onload = run; // CDN blocked: onerror does nothing, the photo stays
    document.head.append(script);
  };
  const later = () => ('requestIdleCallback' in window ? requestIdleCallback(start, { timeout: 1500 }) : setTimeout(start, 200));
  if (document.readyState === 'complete') later();
  else window.addEventListener('load', later, { once: true });

  function init(THREE) {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const desktopQuery = window.matchMedia('(min-width: 900px)');
    const copy = hero.querySelector('.hero-copy');
    const DEG = Math.PI / 180;

    /* ---------- renderer + camera: 1 world unit = 1 CSS pixel at z = 0 ---------- */

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: 'low-power' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(30, 1, 10, 6000);

    let W = 0; let H = 0;
    const resize = () => {
      W = hero.clientWidth; H = hero.clientHeight;
      renderer.setSize(W, H, false);
      camera.aspect = W / H;
      camera.position.set(W / 2, -H / 2, (H / 2) / Math.tan((camera.fov / 2) * DEG));
      camera.lookAt(W / 2, -H / 2, 0);
      camera.updateProjectionMatrix();
    };

    /* ---------- the five photos (webp with alpha, png fallback) + one soft shadow ---------- */

    const KINDS = {
      //            image size      width on desktop / phone   collision circles along the long side
      manubrio:   { w: 1200, h: 537,  d: 210, m: 118, circles: 3 },
      kettlebell: { w: 890,  h: 1200, d: 128, m: 78,  circles: 1 },
      disco:      { w: 1036, h: 1200, d: 150, m: 88,  circles: 1 },
      palla:      { w: 1198, h: 1200, d: 150, m: 88,  circles: 1 },
      bilanciere: { w: 1842, h: 143,  d: 560, m: 260, circles: 7 },
    };
    const MIX = {
      desktop: ['bilanciere', 'manubrio', 'manubrio', 'manubrio', 'kettlebell', 'kettlebell', 'disco', 'disco', 'disco', 'palla'],
      mobile: ['bilanciere', 'manubrio', 'manubrio', 'kettlebell', 'disco', 'disco', 'palla'],
    };

    const loader = new THREE.TextureLoader();
    const loadTexture = (name) => new Promise((resolve) => {
      const done = (t) => { t.encoding = THREE.sRGBEncoding; t.anisotropy = 4; resolve(t); };
      loader.load(`assets/attrezzi/${name}.webp`, done, undefined,
        () => loader.load(`assets/attrezzi/${name}.png`, done, undefined, () => resolve(null)));
    });

    const shadowTexture = (() => {
      const c = document.createElement('canvas'); c.width = c.height = 128;
      const g = c.getContext('2d');
      const grad = g.createRadialGradient(64, 64, 0, 64, 64, 64);
      grad.addColorStop(0, 'rgba(0,0,0,1)'); grad.addColorStop(0.55, 'rgba(0,0,0,0.45)'); grad.addColorStop(1, 'rgba(0,0,0,0)');
      g.fillStyle = grad; g.fillRect(0, 0, 128, 128);
      return new THREE.CanvasTexture(c);
    })();

    /* ---------- deterministic randomness: the same layout on every visit ---------- */

    let seed = 7;
    const rand = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
    const between = (a, b) => a + (b - a) * rand();

    /* ---------- bodies ---------- */

    const textures = {};
    let bodies = [];
    let mode = '';
    let fade = 0; // 0 → 1 over 400ms once the textures are in

    // where the neon sign sits in the photo (fractions of the image): kept clear like the copy
    // phones: just the letters, so objects can frame the sign from the sides; wider screens: some air around it
    const SIGN_PHONE = { x0: 0.25, y0: 0.05, x1: 0.69, y1: 0.36 };
    const SIGN_WIDE = { x0: 0.18, y0: 0.04, x1: 0.76, y1: 0.37 };
    const photo = hero.querySelector('.hero-photo');
    let zones = [];
    const measureFreeZone = () => {
      const h = hero.getBoundingClientRect(); const r = copy.getBoundingClientRect();
      const pad = 24;
      zones = [{ x0: r.left - h.left - pad, y0: r.top - h.top - pad, x1: r.right - h.left + pad, y1: r.bottom - h.top + pad }];
      if (photo && photo.naturalWidth) {
        // object-fit: cover maths, with the photo's own object-position
        const b = photo.getBoundingClientRect();
        const k = Math.max(b.width / photo.naturalWidth, b.height / photo.naturalHeight);
        const iw = photo.naturalWidth * k; const ih = photo.naturalHeight * k;
        const [px, py] = getComputedStyle(photo).objectPosition.split(' ').map((v) => parseFloat(v) / 100);
        const ox = b.left - h.left + (b.width - iw) * px; const oy = b.top - h.top + (b.height - ih) * py;
        const SIGN = desktopQuery.matches ? SIGN_WIDE : SIGN_PHONE;
        zones.push({ x0: ox + iw * SIGN.x0, y0: oy + ih * SIGN.y0, x1: ox + iw * SIGN.x1, y1: oy + ih * SIGN.y1 });
      }
    };
    const inZone = (x, y, r) => zones.some((z) => x + r > z.x0 && x - r < z.x1 && y + r > z.y0 && y - r < z.y1);

    // home points: spread over the hero, never inside the copy's zone or behind the header
    const homes = (n, sizes, long = []) => {
      const top = 96; const pts = [];
      for (let i = 0; i < n; i++) {
        let best = null; let bestScore = -Infinity;
        for (let k = 0; k < 200; k++) {
          const r = sizes[i] / 2;
          // a little bleed past the side edges is fine: it frames the copy instead of crowding it
          const p = { x: between(r * 0.2, W - r * 0.2), y: between(top + r * 0.5, H - r * 0.6) };
          // the barbell is long: its ends must stay clear too, whichever way it tilts
          const L = (long[i] || 0) * 0.47; const tilt = L * 0.3;
          const blocked = inZone(p.x, p.y, r * 0.8) || (L > 0 && [[L, tilt], [L, -tilt], [-L, tilt], [-L, -tilt]].some(([dx, dy]) => inZone(p.x + dx, p.y + dy, 12)));
          if (blocked) continue;
          const score = pts.reduce((m, q) => (q ? Math.min(m, Math.hypot(p.x - q.x, p.y - q.y)) : m), 1e9);
          if (score > bestScore) { best = p; bestScore = score; }
        }
        pts.push(best); // null = no room on this screen: leave it out
      }
      return pts;
    };

    const clearBodies = () => {
      bodies.forEach((b) => { scene.remove(b.group); b.mesh.geometry.dispose(); b.mesh.material.dispose(); b.shadow.geometry.dispose(); b.shadow.material.dispose(); });
      bodies = [];
    };

    const build = () => {
      clearBodies();
      seed = 7;
      const desktop = desktopQuery.matches;
      mode = desktop ? 'desktop' : 'mobile';
      const list = MIX[mode].filter((k) => textures[k]);
      const scales = list.map((k) => (k === 'bilanciere' ? 1 : between(0.8, 1.15)));
      const shortPhone = desktop ? 1 : Math.max(0.7, Math.min(1, H / 844)); // smaller on short phones
      const widths = list.map((k, i) => (desktop ? KINDS[k].d : KINDS[k].m * shortPhone) * scales[i]);
      // the barbell is long and thin: its "size" for spacing is a fraction of its length
      const pts = homes(list.length, widths.map((w, i) => (list[i] === 'bilanciere' ? w * 0.25 : w)), widths.map((w, i) => (list[i] === 'bilanciere' ? w : 0)));

      list.forEach((kind, i) => {
        if (!pts[i]) return;
        const K = KINDS[kind];
        const w = widths[i]; const h = w * (K.h / K.w);
        const group = new THREE.Group();
        const shadow = new THREE.Mesh(
          new THREE.PlaneGeometry(w * 0.95, Math.max(h * 0.75, w * 0.12)),
          new THREE.MeshBasicMaterial({ map: shadowTexture, transparent: true, opacity: 0, depthWrite: false }),
        );
        shadow.position.set(0, -Math.max(10, h * 0.12), -2);
        const mesh = new THREE.Mesh(
          new THREE.PlaneGeometry(w, h),
          new THREE.MeshBasicMaterial({ map: textures[kind], transparent: true, alphaTest: 0.05, depthWrite: false, opacity: 0 }),
        );
        group.add(shadow, mesh);
        // bigger = nearer: drawn last, a little closer to the camera
        group.position.z = (scales[i] - 1) * 60;
        group.renderOrder = Math.round(scales[i] * 100);
        mesh.renderOrder = group.renderOrder + 1; shadow.renderOrder = group.renderOrder;
        scene.add(group);

        // collision circles along the long side of the photo
        const long = Math.max(w, h); const short = Math.min(w, h);
        const n = K.circles; const r = n === 1 ? long * 0.46 : Math.max(short * 0.6, long / (n * 2));
        const circles = Array.from({ length: n }, (_, j) => (n === 1 ? 0 : (j / (n - 1) - 0.5) * (long - r * 2)));

        const baseAngle = kind === 'bilanciere' ? (rand() < 0.5 ? -1 : 1) * between(14, 18) * DEG : between(-12, 12) * DEG;
        bodies.push({
          kind, group, mesh, shadow, w, h, r, circles, horizontal: w >= h,
          home: pts[i], x: pts[i].x, y: pts[i].y, vx: 0, vy: 0,
          angle: baseAngle, va: 0, baseAngle,
          phase: between(0, Math.PI * 2), drift: between(14, 30) * (desktop ? 1 : 0.6), speed: between(0.05, 0.09),
          mass: kind === 'bilanciere' ? 3 : kind === 'manubrio' ? 1.6 : 1,
        });
      });
      // settle before the first frame, so nothing starts overlapping (and the still scene is tidy)
      for (let i = 0; i < 180; i++) step(1 / 60, 0);
      place(0);
    };

    /* ---------- physics ---------- */

    const pointer = { x: -1e4, y: -1e4, vx: 0, vy: 0, active: false, t: 0 };
    const onPointer = (e) => {
      const r = hero.getBoundingClientRect();
      const x = e.clientX - r.left; const y = e.clientY - r.top; const now = performance.now();
      if (pointer.active && now > pointer.t) {
        const dt = Math.max(16, now - pointer.t) / 1000;
        pointer.vx = (x - pointer.x) / dt; pointer.vy = (y - pointer.y) / dt;
      }
      Object.assign(pointer, { x, y, active: true, t: now });
      wake();
    };
    hero.addEventListener('pointermove', onPointer, { passive: true });
    hero.addEventListener('pointerdown', onPointer, { passive: true });
    const offPointer = () => { pointer.active = false; pointer.vx = pointer.vy = 0; };
    hero.addEventListener('pointerleave', offPointer);
    hero.addEventListener('pointercancel', offPointer); // the finger became a scroll

    const circleCenters = (b) => {
      const c = Math.cos(b.angle); const s = Math.sin(b.angle);
      // screen y points down, the scene's y points up: the visual rotation on screen is -angle
      return b.circles.map((o) => (b.horizontal ? { x: b.x + o * c, y: b.y - o * s } : { x: b.x + o * s, y: b.y + o * c }));
    };

    const MAX_ANGLE = 25 * DEG;
    const step = (dt, t) => {
      const reach = desktopQuery.matches ? 170 : 120;
      bodies.forEach((b) => {
        // the home point itself wanders on a slow loop: weightless drift
        const hx = b.home.x + Math.sin(t * b.speed * 2 * Math.PI + b.phase) * b.drift;
        const hy = b.home.y + Math.cos(t * b.speed * 1.6 * Math.PI + b.phase * 1.3) * b.drift * 0.7;
        let fx = (hx - b.x) * 0.9; let fy = (hy - b.y) * 0.9;

        // pointer / finger: push away, plus a share of the pointer's own speed
        if (pointer.active) {
          const dx = b.x - pointer.x; const dy = b.y - pointer.y;
          const d = Math.hypot(dx, dy); const range = reach + Math.max(b.w, b.h) * 0.3;
          if (d < range && d > 0.01) {
            const k = 1 - d / range;
            fx += (dx / d) * k * 2600 / b.mass + pointer.vx * k * 0.9 / b.mass;
            fy += (dy / d) * k * 2600 / b.mass + pointer.vy * k * 0.9 / b.mass;
            // off-centre push turns it a little
            b.va += ((dx * pointer.vy - dy * pointer.vx) / (range * range)) * k * 0.02 / b.mass;
          }
        }

        // free zones (copy, neon sign): a soft wall
        zones.forEach((freeZone) => circleCenters(b).forEach((p) => {
          const nx = Math.max(freeZone.x0, Math.min(p.x, freeZone.x1));
          const ny = Math.max(freeZone.y0, Math.min(p.y, freeZone.y1));
          const dx = p.x - nx; const dy = p.y - ny; const d = Math.hypot(dx, dy);
          if (d < b.r) {
            if (d > 0.01) { fx += (dx / d) * (b.r - d) * 40; fy += (dy / d) * (b.r - d) * 40; }
            else { fx += (p.x < (freeZone.x0 + freeZone.x1) / 2 ? -1 : 1) * 900; }
          }
        }));

        b.vx = (b.vx + fx * dt) * Math.pow(0.12, dt);
        b.vy = (b.vy + fy * dt) * Math.pow(0.12, dt);
        b.x += b.vx * dt; b.y += b.vy * dt;

        // edges: stay mostly inside the hero
        const m = Math.min(b.w, b.h) * 0.1;
        if (b.x < m) { b.x = m; b.vx = Math.abs(b.vx) * 0.5; }
        if (b.x > W - m) { b.x = W - m; b.vx = -Math.abs(b.vx) * 0.5; }
        if (b.y < 70) { b.y = 70; b.vy = Math.abs(b.vy) * 0.5; }
        if (b.y > H - m) { b.y = H - m; b.vy = -Math.abs(b.vy) * 0.5; }

        // rotation: only around Z, slow, back to its own resting angle, never past ±25°
        const target = b.baseAngle + Math.sin(t * b.speed * 1.3 * 2 * Math.PI + b.phase) * 6 * DEG;
        b.va = (b.va + (target - b.angle) * 1.4 * dt) * Math.pow(0.25, dt);
        b.angle += b.va;
        if (Math.abs(b.angle) > MAX_ANGLE) { b.angle = Math.sign(b.angle) * MAX_ANGLE; b.va *= -0.3; }
      });

      // collisions between objects: circle sets, position correction + bounce along the normal
      for (let i = 0; i < bodies.length; i++) {
        for (let j = i + 1; j < bodies.length; j++) {
          const a = bodies[i]; const b = bodies[j];
          const ca = circleCenters(a); const cb = circleCenters(b);
          ca.forEach((p) => cb.forEach((q) => {
            const dx = q.x - p.x; const dy = q.y - p.y; const d = Math.hypot(dx, dy) || 0.01;
            const overlap = a.r + b.r - d;
            if (overlap <= 0) return;
            const nx = dx / d; const ny = dy / d; const total = a.mass + b.mass;
            a.x -= nx * overlap * (b.mass / total); a.y -= ny * overlap * (b.mass / total);
            b.x += nx * overlap * (a.mass / total); b.y += ny * overlap * (a.mass / total);
            const rel = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny;
            if (rel < 0) {
              const j2 = (-(1 + 0.6) * rel) / (1 / a.mass + 1 / b.mass);
              a.vx -= (j2 * nx) / a.mass; a.vy -= (j2 * ny) / a.mass;
              b.vx += (j2 * nx) / b.mass; b.vy += (j2 * ny) / b.mass;
              a.va -= rel * 0.00012 / a.mass; b.va += rel * 0.00012 / b.mass;
            }
          }));
        }
      }
    };

    const place = (t) => {
      bodies.forEach((b) => {
        b.group.position.x = b.x; b.group.position.y = -b.y;
        b.group.rotation.z = b.angle;
        // a gentle sway on X/Y (±6°) gives the flat photo some depth without showing its edge
        b.group.rotation.x = Math.sin(t * b.speed * 2 * Math.PI + b.phase * 2) * 6 * DEG;
        b.group.rotation.y = Math.cos(t * b.speed * 1.7 * Math.PI + b.phase) * 6 * DEG;
        b.mesh.material.opacity = fade;
        b.shadow.material.opacity = 0.35 * fade;
      });
    };

    /* ---------- loop: runs only while the hero is on screen and the tab is visible ---------- */

    let visible = true; let raf = 0; let last = 0; let clock = 0; let fadeStart = 0;
    const frame = (now) => {
      raf = 0;
      const dt = Math.min((now - last) / 1000, 1 / 30); last = now;
      if (fadeStart) fade = Math.min(1, (now - fadeStart) / 400);
      clock += dt;
      step(dt, clock); place(clock);
      renderer.render(scene, camera);
      wake();
    };
    function wake() {
      if (reduceMotion || raf || !visible || document.hidden || !bodies.length) return;
      last = performance.now();
      raf = requestAnimationFrame(frame);
    }
    const sleep = () => { if (raf) cancelAnimationFrame(raf); raf = 0; };

    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      if (visible) wake(); else sleep();
    }).observe(hero);
    document.addEventListener('visibilitychange', () => (document.hidden ? sleep() : wake()));

    const still = () => { fade = 1; place(0); renderer.render(scene, camera); };

    const relayout = () => {
      resize(); measureFreeZone();
      const next = desktopQuery.matches ? 'desktop' : 'mobile';
      if (next !== mode) build();
      else {
        // keep the same objects, just move their homes to the new size
        const pts = homes(bodies.length, bodies.map((b) => (b.kind === 'bilanciere' ? b.w * 0.25 : b.w)), bodies.map((b) => (b.kind === 'bilanciere' ? b.w : 0)));
        bodies.forEach((b, i) => { if (pts[i]) b.home = pts[i]; });
      }
      if (reduceMotion) still();
    };
    let resizeTimer = 0;
    window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(relayout, 150); });

    resize(); measureFreeZone();
    Promise.all(Object.keys(KINDS).map((k) => loadTexture(k).then((t) => { textures[k] = t; }))).then(() => {
      build();
      if (reduceMotion) { still(); return; }
      fadeStart = performance.now();
      wake();
    });
  }
})();
