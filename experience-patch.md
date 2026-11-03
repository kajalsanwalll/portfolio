# Experience section patch

## 1. CSS
Delete the whole `/* EXPERIENCE — rotating carousel */` block (from `.exp-carousel{...}` through `.exp-dot.active{...}`) and paste this in its place:

```css
/* EXPERIENCE — auto-rotating stacked deck */
#experience{overflow-x:hidden;}
.exp-stage{position:relative;padding-top:56px;}           /* room for the peeking cards */
.exp-slide{
  position:absolute;top:56px;left:0;right:0;
  transform-origin:50% 0;
  background:#0a0705;border-radius:20px;
  transition:transform .9s cubic-bezier(.2,.6,0,1),opacity .9s ease,filter .9s ease;
  will-change:transform;
}
.exp-slide .exp-entry,.exp-slide .exp-entry-cofounder{margin:0;padding:0;border:none;}
.exp-slide[data-o="0"]{transform:translateY(0) scale(1);opacity:1;filter:none;z-index:10;}
.exp-slide[data-o="1"]{transform:translateY(-22px) scale(.95);opacity:.65;filter:brightness(.6);z-index:9;pointer-events:none;}
.exp-slide[data-o="2"]{transform:translateY(-44px) scale(.9);opacity:.35;filter:brightness(.45);z-index:8;pointer-events:none;}
.exp-slide[data-o="3"]{transform:translateY(-66px) scale(.85);opacity:0;filter:brightness(.35);z-index:7;pointer-events:none;}
/* the front card swings out in an arc, then tucks in at the back */
.exp-slide.leaving{animation:swingBack 1.1s cubic-bezier(.45,.05,.25,1) both;}
@keyframes swingBack{
  0%  {transform:translate(0,0) scale(1) rotate(0);opacity:1;filter:none;z-index:20;}
  35% {transform:translate(30%,-4%) scale(.97) rotate(6deg);opacity:1;filter:brightness(.9);z-index:20;}
  70% {transform:translate(12%,-48px) scale(.9) rotate(2deg);opacity:.6;filter:brightness(.5);z-index:6;}
  100%{transform:translateY(-66px) scale(.85) rotate(0);opacity:0;filter:brightness(.35);z-index:6;}
}
@media(max-width:820px){
  @keyframes swingBack{
    0%  {transform:translate(0,0) scale(1) rotate(0);opacity:1;z-index:20;}
    35% {transform:translate(18%,-3%) scale(.97) rotate(4deg);opacity:1;z-index:20;}
    100%{transform:translateY(-66px) scale(.85) rotate(0);opacity:0;z-index:6;}
  }
}
```

## 2. HTML
Replace everything inside `<div class="exp-carousel reveal-item" id="expCarousel"> … </div>` with the block below.
Keep your existing SelfShft, BluArmor and Teaching Assistant slides exactly as they are (just the three `<div class="exp-slide">` blocks). Delete the two clone slides, the counter, arrows, progress bar and dots.

```html
<div class="exp-carousel reveal-item" id="expCarousel">
  <div class="exp-stage" id="expStage">

    <!-- SLIDE 1 — SelfShft  (your existing <div class="exp-slide"> block) -->
    <!-- SLIDE 2 — BluArmor  (your existing block) -->
    <!-- SLIDE 3 — Teaching Assistant (your existing block) -->

    <!-- SLIDE 4 — CERN (new) -->
    <div class="exp-slide">
      <div class="exp-entry-cofounder">
        <div class="exp-info-main">
          <p class="exp-eyebrow">2026 · Shortlisted</p>
          <p class="exp-role-title">CERN Studentship — Software Development Engineer</p>
          <p class="exp-subtitle">1-Year Studentship · CERN, Geneva</p>
          <p class="exp-desc">Shortlisted for CERN's <b>1-year SDE studentship</b>. I made it through the selection stages but wasn't selected for the final offer. The process pushed me to sharpen my <b>systems fundamentals, data structures &amp; algorithms and software design</b>, and it's something I plan to apply for again.</p>
          <span class="exp-startup-badge">
            <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            Shortlisted · CERN SDE Studentship
          </span>
        </div>
        <div class="exp-side-card">
          <div>
            <p class="exp-side-label">Outcome</p>
            <p class="exp-side-highlight">Reached the <b>shortlist</b> for one of CERN's competitive software roles. Not selected this time, but a strong benchmark to build toward.</p>
          </div>
          <div class="exp-side-stat">
            <span class="exp-side-stat-num">Shortlisted</span>
            <span class="exp-side-stat-lbl">CERN · SDE</span>
          </div>
        </div>
        <div class="exp-bottom-row">
          <div class="exp-tech">
            <p class="exp-tech-label">Prepared With</p>
            <div class="exp-tags">
              <span class="exp-tag">Data Structures &amp; Algorithms</span><span class="exp-tag">System Design</span><span class="exp-tag">Backend Engineering</span><span class="exp-tag">Embedded Systems</span>
            </div>
          </div>
          <div class="exp-tech">
            <p class="exp-tech-label">Takeaways</p>
            <div class="exp-tags">
              <span class="exp-tag">Competitive Selection</span><span class="exp-tag">Interview Readiness</span><span class="exp-tag">Growth Mindset</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
```

Update the Home paragraph about SelfShft with one extra line (optional):

```html
<p class="home-para fade-in-d4">I was also <b>shortlisted for CERN's 1-year Software Development Engineer studentship</b>, a process that sharpened my systems and engineering fundamentals.</p>
```

## 3. JS
Replace the whole `// ── Experience carousel (rotating loop) ──` IIFE with:

```js
// ── Experience: auto-rotating stacked deck ─────────────
(function(){
  const stage=document.getElementById('expStage');
  if(!stage) return;
  const slides=Array.from(stage.querySelectorAll('.exp-slide'));
  const n=slides.length;
  const INTERVAL=4500, SWING=1100;
  let active=0, timer=null, paused=false;

  function layout(){
    slides.forEach((s,i)=>{
      const o=(i-active+n)%n;
      s.dataset.o=Math.min(o,3);
      if(o===0){s.removeAttribute('inert');s.setAttribute('aria-hidden','false');}
      else{s.setAttribute('inert','');s.setAttribute('aria-hidden','true');}
    });
  }
  function setHeight(){
    const h=Math.max(...slides.map(s=>s.offsetHeight));
    stage.style.height=(h+56)+'px';
  }
  function advance(){
    const leaving=slides[active];
    leaving.classList.add('leaving');
    setTimeout(()=>leaving.classList.remove('leaving'),SWING);
    active=(active+1)%n;
    layout();
  }
  function start(){ clearInterval(timer); timer=setInterval(()=>{ if(!paused) advance(); },INTERVAL); }

  stage.addEventListener('mouseenter',()=>paused=true);   // pause while reading
  stage.addEventListener('mouseleave',()=>paused=false);

  layout(); setHeight(); start();
  window.addEventListener('load',setHeight);
  window.addEventListener('resize',setHeight);
})();
```