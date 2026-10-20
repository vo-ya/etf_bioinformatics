/* Small introductory demonstrations. The lesson stays readable without JavaScript. */
(() => {
  'use strict';
  const tabs = [...document.querySelectorAll('[data-case]')];
  const activate = tab => {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activate(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      activate(tabs[next]);
      tabs[next].focus();
    });
  });
  if (tabs.length) activate(tabs[0]);
  const slider = document.getElementById('intro-quality');
  if (slider) {
    const update = () => {
      const q = Number(slider.value);
      const probability = 100 * 10 ** (-q / 10);
      document.getElementById('intro-q').textContent = `Q${q}`;
      document.getElementById('intro-probability').textContent = `${Number(probability.toPrecision(3))}% estimated error probability`;
    };
    slider.addEventListener('input', update);
    update();
  }
})();
