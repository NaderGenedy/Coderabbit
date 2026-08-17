#!/usr/bin/env Rscript
## =====================================================================
## 16_CALON_G_CYCLE2.R — repo entry point for the CALON-G Cycle-2 R track
## =====================================================================
## Governance: UK Biobank Application 1002450. AGGREGATES ONLY.
## Never write or print eid / NHS number / DOB / FamilyNumber / LSOA.
##
## Locked protocol:
##   ~/Downloads/CALON_DATA_PACKAGE_2026-08-13/debate-teach/CALON_G_BIOSTAT_PROTOCOL.md
## Paste cells (the actual implementation):
##   ~/Downloads/CALON_DATA_PACKAGE_2026-08-13/debate-teach/julius-cycle2-pack-R/
## Python twin (Codex), same SPEC and gates:
##   ~/Downloads/CALON_DATA_PACKAGE_2026-08-13/debate-teach/julius-cycle2-pack/
##
## This file is a THIN ORCHESTRATOR. It holds no statistics of its own: it
## preflights the session, then sources cells 00-06 in order into the global
## environment, exactly as they would be pasted into Julius. Keeping the
## science in the paste cells is deliberate — the artefact the collaborators
## run and the artefact in the repo must be the same bytes.
##
## USAGE
##   FROZEN <- <your frozen UKB risk set>      # permitted ASCVD, I50 excluded
##   wales  <- <All-Wales genotype-confirmed>  # optional
##   source("code/r_cycle2/16_CALON_G_CYCLE2.R")
##   res <- calon_g_cycle2(FROZEN, wales)
##
## This file deliberately does NOT read participant CSVs. Building FROZEN is
## the cohort builder's job (see julius-cycle2-pack-R/15_build_frozen_ukb.R on
## the Mac, or code/15_CALON_FINAL.py). Keeping the fit separate from the build
## is what lets the same cells run on Julius, where the data is already loaded.
##
## SPEC (frozen — do not edit here; edit the protocol and re-freeze)
##   primary     : age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl,
##                 log_tghdl, log_lpa
##   sensitivity : cum_nonhdl -> log_apob_hdl        (the only one)
## =====================================================================

CALON_G_PACK_DIR_DEFAULT <- file.path(
  path.expand("~"), "Downloads", "CALON_DATA_PACKAGE_2026-08-13",
  "debate-teach", "julius-cycle2-pack-R"
)

CALON_G_CELLS <- c(
  "00_findings_lock",
  "01_horizon_prove",
  "02_calong_fit",
  "03_comparators_pdf_faithful",
  "04_headtohead_tripod",
  "05_wales_transport",
  "06_calibration_dca"
)

CALON_G_REQUIRED_COLS <- c(
  "age", "male", "dm", "smoke_curr", "cum_nonhdl", "time_years", "event"
)
CALON_G_ONE_OF <- list(
  hypertension = c("bpmed", "bp_med", "antihypertensive", "htn_med", "htn_any"),
  tg_hdl_axis  = c("log_tghdl", "tg", "trig", "triglycerides"),
  lipoprotein_a= c("log_lpa", "lpa_nmol", "Lpa_nmol", "lpa")
)
CALON_G_OPTIONAL <- c(
  log_apob_hdl = "CALON-G-grey sensitivity",
  hdl          = "FH-Risk-Score and Montreal-FH-SCORE",
  ldl          = "SAFEHEART-RE (measured LDL-C, per Circulation 2017 Table 3)",
  ldl_unt      = "FH-Risk-Score (untreated LDL-C, per ATVB 2021 Data Supplement p.9)",
  bmi          = "SAFEHEART-RE (without it that score is NOT_EVALUABLE for all)",
  smoke_ever   = "Montreal-FH-SCORE (prior OR current smoking)",
  lpa_mgdl     = "removes the CANDIDATE nmol/L -> mg/dL conversion entirely",
  family_id    = "family-clustered CV and cluster-robust bootstrap",
  eid          = "cohort digest only -- never printed"
)

