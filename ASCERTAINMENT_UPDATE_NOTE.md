# Separate programme note: ascertainment-specific FH-Risk-Score updating

The proposed architecture—published FH-Risk-Score linear predictor plus
proband/cascade-specific baseline risk—is plausible and potentially more useful
than re-estimating a full prospective model from 92 events. It borrows stable
published relative-effect information and targets a calibration problem created
by referral route.

It is not yet established that the claimed 90% reduction in calibration error
will generalise. Separate intercepts improve stratum E:O partly by construction.
The next analysis must therefore:

1. fix the 5- or 10-year estimand, baseline, event, censoring, and competing
   death before fitting;
2. establish that ascertainment route is known at baseline and not defined by
   future phenotype;
3. estimate all route-specific baselines inside family-disjoint outer folds;
4. shrink the route effect or fit a penalised route-by-score update;
5. compare against no update, one common intercept update, common
   intercept+slope recalibration, and a full route interaction;
6. report pooled and within-route calibration intercept/slope, Brier score,
   decision curves, and discrimination;
7. quantify route imbalance, event counts, and related-family overlap;
8. validate once in an independent FH registry with ascertainment route.

Safe current wording: “an internally validated ascertainment-specific
recalibration of FH-Risk-Score.” Do not call it a new independent score, the
first such model, or clinically deployable until the literature search and
external validation are complete.

