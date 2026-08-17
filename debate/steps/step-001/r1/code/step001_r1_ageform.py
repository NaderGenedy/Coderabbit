#!/usr/bin/env python3
"""OBJ-001, direction test: how much C-index does the PUBLISHED SAFEHEART age
form lose against the CONTINUOUS age form used in 15_CALON_FINAL.py line 278?

This is a MECHANISM demonstration on public UK Biobank design parameters
(recruitment age 40-69) plus openly published marginal summaries. It is NOT an
analysis of the cohort and it is NOT a substitute for one. It answers one
question only: is the sign and size of the local-minus-Julius SAFEHEART gap what
the coefficient-form difference alone predicts?
"""
import numpy as np
from lifelines.utils import concordance_index

rng = np.random.default_rng(20260815)
N = 3333

def draw():
    a = rng.normal(56.5, 8.0, int(N*3)); a = a[(a >= 40) & (a <= 70)][:N]
    return dict(
        age=a, male=rng.binomial(1, 0.44, N), htn=rng.binomial(1, 0.53, N),
        smoke=rng.binomial(1, 0.44, N), bmi=rng.normal(27.3, 4.6, N),
        ldl=np.clip(rng.normal(4.6, 1.3, N), 1.0, 12.0),
        lpa=rng.binomial(1, 0.20, N))

def local_safeheart(d):                       # 15_CALON_FINAL.py line 278
    return (0.045*d["age"] + 0.6*d["male"] + 0.4*d["htn"] + 0.3*d["smoke"]
            + 0.02*d["bmi"] + 0.15*d["ldl"] + 0.25*d["lpa"])

def published_safeheart(d):                   # Circulation 2017;135:2138-9 Table 3
    ageb = np.where(d["age"] >= 60, 1.45, np.where(d["age"] >= 30, 1.07, 0.0))
    bmib = np.where(d["bmi"] >= 30, 0.98, np.where(d["bmi"] >= 25, 0.88, 0.0))
    mg = d["ldl"] * 38.67
    ldlb = np.where(mg >= 160, 1.57, np.where(mg >= 100, 0.92, 0.0))
    return (0.70*d["male"] + ageb + 0.69*d["htn"] + 0.48*d["smoke"]
            + bmib + ldlb + 0.42*d["lpa"])     # prior ASCVD = 0 by design

def published_fhrs_beta(d):                   # ATVB 2021 Table 3 / beta scale
    a = d["age"]
    ab = np.select([a <= 30, a <= 35, a <= 40, a <= 45, a <= 50, a <= 55, a <= 60],
                   [0, .938, 1.383, 1.621, 1.738, 1.804, 1.964], 2.256)
    l = d["ldl"]
    lb = np.select([l <= 5.5, l <= 7.5, l <= 8.5, l <= 9.5], [0, .315, .718, .918], 1.136)
    return ab + lb + 0.721*d["male"] + 0.644*d["htn"] + 0.625*d["smoke"] + 0.434*d["lpa"]

TRUTHS = {
    "truth = published FH-RS beta scale": published_fhrs_beta,
    "truth = published SAFEHEART form":   published_safeheart,
    "truth = smooth age + risk factors":  lambda d: (0.055*(d["age"]-56.5) + 0.55*d["male"]
                                                     + 0.45*d["htn"] + 0.40*d["smoke"]
                                                     + 0.18*(d["ldl"]-4.6) + 0.35*d["lpa"]),
}
print(f"{'generative truth':38s} {'C local(cont age)':>18s} {'C published(3-band)':>20s} {'gap':>8s}")
rows = []
for name, truth in TRUTHS.items():
    gaps = []
    for rep in range(20):
        d = draw()
        eta = truth(d); eta = eta - eta.mean()
        # exponential baseline calibrated to ~289 events in ~13.8 y median follow-up
        t = rng.exponential(1.0 / (0.0063 * np.exp(eta)))
        c = rng.uniform(5, 15, N)
        T = np.minimum(t, c); E = (t <= c).astype(int)
        cl = concordance_index(T, -local_safeheart(d), E)
        cp = concordance_index(T, -published_safeheart(d), E)
        gaps.append((cl, cp))
    cl, cp = np.mean([g[0] for g in gaps]), np.mean([g[1] for g in gaps])
    print(f"{name:38s} {cl:18.4f} {cp:20.4f} {cl-cp:+8.4f}")
    rows.append(cl - cp)
print(f"\n  mean C penalty of the published 3-band age form: {np.mean(rows):+.4f}")
print(f"  observed local-minus-Julius SAFEHEART gap        : +0.0664  (0.6944 - 0.628)")
print("\n  The published form collapses to a single age>=60 split in a 40-69 cohort:")
d = draw(); print(f"    share age<30 (reference level, EMPTY in UKB): "
                  f"{float((d['age'] < 30).mean()):.4f}")
print("  Same test for FH-RS: the local beta vector and the Spec Kit chart points")
print("  are a monotone affine map (18/18, section A), so NO comparable mechanism")
print("  exists there. A 0.023 FH-RS gap is therefore NOT explained by coefficient form.")
