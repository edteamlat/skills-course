# HTML Technical Spec

Copy this scaffold and fill in slides. Do NOT change the core CSS variables or nav logic.

---

## Full file structure

```html
<!DOCTYPE html>
<html lang="LANG"><!-- es / en / pt etc -->
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DECK TITLE</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  /* ── RESET ── */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  /* ── THEME VARIABLES (dark-gold default) ── */
  :root {
    --bg:       #0a0a0a;
    --surface:  #111111;
    --surface2: #1a1a1a;
    --border:   rgba(255,255,255,0.08);
    --border2:  rgba(255,255,255,0.14);
    --text:     #f0ede8;
    --muted:    #6b6b6b;
    --accent:   #e8d5a3;   /* primary highlight — gold */
    --accent2:  #c8b98a;
    --green:    #7dba8a;
    --red:      #d97070;
    --blue:     #7aafcf;
    --mono:     'DM Mono', monospace;
    --sans:     'Inter', sans-serif;
    --display:  'Syne', sans-serif;
  }

  /* ── BASE ── */
  html, body { width:100%; height:100%; background:var(--bg); color:var(--text); font-family:var(--sans); overflow:hidden; }
  .deck { width:100%; height:100vh; position:relative; }

  /* ── SLIDE TRANSITIONS ── */
  .slide {
    position:absolute; inset:0;
    display:flex; flex-direction:column; justify-content:center; align-items:center;
    padding:60px;
    opacity:0; pointer-events:none;
    transition:opacity 0.4s ease, transform 0.4s ease;
    transform:translateX(40px);
  }
  .slide.active  { opacity:1; pointer-events:all; transform:translateX(0); }
  .slide.exit    { opacity:0; transform:translateX(-40px); pointer-events:none; }

  /* ── NAVIGATION ── */
  .nav {
    position:fixed; bottom:36px; left:50%; transform:translateX(-50%);
    display:flex; align-items:center; gap:20px;
    background:var(--surface); border:1px solid var(--border2);
    border-radius:40px; padding:10px 20px; z-index:100;
  }
  .nav button {
    background:none; border:none; color:var(--muted);
    font-family:var(--mono); font-size:13px; cursor:pointer;
    padding:6px 14px; border-radius:20px; transition:all 0.2s;
  }
  .nav button:hover { color:var(--text); background:var(--surface2); }
  .counter { font-family:var(--mono); font-size:12px; color:var(--muted); min-width:52px; text-align:center; }
  .progress-dots { display:flex; gap:6px; align-items:center; }
  .dot { width:6px; height:6px; border-radius:50%; background:var(--border2); transition:all 0.3s; cursor:pointer; }
  .dot.active { background:var(--accent); transform:scale(1.3); }

  /* ── KEYBOARD HINT ── */
  .key-hint { position:fixed; top:24px; right:28px; font-family:var(--mono); font-size:11px; color:var(--muted); display:flex; gap:6px; align-items:center; }
  .key { border:1px solid var(--border2); border-radius:4px; padding:2px 7px; }

  /* ── TYPOGRAPHY ── */
  h1 { font-family:var(--display); font-size:clamp(40px,5vw,64px); font-weight:800; line-height:1.05; letter-spacing:-0.03em; }
  h2 { font-family:var(--display); font-size:clamp(28px,3.5vw,44px); font-weight:700; line-height:1.1; letter-spacing:-0.02em; margin-bottom:8px; }
  h3 { font-family:var(--display); font-size:20px; font-weight:600; }
  p  { font-size:16px; line-height:1.65; color:rgba(240,237,232,0.7); }
  .mono    { font-family:var(--mono); }
  .accent  { color:var(--accent); }
  .green   { color:var(--green); }
  .red     { color:var(--red); }
  .blue    { color:var(--blue); }
  .muted   { color:var(--muted); }

  /* ── COVER SLIDE ── */
  #s0 .eyebrow { font-family:var(--mono); font-size:11px; color:var(--muted); letter-spacing:0.12em; text-transform:uppercase; margin-bottom:24px; }
  #s0 h1 { max-width:700px; text-align:center; margin-bottom:20px; }
  #s0 .subtitle { font-size:16px; color:rgba(240,237,232,0.45); max-width:480px; text-align:center; line-height:1.6; }
  .divider { width:40px; height:1px; background:var(--border2); margin:28px auto; }

  /* ── ANIMATIONS ── */
  @keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }

  /* ── VS SPLIT ── */
  .vs-content { display:grid; grid-template-columns:1fr 1fr; gap:24px; width:100%; max-width:900px; }
  .vs-card { border:1px solid var(--border); border-radius:16px; padding:36px; position:relative; overflow:hidden; animation:fadeUp 0.5s ease both; }
  .vs-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
  .vs-card.bad::before  { background:var(--red); }
  .vs-card.good::before { background:var(--green); }
  .vs-card.neutral::before { background:var(--border2); }
  .vs-card.bad  { animation-delay:0.1s; }
  .vs-card.good { animation-delay:0.25s; }
  .vs-tag { font-family:var(--mono); font-size:10px; letter-spacing:0.1em; text-transform:uppercase; padding:4px 10px; border-radius:20px; display:inline-block; margin-bottom:20px; }
  .vs-tag.bad  { background:rgba(217,112,112,0.12); color:var(--red); }
  .vs-tag.good { background:rgba(125,186,138,0.12); color:var(--green); }
  .vs-tag.neutral { background:rgba(255,255,255,0.06); color:var(--muted); }
  .vs-card h3 { margin-bottom:20px; font-size:24px; }
  .vs-list { list-style:none; }
  .vs-list li { font-size:14px; color:rgba(240,237,232,0.65); padding:8px 0; border-bottom:1px solid var(--border); display:flex; align-items:flex-start; gap:10px; line-height:1.45; }
  .vs-list li:last-child { border-bottom:none; }
  .vs-list li::before { flex-shrink:0; margin-top:1px; font-size:12px; }
  .vs-card.bad  .vs-list li::before { content:'—'; color:var(--red);   opacity:0.7; }
  .vs-card.good .vs-list li::before { content:'→'; color:var(--green); opacity:0.9; }
  .vs-card.neutral .vs-list li::before { content:'·'; color:var(--muted); }

  /* ── ARTIFACT FLOW ── */
  .artifact-flow { display:flex; align-items:center; width:100%; max-width:960px; margin-top:40px; }
  .artifact-card { flex:1; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:22px 18px; text-align:center; animation:fadeUp 0.5s ease both; transition:border-color 0.2s; }
  .artifact-card:hover { border-color:var(--accent2); }
  .artifact-num  { font-family:var(--mono); font-size:10px; color:var(--muted); margin-bottom:10px; }
  .artifact-icon { font-size:22px; margin-bottom:10px; display:block; font-family:var(--mono); }
  .artifact-card h3 { font-size:13px; font-weight:600; margin-bottom:6px; }
  .artifact-card .fname { font-family:var(--mono); font-size:11px; color:var(--accent2); margin-bottom:10px; display:block; }
  .artifact-card p { font-size:11px; color:var(--muted); line-height:1.5; }
  .arrow-sep { flex-shrink:0; width:28px; display:flex; align-items:center; justify-content:center; }
  .arrow-sep svg { width:18px; opacity:0.3; }
  .insight { margin-top:32px; background:rgba(232,213,163,0.07); border:1px solid rgba(232,213,163,0.15); border-radius:10px; padding:16px 24px; font-size:13px; color:rgba(240,237,232,0.75); max-width:960px; text-align:center; line-height:1.6; }

  /* ── COMPARISON TABLE ── */
  .table-wrap { width:100%; max-width:860px; margin-top:36px; }
  .comp-table { width:100%; border-collapse:collapse; }
  .comp-table th { font-family:var(--mono); font-size:10px; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted); padding:0 20px 14px; text-align:left; }
  .comp-table th:first-child { width:160px; }
  .comp-table td { padding:14px 20px; border-top:1px solid var(--border); font-size:14px; vertical-align:top; line-height:1.5; }
  .comp-table td:first-child { font-family:var(--mono); font-size:12px; color:var(--muted); }
  .comp-table td.h { color:var(--accent); font-weight:500; }
  .badge { display:inline-block; font-family:var(--mono); font-size:10px; padding:3px 8px; border-radius:4px; font-weight:500; }
  .badge-blue { background:rgba(122,175,207,0.12); color:var(--blue); }
  .badge-green { background:rgba(125,186,138,0.12); color:var(--green); }
  .badge-gold  { background:rgba(232,213,163,0.12); color:var(--accent); }
  .badge-red   { background:rgba(217,112,112,0.12); color:var(--red); }
  .footnote { margin-top:24px; font-size:12px; color:var(--muted); max-width:860px; line-height:1.5; }

  /* ── TIMELINE ── */
  .timeline { width:100%; max-width:900px; margin-top:40px; }
  .tl-line { display:flex; align-items:stretch; }
  .tl-step { flex:1; position:relative; animation:fadeUp 0.5s ease both; }
  .tl-step:nth-child(1){animation-delay:0.05s} .tl-step:nth-child(2){animation-delay:0.15s}
  .tl-step:nth-child(3){animation-delay:0.25s} .tl-step:nth-child(4){animation-delay:0.35s}
  .tl-step:nth-child(5){animation-delay:0.45s}
  .tl-bar { height:4px; margin-bottom:20px; border-radius:2px; position:relative; }
  .tl-bar::after { content:''; position:absolute; right:-1px; top:50%; transform:translateY(-50%); width:10px; height:10px; border-radius:50%; background:inherit; box-shadow:0 0 0 3px var(--bg); }
  .tl-step:last-child .tl-bar::after { display:none; }
  .tl-step:not(.current) .tl-bar { background:var(--surface2); border:1px solid var(--border2); }
  .tl-step.current .tl-bar { background:var(--accent); }
  .tl-step.current .tl-title { color:var(--accent); }
  .tl-year  { font-family:var(--mono); font-size:10px; color:var(--muted); margin-bottom:6px; }
  .tl-title { font-family:var(--display); font-size:14px; font-weight:600; margin-bottom:8px; line-height:1.3; }
  .tl-desc  { font-size:12px; color:var(--muted); line-height:1.5; }
  .tl-body  { padding-right:20px; }

  /* ── TOOLS GRID ── */
  .tools-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; width:100%; max-width:900px; margin-top:40px; }
  .tool-card { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:28px 22px; position:relative; overflow:hidden; animation:fadeUp 0.5s ease both; transition:all 0.25s; }
  .tool-card:hover { border-color:var(--border2); transform:translateY(-2px); }
  .tool-card.featured { border-color:rgba(232,213,163,0.3); background:rgba(232,213,163,0.04); }
  .tool-card.featured::after { content:attr(data-badge); position:absolute; top:14px; right:14px; font-family:var(--mono); font-size:9px; color:var(--accent); letter-spacing:0.08em; background:rgba(232,213,163,0.1); padding:3px 8px; border-radius:20px; }
  .tool-card:not([data-badge]).featured::after { content:'elegido'; }
  .tool-logo { font-family:var(--mono); font-size:11px; color:var(--muted); margin-bottom:14px; }
  .tool-card h3 { font-size:18px; margin-bottom:8px; }
  .tool-card p { font-size:12px; line-height:1.55; }
  .tool-tags { display:flex; flex-wrap:wrap; gap:6px; margin-top:14px; }
  .tool-tag  { font-family:var(--mono); font-size:10px; padding:3px 8px; border:1px solid var(--border2); border-radius:4px; color:var(--muted); }
  .tool-card:nth-child(1){animation-delay:0.05s} .tool-card:nth-child(2){animation-delay:0.15s}
  .tool-card:nth-child(3){animation-delay:0.25s} .tool-card:nth-child(4){animation-delay:0.35s}

  /* ── REASONS GRID ── */
  .reasons { display:grid; grid-template-columns:1fr 1fr; gap:16px; width:100%; max-width:820px; margin-top:40px; }
  .reason-card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:26px 24px; animation:fadeUp 0.5s ease both; display:flex; gap:16px; align-items:flex-start; }
  .reason-card:nth-child(1){animation-delay:0.05s} .reason-card:nth-child(2){animation-delay:0.15s}
  .reason-card:nth-child(3){animation-delay:0.25s} .reason-card:nth-child(4){animation-delay:0.35s}
  .reason-num { font-family:var(--mono); font-size:22px; font-weight:500; color:var(--accent); opacity:0.5; flex-shrink:0; line-height:1; }
  .reason-card h3 { font-size:15px; margin-bottom:6px; }
  .reason-card p  { font-size:13px; }

  /* ── ATTRIBUTE GRID ── */
  .attr-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; width:100%; max-width:900px; margin-top:36px; }
  .attr-grid.attr-grid-2 { grid-template-columns:repeat(2,1fr); }
  .attr-item { display:flex; gap:14px; align-items:flex-start; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px 18px; animation:fadeUp 0.5s ease both; transition:border-color 0.2s; }
  .attr-item:hover { border-color:var(--border2); }
  .attr-item.attr-full { grid-column:1/-1; }
  .attr-item.attr-danger { border-color:rgba(217,112,112,0.18); background:rgba(217,112,112,0.04); }
  .attr-icon { font-size:14px; flex-shrink:0; margin-top:2px; color:var(--accent); opacity:0.5; }
  .attr-item h3 { font-size:14px; margin-bottom:5px; }
  .attr-item p  { font-size:12px; }
  .attr-item:nth-child(1){animation-delay:0.05s} .attr-item:nth-child(2){animation-delay:0.12s}
  .attr-item:nth-child(3){animation-delay:0.19s} .attr-item:nth-child(4){animation-delay:0.26s}
  .attr-item:nth-child(5){animation-delay:0.33s} .attr-item:nth-child(6){animation-delay:0.40s}
  .attr-item:nth-child(7){animation-delay:0.47s}

  /* ── FLOW STEPS ── */
  .flow-steps { display:flex; flex-direction:column; width:100%; max-width:680px; margin-top:36px; }
  .fs-step { display:flex; gap:20px; align-items:flex-start; animation:fadeUp 0.5s ease both; }
  .fs-step:nth-child(1){animation-delay:0.05s} .fs-step:nth-child(3){animation-delay:0.15s}
  .fs-step:nth-child(5){animation-delay:0.25s} .fs-step:nth-child(7){animation-delay:0.35s}
  .fs-num { font-family:var(--mono); font-size:13px; font-weight:500; flex-shrink:0; width:28px; padding-top:2px; }
  .fs-body h3 { font-size:15px; margin-bottom:5px; }
  .fs-body p  { font-size:13px; line-height:1.55; }
  .fs-connector { width:1px; height:22px; background:var(--border2); margin-left:13px; flex-shrink:0; }

  /* ── CONTEXT COLUMNS ── */
  .ctx-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; width:100%; max-width:960px; margin-top:36px; }
  .ctx-card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:22px 18px; animation:fadeUp 0.5s ease both; }
  .ctx-card:nth-child(1){animation-delay:0.05s} .ctx-card:nth-child(2){animation-delay:0.15s}
  .ctx-card:nth-child(3){animation-delay:0.25s} .ctx-card:nth-child(4){animation-delay:0.35s}
  .ctx-card.ctx-key { border-color:rgba(232,213,163,0.2); background:rgba(232,213,163,0.04); }
  .ctx-label { font-size:10px; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted); margin-bottom:8px; display:block; }
  .ctx-card h3 { font-size:14px; margin-bottom:14px; }
  .ctx-list { list-style:none; display:flex; flex-direction:column; gap:8px; }
  .ctx-list li { font-size:12px; color:rgba(240,237,232,0.6); line-height:1.5; padding-left:12px; position:relative; }
  .ctx-list li::before { content:'–'; position:absolute; left:0; color:var(--muted); }

  /* ── BVS (DETAILED VS) ── */
  .bvs-wrap { display:grid; grid-template-columns:1fr auto 1fr; width:100%; max-width:920px; margin-top:36px; align-items:start; }
  .bvs-col { padding:0 8px; }
  .bvs-header { margin-bottom:20px; }
  .bvs-tag { font-family:var(--mono); font-size:11px; letter-spacing:0.08em; padding:4px 12px; border-radius:20px; display:inline-block; margin-bottom:10px; }
  .bvs-tag.sk   { background:rgba(125,186,138,0.12); color:var(--green); }
  .bvs-tag.bmad { background:rgba(122,175,207,0.12); color:var(--blue);  }
  .bvs-tag.gold { background:rgba(232,213,163,0.12); color:var(--accent); }
  .bvs-when { font-size:13px; color:var(--muted); line-height:1.4; }
  .bvs-list { list-style:none; display:flex; flex-direction:column; gap:10px; }
  .bvs-list li { font-size:13px; color:rgba(240,237,232,0.7); display:flex; gap:10px; align-items:flex-start; line-height:1.45; }
  .bvs-check { flex-shrink:0; font-size:12px; margin-top:1px; }
  .bvs-divider { display:flex; align-items:center; justify-content:center; padding:0 20px; padding-top:60px; }
  .bvs-divider span { font-family:var(--display); font-size:13px; color:var(--muted); background:var(--surface2); border:1px solid var(--border2); width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; }
  .bvs-note { margin-top:28px; max-width:920px; font-size:12px; color:var(--muted); text-align:center; border-top:1px solid var(--border); padding-top:18px; line-height:1.6; }

  /* ── QUIZ ── */
  .quiz-wrap { width:100%; max-width:760px; }
  .quiz-header { margin-bottom:32px; }
  .quiz-header h2 { font-size:32px; margin-bottom:6px; }
  .quiz-header p  { font-size:13px; color:var(--muted); }
  .question { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:28px; margin-bottom:16px; transition:border-color 0.3s; }
  .question.answered { border-color:var(--border2); }
  .q-number { font-family:var(--mono); font-size:10px; color:var(--muted); margin-bottom:10px; letter-spacing:0.08em; }
  .q-text   { font-size:15px; color:var(--text); margin-bottom:18px; line-height:1.5; font-weight:500; }
  .options  { display:flex; flex-direction:column; gap:8px; }
  .option   { display:flex; align-items:center; gap:12px; padding:12px 16px; border-radius:10px; border:1px solid var(--border); cursor:pointer; transition:all 0.25s; font-size:14px; color:rgba(240,237,232,0.75); user-select:none; }
  .option:hover:not(.locked) { border-color:var(--border2); color:var(--text); background:var(--surface2); }
  .opt-letter { font-family:var(--mono); font-size:11px; color:var(--muted); flex-shrink:0; width:18px; }
  .option.wrong   { border-color:rgba(217,112,112,0.25); background:rgba(217,112,112,0.06); color:var(--muted); text-decoration:line-through; text-decoration-color:rgba(217,112,112,0.4); text-decoration-thickness:1.5px; }
  .option.wrong .opt-letter  { color:rgba(217,112,112,0.5); }
  .option.correct { border-color:rgba(125,186,138,0.4); background:rgba(125,186,138,0.08); color:var(--green); }
  .option.correct .opt-letter { color:var(--green); }
  .locked { cursor:default; }
  .q-feedback { margin-top:14px; font-size:12px; line-height:1.5; color:var(--muted); display:none; padding-left:4px; }
  .q-feedback.show { display:block; }
  .quiz-score { display:none; background:var(--surface2); border:1px solid var(--border2); border-radius:14px; padding:28px; margin-top:8px; text-align:center; }
  .quiz-score.show { display:block; }
  .score-num   { font-family:var(--display); font-size:52px; font-weight:800; color:var(--accent); line-height:1; margin-bottom:8px; }
  .score-label { font-size:14px; color:var(--muted); margin-bottom:20px; }
  .score-msg   { font-size:15px; color:var(--text); }
  .btn-reset { margin-top:20px; background:none; border:1px solid var(--border2); color:var(--muted); font-family:var(--mono); font-size:12px; padding:10px 24px; border-radius:8px; cursor:pointer; transition:all 0.2s; }
  .btn-reset:hover { border-color:var(--accent2); color:var(--accent); }

  /* ADD SLIDE-SPECIFIC STYLES BELOW THIS LINE */
</style>
</head>
<body>

<div class="key-hint">
  <span class="key">←</span>
  <span class="key">→</span>
</div>

<div class="deck" id="deck">

  <!-- SLIDES GO HERE -->

</div>

<div class="nav">
  <button onclick="prev()">← PREV_LABEL</button><!-- translate: anterior / previous -->
  <div class="progress-dots" id="dots"></div>
  <span class="counter" id="counter">1 / N</span>
  <button onclick="next()">NEXT_LABEL →</button><!-- translate: siguiente / next -->
</div>

<script>
  const TOTAL = N; // ← set to total number of slides
  let current = 0;

  function buildDots() {
    const d = document.getElementById('dots');
    for (let i = 0; i < TOTAL; i++) {
      const dot = document.createElement('div');
      dot.className = 'dot' + (i === 0 ? ' active' : '');
      dot.onclick = () => goTo(i);
      d.appendChild(dot);
    }
  }

  function goTo(n) {
    const slides = document.querySelectorAll('.slide');
    slides[current].classList.remove('active');
    slides[current].classList.add('exit');
    setTimeout(() => slides[current].classList.remove('exit'), 400);
    current = n;
    slides[current].classList.add('active');
    document.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === current));
    document.getElementById('counter').textContent = (current + 1) + ' / ' + TOTAL;
  }

  function next() { if (current < TOTAL - 1) goTo(current + 1); }
  function prev() { if (current > 0) goTo(current - 1); }

  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next();
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   prev();
  });

  buildDots();

  // QUIZ LOGIC — only include if deck has a quiz slide
  // (paste quiz JS from references/slide-types.md § Quiz here)
</script>
</body>
</html>
```

---

## Checklist before saving

- [ ] `TOTAL` in JS matches the number of `<div class="slide">` elements
- [ ] First slide has `class="slide active"`, all others just `class="slide"`
- [ ] Nav button labels match the deck language
- [ ] Quiz `answers` object keys and `QUIZ_TOTAL` are correct
- [ ] Quiz slide has `#sN.active { overflow-y: auto; }` if 4+ questions
- [ ] Each slide title uses `<span class="accent">` on at least one word
- [ ] `featured` tool cards have correct `data-badge` for non-Spanish decks
