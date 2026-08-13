# Cover letter — Journal of Clinical Lipidology

Dr Nader Genedy, MBBCh, MRCP(UK), MRCPI, SCE(AIM), MRCGP
Department of Metabolic Medicine, University Hospital of Wales
Cardiff and Vale University Health Board, Cardiff, UK
[redacted]

The Editor-in-Chief
*Journal of Clinical Lipidology*

Dear Professor,

**Re: Original Research — "Apolipoprotein B–LDL discordance identifies established cardiovascular disease in genetically defined familial hypercholesterolaemia, but absolute risk does not transport between clinic and biobank"**

We submit the above manuscript for consideration as an Original Research article.

Existing familial hypercholesterolaemia risk instruments were developed in clinically ascertained cohorts using conventional lipids, and we could identify none built from raw apolipoprotein measurements and tested for transport between ascertainment settings. We therefore developed CALON-N, a seven-variable classifier of established atherosclerotic cardiovascular disease fitted from raw clinical and laboratory variables — with published scores prohibited as inputs and retained only as comparators — and evaluated it reciprocally between a genetically ascertained Welsh specialist FH clinic (424 participants, 62 cases, 219 families) and coordinate-verified UK Biobank *LDLR* pathogenic/likely pathogenic carriers (890 participants, 57 cases). Discrimination transported in both directions (AUC 0.767, 95% CI 0.712–0.828, and 0.848, 0.796–0.896), but absolute probabilities did not: expected:observed ratios were 3.00 and 0.45.

We believe the work suits the Journal for two reasons. First, apolipoprotein B is moving from a research measurement to a clinical one, and this is, to our knowledge, the first FH-specific model built from raw apoB, LDL-C and apoA1 and subjected to reciprocal clinic-to-biobank transport. Second, and more importantly, the paper is as informative where it fails as where it succeeds. CALON-N did not outperform Montreal-FH-SCORE in either direction, age plus sex alone achieved the highest AUC in the clinic cohort (0.895), and the model exceeded the best comparator in only one of 14 estimable subgroup analyses. We report all of this, including two candidate architectures that failed a prespecified coefficient-direction gate, and we withdrew a comparative decision-curve analysis at quality control after establishing that the comparators were ranking scores rather than calibrated probabilities on a common scale. The calibration reversal is, in our view, the paper's most useful result for the field: it quantifies how far a single equation can drift when ascertainment changes within one disease.

The study carries the analyses a critical reader will expect: prespecified low-dimensional candidate architectures with ridge penalisation; family-intact and qualifying-variant-component-intact resampling; fold-local completion, transformation, scaling and penalty tuning; a locked physiological sign gate; reciprocal transport without target recalibration; 4,000-replicate cluster bootstraps for all paired differences; and sensitivity analyses across an alternative genetic definition, two alternative endpoint definitions, and complete cases. Reporting was mapped item by item to TRIPOD+AI and STROBE, with risk of bias appraised by PROBAST; we state plainly that architecture selection consumed outcome information from both cohorts and that this is therefore target-informed reciprocal development rather than protected external validation. We make no prospective-risk, threshold, or clinical-deployment claim.

We confirm that this manuscript is original, is not under consideration elsewhere, and has been approved by all authors. UK Biobank analyses were conducted under Application 1002450 (NHS Research Ethics Service approval 11/NW/0382); Welsh service data were analysed under local research governance, and only aggregate, de-identified results are reported. Participant-level NHS Wales and UK Biobank data cannot be redistributed, but aggregate outputs, code, the deterministic model object, protocol and amendment, quality-control reports and checksum manifests are available subject to institutional and UK Biobank requirements. Generative-AI-assisted tools were used for code review, document structuring and language editing; no participant-level data were transmitted to any such service, and the authors accept full responsibility for the content.

We would be glad to suggest or exclude reviewers on request, and we thank you for considering our work.

Yours sincerely,

Nader Genedy, on behalf of all authors

---

## Pre-submission checklist

**Complete before sending:**

- [ ] Welsh PASS/DRAGON approval or service-evaluation determination, consent or waiver, UK GDPR legal basis, data controller, and R&D/information-governance reference
- [ ] Patient and public involvement statement — confirm or describe
- [ ] Author contributions using the CRediT taxonomy
- [ ] Individual COI disclosure forms for every author
- [ ] Confirm funding statement with all authors
- [ ] Figures 1 and 2 exported at journal resolution
- [ ] Supplement compiled (Methods 0–2, Tables S1–S6, exposure hierarchy note)

**Journal cascade if declined:**
1. *Journal of Clinical Lipidology* — primary; published both comparator scores and the group's prior apoB/LDL-C work
2. *Atherosclerosis* — published the French SAFEHEART-RE validation; receptive to transport and methodology
3. *Journal of Clinical Medicine* / *Open Heart* — pragmatic fallback for a well-reported negative-leaning methodological study