## ---------------------------------------------------------------------
## Locate the pack. Order: explicit argument, CALON_G_PACK_DIR, a `cells/`
## directory beside this file (for a self-contained repo checkout), then the
## Downloads default. A directory only counts if cell 00 is actually in it.
calon_g_pack_dir <- function(pack_dir = NULL) {
  cand <- c(pack_dir,
            Sys.getenv("CALON_G_PACK_DIR", unset = ""),
            file.path("code", "r_cycle2", "cells"),
            "cells",
            CALON_G_PACK_DIR_DEFAULT)
  cand <- unique(cand[!is.na(cand) & nzchar(cand)])
  for (d in cand) {
    if (dir.exists(d) && length(list.files(d, pattern = "^00_.*\\.R$"))) return(normalizePath(d))
  }
  stop(sprintf("cannot locate the CALON-G R pack (no 00_*.R found). Looked in:\n  %s\nSet CALON_G_PACK_DIR or pass pack_dir=",
               paste(cand, collapse = "\n  ")))
}

## ---------------------------------------------------------------------
calon_g_preflight <- function(FROZEN, wales = NULL, verbose = TRUE) {
  problems <- character(0); notes <- character(0)

  need <- c("survival", "jsonlite")
  want <- c("glmnet", "digest", "rms")
  miss_need <- need[!vapply(need, requireNamespace, logical(1), quietly = TRUE)]
  miss_want <- want[!vapply(want, requireNamespace, logical(1), quietly = TRUE)]
  if (length(miss_need))
    problems <- c(problems, sprintf("required packages missing: %s -- install.packages(c(%s))",
                                    paste(miss_need, collapse = ", "),
                                    paste(sprintf('"%s"', miss_need), collapse = ", ")))
  if (length(miss_want))
    notes <- c(notes, sprintf("optional packages missing: %s (glmnet -> ridge falls back to coxph(ridge()); digest -> SHA gate UNVERIFIED)",
                              paste(miss_want, collapse = ", ")))

  if (!is.data.frame(FROZEN)) {
    problems <- c(problems, "FROZEN is not a data frame")
  } else {
    absent <- setdiff(CALON_G_REQUIRED_COLS, names(FROZEN))
    if (length(absent))
      problems <- c(problems, sprintf("FROZEN missing required column(s): %s", paste(absent, collapse = ", ")))
    for (grp in names(CALON_G_ONE_OF)) {
      if (!any(CALON_G_ONE_OF[[grp]] %in% names(FROZEN)))
        problems <- c(problems, sprintf("FROZEN has none of the %s columns: %s",
                                        grp, paste(CALON_G_ONE_OF[[grp]], collapse = " / ")))
    }
    for (o in names(CALON_G_OPTIONAL)) {
      if (!o %in% names(FROZEN))
        notes <- c(notes, sprintf("optional column '%s' absent -- affects: %s", o, CALON_G_OPTIONAL[[o]]))
    }
    if (all(c("time_years", "event") %in% names(FROZEN))) {
      ev <- as.integer(FROZEN$event)
      notes <- c(notes, sprintf("FROZEN: n=%d, events=%d, 5y events (correct truncation)=%d",
                                nrow(FROZEN), sum(ev == 1L, na.rm = TRUE),
                                sum(ev == 1L & as.numeric(FROZEN$time_years) <= 5, na.rm = TRUE)))
    }
  }
  if (!is.null(wales) && !is.data.frame(wales))
    problems <- c(problems, "`wales` supplied but is not a data frame")

  if (verbose) {
    cat("\n=== CALON-G CYCLE-2 PREFLIGHT ===\n")
    if (length(notes))    for (n in notes)    cat("  [note ] ", n, "\n", sep = "")
    if (length(problems)) for (p in problems) cat("  [BLOCK] ", p, "\n", sep = "")
    if (!length(problems)) cat("  ready\n")
  }
  invisible(list(ok = !length(problems), problems = problems, notes = notes))
}

