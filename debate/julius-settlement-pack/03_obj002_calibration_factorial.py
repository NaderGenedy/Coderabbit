# Julius Cell 3 — OBJ-002 calibration factorial (one comparator, four variants)
# Variants: centred/uncentred × S0(5y)/S0(10y). Report slope + CITL only (aggregates).

from __future__ import annotations
import statsmodels.api as sm

S0 = {5: 0.9532, 10: 0.9025}
CENTRE = 5.4078  # Spec Kit SAFEHEART centre — confirm against PDF on disk before trusting


def safeheart_risk(lp: float, horizon: int, centre: float | None) -> float:
    s0 = S0[horizon]
    x = lp - (centre if centre is not None else 0.0)
    return 1.0 - (s0 ** math.exp(x))


def calib_slope(y_event: np.ndarray, p: np.ndarray) -> dict:
    # logistic calibration: logit(p) as sole covariate
    p = np.clip(p, 1e-6, 1 - 1e-6)
    logit = np.log(p / (1 - p))
    X = sm.add_constant(logit)
    fit = sm.Logit(y_event, X).fit(disp=False)
    return {
        "citl": float(fit.params[0]),
        "slope": float(fit.params[1]),
        "n": int(len(y_event)),
        "events": int(y_event.sum()),
        "p_min": float(p.min()),
        "p_max": float(p.max()),
        "p_mean": float(p.mean()),
    }


# Reuse `cc` with `lp_spec` and a binary event at a FIXED horizon for this diagnostic.
# For 5y/10y event indicators, define on Julius from time_years / event.
results = {}
for horizon in (5, 10):
    y = ((cc["event"] == 1) & (cc["time_years"] <= horizon)).astype(int).to_numpy()
    # people censored before horizon without event are 0; exclude unknown follow-up < horizon if you require complete follow-up
    for label, centre in (("centred", CENTRE), ("uncentred", None)):
        p = np.array([safeheart_risk(lp, horizon, centre) for lp in cc["lp_spec"].to_numpy()])
        results[f"h{horizon}_{label}"] = calib_slope(y, p)

AggregateReport(
    script="03_obj002_calibration_factorial",
    notes=[
        "OBJ-002 predicts slopes ~0.52-0.57 under a shared bug",
        "If uncentred or alternate S0 moves slope toward 1.0, mechanism is identified",
        "Confirm CENTRE and S0 against Pérez de Isla PDF before publication use",
    ],
    metrics=results,
).show()
