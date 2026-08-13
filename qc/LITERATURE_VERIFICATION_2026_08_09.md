# CALON-N literature verification log — 9 August 2026

Scope: targeted, non-systematic verification of comparator metadata, closest cross-sectional FH validations, apoB/apoA1 background, and the novelty boundary. This log does not constitute a systematic review.

## Connectors used

| Source | Query role | Result |
|---|---|---|
| Consensus | FH apoB/LDL discordance and risk prediction | Located the prior Genedy–Zouwail cohort report and FH-Risk-Score; full Consensus records fetched before use. |
| scite | DOI-level metadata, citation context, correction flags | Verified Montreal derivation/validation, FH-Risk-Score, SAFEHEART, Australian validation, and prior CALON discordance article; detected the published correction DOI for the latter. |
| SciSpace | Broad semantic search for FH models using direct apoB, apoB/LDL or apoA1 | Returned general apoB prediction and apoB/apoA1 studies plus genotype-first FH cohorts, but no clearly matching reciprocal clinic–biobank FH model. |
| Sider Scholar | OpenAlex-based broad scholarly search | Recovered background lipid/FH literature; the simple query had low specificity and was used only as a recall check. |
| NCBI Entrez/PubMed | Exact DOI/PMID metadata | Verified the Australian validation, Montreal refinement, and prior discordance report records. |
| Scholar Gateway | Semantic novelty search | Failed twice with an internal MCP error; no evidence from this connector was used. |
| Elicit | Semantic paper search | API access was denied by the connected account plan; no Elicit evidence was used. |

## DOI/metadata checks incorporated

- Montreal derivation: `10.1016/j.jacl.2016.10.004`.
- Montreal validation/refinement: `10.1016/j.jacl.2017.07.008`.
- FH-Risk-Score: `10.1161/ATVBAHA.121.316106`; abstract confirms 3,881 adults and 32,361 person-years.
- SAFEHEART-RE: `10.1161/CIRCULATIONAHA.116.024541`.
- Australian cross-sectional validation: `10.1016/j.cjca.2025.07.042`; PubMed PMID 40850469.
- Prior Genedy–Zouwail discordance study: `10.1016/j.jacl.2025.11.008`; PubMed PMID 41617625.
- Correction to prior study: `10.1016/j.jacl.2026.03.024`.
- AMORIS apoB/apoA1 cohort: `10.1371/journal.pmed.1003853`.

## Novelty conclusion

The search supports only an incremental methodological claim. ApoB particle biology, apoB/LDL discordance, apoA1 associations, and FH risk scores are established. The same DRAGON cohort has already contributed to a hypothesis-generating apoB/LDL report. Across the retrieved sources, no clearly matching FH-specific model was found that was built de novo from raw apoB/LDL and apoA1 measurements and evaluated by reciprocal transport between a specialist clinic and a population biobank. Because the search was targeted rather than systematic—and two requested connectors were unavailable—the manuscript uses “we found no” and avoids “first ever”.
