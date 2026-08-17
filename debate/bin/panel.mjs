#!/usr/bin/env node
// panel-relay.mjs — fan one prompt out to available AI CLIs in parallel, capture each response.
// No dependencies (Node built-ins only). Shells out only to the model CLIs. Makes no network
// calls of its own and reads/writes no credentials — each CLI authenticates exactly as it does
// when you run it yourself. Read this file before running it.
import { spawn, execSync } from 'node:child_process';
import { writeFileSync, mkdirSync, readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : d; };
let prompt = opt('--prompt', '');
if (!prompt && opt('--prompt-file')) prompt = readFileSync(opt('--prompt-file'), 'utf8');
if (!prompt) { console.error('Usage: panel-relay.mjs --prompt "<text>" [--out DIR] [--panel auto|codex,claude,kimi,gemini] [--timeout MS]'); process.exit(2); }

// Inject full Julius Spec-kit dump into EVERY agent prompt when present.
const DEBATE_ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const JULIUS_DIR = join(DEBATE_ROOT, 'evidence', 'julius-spec-kit');
function juliusBlock() {
  if (!existsSync(JULIUS_DIR)) return '';
  const files = [
    'FOR_ALL_AGENTS.md',
    'CALON_G_BIOSTAT_PROTOCOL.md',
    'CYCLE2_RESTART.md',
    'spec_kit_execution_report.md',
    'spec_kit_execution_status.csv',
    'spec_kit_confirmatory_tally.csv',
    'calon_settlement_out/spec_frozen.json',
    'calon_settlement_out/obj002_factorial.json',
    'calon_settlement_out/obj003_collinearity.json',
    'calon_settlement_out/comparator_provenance.csv',
    'calon_settlement_out/obj001_rescore.csv',
    'calon_settlement_out/headtohead_full.csv',
    'cycle2_r_pilot/calong_run_meta.json',
    'cycle2_r_pilot/calong_headtohead_full.csv',
    'cycle2_r_pilot/comparator_patient_set_audit.csv',
  ];
  const parts = [
    '\n\n--- JULIUS SPEC-KIT OUTPUTS (FULL DUMP — ALL AGENTS MUST USE THESE NUMBERS) ---',
    `Directory: ${JULIUS_DIR}`,
    'Quote from these artefacts. Do not invent Julius results. Horizon cells using',
    '`(time <= H) | (event == 1)` are withdrawn per the execution report.',
  ];
  for (const rel of files) {
    const p = join(JULIUS_DIR, rel);
    if (!existsSync(p)) continue;
    const body = readFileSync(p, 'utf8');
    // Keep head-to-head full but cap absurdly large future dumps.
    const clipped = body.length > 120_000 ? body.slice(0, 120_000) + '\n…[truncated]…\n' : body;
    parts.push(`\n### FILE: ${rel}\n\`\`\`\n${clipped}\n\`\`\`\n`);
  }
  return parts.join('\n');
}

const FORMAT_REQUIREMENT = `

--- OUTPUT FORMAT (MANDATORY — human-readable) ---
Reply in Markdown only. Start with: # Step NNN · Round R · <your-name>
Use H2 headings exactly:
## 1. Methodology
## 2. Implementation
## 3. Adversarial audit
## 4. Clinical and publication reality
Use GitHub-flavoured tables. Put code in fenced blocks with a language tag
(python, bash, r, json). Put each objection in a \`\`\`objection fence.
End with ## Artefacts listing proposed scripts/paths. Do not write plain
prose dumps without headings. The orchestrator saves your reply as .md.
`;
prompt = `${prompt.trim()}\n${juliusBlock()}\n${FORMAT_REQUIREMENT}`;
const outDir = opt('--out', `/tmp/delegate-${Date.now()}`);
const timeout = parseInt(opt('--timeout', '300000'), 10);
const panelArg = opt('--panel', 'auto');
mkdirSync(outDir, { recursive: true });

