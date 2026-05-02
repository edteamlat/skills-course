# Slide Types — Layout Library

Every slide is a `<div class="slide" id="sN">` (N = 0, 1, 2…).
The first slide is always the cover (`id="s0"`).
Use `<h2>Title <span class="accent">word</span></h2>` for slide titles.
Omit slide-label tags unless the user explicitly wants section labels.

---

## 0 · Cover slide

```html
<div class="slide active" id="s0">
  <div class="eyebrow">MODULE NAME · Subtitle line</div>
  <h1>Main <span class="accent">Title</span></h1>
  <div class="divider"></div>
  <p class="subtitle">One-line description of what this deck covers</p>
</div>
```

Use `<h1>` only here. All other slides use `<h2>`.
Omit `eyebrow` or `subtitle` if not relevant.

---

## 1 · VS Split (two-column contrast)

Best for: comparisons, before/after, option A vs B.

```html
<div class="slide" id="sN">
  <h2>Left <span class="accent">vs.</span> Right</h2>
  <div class="vs-content">
    <div class="vs-card bad">
      <span class="vs-tag bad">Label A</span>
      <h3 class="red">Title A</h3>
      <ul class="vs-list">
        <li>Point one</li>
        <li>Point two</li>
        <li>Point three</li>
      </ul>
    </div>
    <div class="vs-card good">
      <span class="vs-tag good">Label B</span>
      <h3 class="green">Title B</h3>
      <ul class="vs-list">
        <li>Point one</li>
        <li>Point two</li>
        <li>Point three</li>
      </ul>
    </div>
  </div>
</div>
```

CSS classes: `vs-card bad` (red top border) / `vs-card good` (green top border).
For neutral comparisons (no good/bad), use `vs-card neutral` on both sides.

---

## 2 · Artifact Flow (horizontal pipeline)

Best for: sequential steps, pipelines, workflows with named artifacts.

```html
<div class="slide" id="sN">
  <h2>The <span class="accent">Flow</span></h2>
  <div class="artifact-flow">
    <div class="artifact-card">
      <div class="artifact-num">01</div>
      <span class="artifact-icon mono">/command</span>
      <h3>Step Name</h3>
      <span class="fname">filename.md</span>
      <p>One-sentence description of what this artifact is.</p>
    </div>
    <!-- arrow separator -->
    <div class="arrow-sep">
      <svg viewBox="0 0 18 18" fill="none"><path d="M4 9h10M10 5l4 4-4 4" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </div>
    <div class="artifact-card">
      <div class="artifact-num">02</div>
      <span class="artifact-icon mono">/command</span>
      <h3>Step Name</h3>
      <span class="fname">filename.md</span>
      <p>One-sentence description.</p>
    </div>
    <!-- repeat pattern for each step; max 5 steps -->
  </div>
  <div class="insight">
    Key takeaway about the flow — one sentence, centered below the pipeline.
  </div>
</div>
```

Limit to 5 steps maximum for readability. For longer pipelines, split into two slides.

---

## 3 · Comparison Table

Best for: feature matrices, methodology comparisons (3 columns max).

```html
<div class="slide" id="sN">
  <h2>A, B <span class="accent">and</span> C</h2>
  <div class="table-wrap">
    <table class="comp-table">
      <thead>
        <tr>
          <th></th>
          <th><span class="badge badge-blue">Option A</span></th>
          <th><span class="badge badge-green">Option B</span></th>
          <th><span class="badge badge-gold">Option C</span></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Criterion 1</td>
          <td>Value</td>
          <td>Value</td>
          <td class="h">Highlighted value</td>
        </tr>
        <!-- repeat rows -->
      </tbody>
    </table>
  </div>
  <p class="footnote">Optional clarifying note below the table.</p>
</div>
```

Badge color classes: `badge-blue`, `badge-green`, `badge-gold`, `badge-red`.
Use `class="h"` on cells you want to highlight in accent color.

---

## 4 · Timeline

Best for: historical progression, evolution, phases over time.

