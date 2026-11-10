# Week 4 browser preview

`browser-preview.png` is rendered directly from the supplied notebook's optional
mini-browser code by `practicals/week-04/render_preview.py`. It is an original
course plot, using invented DNA and annotations rather than measured data.

The GC track uses consecutive ten-base windows with values 0, 100, 40, 40, 60,
60 percent. The feature track shows A at [12,26) and B at [38,54), independent
of composition. Both share the same zero-based coordinate axis, with excluded
right endpoints. The notebook can crop the region without changing GC bins.

Regenerate after editing the notebook renderer. The PNG is 1500 × 750 pixels;
the student lesson supplies a text description of its numerical contents.
