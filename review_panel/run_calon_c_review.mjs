#!/usr/bin/env node
// Blind CALON-C manuscript review using the user's existing subscription-authenticated CLIs.
// No API keys are read or added. Each agent reads aggregate manuscript text only.
import { spawn, execSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const ROOT = resolve(process.cwd());
const protocolPath = join(ROOT, 'review_panel', 'CALON_C_REVIEW_PROTOCOL.md');
const outDir = join(ROOT, 'outputs', 'manuscript_2026-08-16', 'multi_agent_review_2026-08-17', 'round-1-independent');
const protocol = readFileSync(protocolPath, 'utf8');
mkdirSync(outDir, { recursive: true });

process.env.PATH = [
  `${process.env.HOME}/.local/bin`,
  `${process.env.HOME}/.hermes/node/bin`,
  `${process.env.HOME}/.grok/bin`,
  `${process.env.HOME}/.kimi-code/bin`,
  process.env.PATH,
].join(':');

// Fail closed if API-key environment variables could divert billing from subscriptions.
for (const key of ['ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','OPENAI_API_KEY','MOONSHOT_API_KEY','KIMI_API_KEY','XAI_API_KEY']) {
  if (process.env[key]) {
    console.error(`FAIL: ${key} is set; refusing to run outside subscription authentication.`);
    process.exit(2);
  }
}

const seats = {
  kimi: {
    provider: 'Moonshot · Kimi subscription OAuth',
    model: 'kimi-code/k3 · max',
    lens: `You are the BIOSTATISTICIAN. Stay focused on study design, estimands, event counts and effective sample size, model specification, internal validation, optimism, discrimination, calibration, competing risk, comparator fairness, paired uncertainty, multiplicity, missing data, family clustering, predictor timing, transport versus external validation, PROBAST and TRIPOD+AI. Audit whether each numerical interpretation is statistically earned.`,
    cmd: 'kimi',
    args: prompt => ['-p', prompt, '-m', 'kimi-code/k3'],
    clean: raw => raw.replace(/\nTo resume this session:.*$/s, '').trim(),
  },
  grok: {
    provider: 'xAI · Grok subscription OAuth',
    model: 'grok-4.6 · xhigh',
    lens: `You are the LIPID-MEDICINE SPECIALIST. Stay focused on LDLR/FH phenotype definition, cumulative atherogenic exposure, non-HDL-C/remnant biology, lipid measurement, treatment correction, statin and non-statin pharmacology, Lp(a), apoB, guideline alignment, biological plausibility, ascertainment route and whether the clinical lipid claims exceed the data.`,
    cmd: 'grok',
    args: prompt => ['-p', prompt, '--model', 'grok-4.6', '--reasoning-effort', 'xhigh', '--output-format', 'json', '--max-turns', '160', '--permission-mode', 'bypassPermissions'],
    clean: raw => {
      const s = raw.trim();
      const i = s.indexOf('{');
      if (i < 0) return s;
      try {
        const j = JSON.parse(s.slice(i));
        return `${(j.text || '').trim()}\n\n<!-- stopReason=${j.stopReason || 'unknown'}; num_turns=${j.num_turns ?? 'unknown'} -->`.trim();
      } catch { return s; }
    },
  },
  claude: {
    provider: 'Anthropic · Claude.ai subscription',
    model: 'Claude Opus · max',
    lens: `You are the CARDIOLOGIST. Stay focused on clinical population, endpoint content and adjudication, first-event relevance, competing mortality, risk horizons, treatment-escalation implications, patient selection, calibration for decisions, decision curves, guideline translation, harms of de-risking FH, practice workflow and the threshold for publication and clinical adoption.`,
    cmd: 'claude',
    args: prompt => ['-p', prompt, '--model', 'opus', '--effort', 'max', '--dangerously-skip-permissions', '--max-turns', '120'],
    clean: raw => raw.trim(),
  },
};

function have(cmd) {
  try { execSync(`command -v ${cmd}`, { shell: '/bin/zsh', stdio: 'ignore' }); return true; }
  catch { return false; }
}

function run(name, seat) {
  return new Promise(resolveRun => {
    const started = new Date().toISOString();
    const prompt = `${seat.lens}\n\n${protocol}\n\nYour panel identity is **${name.toUpperCase()} — ${seat.model}**. Work independently. Read the manuscript from the stated local path now and produce the complete review in Markdown. Do not edit any project file.`;
    writeFileSync(join(outDir, `${name}.prompt.md`), prompt, 'utf8');
    if (!have(seat.cmd)) {
      resolveRun({ name, ok: false, provider: seat.provider, model: seat.model, error: 'CLI not installed', started });
      return;
    }
    console.log(`[${started}] START ${name} · ${seat.provider} · ${seat.model}`);
    const t0 = Date.now();
    const child = spawn(seat.cmd, seat.args(prompt), { cwd: ROOT, env: process.env });
    let stdout = '', stderr = '';
    child.stdout.on('data', d => { stdout += d; });
    child.stderr.on('data', d => { stderr += d; });
    child.stdin.end();
    const killer = setTimeout(() => child.kill('SIGKILL'), 45 * 60 * 1000);
    child.on('close', code => {
      clearTimeout(killer);
      const text = seat.clean(stdout);
      if (stdout) writeFileSync(join(outDir, `${name}.raw.txt`), stdout, 'utf8');
      if (stderr) writeFileSync(join(outDir, `${name}.stderr.log`), stderr, 'utf8');
      if (text) writeFileSync(join(outDir, `${name}.md`), text + '\n', 'utf8');
      const result = {
        name, provider: seat.provider, model: seat.model, started,
        finished: new Date().toISOString(), elapsed_ms: Date.now() - t0,
        code, ok: code === 0 && text.length > 1000, response_chars: text.length,
        error: code === 0 && text.length > 1000 ? '' : (stderr.trim().split('\n').slice(-3).join(' ') || `exit ${code}; ${text.length} chars`),
      };
      writeFileSync(join(outDir, `${name}.result.json`), JSON.stringify(result, null, 2), 'utf8');
      console.log(`[${result.finished}] ${result.ok ? 'OK' : 'FAIL'} ${name} · ${result.response_chars} chars · ${result.elapsed_ms} ms`);
      resolveRun(result);
    });
  });
}

writeFileSync(join(outDir, 'RUN_MANIFEST.json'), JSON.stringify({
  created: new Date().toISOString(),
  manuscript: 'outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md',
  protocol: 'review_panel/CALON_C_REVIEW_PROTOCOL.md',
  evidence_window: ['2016-08-17', '2026-08-17'],
  auth_policy: 'existing subscription OAuth only; fail closed on API-key environment overrides',
  independence: 'blind round 1',
  seats: Object.fromEntries(Object.entries(seats).map(([k,v]) => [k, { provider: v.provider, model: v.model, lens: v.lens }])),
}, null, 2), 'utf8');

const results = await Promise.all(Object.entries(seats).map(([name, seat]) => run(name, seat)));
writeFileSync(join(outDir, 'PANEL_RESULTS.json'), JSON.stringify({ finished: new Date().toISOString(), results }, null, 2), 'utf8');
writeFileSync(join(outDir, 'README.md'), [
  '# CALON-C blind multi-agent review', '',
  ...results.map(r => `- **${r.name}** — ${r.ok ? `complete: [${r.name}.md](./${r.name}.md)` : `FAILED: ${r.error}`}`),
  '', 'See `RUN_MANIFEST.json` for model, lens, evidence-window and authentication provenance.', ''
].join('\n'), 'utf8');
console.log(`PANEL ${results.filter(r => r.ok).length}/${results.length} complete → ${outDir}`);
process.exit(results.every(r => r.ok) ? 0 : 1);