## ---------------------------------------------------------------------
## Run cells 00-06 in order. Sourced into globalenv so the cells behave
## exactly as pasted -- each one reads objects the previous ones defined.
## ---------------------------------------------------------------------
calon_g_cycle2 <- function(FROZEN, wales = NULL, cells = CALON_G_CELLS,
                           pack_dir = NULL, stop_on_error = TRUE) {
  dir <- calon_g_pack_dir(pack_dir)
  pf <- calon_g_preflight(FROZEN, wales)
  if (!pf$ok && stop_on_error)
    stop("preflight blocked -- fix the items above before fitting")

  assign("FROZEN", FROZEN, envir = globalenv())
  if (!is.null(wales)) assign("wales", wales, envir = globalenv())

  cat(sprintf("\n=== CALON-G CYCLE-2 (R) -- pack: %s ===\n", dir))
  ran <- character(0)
  for (cell in cells) {
    f <- list.files(dir, pattern = sprintf("^%s\\.R$", cell), full.names = TRUE)
    if (!length(f)) {
      msg <- sprintf("cell not found: %s.R in %s", cell, dir)
      if (stop_on_error) stop(msg) else { warning(msg); next }
    }
    cat(sprintf("\n---------- %s ----------\n", cell))
    res <- try(source(f[1], local = FALSE, echo = FALSE), silent = TRUE)
    if (inherits(res, "try-error")) {
      cat(sprintf("[FAILED] %s: %s\n", cell, conditionMessage(attr(res, "condition"))))
      if (stop_on_error) stop(sprintf("cell %s failed -- stopping (fail-loud by design)", cell))
    } else {
      ran <- c(ran, cell)
    }
  }

  gates <- if (exists("gate_table", envir = globalenv())) get("gate_table", envir = globalenv())() else NULL
  verdict <- if (is.null(gates) || !nrow(gates)) "NO GATES RECORDED"
             else if (all(gates$status == "PASS")) "CONFIRMATORY-ELIGIBLE"
             else "EXPLORATORY ONLY"
  cat(sprintf("\n=== CALON-G CYCLE-2 COMPLETE -- %d/%d cells -- %s ===\n",
              length(ran), length(cells), verdict))
  invisible(list(cells_run = ran, gates = gates, verdict = verdict, pack_dir = dir))
}

## ---------------------------------------------------------------------
## Cross-track reconciliation. Two implementations against one lock are
## only worth the cost if somebody actually diffs them.
## ---------------------------------------------------------------------
calon_g_compare_tracks <- function(r_csv, py_csv, tol = 0.01) {
  if (!file.exists(r_csv) || !file.exists(py_csv))
    stop("both head-to-head CSVs must exist to reconcile the R and Python tracks")
  R  <- utils::read.csv(r_csv,  stringsAsFactors = FALSE)
  PY <- utils::read.csv(py_csv, stringsAsFactors = FALSE)
  key <- c("comparator", "subgroup", "horizon")
  m <- merge(R, PY, by = key, suffixes = c("_R", "_PY"))
  m$delta_gap    <- round(abs(m$delta_R - m$delta_PY), 4)
  m$verdict_same <- m$verdict_R == m$verdict_PY
  out <- m[, c(key, "delta_R", "delta_PY", "delta_gap", "verdict_R", "verdict_PY", "verdict_same")]
  out <- out[order(-out$delta_gap), ]
  cat(sprintf("\n=== R vs PYTHON RECONCILIATION (%d matched cells) ===\n", nrow(out)))
  cat(sprintf("verdicts agreeing : %d/%d\n", sum(out$verdict_same), nrow(out)))
  cat(sprintf("max |delta gap|   : %.4f (tolerance %.4f)\n", max(out$delta_gap, na.rm = TRUE), tol))
  disagree <- out[!out$verdict_same | out$delta_gap > tol, ]
  if (nrow(disagree)) {
    cat("\ncells to reconcile BEFORE reporting:\n"); print(head(disagree, 25), row.names = FALSE)
  } else {
    cat("\ntracks agree within tolerance on every matched cell.\n")
  }
  invisible(out)
}

if (!interactive() && identical(environment(), globalenv())) {
  cat(paste(
    "16_CALON_G_CYCLE2.R loaded.\n",
    "  calon_g_preflight(FROZEN)            check the session\n",
    "  calon_g_cycle2(FROZEN, wales)        run cells 00-06\n",
    "  calon_g_compare_tracks(r_csv, py_csv) reconcile against the Python twin\n",
    "This file loads no participant data. Build FROZEN first.\n", sep = ""))
}
