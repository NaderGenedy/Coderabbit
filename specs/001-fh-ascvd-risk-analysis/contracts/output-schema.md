# Output contract — 001-fh-ascvd-risk-analysis

Every result file must satisfy this schema. Anything absent is a finding.

## Per cohort

| Field | Meaning |
|---|---|
| `n` | Analysis set size |
| `events` | Incident events |
| `person_years` | Total follow-up |
| `median_followup` | Years |
| `epv` | Events per variable |
| `terms_used` | Predictors after eligibility rules |
| `dropped_collinearity_guard` | Terms removed as linear duplicates of age |
| `dropped_minimum_information_rule` | Terms removed for sparse events |
| `leak_detector_tx_alone_C` | Concordance of baseline treatment alone |
| `outcome_file`, `outcome_field` | Provenance of the outcome |

## Per comparison

| Field | Meaning |
|---|---|
| `c_index` | Model discrimination |
| `repeat_sd` | Across re-randomised repeats |
| `fold_failures` | Convergence failures; zero expected |
| `comparator_c` | Comparator discrimination |
| `delta`, `ci` | Paired difference and 95% interval |
| `verdict` | WIN / tie / LOSS by the interval rule |

## Suppression

Any stratum with fewer than ten events is emitted as
`"<10, non-estimable"` and carries no estimate.

## Prohibited in any output

Participant rows, participant identifiers, family identifiers, dates of birth,
variant coordinates, participant-level predictions.
