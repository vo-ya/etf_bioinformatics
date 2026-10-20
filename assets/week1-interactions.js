/* Introductory predictions and small, explicitly synthetic experiments. */
(function (root) {
  'use strict';
  const quality = [40, 40, 40, 40, 20, 20, 10, 10];
  function signalAt(interference) {
    if (!Number.isFinite(interference) || interference < 0 || interference > 100) throw new RangeError('Use a control value from 0 to 100.');
    const intensities = [90 - .6 * interference, 12 + .7 * interference,
      8 + .1 * interference, 5 + .05 * interference];
    const ranked = intensities.map((value, index) => ({ value, base: 'ACGT'[index] }))
      .sort((a, b) => b.value - a.value);
    const gap = ranked[0].value - ranked[1].value;
    return { intensities, call: Math.abs(gap) < 1e-9 ? null : ranked[0].base, gap };
  }
  function retainedEvidence(count) {
    if (!Number.isInteger(count) || count < 0 || count > quality.length) throw new RangeError('Keep 0 to 8 bases.');
    const expectedErrors = quality.slice(0, count).reduce((sum, q) => sum + 10 ** (-q / 10), 0);
    return { count, retainedPercent: 100 * count / quality.length,
      meanError: count ? expectedErrors / count : null };
  }
  const api = { signalAt, retainedEvidence };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;
  root.Week1Interactions = api;
  const byId = id => document.getElementById(id);

  const moleculeGroup = document.querySelector('[data-feedback-group="molecules"]');
  if (moleculeGroup) {
    const explanations = {
      sequence: 'DNA letters can stay the same while regulation changes RNA abundance. The DNA sequence alone does not describe the current state of the cell.',
      regulation: 'Yes. Cells can change RNA production and degradation without changing DNA sequence. RNA measurements could investigate this possibility; they would not by themselves explain the growth difference.',
      protein: 'RNA abundance can inform an investigation, but protein amount, regulation, and activity introduce additional steps. An RNA measurement does not directly measure a protein’s activity.'
    };
    moleculeGroup.disabled = false;
    moleculeGroup.addEventListener('change', event => {
      if (event.target.checked && explanations[event.target.value]) byId('molecules-feedback').textContent = explanations[event.target.value];
    });
  }

  const signalControl = byId('signal-interference');
  if (signalControl) {
    const update = () => {
      const value = Number(signalControl.value);
      const state = signalAt(value);
      byId('signal-level').textContent = value;
      byId('signal-bars').querySelectorAll('meter').forEach((meter, index) => {
        meter.value = state.intensities[index];
        meter.textContent = state.intensities[index].toFixed(1);
        meter.nextElementSibling.textContent = state.intensities[index].toFixed(1);
      });
      byId('signal-result').textContent = state.call
        ? `Called letter: ${state.call}. The two largest signals differ by ${state.gap.toFixed(1)} arbitrary units.`
        : 'A and C are tied. This rule cannot choose a unique letter. The signal gap is 0.0 arbitrary units.';
    };
    signalControl.disabled = false;
    signalControl.addEventListener('input', update);
    update();
  }

  const question = byId('investigation-question');
  const measurement = byId('investigation-measurement');
  if (question && measurement) {
    const responses = {
      dna: {
        dna: 'This directly addresses sequence differences. Compare well-supported sequence calls across labelled samples. A difference would still need further evidence to explain slower growth.',
        rna: 'RNA can reveal expression differences and some expressed sequence differences, but it does not cover the whole genome uniformly. DNA sequencing is the more direct starting point for a genome-wide sequence question.',
        protein: 'An activity assay measures what the protein does under the assay conditions. It does not identify the DNA sequence; DNA sequencing directly addresses this question.'
      },
      rna: {
        dna: 'DNA sequencing describes the sequence template. Cells sharing DNA can accumulate different amounts of RNA. RNA abundance measurements directly address this question.',
        rna: 'This directly addresses RNA abundance. Use biological replicates, account for sampling differences, and compare conditions. An RNA change alone does not establish the cause of slower growth.',
        protein: 'A protein activity assay can investigate a consequence or another mechanism, but it does not measure RNA abundance. Measure RNA to address this question directly.'
      },
      protein: {
        dna: 'A DNA difference might suggest a hypothesis about a protein. It does not directly establish protein activity. A suitable activity assay is the more direct measurement.',
        rna: 'RNA abundance can suggest a hypothesis, but it does not directly establish protein activity. A suitable activity assay is the more direct measurement.',
        protein: 'This directly addresses activity under the assay conditions. Include appropriate controls and replicates. Activity measured in an assay may differ from activity inside a living cell, and still needs connecting to growth.'
      }
    };
    const update = () => {
      const selected = measurement.querySelector('input:checked');
      byId('evidence-feedback').textContent = selected ? responses[question.value][selected.value]
        : 'Choose a measurement, then try changing the question.';
    };
    question.disabled = false;
    measurement.disabled = false;
    question.addEventListener('change', update);
    measurement.addEventListener('change', update);
  }

  const retention = byId('retained-bases');
  if (retention) {
    const update = () => {
      const count = Number(retention.value);
      const state = retainedEvidence(count);
      byId('retained-count').textContent = count;
      byId('retained-strip').querySelectorAll(':scope > span').forEach((base, index) => {
        base.classList.toggle('removed-base', index >= count);
        base.setAttribute('aria-label', `Position ${index + 1}: ${'ACGTACGT'[index]}, Q${quality[index]}, ${index < count ? 'retained' : 'removed'}`);
      });
      byId('retention-result').textContent = count
        ? `${count} of 8 bases retained (${state.retainedPercent}%). Mean estimated error probability per retained base: ${Number((100 * state.meanError).toFixed(4))}%.`
        : '0 of 8 bases retained (0%). Mean error probability is undefined: there are no retained bases.';
      byId('retention-tradeoff').textContent = count === 0
        ? 'Removing everything leaves no usable sequence. A zero total error estimate would not make this useful data.'
        : count === 8 ? 'Keeping all eight positions preserves the most sequence, including the uncertain tail.'
        : count >= 6 ? 'You retain most of the sequence. Compare the uncertain tail with the sequence information you lose.'
        : 'You keep fewer positions with stronger estimated support. A shorter sequence can be harder to locate uniquely.';
    };
    retention.disabled = false;
    retention.addEventListener('input', update);
    update();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