// Highest reasoning tier available on each subscription (verified 2026-08-15):
//   Claude  → opus + effort max
//   Codex   → gpt-5.6-sol + reasoning ultra (matches ~/.codex/config.toml)
//   Kimi    → kimi-code/k3 (supports effort max; default_effort=max in config)
//   Grok    → grok-4.6 + reasoning-effort xhigh
const SPEC = {
  // closeStdin:true for every CLI — leaving stdin open hangs Claude/Kimi on
  // "no stdin data received" and can stall Codex waiting for pipe input.
  codex: {
    provider: 'OpenAI · Codex · gpt-5.6-sol/ultra',
    cmd: 'codex',
    args: p => ['exec', '--skip-git-repo-check', '-m', 'gpt-5.6-sol', '-c', 'model_reasoning_effort="ultra"', p],
    closeStdin: true,
  },
  // --tools '' currently trips a bad MCP tool schema (400). Skip-permissions
  // print mode works with opus/max; agents must reason from the prompt only.
  claude: {
    provider: 'Anthropic · Claude · opus/max',
    cmd: 'claude',
    args: p => ['-p', p, '--model', 'opus', '--effort', 'max', '--dangerously-skip-permissions'],
    closeStdin: true,
  },
  kimi: {
    provider: 'Moonshot · Kimi · k3/max',
    cmd: 'kimi',
    args: p => ['-p', p, '-m', 'kimi-code/k3'],
    closeStdin: true,
  },
  gemini: { provider: 'Google · Gemini', cmd: 'gemini', args: p => ['-p', p], closeStdin: true },
  // Grok's `plain` headless format prints only its inter-tool narration and
  // drops the final message, so a full turn arrived as a ~1 KB preamble three
  // times. `--output-format json` returns {text, stopReason, num_turns};
  // clean() below extracts .text. Without bypassPermissions the turn dies as
  // stopReason=Cancelled on its first tool call, which looked like a weak
  // answer rather than a blocked one.
  grok: {
    provider: 'xAI · Grok · 4.6/xhigh',
    cmd: 'grok',
    args: p => ['-p', p, '--model', 'grok-4.6', '--reasoning-effort', 'xhigh',
                '--output-format', 'json', '--max-turns', '120',
                '--permission-mode', 'bypassPermissions'],
    closeStdin: true,
    json: true,
  },
};
// PATH is load-bearing: `gemini` exists ONLY in ~/.hermes/node/bin and `kimi` may
// too. Without this prefix `command -v` fails and the panel silently shrinks by a
// model with no error - a silent 5->4 degradation is exactly the failure this
// whole workflow exists to prevent.
process.env.PATH = [
  `${process.env.HOME}/.local/bin`,
  `${process.env.HOME}/.hermes/node/bin`,
  `${process.env.HOME}/.grok/bin`,
  `${process.env.HOME}/.kimi-code/bin`,
  process.env.PATH,
].join(':');

const have = cmd => { try { execSync(`command -v ${cmd}`, { stdio: 'ignore', shell: '/bin/zsh' }); return true; } catch { return false; } };

let names = panelArg === 'auto' ? Object.keys(SPEC) : panelArg.split(',').map(s => s.trim());
names = names.filter(n => SPEC[n]);

function clean(name, raw) {
  let s = (raw || '').trim();
  if (name === 'kimi') s = s.replace(/\nTo resume this session:.*$/s, '').trim();
  if (SPEC[name]?.json && s) {
    // The CLI may print log lines before the JSON object; take the last {...}.
    const start = s.indexOf('{');
    if (start >= 0) {
      try {
        const parsed = JSON.parse(s.slice(start));
        const text = (parsed.text || '').trim();
        if (text) {
          const stop = parsed.stopReason || 'unknown';
          s = stop === 'EndTurn'
            ? text
            : `${text}\n\n<!-- panel: stopReason=${stop} num_turns=${parsed.num_turns} — turn may be incomplete -->`;
        }
      } catch { /* leave raw so the failure is visible rather than silent */ }
    }
  }
  return s;
}
function asMarkdown(name, body, ok) {
  const text = ok ? (body || '') : `[UNAVAILABLE] ${body || 'no output'}`;
  const needsWrap = ok && !/^#\s/m.test(text);
  if (!needsWrap) return text.endsWith('\n') ? text : text + '\n';
  return [
    `---`,
    `agent: ${name}`,
    `status: auto-wrapped`,
    `---`,
    ``,
    `# Panel turn · ${name}`,
    ``,
    text.trim(),
    ``,
  ].join('\n');
}

