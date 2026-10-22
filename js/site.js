/* DBK Games — shared site script. Every block checks that its elements exist,
   so the same file runs on the home page, the game pages and the 404 page. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- nav ---------- */
  const nav = $('#nav'), menuBtn = $('#menuBtn');
  if (nav){
    let lastY = 0;
    addEventListener('scroll', () => {
      const y = scrollY;
      nav.classList.toggle('solid', y > 40);
      nav.classList.toggle('hide', y > 600 && y > lastY && !nav.classList.contains('open'));
      lastY = y;
    }, {passive:true});
  }
  if (nav && menuBtn){
    menuBtn.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open);
    });
    $$('#menu a').forEach(a => a.addEventListener('click', () => {
      nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', false);
    }));
  }

  /* ---------- starfield: warp in, then drift with pointer parallax ---------- */
  const cv = $('#stars');
  if (cv){
    const ctx = cv.getContext('2d');
    let W, H, DPR, stars = [], speed = reduce ? 0.4 : (cv.dataset.warp === 'off' ? 0.55 : 38), target = 0.55, mx = 0, my = 0, tmx = 0, tmy = 0;
    const N = innerWidth < 700 ? 420 : 900;
    const resize = () => {
      DPR = Math.min(devicePixelRatio || 1, 2);
      W = cv.clientWidth; H = cv.clientHeight;
      cv.width = W * DPR; cv.height = H * DPR; ctx.setTransform(DPR,0,0,DPR,0,0);
    };
    const spawn = (s, far) => {
      s.x = (Math.random() - .5) * 2; s.y = (Math.random() - .5) * 2;
      s.z = far ? 1 : Math.random(); s.pz = s.z;
      s.t = Math.random() < .08 ? 1 : 0; // a few tinted ion-blue stars
      return s;
    };
    for (let i = 0; i < N; i++) stars.push(spawn({}, false));
    resize(); addEventListener('resize', resize);
    addEventListener('pointermove', e => { tmx = (e.clientX / innerWidth - .5); tmy = (e.clientY / innerHeight - .5); }, {passive:true});
    let visible = true;
    new IntersectionObserver(([e]) => visible = e.isIntersecting).observe(cv);
    const frame = () => {
      requestAnimationFrame(frame);
      if (!visible) return;
      speed += (target - speed) * 0.035;
      mx += (tmx - mx) * .05; my += (tmy - my) * .05;
      ctx.fillStyle = speed > 4 ? 'rgba(6,7,10,.35)' : '#06070a';
      ctx.fillRect(0,0,W,H);
      const cx = W/2 - mx*60, cy = H*.46 - my*40, f = Math.max(W,H)*.5;
      for (const s of stars){
        s.pz = s.z; s.z -= speed * 0.0016;
        if (s.z <= 0.02) { spawn(s, true); continue; }
        const sx = cx + s.x / s.z * f, sy = cy + s.y / s.z * f;
        const px = cx + s.x / s.pz * f, py = cy + s.y / s.pz * f;
        if (sx < -50 || sx > W+50 || sy < -50 || sy > H+50) { spawn(s, true); continue; }
        const a = Math.min(1, (1 - s.z) * 1.3), r = (1 - s.z) * 1.6;
        ctx.strokeStyle = ctx.fillStyle = s.t ? `rgba(143,184,255,${a})` : `rgba(232,235,240,${a})`;
        if (speed > 1.5){ ctx.lineWidth = r; ctx.beginPath(); ctx.moveTo(px,py); ctx.lineTo(sx,sy); ctx.stroke(); }
        else { ctx.beginPath(); ctx.arc(sx, sy, Math.max(.35, r*.7), 0, 6.283); ctx.fill(); }
      }
    };
    frame();
  }

  /* ---------- contact form (not connected to a mail service yet) ---------- */
  const form = $('#pitchForm'), note = $('#formNote');
  if (form && note){
    form.addEventListener('submit', e => {
      e.preventDefault();
      const bad = $$('[required]', form).find(el => !el.value.trim() || (el.type === 'email' && !/^\S+@\S+\.\S+$/.test(el.value)));
      note.classList.remove('ok');
      if (bad){ note.textContent = bad.id === 'f-email' ? 'Enter a valid email address.' : 'Fill in your name, email and message.'; bad.focus(); return; }
      note.classList.add('ok');
      note.textContent = 'Our contact form is still being set up. Until then, reach us on Discord: discord.gg/dbkgames';
    });
  }

  /* ---------- "classified" title decodes from random glyphs every few seconds ---------- */
  const ci = $('#cipher');
  if (ci && !reduce){
    const word = 'CLASSIFIED', glyphs = 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#/%<>';
    const decode = () => { let f = 0; const id = setInterval(() => {
      ci.textContent = [...word].map((c,i) => i < f/3 ? c : glyphs[Math.random()*glyphs.length|0]).join('');
      if (++f > word.length*3) { clearInterval(id); ci.textContent = word; }
    }, 45); };
    decode(); setInterval(decode, 4500);
  }

  /* ---------- gallery lightbox (game pages) ---------- */
  const shots = $$('[data-lightbox] a');
  if (shots.length){
    const box = document.createElement('div');
    box.className = 'lightbox'; box.hidden = true;
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Screenshot viewer');
    box.innerHTML = '<img alt=""><button class="lb-close" aria-label="Close">×</button>' +
      '<button class="lb-prev" aria-label="Previous screenshot">←</button><button class="lb-next" aria-label="Next screenshot">→</button>' +
      '<span class="lb-count mono"></span>';
    document.body.append(box);
    const img = $('img', box), count = $('.lb-count', box);
    let i = 0, opener = null;
    const show = n => { i = (n + shots.length) % shots.length; img.src = shots[i].href; img.alt = $('img', shots[i]).alt; count.textContent = `${i+1} / ${shots.length}`; };
    const close = () => { box.hidden = true; document.body.style.overflow = ''; opener && opener.focus(); };
    shots.forEach((a, n) => a.addEventListener('click', e => {
      e.preventDefault(); opener = a; show(n); box.hidden = false; document.body.style.overflow = 'hidden'; $('.lb-close', box).focus();
    }));
    $('.lb-close', box).onclick = close;
    $('.lb-prev', box).onclick = () => show(i - 1);
    $('.lb-next', box).onclick = () => show(i + 1);
    box.addEventListener('click', e => { if (e.target === box) close(); });
    addEventListener('keydown', e => {
      if (box.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(i - 1);
      if (e.key === 'ArrowRight') show(i + 1);
    });
  }

  /* ---------- motion (content is fully visible without this) ---------- */
  if (!window.gsap || reduce) return;
  if (window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);
  const has = s => !!$(s);

  // home intro: chrome letters rise, supporting lines follow
  if (has('.hero h1 .ln')){
    gsap.timeline({defaults:{ease:'expo.out'}})
      .from('.hero h1 .ln > span', {yPercent:110, duration:1.6, stagger:.12, delay:.15})
      .from('.h-in', {y:24, opacity:0, duration:1.1, stagger:.09}, '-=1.1');
    gsap.to('.hero .wrap', {yPercent:-12, opacity:.15, ease:'none',
      scrollTrigger:{trigger:'.hero', start:'top top', end:'bottom top', scrub:true}});
    gsap.to('.hero-emblem', {rotate:-8, yPercent:-20, ease:'none',
      scrollTrigger:{trigger:'.hero', start:'top top', end:'bottom top', scrub:true}});
  }

  // hero emblem: the eagle flies in level from the left with its tail streaming straight
  // behind it, then the tail curls round into the circular emblem; it lands with a squash,
  // flares, a light sweeps across it and it fades back to a watermark.
  //
  // The tail is the logo's own outline, unrolled. Every point is expressed as
  // (arc length along a circle round the emblem's centre, offset from that circle);
  // drawing those points on a circle of curvature k*R0 gives a straight tail at k=0
  // and exactly the original logo at k=1. The numbers below belong to img/logo.svg:
  // EMB_C/EMB_R = centre and radius of the ring, the head stays rigid up to EMB_ROOT,
  // sub-paths 1 and 3 (eye details) are rigid, sub-path 2's points past 250deg are the
  // beak (rigid), sub-path 4's points before 90deg are the tail's far tip.
  const fly = $('.emb-fly');
  if (fly){
    const flap = $('.emb-flap', fly), img = $('img', flap), sheen = $('.emb-sheen', flap);
    const EMB_C = [627, 606], EMB_R = 330, EMB_ROOT = 20 * Math.PI / 180, TAU = Math.PI * 2;
    gsap.set(fly, {opacity:0});
    fetch(img.currentSrc || img.src).then(r => r.text()).then(txt => {
      const d = (txt.match(/\sd="([^"]+)"/) || [])[1];
      const vb = (txt.match(/viewBox="([^"]+)"/) || [])[1];
      if (!d || !vb) throw new Error('logo has no path');
      const parts = d.split('Z').filter(s => s.trim()).map((sp, i) => {
        const nums = sp.match(/-?[\d.]+/g).map(Number), pts = [];
        for (let n = 0; n + 1 < nums.length; n += 2){
          const x = nums[n], y = nums[n + 1];
          let psi = -1;
          if (i !== 1 && i !== 3){
            psi = Math.atan2(-(x - EMB_C[0]), -(y - EMB_C[1]));   // counter-clockwise from straight up
            if (psi < 0) psi += TAU;
            if (i === 2 && psi > 250 * Math.PI / 180) psi -= TAU;
            if (i === 4 && psi < Math.PI / 2) psi += TAU;
          }
          pts.push([x, y, psi, Math.hypot(x - EMB_C[0], y - EMB_C[1]) - EMB_R]);
        }
        return pts;
      });
      const sr = Math.sin(EMB_ROOT), cr = Math.cos(EMB_ROOT);
      const A = [EMB_C[0] - EMB_R * sr, EMB_C[1] - EMB_R * cr];   // where the tail leaves the head
      const build = k => parts.map(pts => 'M' + pts.map(([x, y, psi, n]) => {
        if (psi <= EMB_ROOT) return x.toFixed(1) + ' ' + y.toFixed(1);
        const s = (psi - EMB_ROOT) * EMB_R;
        if (k < 1e-4) return (A[0] - cr * s - sr * n).toFixed(1) + ' ' + (A[1] + sr * s - cr * n).toFixed(1);
        const rho = EMB_R / k, a = s / rho, ca = Math.cos(a), sa = Math.sin(a);
        const vx = -sr, vy = -cr, rx = vx * ca + vy * sa, ry = -vx * sa + vy * ca;
        return (A[0] + sr * rho + rx * (rho + n)).toFixed(1) + ' ' + (A[1] + cr * rho + ry * (rho + n)).toFixed(1);
      }).join('L') + 'Z').join('');
      const NS = 'http://www.w3.org/2000/svg';
      const svg = document.createElementNS(NS, 'svg'), path = document.createElementNS(NS, 'path');
      svg.setAttribute('viewBox', vb); svg.setAttribute('aria-hidden', 'true');
      path.setAttribute('fill', '#fff'); path.setAttribute('fill-rule', 'evenodd');
      svg.append(path); flap.insertBefore(svg, img); img.remove();
      const state = {k:0}, draw = () => path.setAttribute('d', build(state.k));
      draw();

      const box = fly.getBoundingClientRect();
      const startX = -box.right - 40;            // whole eagle, tail included, starts off the left edge
      const curl = .55, land = curl + 1.1;   // the tail starts curling while the eagle is still arriving
      gsap.timeline({delay:.2})
        .set(fly, {opacity:.6, x:startX, rotation:EMB_ROOT * 180 / Math.PI})   // tilted so the straight tail is level
        .to(fly, {x:0, duration:.95, ease:'power2.out'}, 0)
        .to(state, {k:1, duration:1.1, ease:'power2.inOut', onUpdate:draw}, curl)
        .to(fly, {rotation:0, duration:1.1, ease:'power2.inOut'}, curl)
        .to(flap, {scaleX:1.08, scaleY:.9, duration:.12, ease:'power2.out'}, land)
        .to(flap, {scaleX:1, scaleY:1, duration:1, ease:'elastic.out(1,.32)'}, land + .12)
        .to(svg, {filter:'drop-shadow(0 0 70px rgba(143,184,255,.95))', duration:.25, ease:'power2.out'}, land)
        .to(svg, {filter:'drop-shadow(0 0 40px rgba(143,184,255,.4))', duration:1.4, ease:'power2.inOut'}, land + .3)
        .fromTo(sheen, {opacity:1, backgroundPosition:'120% 0'}, {backgroundPosition:'-20% 0', duration:1.1, ease:'power2.inOut', immediateRender:false}, land + .25)
        .to(sheen, {opacity:0, duration:.3}, land + 1.25)
        .to(fly, {opacity:.08, duration:1.4, ease:'power2.out'}, land + 1.1);
    }).catch(() => gsap.set(fly, {opacity:.08}));   // keep the still emblem if anything fails
  }

  // game page intro: key art settles, title rises, image drifts on scroll
  if (has('.ghero')){
    gsap.timeline({defaults:{ease:'expo.out'}})
      .from('.ghero .art img', {scale:1.14, duration:2.4, ease:'power2.out'})
      .from('.ghero h1 .ln > span', {yPercent:110, duration:1.5}, .1)
      .from('.g-in', {y:24, opacity:0, duration:1.1, stagger:.08}, .4);
    gsap.to('.ghero .art', {yPercent:14, ease:'none',
      scrollTrigger:{trigger:'.ghero', start:'top top', end:'bottom top', scrub:true}});
  }

  // headings slide up gently (they start visible-ish so nothing is hidden at rest)
  $$('.rv').forEach(el => gsap.from(el, {y:46, opacity:.12, duration:1.3, ease:'expo.out',
    scrollTrigger:{trigger:el, start:'top 88%'}}));

  // game panels: parallax image + clip reveal
  $$('.game').forEach(card => {
    const media = $('.media', card);
    if (media) gsap.fromTo(media, {yPercent:-6}, {yPercent:6, ease:'none',
      scrollTrigger:{trigger:card, start:'top bottom', end:'bottom top', scrub:true}});
    gsap.from(card, {clipPath:'inset(12% 6% 12% 6%)', duration:1.6, ease:'expo.out',
      scrollTrigger:{trigger:card, start:'top 85%'}});
    gsap.from($$('.body > *', card), {y:30, opacity:.1, duration:1.1, stagger:.07, ease:'expo.out',
      scrollTrigger:{trigger:card, start:'top 70%'}});
  });

  // feature cells and gallery tiles rise in rows
  $$('.features, .gallery').forEach(g => gsap.from(g.children, {y:34, opacity:.12, duration:1.1, stagger:.06, ease:'expo.out',
    scrollTrigger:{trigger:g, start:'top 85%'}}));

  // filmstrip: pinned horizontal travel on wide screens, native scroll on phones
  if (has('#strip')){
    gsap.matchMedia().add('(min-width: 900px)', () => {
      const strip = $('#strip'), sec = $('#gallery');
      sec.classList.add('js-pin');
      const dist = () => strip.scrollWidth - innerWidth;
      gsap.to(strip, {x:() => -dist(), ease:'none',
        scrollTrigger:{trigger:sec, start:'top top', end:() => '+=' + dist(), pin:true, scrub:.6, invalidateOnRefresh:true}});
      return () => sec.classList.remove('js-pin'); // gsap.matchMedia reverts the tween and its pin itself
    });
  }

  // process steps: progress line fills in sequence
  if (has('#steps')) ScrollTrigger.create({trigger:'#steps', start:'top 80%', once:true, onEnter:() =>
    $$('.step').forEach((s,i) => setTimeout(() => s.classList.add('on'), i*260))});

  // studio log rows + footer wordmark
  if (has('.log')) gsap.from('.log li', {x:-24, opacity:.15, stagger:.1, duration:1, ease:'expo.out', scrollTrigger:{trigger:'.log', start:'top 85%'}});
  if (has('.wordmark')) gsap.from('.wordmark', {yPercent:60, opacity:0, duration:1.6, ease:'expo.out', scrollTrigger:{trigger:'footer', start:'top 90%'}});

  // magnetic buttons
  if (matchMedia('(pointer:fine)').matches) $$('.btn').forEach(b => {
    b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect();
      gsap.to(b, {x:(e.clientX - r.left - r.width/2)*.18, y:(e.clientY - r.top - r.height/2)*.3, duration:.4, ease:'power3.out'}); });
    b.addEventListener('pointerleave', () => gsap.to(b, {x:0, y:0, duration:.7, ease:'elastic.out(1,.4)'}));
  });
})();
