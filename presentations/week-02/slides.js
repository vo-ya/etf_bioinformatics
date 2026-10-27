(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.slide')];
  if (!slides.length) return;
  const byId = id => document.getElementById(id);
  const previous = byId('previous');
  const next = byId('next');
  const counter = byId('counter');
  const progress = byId('progress');
  const help = byId('help');
  const notes = byId('notes-panel');
  const notesButton = byId('notes-toggle');
  const revealButton = byId('reveal-next');
  const revealCount = byId('reveal-count');
  const steps = slides.map(() => 0);
  let index = 0;
  let printing = false;
  const totalSteps = slide => Number(slide.dataset.steps || 0);

  function fitFigure(figure) {
    const image = figure.querySelector('img');
    const width = Number(image.getAttribute('width'));
    const height = Number(image.getAttribute('height'));
    if (!width || !height || !figure.clientWidth || !figure.clientHeight) return;
    const scale = Math.min(figure.clientWidth / width, figure.clientHeight / height);
    // Match the element box to the SVG's aspect ratio before applying clips.
    image.style.width = `${width * scale}px`;
    image.style.height = `${height * scale}px`;
  }

  function resize() {
    const deck = document.querySelector('.deck');
    const style = getComputedStyle(deck);
    const horizontal = parseFloat(style.paddingLeft) + parseFloat(style.paddingRight);
    const vertical = parseFloat(style.paddingTop) + parseFloat(style.paddingBottom);
    const scale = Math.min((deck.clientWidth - horizontal) / 1280,
      (deck.clientHeight - vertical) / 720);
    document.documentElement.style.setProperty('--scale', Math.max(.05, scale));
    slides[index].querySelectorAll('[data-clips]').forEach(fitFigure);
  }

  function renderStep() {
    const slide = slides[index];
    const step = steps[index];
    const total = totalSteps(slide);
    slide.querySelectorAll('[data-reveal]').forEach(part => {
      const revealed = Number(part.dataset.reveal) <= step;
      part.classList.toggle('is-revealed', revealed);
      part.setAttribute('aria-hidden', String(!revealed));
      part.inert = !revealed;
    });
    slide.querySelectorAll('[data-clips]').forEach(figure => {
      fitFigure(figure);
      const clips = figure.dataset.clips.split('|');
      figure.querySelector('img').style.clipPath = clips[Math.min(step, clips.length - 1)];
    });
    slide.querySelectorAll('[data-captions]').forEach(caption => {
      const captions = caption.dataset.captions.split('|');
      caption.textContent = captions[Math.min(step, captions.length - 1)];
    });
    previous.disabled = index === 0 && step === 0;
    next.disabled = index === slides.length - 1 && step === total;
    revealButton.hidden = total === 0;
    revealButton.disabled = step === total;
    revealButton.setAttribute('aria-controls', slide.id);
    revealButton.setAttribute('aria-label', `Reveal next part of slide ${index + 1}`);
    revealCount.textContent = total ? `${step} / ${total} reveals` : '';
    const caption = slide.querySelector('[data-captions]');
    const newlyRevealed = [...slide.querySelectorAll('[data-reveal]')]
      .filter(part => Number(part.dataset.reveal) === step)
      .map(part => part.textContent.trim()).join('. ');
    byId('status').textContent = `Slide ${index + 1} of ${slides.length}. ${slide.querySelector('h1,h2').textContent}.` +
      (total ? ` Reveal ${step} of ${total}.` : '') + (caption ? ` ${caption.textContent}` : '') +
      (newlyRevealed ? ` ${newlyRevealed}` : '');
  }

  function show(target, changeHash = true) {
    index = Math.max(0, Math.min(slides.length - 1, target));
    slides.forEach((slide, i) => { slide.hidden = i !== index; });
    counter.textContent = `${index + 1} / ${slides.length}`;
    progress.style.width = `${100 * (index + 1) / slides.length}%`;
    const slide = slides[index];
    notes.innerHTML = slide.querySelector('.notes')?.innerHTML || 'No additional notes.';
    document.title = `${index + 1}. ${slide.querySelector('h1,h2').textContent} | Week 2`;
    if (changeHash) history.replaceState(null, '', `#${slide.id}`);
    renderStep();
  }

  function advance() {
    if (steps[index] < totalSteps(slides[index])) { steps[index]++; renderStep(); }
    else show(index + 1);
  }
  function back() {
    if (steps[index] > 0) { steps[index]--; renderStep(); }
    else if (index > 0) { steps[index - 1] = totalSteps(slides[index - 1]); show(index - 1); }
  }
  function replay() { steps[index] = 0; renderStep(); }
  function fromHash() {
    const target = slides.findIndex(slide => `#${slide.id}` === location.hash);
    show(target < 0 ? 0 : target, false);
  }
  function toggleNotes() {
    const open = !notes.classList.contains('open');
    notes.classList.toggle('open', open);
    document.body.classList.toggle('notes-open', open);
    notesButton.setAttribute('aria-expanded', String(open));
    resize();
  }

  previous.addEventListener('click', back);
  next.addEventListener('click', advance);
  revealButton.addEventListener('click', () => {
    if (steps[index] < totalSteps(slides[index])) { steps[index]++; renderStep(); }
  });
  byId('help-toggle').addEventListener('click', () => help.showModal());
  byId('help-close').addEventListener('click', () => help.close());
  notesButton.addEventListener('click', toggleNotes);
  byId('print').addEventListener('click', () => window.print());
  const fullscreen = byId('fullscreen');
  if (!document.documentElement.requestFullscreen) fullscreen.hidden = true;
  fullscreen.addEventListener('click', async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await document.documentElement.requestFullscreen();
    } catch { byId('status').textContent = 'Fullscreen is unavailable in this browser. Use the browser fullscreen command.'; }
  });

  document.addEventListener('keydown', event => {
    if (help.open || /^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName) || event.target.isContentEditable || event.altKey || event.ctrlKey || event.metaKey) return;
    // Space activates focused controls. Arrows continue working after a click.
    if (event.key === ' ' && /^(BUTTON|A)$/.test(event.target.tagName)) return;
    if (['ArrowRight', 'ArrowDown', ' '].includes(event.key)) {
      event.preventDefault(); event.shiftKey ? back() : advance();
    } else if (['ArrowLeft', 'ArrowUp'].includes(event.key)) {
      event.preventDefault(); back();
    } else if (event.key === 'PageDown') { event.preventDefault(); show(index + 1);
    } else if (event.key === 'PageUp') { event.preventDefault(); show(index - 1);
    } else if (event.key === 'Home') { event.preventDefault(); steps[0] = 0; show(0);
    } else if (event.key === 'End') { event.preventDefault(); show(slides.length - 1);
    } else if (event.key === '?') { event.preventDefault(); help.showModal();
    } else if (event.key.toLowerCase() === 'n') { event.preventDefault(); toggleNotes();
    } else if (event.key.toLowerCase() === 'r') { event.preventDefault(); replay(); }
  });
  window.addEventListener('hashchange', fromHash);
  window.addEventListener('resize', resize);
  window.addEventListener('beforeprint', () => {
    if (printing) return;
    printing = true;
    slides.forEach(slide => {
      slide.hidden = false;
      slide.querySelectorAll('[data-reveal]').forEach(part => {
        part.classList.add('is-revealed');
        part.setAttribute('aria-hidden', 'false');
        part.inert = false;
      });
      slide.querySelectorAll('[data-clips]').forEach(figure => {
        figure.querySelector('img').style.clipPath = 'none';
      });
      slide.querySelectorAll('[data-captions]').forEach(caption => {
        caption.textContent = caption.dataset.captions.split('|').pop();
      });
    });
  });
  window.addEventListener('afterprint', () => {
    printing = false;
    const activeIndex = index;
    slides.forEach((_, i) => { index = i; renderStep(); });
    show(activeIndex, false);
    resize();
  });
  document.addEventListener('fullscreenchange', () => {
    fullscreen.textContent = document.fullscreenElement ? 'Exit fullscreen' : 'Fullscreen'; resize();
  });

  // Initialize every slide, so no unseen reveal leaks into keyboard focus.
  document.body.classList.add('presenting');
  slides.forEach((_, i) => { index = i; renderStep(); });
  fromHash(); resize();
})();