```html
<div class="slide" id="sN">
  <h2>The <span class="accent">Evolution</span></h2>
  <div class="timeline">
    <div class="tl-line">
      <div class="tl-step">
        <div class="tl-bar" style="background:#333;"></div>
        <div class="tl-body">
          <div class="tl-year">~2021</div>
          <div class="tl-title">Era Name</div>
          <div class="tl-desc">Brief description of this period.</div>
        </div>
      </div>
      <!-- repeat; mark current/highlighted step with class="tl-step current" -->
      <div class="tl-step current">
        <div class="tl-bar"></div><!-- no inline style = accent color -->
        <div class="tl-body">
          <div class="tl-year">2025 →</div>
          <div class="tl-title">Current Era</div>
          <div class="tl-desc">What is happening now.</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

Max 5 steps. The `current` step uses the accent color bar automatically.

---

## 5 · Tools Grid (feature cards)

Best for: ecosystem overview, product/tool showcase.

```html
<div class="slide" id="sN">
  <h2>The <span class="accent">Ecosystem</span></h2>
  <div class="tools-grid">
    <div class="tool-card featured"><!-- "featured" adds a label badge -->
      <div class="tool-logo">tool-name</div>
      <h3>Tool Name</h3>
      <p>Short description of what it does and who it's for.</p>
      <div class="tool-tags">
        <span class="tool-tag">tag1</span>
        <span class="tool-tag">tag2</span>
      </div>
    </div>
    <div class="tool-card">
      <!-- same structure without "featured" -->
    </div>
    <!-- 2–4 cards total -->
  </div>
</div>
```

Use `featured` on the recommended/primary tool. The badge text is "elegido" by default;
override with `data-badge="chosen"` for English decks.

---

## 6 · Reasons / Features Grid (2×2)

Best for: "why X?", "key features", "main benefits".

```html
<div class="slide" id="sN">
  <h2>¿Por qué <span class="accent">usar esto</span>?</h2>
  <div class="reasons">
    <div class="reason-card">
      <div class="reason-num">01</div>
      <div>
        <h3>Reason title</h3>
        <p>One or two sentences of explanation.</p>
      </div>
    </div>
    <!-- 3 more reason-cards (total 4) -->
  </div>
</div>
```

---

## 7 · Attribute Grid (icon + title + description)

Best for: listing named concepts, configuration options, components.
Example: Constitution contents, API endpoints, architecture layers.

```html
<div class="slide" id="sN">
  <h2>Slide <span class="accent">Title</span></h2>
  <div class="attr-grid">
    <div class="attr-item">
      <span class="attr-icon mono">⬡</span>
      <div>
        <h3>Attribute Name</h3>
        <p>Short description.</p>
      </div>
    </div>
    <!-- repeat; last item can span full width with class="attr-item attr-full" -->
    <div class="attr-item attr-full attr-danger">
      <span class="attr-icon red">✕</span>
      <div>
        <h3 class="red">Danger / exclusion item</h3>
        <p>What should NOT be done or included.</p>
      </div>
    </div>
  </div>
</div>
```

Grid is 3 columns by default. For 4 items use `class="attr-grid attr-grid-2"` (2 cols).

---

## 8 · Flow Steps (vertical numbered steps)

Best for: how-to guides, process walkthroughs, best practices.

```html
<div class="slide" id="sN">
  <h2>Your own <span class="accent">workflow</span></h2>
  <div class="flow-steps">
    <div class="fs-step">
      <div class="fs-num accent">01</div>
      <div class="fs-body">
        <h3>Step title</h3>
        <p>Explanation with optional <span class="mono accent">/command</span> reference.</p>
      </div>
    </div>
    <div class="fs-connector"></div>
    <div class="fs-step">
      <div class="fs-num accent">02</div>
      <div class="fs-body">
        <h3>Step title</h3>
        <p>Explanation.</p>
      </div>
    </div>
    <!-- alternate fs-step / fs-connector; 3–5 steps ideal -->
  </div>
</div>
```

---

## 9 · Context Columns (audience segmentation)

Best for: "when to use X", adapting to different team sizes or roles.

```html
<div class="slide" id="sN">
  <h2>Adapting to <span class="accent">your context</span></h2>
  <div class="ctx-grid">
    <div class="ctx-card">
      <div class="ctx-label mono">Audience A</div>
      <h3>Label</h3>
      <ul class="ctx-list">
        <li>Point one</li>
        <li>Point two</li>
        <li>Point three</li>
      </ul>
    </div>
    <!-- 2–3 more ctx-cards; last one with class="ctx-card ctx-key" for highlight -->
    <div class="ctx-card ctx-key">
      <div class="ctx-label mono accent">key</div>
      <h3>Always true</h3>
      <ul class="ctx-list">
        <li>Universal rule</li>
      </ul>
    </div>
  </div>
