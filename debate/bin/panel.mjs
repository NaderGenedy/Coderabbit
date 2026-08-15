#!/usr/bin/env node
// panel-relay.mjs — fan one prompt out to available AI CLIs in parallel, capture each response.
// No dependencies (Node built-ins only). Shells out only to the model CLIs. Makes no network
// calls of its own and reads/writes no credentials — each CLI authenticates exactly as it does
// when you run it yourself. Read this file before running it.
import { spawn, execSync } from 'node:child_process';
import { writeFileSync, mkdirSync, readFileSync } from 'node:fs';

const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : d; };
let prompt = opt('--prompt', '');
if (!prompt && opt('--prompt-file')) prompt = readFileSync(opt('--prompt-file'), 'utf8');
if (!prompt) { console.error('Usage: panel-relay.mjs --prompt "<text>" [--out DIR] [--panel auto|codex,claude,kimi,gemini] [--timeout MS]'); process.exit(2); }
const outDir = opt('--out', `/tmp/delegate-${Date.now()}`);
const timeout = parseInt(opt('--timeout', '300000'), 10);
const panelArg = opt('--panel', 'auto');
mkdirSync(outDir, { recursive: true });

const SPEC = {
  // closeStdin:true for every CLI — leaving stdin open hangs Claude/Kimi on
  // "no stdin data received" and can stall Codex waiting for pipe input.
  codex:  { provider: 'OpenAI · Codex',     cmd: 'codex',  args: p => ['exec', '--skip-git-repo-check', p], closeStdin: true },
  claude: { provider: 'Anthropic · Claude',  cmd: 'claude', args: p => ['-p', p, '--tools', ''], closeStdin: true },
  kimi:   { provider: 'Moonshot · Kimi K3',  cmd: 'kimi',   args: p => ['-p', p], closeStdin: true },
  gemini: { provider: 'Google · Gemini',     cmd: 'gemini', args: p => ['-p', p], closeStdin: true },
  // Verified 2026-08-15: `grok --help` shows `-p, --single <PROMPT>` for headless.
  grok:   { provider: 'xAI · Grok',          cmd: 'grok',   args: p => ['-p', p], closeStdin: true },
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
  return s;
}
function run(name) {
  return new Promise(res => {
    const s = SPEC[name];
    if (!have(s.cmd)) return res({ name, provider: s.provider, ok: false, ms: 0, error: 'CLI not installed', response: '' });
    const t0 = Date.now();
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
      const authErr = /IneligibleTierError|not logged in|unauthor|forbidden|api key/i.test(err);
      const ok = code === 0 && resp.length > 0 && !authErr;
      res({ name, provider: s.provider, ok, code, ms, response: resp,
            error: ok ? '' : (authErr ? err.trim().split('\n').filter(Boolean).slice(-1)[0] : (err.trim().split('\n').filter(Boolean).slice(-2).join(' ') || `exit ${code}, no output`)) });
    });
  });
}

const results = await Promise.all(names.map(run));
for (const r of results) writeFileSync(`${outDir}/${r.name}.txt`, r.ok ? r.response : `[UNAVAILABLE] ${r.error}`, 'utf8');
writeFileSync(`${outDir}/panel.json`, JSON.stringify({ prompt, outDir, results }, null, 2), 'utf8');
console.log(`PANEL (${results.filter(r=>r.ok).length}/${results.length} responded) → ${outDir}`);
for (const r of results) console.log(`  ${r.ok ? 'OK  ' : 'FAIL'} ${r.name.padEnd(7)} ${r.provider.padEnd(20)} ${r.ms}ms ${r.ok ? `· ${r.response.length} chars` : `· ${r.error}`}`);
console.log(`\nPer-model text: ${outDir}/<name>.txt   |   structured: ${outDir}/panel.json`);
