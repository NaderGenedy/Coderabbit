#!/usr/bin/env node
/**
 * subscription-preflight.mjs — Gate 0 before any panel dispatch.
 * Fail closed if Claude / Codex / Kimi / Grok are not on subscription auth,
 * or if API-key env vars would divert billing off those subscriptions.
 */
import { spawnSync, execSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '..');
const skipSmoke = process.argv.includes('--skip-smoke');

process.env.PATH = [
  `${process.env.HOME}/.local/bin`,
  `${process.env.HOME}/.hermes/node/bin`,
  `${process.env.HOME}/.grok/bin`,
  `${process.env.HOME}/.kimi-code/bin`,
  process.env.PATH,
].join(':');

const BAD_ENV = [
  'ANTHROPIC_API_KEY',
  'ANTHROPIC_AUTH_TOKEN',
  'OPENAI_API_KEY',
  'MOONSHOT_API_KEY',
  'KIMI_API_KEY',
  'XAI_API_KEY',
];

function fail(msg) {
  console.error(`FAIL: ${msg}`);
  process.exit(1);
}

function ok(msg) {
  console.log(`OK: ${msg}`);
}

for (const k of BAD_ENV) {
  if (process.env[k]) fail(`${k} is set — unset it so the CLI uses subscription auth`);
}
ok('no API-key env overrides');

const claude = spawnSync('claude', ['auth', 'status'], { encoding: 'utf8' });
if (claude.status !== 0 || !/"authMethod":\s*"claude.ai"/.test((claude.stdout || '') + (claude.stderr || ''))) {
  fail('claude is not on claude.ai subscription auth');
}
ok('claude · claude.ai subscription');

const codex = spawnSync('codex', ['login', 'status'], { encoding: 'utf8' });
const codexOut = (codex.stdout || '') + (codex.stderr || '');
if (!/ChatGPT/i.test(codexOut)) fail('codex is not logged in with ChatGPT');
ok('codex · ChatGPT');

const kimi = spawnSync('kimi', ['provider', 'list'], { encoding: 'utf8' });
if (!/source=oauth/.test((kimi.stdout || '') + (kimi.stderr || ''))) {
  fail('kimi is not on OAuth (managed:kimi-code)');
}
ok('kimi · OAuth');

if (!existsSync(`${process.env.HOME}/.grok/auth.json`)) fail('~/.grok/auth.json missing');
ok('grok · auth.json present');

for (const cmd of ['claude', 'codex', 'kimi', 'grok']) {
  try {
    execSync(`command -v ${cmd}`, { stdio: 'ignore', shell: '/bin/zsh' });
  } catch {
    fail(`${cmd} not on PATH`);
  }
}

if (skipSmoke) {
  console.log('Gate 0 PASS (auth only; smoke skipped)');
  process.exit(0);
}

const outDir = `/tmp/gate0-smoke-${Date.now()}`;
const panel = resolve(HERE, 'panel.mjs');
console.log('Running four-CLI smoke (SUBSCRIPTION_OK)…');
const smoke = spawnSync(
  'node',
  [
    panel,
    '--panel', 'claude,codex,kimi,grok',
    '--out', outDir,
    '--timeout', '180000',
    '--prompt', 'Reply with exactly: SUBSCRIPTION_OK',
  ],
  { encoding: 'utf8', cwd: ROOT },
);
process.stdout.write(smoke.stdout || '');
process.stderr.write(smoke.stderr || '');
if (smoke.status !== 0) fail(`panel smoke exited ${smoke.status}`);

const pj = JSON.parse(readFileSync(`${outDir}/panel.json`, 'utf8'));
for (const n of ['claude', 'codex', 'kimi', 'grok']) {
  const r = pj.results.find((x) => x.name === n);
  if (!r || !r.ok) fail(`smoke FAIL for ${n}: ${r?.error || 'missing'}`);
}

console.log(`Gate 0 PASS — all four subscriptions smoked → ${outDir}`);
process.exit(0);
