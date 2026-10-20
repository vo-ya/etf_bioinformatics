// Adapted from bioinformatis-web. Modified for Week 1 to allow iframe shrinkage.
// Apache-2.0; see ../../third_party/bioinformatis-web-LICENSE.
// Auto-size the embedding iframe to this artifact's natural height.
// Parent listens for { type: 'artifact-resize', height } and sets iframe.style.height.
(function () {
  if (window.parent === window) return;

  let lastHeight = 0;

  function measure() {
    // Body has natural height and padding. Including the root viewport height
    // would prevent the parent from shrinking after results are hidden.
    return Math.ceil(document.body.getBoundingClientRect().height);
  }

  function post() {
    const h = measure();
    if (h === lastHeight) return;
    lastHeight = h;
    window.parent.postMessage({ type: 'artifact-resize', height: h }, '*');
  }

  if (typeof ResizeObserver !== 'undefined') {
    const ro = new ResizeObserver(post);
    ro.observe(document.documentElement);
    ro.observe(document.body);
  } else {
    setInterval(post, 250);
  }

  window.addEventListener('load', post);
  window.addEventListener('resize', post);
  document.addEventListener('DOMContentLoaded', post);
})();