function persistOne(r) {
  const payload = r.ok ? r.response : r.error;
  writeFileSync(`${outDir}/${r.name}.txt`, r.ok ? r.response : `[UNAVAILABLE] ${r.error}`, 'utf8');
  writeFileSync(`${outDir}/${r.name}.md`, asMarkdown(r.name, payload, r.ok), 'utf8');
  const line = `${r.ok ? 'OK  ' : 'FAIL'} ${r.name.padEnd(7)} ${r.provider.padEnd(28)} ${r.ms}ms ${r.ok ? `· ${r.response.length} chars` : `· ${r.error}`}\n`;
  writeFileSync(`${outDir}/progress.log`, line, { flag: 'a' });
  console.log(`  [${new Date().toISOString()}] ${line.trim()}`);
}

function run(name) {
  return new Promise(res => {
    const s = SPEC[name];
    if (!have(s.cmd)) {
      const r = { name, provider: s.provider, ok: false, ms: 0, error: 'CLI not installed', response: '' };
      persistOne(r);
      return res(r);
    }
    const t0 = Date.now();
    console.log(`  [${new Date().toISOString()}] START ${name} (${s.provider})`);
    const child = spawn(s.cmd, s.args(prompt), { env: process.env });
    let out = '', err = '';
    child.stdout.on('data', d => (out += d));
    child.stderr.on('data', d => (err += d));
    if (s.closeStdin) child.stdin.end();
    const killer = setTimeout(() => child.kill('SIGKILL'), timeout);
    child.on('close', code => {
      clearTimeout(killer);
      const ms = Date.now() - t0;
      const resp = clean(name, out);
      // The auth heuristic scans stderr, which for `codex exec` contains the
      // echoed transcript - so an agent merely WRITING "forbidden" or
      // "unauthorised" flagged its own good turn as an auth failure and a
      // 7,421-character answer was overwritten with "[UNAVAILABLE]". A
      // heuristic must never outvote a real response: only consult it when
      // there is nothing on stdout to keep.
      const authErr = resp.length === 0 &&
        /IneligibleTierError|not logged in|unauthor|forbidden|api key|usage limit|quota/i.test(err);
      const ok = code === 0 && resp.length > 0;
      const r = {
        name, provider: s.provider, ok, code, ms, response: resp,
        error: ok ? '' : (authErr ? err.trim().split('\n').filter(Boolean).slice(-1)[0] : (err.trim().split('\n').filter(Boolean).slice(-2).join(' ') || `exit ${code}, no output`)),
      };
      // Keep the raw streams whatever the verdict, so a misjudged turn can be
      // recovered instead of being lost to an overwrite.
      if (err.trim()) writeFileSync(`${outDir}/${name}.stderr.log`, err, 'utf8');
      if (!ok && out.trim()) writeFileSync(`${outDir}/${name}.raw-stdout.log`, out, 'utf8');
      persistOne(r);
      res(r);
    });
  });
}

writeFileSync(`${outDir}/progress.log`, `PANEL START ${new Date().toISOString()} names=${names.join(',')}\n`, 'utf8');
const results = await Promise.all(names.map(run));
writeFileSync(`${outDir}/panel.json`, JSON.stringify({
  outDir,
  model_pin: {
    claude: 'opus/max',
    codex: 'gpt-5.6-sol/ultra',
    kimi: 'kimi-code/k3',
    grok: 'grok-4.6/xhigh',
  },
  prompt_chars: prompt.length,
  results: results.map(({ response, ...meta }) => ({ ...meta, response_chars: (response || '').length })),
}, null, 2), 'utf8');
writeFileSync(`${outDir}/README.md`, [
  `# Panel output — ${outDir}`,
  ``,
  `Open the \`.md\` files for human reading. \`.txt\` is the raw CLI capture.`,
  `Each agent is written as soon as it finishes (see \`progress.log\`).`,
  ``,
  ...results.map(r => `- **${r.name}**: ${r.ok ? `[${r.name}.md](./${r.name}.md)` : `UNAVAILABLE — ${r.error}`}`),
  ``,
].join('\n'), 'utf8');
console.log(`PANEL (${results.filter(r=>r.ok).length}/${results.length} responded) → ${outDir}`);
for (const r of results) console.log(`  ${r.ok ? 'OK  ' : 'FAIL'} ${r.name.padEnd(7)} ${r.provider.padEnd(28)} ${r.ms}ms ${r.ok ? `· ${r.response.length} chars` : `· ${r.error}`}`);
console.log(`\nHuman Markdown: ${outDir}/<name>.md   |   raw: ${outDir}/<name>.txt   |   progress: ${outDir}/progress.log`);