</div>
```

---

## 10 · BMAD-style Two-Column Comparison (with divider)

Best for: tool-vs-tool with detailed attribute lists.

```html
<div class="slide" id="sN">
  <h2>A <span class="accent">vs.</span> B</h2>
  <div class="bvs-wrap">
    <div class="bvs-col">
      <div class="bvs-header">
        <span class="bvs-tag sk">Tool A</span>
        <p class="bvs-when">When to use A</p>
      </div>
      <ul class="bvs-list">
        <li><span class="bvs-check green">✓</span> Feature or benefit</li>
        <li><span class="bvs-check muted">~</span> Neutral attribute</li>
      </ul>
    </div>
    <div class="bvs-divider"><span>vs</span></div>
    <div class="bvs-col">
      <div class="bvs-header">
        <span class="bvs-tag bmad">Tool B</span>
        <p class="bvs-when">When to use B</p>
      </div>
      <ul class="bvs-list">
        <li><span class="bvs-check blue">✓</span> Feature or benefit</li>
        <li><span class="bvs-check muted">~</span> Neutral attribute</li>
      </ul>
    </div>
  </div>
  <div class="bvs-note">Bottom note — relationship between the two tools.</div>
</div>
```

Tag color classes: `bvs-tag sk` (green), `bvs-tag bmad` (blue), `bvs-tag gold` (gold).

---

## 11 · Quiz (EDquiz)

Best for: end-of-module knowledge check. Place as the last (or second-to-last) slide.

```html
<div class="slide" id="sN">
  <div class="quiz-wrap">
    <div class="quiz-header">
      <h2>ED<span class="accent">quiz</span></h2>
      <p>Select the correct answer for each question</p><!-- translate to deck language -->
    </div>

    <!-- Question block — repeat for each question -->
    <div class="question" id="qN">
      <div class="q-number">QUESTION 01 / 05</div>
      <div class="q-text">Question text goes here?</div>
      <div class="options">
        <div class="option" onclick="answer(N,'a')"><span class="opt-letter">a</span> Option A text</div>
        <div class="option" onclick="answer(N,'b')"><span class="opt-letter">b</span> Option B text</div>
        <div class="option" onclick="answer(N,'c')"><span class="opt-letter">c</span> Option C text</div>
        <div class="option" onclick="answer(N,'d')"><span class="opt-letter">d</span> Option D text</div>
      </div>
      <div class="q-feedback" id="fN">Explanation shown after answering — why the correct answer is right.</div>
    </div>
    <!-- /Question block -->

    <div class="quiz-score" id="quiz-score">
      <div class="score-num" id="score-num">0/5</div>
      <div class="score-label">correct answers</div><!-- translate -->
      <div class="score-msg" id="score-msg"></div>
      <button class="btn-reset" onclick="resetQuiz()">Try again</button><!-- translate -->
    </div>
  </div>
</div>
```

**Quiz JS** — place inside the main `<script>` block at the bottom, after the nav logic:

```javascript
// Quiz — keys are question numbers (1-based), values are correct option letters
const answers = { 1:'b', 2:'c', 3:'a', 4:'d', 5:'b' }; // update per deck
const quizState = {};
let totalCorrect = 0;
const QUIZ_TOTAL = 5; // update to match question count

function answer(qn, choice) {
  if (quizState[qn]) return;
  quizState[qn] = choice;
  const q = document.getElementById('q' + qn);
  const opts = q.querySelectorAll('.option');
  const correct = answers[qn];
  opts.forEach((opt, i) => {
    opt.classList.add('locked');
    const letter = ['a','b','c','d'][i];
    if (letter === correct) opt.classList.add('correct');
    else opt.classList.add('wrong');
  });
  q.classList.add('answered');
  document.getElementById('f' + qn).classList.add('show');
  if (choice === correct) totalCorrect++;
  if (Object.keys(quizState).length === QUIZ_TOTAL) showScore();
}

function showScore() {
  const sc = document.getElementById('quiz-score');
  sc.classList.add('show');
  document.getElementById('score-num').textContent = totalCorrect + '/' + QUIZ_TOTAL;
  const msgs = [
    'Review the module before continuing.',
    'Almost. Review the concepts you missed.',
    'Good. You have the foundation.',
    'Very good! Ready for the next module.',
    'Perfect! You mastered this module.'
  ]; // translate array to deck language
  document.getElementById('score-msg').textContent = msgs[totalCorrect] || msgs[QUIZ_TOTAL];
  sc.scrollIntoView({ behavior: 'smooth' });
}

function resetQuiz() {
  Object.keys(quizState).forEach(k => delete quizState[k]);
  totalCorrect = 0;
  for (let i = 1; i <= QUIZ_TOTAL; i++) {
    const q = document.getElementById('q' + i);
    q.querySelectorAll('.option').forEach((o, idx) => {
      o.className = 'option';
      const letter = ['a','b','c','d'][idx];
      o.onclick = () => answer(i, letter);
    });
    q.classList.remove('answered');
    document.getElementById('f' + i).classList.remove('show');
  }
  document.getElementById('quiz-score').classList.remove('show');
}
```

The quiz slide should use `overflow-y: auto` via `#sN.active { overflow-y: auto; }` 
when there are 4+ questions.
