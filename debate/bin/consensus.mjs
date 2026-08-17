#!/usr/bin/env node
/**
 * consensus.mjs — decides whether a debate step may close.
 *
 * WHY THIS IS CODE AND NOT PROSE
 * A model will type "CONSENSUS REACHED" to end a conversation. The existing
 * delegate skill defines MAX_ROUNDS and a consensus table entirely in markdown
 * and trusts the orchestrator to honour them; neither is a variable anywhere.
 * This programme has already been bitten by exactly that class of failure —
 * two quality checks whose condition was the constant `True` printed PASS for
 * weeks while testing nothing.
 *
 * So closure is computed from the objection register, never asserted:
 *   - an objection is CLOSED only if it is ANSWERED with a named artefact, or
 *     ACCEPTED-RISK with a named dissenter
 *   - anything else is OPEN and the step cannot close
 *   - MAX_ROUNDS is enforced here, and hitting it writes DEADLOCK rather than
 *     allowing a face-saving convergence
 *
 * The orchestrator RUNS this. It does not judge. Exit code is the verdict.
 *
 * Usage:
 *   node consensus.mjs --step 003 [--state ../state] [--max-rounds 4] [--json]
 * Exit codes:
 *   0  CLOSEABLE   every objection resolved
 *   1  OPEN        unresolved objections remain; more rounds needed
 *   2  DEADLOCK    MAX_ROUNDS hit with objections still open
 *   3  MALFORMED   register unparseable or required fields missing
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const opt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
const step = opt('--step', null);
const stateDir = resolve(HERE, opt('--state', '../state'));
const MAX_ROUNDS = parseInt(opt('--max-rounds', '4'), 10);
const asJson = argv.includes('--json');

if (!step) { console.error('consensus.mjs: --step NNN is required'); process.exit(3); }

const REG = join(stateDir, 'open-questions.md');
if (!existsSync(REG)) { console.error(`consensus.mjs: no register at ${REG}`); process.exit(3); }

/* ------------------------------------------------------------------ parsing
 * The register is markdown so a cold model can read it, but each entry is a
 * fenced YAML-ish block so it can also be parsed exactly. Free prose between
 * blocks is ignored, which lets agents argue in the file without breaking it.
 */
const RAW = readFileSync(REG, 'utf8');
const BLOCK = /```objection\s*\n([\s\S]*?)```/g;

const REQUIRED = ['id', 'step', 'raised_by', 'claim', 'settled_by', 'status'];
const VALID_STATUS = ['OPEN', 'ANSWERED', 'ACCEPTED-RISK', 'WITHDRAWN'];

const objections = [];
const malformed = [];
let m;
while ((m = BLOCK.exec(RAW)) !== null) {
  const body = m[1];
  const o = {};
  for (const line of body.split('\n')) {
    const kv = line.match(/^\s*([a-z_]+)\s*:\s*(.*)$/);
    if (kv) o[kv[1]] = kv[2].trim();
  }
  const missing = REQUIRED.filter(k => !o[k]);
  if (missing.length) { malformed.push({ raw: body.slice(0, 80), missing }); continue; }
  if (!VALID_STATUS.includes(o.status)) {
    malformed.push({ id: o.id, missing: [`status must be one of ${VALID_STATUS.join('|')}, got "${o.status}"`] });
    continue;
  }
  objections.push(o);
}

const mine = objections.filter(o => String(o.step) === String(step));

/* ------------------------------------------------- the rules with the teeth */
const problems = [];

for (const o of mine) {
  if (o.status === 'ANSWERED') {
    // An answer is only an answer if it points at something checkable.
    // "we discussed it and agree" is not an artefact.
    if (!o.evidence || o.evidence.length < 4) {
      problems.push(`${o.id}: ANSWERED but no evidence artefact named`);
    } else if (!/[./]|\d/.test(o.evidence)) {
      problems.push(`${o.id}: evidence "${o.evidence}" names no file, path or number`);
    }
  }
  if (o.status === 'ACCEPTED-RISK') {
    // Accepting a risk requires someone's name against it. Anonymous
    // acceptance is how disagreement gets smoothed away.
    if (!o.dissenter || o.dissenter.length < 2) {
      problems.push(`${o.id}: ACCEPTED-RISK but no dissenter named`);
    }
    if (!o.risk_text || o.risk_text.length < 10) {
      problems.push(`${o.id}: ACCEPTED-RISK but the risk is not written out`);
    }
  }
  if (o.status === 'WITHDRAWN' && (!o.withdrawn_because || o.withdrawn_because.length < 10)) {
    problems.push(`${o.id}: WITHDRAWN without a stated reason`);
  }
}

