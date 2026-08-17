#!/usr/bin/env python3
"""Step 001 round 1 - all arithmetic used in claude's turn. No participant data.

Sections
  A  FH-Risk-Score provenance : Table 3 chart points (ATVB 2021;41:2637) vs the
     beta vector hard-coded in code/15_CALON_FINAL.py lines 267-271.
  B  SAFEHEART provenance     : Table 3 multivariable HRs (Circulation
     2017;135:2138-2139) vs the published equation coefficients printed in the
     worked examples on p2139, vs 15_CALON_FINAL.py line 278.
  C  OBJ-002  : exact slope ratios for the centred x horizon factorial, computed
     on the full attainable support of the published SAFEHEART LP.
  D  OBJ-003  : algebraic bound on r(age, log(age * untreated non-HDL)) and on
     r(age, sp50), against the 0.999 drop rule at 15_CALON_FINAL.py line 300.
"""
import itertools, math
import numpy as np

def rule(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# ---------------------------------------------------------------- A  FH-RS
rule("A. FH-Risk-Score: published Table 3 points vs local beta vector")
# Paquette et al, ATVB 2021;41:2632-2640, Table 3, page 2637. Read from
# FH_Risk_Score_2021.pdf (sha256 9330f910f8879432), PDF page 6.
PTS = {"male":7,
       "age_31_35":9,"age_36_40":14,"age_41_45":16,"age_46_50":17,
       "age_51_55":18,"age_56_60":20,"age_gt60":23,
       "hdl_101_130":3,"hdl_085_100":7,"hdl_lt085":8,
       "ldl_551_750":3,"ldl_751_850":7,"ldl_851_950":9,"ldl_gt950":11,
       "htn":6,"smoke":6,"lpa_ge50":4}
# code/15_CALON_FINAL.py lines 267-277
LOC = {"male":0.721,
       "age_31_35":0.938,"age_36_40":1.383,"age_41_45":1.621,"age_46_50":1.738,
       "age_51_55":1.804,"age_56_60":1.964,"age_gt60":2.256,
       "hdl_101_130":0.298,"hdl_085_100":0.712,"hdl_lt085":0.752,
       "ldl_551_750":0.315,"ldl_751_850":0.718,"ldl_851_950":0.918,"ldl_gt950":1.136,
       "htn":0.644,"smoke":0.625,"lpa_ge50":0.434}
print(f"{'term':14s} {'points':>7s} {'local b':>9s} {'pts/b':>7s} {'round(10b)':>11s} {'match':>6s}")
ok = 0
for k in PTS:
    r = PTS[k] / LOC[k]; pred = round(10 * LOC[k]); m = pred == PTS[k]; ok += m
    print(f"{k:14s} {PTS[k]:7d} {LOC[k]:9.3f} {r:7.3f} {pred:11d} {str(m):>6s}")
print(f"\n  round(10*beta) reproduces the published chart point in {ok}/{len(PTS)} terms")
print("  => the local FH-RS beta vector IS the published equation on the beta scale.")
print("  => points and betas are a monotone affine map, so C-index is invariant to")
print("     the choice between them, up to point-rounding ties.")

# ---------------------------------------------------------------- B  SAFEHEART
rule("B. SAFEHEART: Table 3 multivariable HR -> published coefficient -> local")
# Perez de Isla et al, Circulation 2017;135:2133-2144. Table 3 pp2138-2139 (PDF
# pages 6-7); worked examples printing the coefficients are on p2139 (PDF p7).
HR = {"age_30_59":2.92,"age_ge60":4.27,"male":2.01,"prior_ascvd":4.15,
      "htn":1.99,"bmi_ow":2.40,"bmi_ob":2.67,"smoke_active":1.62,
      "ldl_100_159":2.50,"ldl_ge160":4.80,"lpa_gt50":1.52}
EQ = {"age_30_59":1.07,"age_ge60":1.45,"male":0.70,"prior_ascvd":1.42,
      "htn":0.69,"bmi_ow":0.88,"bmi_ob":0.98,"smoke_active":0.48,
      "ldl_100_159":0.92,"ldl_ge160":1.57,"lpa_gt50":0.42}
print(f"{'term':14s} {'HR':>6s} {'ln(HR)':>8s} {'eq coef':>8s} {'|diff|':>7s}")
worst = 0
for k in HR:
    d = abs(math.log(HR[k]) - EQ[k]); worst = max(worst, d)
    print(f"{k:14s} {HR[k]:6.2f} {math.log(HR[k]):8.4f} {EQ[k]:8.2f} {d:7.4f}")
print(f"\n  max |ln(HR) - printed coefficient| = {worst:.4f}  (all 11 agree to 2 dp)")
print("  local 15_CALON_FINAL.py line 278:")
print("    0.045*age(cont) + 0.6*male + 0.4*htn + 0.3*smoke + 0.02*bmi(cont)")
print("    + 0.15*ldl_untreated(mmol/L) + 0.25*lpa>=105nmol/L")
print("  published male/htn/smoke/lpa = 0.70/0.69/0.48/0.42; local = 0.60/0.40/0.30/0.25")
for k, loc in (("male",0.6),("htn",0.4),("smoke_active",0.3),("lpa_gt50",0.25)):
    print(f"    {k:14s} published {EQ[k]:.2f}  local {loc:.2f}  ratio {EQ[k]/loc:.3f}")
print("  the four ratios are 1.167 / 1.725 / 1.600 / 1.680 - not a common rescaling.")

# ---------------------------------------------------------------- C  OBJ-002
rule("C. OBJ-002: exact factorial slope ratios on the attainable SAFEHEART LP")
S0 = {5: 0.9532, 10: 0.9025}; CENTRE = 5.4078
def lp_support(primary_prevention=True):
    v = []
    for male, ageb, htn, smk, bmib, ldlb, lpa in itertools.product(
            (0,1), (0.0,1.07,1.45), (0,1), (0,1), (0.0,0.88,0.98),
            (0.0,0.92,1.57), (0,1)):
        v.append(0.70*male + ageb + 0.69*htn + 1.42*(0 if primary_prevention else 1)
                 + 0.48*smk + bmib + ldlb + 0.42*lpa)
    return np.array(sorted(set(v)))
def logit_p(lp, horizon, centred):
    x = lp - (CENTRE if centred else 0.0)
    p = 1.0 - S0[horizon] ** np.exp(x)
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return np.log(p / (1 - p)), p
LP = lp_support()
print(f"  attainable distinct LP values (primary prevention, prior ASCVD=0): {len(LP)}")
print(f"  LP range {LP.min():.2f} to {LP.max():.2f}\n")
base, _ = logit_p(LP, 5, True)
print(f"{'cell':18s} {'b vs centred-5y':>16s} {'r^2':>9s} {'slope=s/b':>11s} "
      f"{'mean p':>9s} {'max p':>8s}")
for horizon, centred in ((5,True),(10,True),(5,False),(10,False)):
    z, p = logit_p(LP, horizon, centred)
    b, a = np.polyfit(base, z, 1)
    r2 = np.corrcoef(base, z)[0,1] ** 2
    lab = f"h{horizon}_{'centred' if centred else 'uncentred'}"
    print(f"{lab:18s} {b:16.4f} {r2:9.6f} {0.55/b:11.4f} {p.mean():9.4f} {p.max():8.4f}")
print("\n  If logit(p_cell) = a + b*logit(p_ref) exactly, then for ANY outcome vector")
print("  slope_cell = slope_ref / b. Column 4 shows where an observed 0.55 would go.")
print("  Wrong horizon: b=1.003 -> slope moves by 0.3%. CANNOT produce 0.55 from 1.0.")
print("  Uncentred: b~1.96-3.33 -> slope ~0.28-0.53, BUT mean predicted risk becomes")
print("  ~1.0, which any risk-range print would have caught.")

# what a shared receiving-cohort attenuation predicts
print("\n  Shared-attenuation alternative (no bug):")
for k in (1.6, 1.8, 2.0):
    print(f"    if true UKB betas = published/{k:.1f}, every score's slope = {1/k:.3f}")
print("  This is the only mechanism that also applies to Montreal and FH-RS, which")
print("  are POINTS instruments: they have no baseline survival and no centring")
print("  constant, so neither of the two mechanisms named in OBJ-002 exists for them.")

# ---------------------------------------------------------------- D  OBJ-003
rule("D. OBJ-003: can the 0.999 drop rule ever fire on cholesterol-years?")
print("  15_CALON_FINAL.py line 249:  cum_nonhdl = log(untreated non-HDL * age)")
print("                            = log(non-HDL) + log(age)")
print("  Under independence of age and non-HDL, delta method:")
print("      r(age, cum_nonhdl) ~= CV_age / sqrt(CV_age^2 + CV_nonHDL^2)")
print(f"\n{'CV_age':>7s} {'CV_nonHDL':>10s} {'r':>8s}")
for cva in (0.12, 0.142, 0.16):
    for cvc in (0.15, 0.20, 0.26, 0.32):
        print(f"{cva:7.3f} {cvc:10.3f} {cva/math.sqrt(cva**2+cvc**2):8.3f}")
thr = 0.999
need = math.sqrt(1/thr**2 - 1)
print(f"\n  To reach r >= {thr} you need CV_nonHDL <= CV_age * {need:.5f}")
for cva in (0.12, 0.142, 0.16):
    print(f"    CV_age={cva:.3f} -> CV_nonHDL <= {cva*need:.5f}"
          f"  (SD of non-HDL <= {cva*need*4.6:.3f} mmol/L at mean 4.6)")
print("  Assay analytical CV alone is ~2%. The rule is unreachable by 1-2 orders")
print("  of magnitude. r is ~0.4-0.6, not near-deterministic.")

print("\n  Second, independent reason it cannot fire: line 300 reads")
print('      if f.startswith("sp") and abs(corr(age, f)) >= 0.999:')
print("  The guard is NAME-SCOPED to the spline terms. cum_nonhdl is never tested.")

print("\n  The pair the guard does let through: age vs sp50 = max(age-50, 0).")
rng = np.random.default_rng(0)
def r_sp(age):
    sp = np.clip(age - 50, 0, None)
    return float(np.corrcoef(age, sp)[0, 1])
scen = {
  "uniform 40-70": rng.uniform(40, 70, 400000),
  "N(56.5,8) trunc[40,70]": None,
  "N(57,7.5) trunc[40,70]": None,
  "N(60,6) trunc[40,70]": None,
}
for mu, sd, key in ((56.5,8,"N(56.5,8) trunc[40,70]"),(57,7.5,"N(57,7.5) trunc[40,70]"),
                    (60,6,"N(60,6) trunc[40,70]")):
    a = rng.normal(mu, sd, 2000000); a = a[(a >= 40) & (a <= 70)][:400000]
    scen[key] = a
print(f"\n{'age distribution':26s} {'r(age,sp50)':>12s} {'r(age,sp18)':>12s} {'>=0.999?':>9s}")
for k, a in scen.items():
    sp18 = np.clip(a - 18, 0, None)
    print(f"{k:26s} {r_sp(a):12.4f} {float(np.corrcoef(a,sp18)[0,1]):12.4f} "
          f"{str(r_sp(a) >= 0.999):>9s}")
print("\n  sp18/sp30 are exact duplicates of age when min(age) > 30, so the guard")
print("  fires on them (calon_final.json: dropped_collinearity_guard = [sp18, sp30]).")
print("  sp50 survives at r ~ 0.90-0.96. age and sp50 are then both in the UKB spec")
print("  (calon_final.json cohort_spec), so the age coefficient is split across two")
print("  near-collinear terms. That, not cholesterol-years, is what nulls age.")
