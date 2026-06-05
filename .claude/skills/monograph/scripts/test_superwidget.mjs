// Test structurel du câblage super-widget de ../workflow.js (kind + mode superwidgetOnly).
// Lancer : node .claude/skills/monograph/scripts/test_superwidget.mjs   (exit ≠ 0 si échec)
// Même technique que test_resume.mjs : copie temporaire enveloppée en ESM, globals harness mockés,
// agent mocké par label + CAPTURE des prompts. Ne teste pas le LLM — seulement le contrôle de flux.
import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
const srcPath = join(here, '..', 'workflow.js');
const src = readFileSync(srcPath, 'utf8').replace(/^export const meta/m, 'const meta');
const wrapped =
  'export default async function __run(__env) {\n' +
  '  const { agent, parallel, pipeline, phase, log, args, budget } = __env;\n' +
  src + '\n}\n';
const modPath = join(tmpdir(), `wf_sw_${process.pid}.mjs`);
writeFileSync(modPath, wrapped, 'utf8');
let runWorkflow;
try { ({ default: runWorkflow } = await import(pathToFileURL(modPath).href)); }
finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }

// ── Mock agent (full pipeline + top-up), capture {label, prompt} ──────────────
function makeEnv(disk, planWidgets) {
  const calls = [];          // labels
  const prompts = {};        // label-prefix → dernier prompt vu
  const log = () => {};
  const phase = () => {};
  const parallel = (thunks) => Promise.all(thunks.map(t => Promise.resolve().then(t).catch(() => null)));
  const pipeline = async (items, ...stages) => Promise.all(items.map(async (it, i) => {
    let v = it; for (const st of stages) { try { v = await st(v, it, i); } catch { return null; } } return v;
  }));
  const ARCH = { title: 'T', kicker: 'k', outline: [
    { id: 's1', heading: 'S1', angle: 'a', kind: 'normal', angle_key: 'foundations' },
    { id: 's2', heading: 'S2', angle: 'a', kind: 'normal', angle_key: 'theory' },
    { id: 's3', heading: 'S3', angle: 'a', kind: 'normal', angle_key: 'variants' },
  ] };
  function agent(prompt, opts) {
    const label = (opts && opts.label) || '';
    calls.push(label); prompts[label] = prompt;
    if (/Chemin\s*:/.test(prompt)) {                       // toute écriture de fichier → {written}
      const pm = prompt.match(/Chemin\s*:\s*(.+)/); const cm = prompt.match(/Contenu\s*:\n([\s\S]*)$/);
      const rel = pm ? (pm[1].trim().split('/.monograph/')[1]) : ''; if (rel && cm) disk[rel] = cm[1];
      return Promise.resolve({ written: true });
    }
    if (label === 'resume-load') return Promise.resolve({ research: '', widgets: '', sections: [] });
    if (label === 'topup-load') return Promise.resolve({ sections: [
      { id: 's1', heading: 'S1', prose: '<p>x</p>', claims: ['énoncé 1'] } ] });
    if (label === 'plan') return Promise.resolve(JSON.parse(JSON.stringify(ARCH)));
    if (label.startsWith('sweep:')) return Promise.resolve({
      sources: [{ title: 'src', url: 'http://e/' + label, kind: 'paper' }],
      findings: [{ point: 'p', url: 'http://e/' + label }] });
    if (label.startsWith('extract:')) return Promise.resolve({
      id: label.slice(8), heading: 'h', prose: '<p>x</p>',
      claims: [ { statement: 'c1', candidate_sources: ['http://e/'], kind: 'established' },
                { statement: 'c2', candidate_sources: ['http://e/'], kind: 'established' } ], pointers: [] });
    if (label.startsWith('verify:')) { const j = label.split('/').pop();
      return Promise.resolve({ holds: true, corrected_statement: '',
        independent_sources: [{ title: 'v' + j, url: 'http://v' + j + '/' }], note: 'ok' }); }
    if (label === 'widget-plan') return Promise.resolve({ widgets: planWidgets });
    if (label.startsWith('widget-code:') || label.startsWith('widget-recode:')) {
      const m = prompt.match(/kind = "(\w+)"|kind="(\w+)"/); const kind = (m && (m[1] || m[2])) || 'probe';
      return Promise.resolve({ ref: 'w-' + kind, title: 'W ' + kind, after_section_id: 's1', kind }); }
    if (label.startsWith('widget-critic:')) return Promise.resolve({ ok: true, issues: [] });
    if (label === 'manifest-insert') return Promise.resolve({ inserted: ['w-process'], already_present: [] });
    if (label === 'author') return Promise.resolve({ files_written: ['glossary.json', 'tldr.json'] });
    if (label === 'compose') return Promise.resolve({ files_written: ['manifest.json'], element_counts: { document: 5 } });
    if (label === 'build') return Promise.resolve({ success: true, files: ['dist/demo.html'],
      acceptance: { confirmed_claims: 6, all_confirmed_have_2plus_sources: true, audit_categories_present: ['confirmed'] }, errors: [] });
    throw new Error('label non mocké: ' + label);
  }
  return { agent, parallel, pipeline, phase, log, calls, prompts,
    budget: { total: null, spent: () => 0, remaining: () => Infinity } };
}

const run = (env, args) => runWorkflow({ ...env, args });
const ARGS = { subject: 'Sujet', slug: 'demo', themeDir: '/repo/themes/demo' };
let failures = 0;
const ok = (cond, msg) => { console.log((cond ? '  PASS ' : '  FAIL ') + msg); if (!cond) failures++; };
const has = (calls, p) => calls.some(c => c === p || c.startsWith(p));

// ── Scénario A : mode normal, le plan contient un widget process ───────────────
console.log('Scénario A — kind=process routé dans la phase Widgets normale :');
{
  const disk = {};
  const env = makeEnv(disk, [{ concept: 'c', after_section_id: 's1', brief: 'b', kind: 'process' }]);
  await run(env, ARGS);
  ok(has(env.calls, 'widget-plan'), 'planner appelé');
  ok(/probe.*process|process.*probe|enum:\['probe','process'\]|"probe"\|"process"|kind \("probe"\|"process"\)/.test(env.prompts['widget-plan'] || ''),
     'le prompt planner expose les deux kinds (probe|process)');
  ok(/PROCESSUS DE BOUT EN BOUT|super-widget|SUPER-WIDGET/i.test(env.prompts['widget-plan'] || ''),
     'le prompt planner décrit la rubrique process');
  const codeKey = Object.keys(env.prompts).find(k => k.startsWith('widget-code:'));
  ok(!!codeKey, 'un widget-code a été appelé');
  const wjson = disk['widgets.json'] || '';
  ok(/"kind"\s*:\s*"process"/.test(wjson), 'le checkpoint widgets.json porte kind=process');
}
console.log(failures === 0 ? '\n✅ TOUS LES TESTS PASSENT' : `\n❌ ${failures} test(s) en échec`);
process.exit(failures === 0 ? 0 : 1);