// Self-closure is forbidden: the agent that raised an objection may not be the
// one that answers it. Otherwise a model files a soft objection and immediately
// resolves it, manufacturing the appearance of adversarial review.
for (const o of mine) {
  if (o.status === 'ANSWERED' && o.answered_by && o.answered_by === o.raised_by) {
    problems.push(`${o.id}: answered by the same agent that raised it (${o.raised_by})`);
  }
}

const open = mine.filter(o => o.status === 'OPEN');

// Rounds are counted from turn files on disk, not from anything a model says.
const stepDir = join(stateDir, '..', 'steps', `step-${step}`);
let rounds = 0;
if (existsSync(stepDir)) {
  // Accept both legacy `r1-claude.md` files and directory rounds `r1/`, `r1b/`, `r2/`.
  const entries = readdirSync(stepDir, { withFileTypes: true });
  for (const ent of entries) {
    const m = ent.name.match(/^r(\d+)/);
    if (m) rounds = Math.max(rounds, parseInt(m[1], 10));
  }
}

// A step with no objections at all is not consensus — it is an unexamined step.
// At least two distinct agents must have engaged, or there was no debate.
const agents = new Set(mine.map(o => o.raised_by));
const noDebate = mine.length === 0 || agents.size < 2;

let code, verdict, detail;
if (malformed.length) {
  code = 3; verdict = 'MALFORMED';
  detail = malformed.map(x => `${x.id || x.raw}: ${x.missing.join('; ')}`);
} else if (problems.length) {
  code = 1; verdict = 'OPEN';
  detail = problems;
} else if (noDebate) {
  code = 1; verdict = 'OPEN';
  detail = [`only ${agents.size} agent(s) filed objections on step ${step} ` +
            `(${[...agents].join(', ') || 'none'}); a step nobody challenged has not been debated`];
} else if (open.length) {
  code = rounds >= MAX_ROUNDS ? 2 : 1;
  verdict = code === 2 ? 'DEADLOCK' : 'OPEN';
  detail = open.map(o => `${o.id} [${o.raised_by}] ${o.claim}`);
} else {
  code = 0; verdict = 'CLOSEABLE';
  detail = mine.map(o => `${o.id} ${o.status}` +
    (o.status === 'ACCEPTED-RISK' ? ` (dissent: ${o.dissenter})` : ''));
}

const out = {
  step, verdict, rounds, max_rounds: MAX_ROUNDS,
  objections_total: mine.length,
  by_status: VALID_STATUS.reduce((a, s) => (a[s] = mine.filter(o => o.status === s).length, a), {}),
  agents_engaged: [...agents],
  detail,
};

if (asJson) { console.log(JSON.stringify(out, null, 2)); }
else {
  console.log(`\nSTEP ${step} — ${verdict}   (round ${rounds}/${MAX_ROUNDS})`);
  console.log(`objections: ${mine.length}  ${JSON.stringify(out.by_status)}`);
  console.log(`agents engaged: ${[...agents].join(', ') || 'NONE'}`);
  if (detail.length) { console.log('');
    for (const d of detail) console.log(`  - ${d}`); }
  console.log('');
  if (code === 0) console.log('CLOSEABLE — orchestrator may write the locked decision.');
  if (code === 1) console.log('OPEN — another round is required. Do NOT close this step.');
  if (code === 2) console.log('DEADLOCK — write the open risks into the record. Do NOT fake convergence.');
  if (code === 3) console.log('MALFORMED — fix the register before anything else.');
}
process.exit(code);
