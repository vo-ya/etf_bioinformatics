/* Navigation and local artifact embedding; no external dependencies. */
(() => {
  'use strict';
  const frames = [...document.querySelectorAll('iframe.artifact-frame')];
  window.addEventListener('message', event => {
    const frame = frames.find(item => item.contentWindow === event.source);
    const height = event.data?.height;
    if (!frame || event.data?.type !== 'artifact-resize' || !Number.isFinite(height)) return;
    frame.style.height = `${Math.min(8000, Math.max(240, Math.ceil(height)))}px`;
  });
  const progress = document.getElementById('scroll-progress');
  const updateProgress = () => {
    const available = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = `${available > 0 ? 100 * window.scrollY / available : 0}%`;
  };
  window.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('resize', updateProgress);
  updateProgress();
  const links = [...document.querySelectorAll('.lecture-toc a[href^="#"]')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const current = entries.find(entry => entry.isIntersecting);
      if (!current) return;
      links.forEach(link => {
        const active = link.hash === `#${current.target.id}`;
        link.classList.toggle('is-current', active);
        if (active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-10% 0px -65% 0px' });
    document.querySelectorAll('.lecture-prose section[id]').forEach(section => observer.observe(section));
  }
})();
