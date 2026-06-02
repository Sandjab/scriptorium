// Test du FLUX de reprise disque (Fix 2) de ../workflow.js.
//
// Lancer :  node .claude/skills/monograph/scripts/test_resume.mjs   (exit ≠ 0 si échec)
//
// Mocke agent/parallel/pipeline/phase/log pour exécuter l'orchestration SANS LLM ni disque réels,
// et vérifie que `args.resume=true` saute EXACTEMENT le travail déjà checkpointé (research, sections,
// widgets) et ne recalcule que les sections sans checkpoint. Ne teste PAS le comportement LLM —
// seulement le câblage du contrôle de flux, qui est la partie cassable silencieusement.
//
// Technique : on enveloppe une COPIE TEMPORAIRE du workflow dans un module ESM qui reçoit les globals
// du harness en paramètre, puis on l'importe. Le vrai workflow.js n'est jamais modifié ni enveloppé
// (l'envelopper romprait son idiome `return` top-level — cf. mémoire workflow-js-verification).
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
const modPath = join(tmpdir(), `wf_under_test_${process.pid}.mjs`);
writeFileSync(modPath, wrapped, 'utf8');
let runWorkflow;
try { ({ default: runWorkflow } = await import(pathToFileURL(modPath).href)); }
finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }

// ── Mocks ────────────────────────────────────────────────────────────────────
function makeEnv(disk) {
  const calls = [];
  const log = () => {};
  const phase = () => {};
  const parallel = (thunks) => Promise.all(thunks.map(t => Promise.resolve().then(t).catch(() => null)));
  const pipeline = async (items, ...stages) => Promise.all(items.map(async (it, i) => {
    let v = it;
    for (const st of stages) { try { v = await st(v, it, i); } catch { return null; } }
    return v;
  }));

  const ARCH = { title: 'T', kicker: 'k', outline: [
    { id: 's1', heading: 'S1', angle: 'a', kind: 'normal', angle_key: 'foundations' },
    { id: 's2', heading: 'S2', angle: 'a', kind: 'normal', angle_key: 'theory' },
    { id: 's3', heading: 'S3', angle: 'a', kind: 'normal', angle_key: 'variants' },
  ] };

  function agent(prompt, opts) {
    const label = (opts && opts.label) || '';
    calls.push(label);

    // Toute écriture de fichier ("Chemin : …\nContenu :\n…") → schéma {written}. On capture les
    // artefacts .monograph dans le "disque" pour le round-trip ; les autres fichiers sont ignorés.
    if (/Chemin\s*:/.test(prompt)) {
      const pm = prompt.match(/Chemin\s*:\s*(.+)/);
      const cm = prompt.match(/Contenu\s*:\n([\s\S]*)$/);
      const path = pm ? pm[1].trim() : '';
      const rel = path.split('/.monograph/')[1];
      if (rel && cm) disk[rel] = cm[1];
      return Promise.resolve({ written: true });
    }
    if (label === 'resume-load') {
      const sections = Object.keys(disk).filter(k => /^sec-.*\.json$/.test(k))
        .map(k => ({ id: k.replace(/^sec-/, '').replace(/\.json$/, ''), content: disk[k] }));
      return Promise.resolve({ research: disk['research.json'] || '', widgets: disk['widgets.json'] || '', sections });
    }
    if (label === 'plan') return Promise.resolve(JSON.parse(JSON.stringify(ARCH)));
    if (label.startsWith('sweep:')) return Promise.resolve({
      sources: [{ title: 'src', url: 'http://e/' + label, kind: 'paper' }],
      findings: [{ point: 'p', url: 'http://e/' + label }] });
    if (label.startsWith('extract:')) return Promise.resolve({
      id: label.slice(8), heading: 'h', prose: '<p>x</p>',
      claims: [
        { statement: 'c1', candidate_sources: ['http://e/'], kind: 'established' },
        { statement: 'c2', candidate_sources: ['http://e/'], kind: 'established' },
      ], pointers: [] });
    if (label.startsWith('verify:')) {
      const j = label.split('/').pop();             // index du juré → sources distinctes
      return Promise.resolve({ holds: true, corrected_statement: '',
        independent_sources: [{ title: 'v' + j, url: 'http://v' + j + '/' }], note: 'ok' });
    }
    if (label === 'widget-plan') return Promise.resolve({ widgets: [{ concept: 'c', after_section_id: 's1', brief: 'b' }] });
    if (label.startsWith('widget-code:')) return Promise.resolve({ ref: 'w1', title: 'W1', after_section_id: 's1' });
    if (label.startsWith('widget-critic:')) return Promise.resolve({ ok: true, issues: [] });
    if (label === 'author') return Promise.resolve({ files_written: ['glossary.json', 'tldr.json'] });
    if (label === 'compose') return Promise.resolve({ files_written: ['manifest.json'], element_counts: { document: 5 } });
    if (label === 'build') return Promise.resolve({ success: true, files: ['dist/demo.html'],
      acceptance: { confirmed_claims: 6, all_confirmed_have_2plus_sources: true, audit_categories_present: ['confirmed'] }, errors: [] });
    throw new Error('label non mocké: ' + label);
  }
  return { agent, parallel, pipeline, phase, log, calls, budget: { total: null, spent: () => 0, remaining: () => Infinity } };
}

const run = (env, args) => runWorkflow({ ...env, args });
const ARGS = { subject: 'Sujet', slug: 'demo', themeDir: '/repo/themes/demo' };
let failures = 0;
const ok = (cond, msg) => { console.log((cond ? '  PASS ' : '  FAIL ') + msg); if (!cond) failures++; };
const has = (calls, p) => calls.some(c => c === p || c.startsWith(p));

// ── Scénario 1 : run FRAIS ────────────────────────────────────────────────────
console.log('Scénario 1 — run frais (sans resume) :');
const disk1 = {};
const env1 = makeEnv(disk1);
const r1 = await run(env1, ARGS);
ok(!has(env1.calls, 'resume-load'), 'pas de sonde de reprise sur un run frais');
ok(env1.calls.filter(c => c.startsWith('sweep:')).length === 6, '6 agents Sweep appelés');
ok(has(env1.calls, 'plan'), 'Plan appelé');
ok(['s1', 's2', 's3'].every(s => has(env1.calls, 'extract:' + s)), 'Extract appelé pour s1,s2,s3');
ok(has(env1.calls, 'widget-plan'), 'phase Widgets exécutée');
ok(['research.json', 'sec-s1.json', 'sec-s2.json', 'sec-s3.json', 'widgets.json'].every(f => f in disk1),
  'checkpoints écrits : research + sec-s1/s2/s3 + widgets');
ok(r1 && r1.claims && r1.claims.total === 6 && r1.claims.confirmed === 6, 'résultat : 6 claims, 6 confirmés');

// ── Scénario 2 : REPRISE avec s2 manquante (simule un crash mid-Verify sur s2) ──
console.log('Scénario 2 — reprise, section s2 jamais terminée :');
const disk2 = { ...disk1 };
delete disk2['sec-s2.json'];                 // s2 sans checkpoint → doit être recalculée
const env2 = makeEnv(disk2);
const r2 = await run(env2, { ...ARGS, resume: true });
ok(has(env2.calls, 'resume-load'), 'sonde de reprise appelée');
ok(env2.calls.filter(c => c.startsWith('sweep:')).length === 0, 'Sweep SAUTÉ (research repris)');
ok(!has(env2.calls, 'plan'), 'Plan SAUTÉ');
ok(!has(env2.calls, 'extract:s1') && !has(env2.calls, 'extract:s3'), 's1 et s3 NON recalculées (reprises du disque)');
ok(has(env2.calls, 'extract:s2'), 's2 RECALCULÉE (pas de checkpoint)');
ok(env2.calls.filter(c => c.startsWith('verify:s2')).length > 0, 'Verify rejoué pour s2');
ok(env2.calls.filter(c => c.startsWith('verify:s1')).length === 0, 'Verify NON rejoué pour s1');
ok(!has(env2.calls, 'widget-plan'), 'Widgets SAUTÉ (widgets.json repris)');
ok(r2 && r2.claims && r2.claims.total === 6, 'résultat complet reconstruit : 6 claims');

// ── Scénario 3 : REPRISE tout sauvegardé (rien de coûteux à refaire) ───────────
console.log('Scénario 3 — reprise, tout déjà sauvegardé :');
const disk3 = { ...disk1 };
const env3 = makeEnv(disk3);
const r3 = await run(env3, { ...ARGS, resume: true });
ok(['sweep:', 'plan', 'extract:', 'verify:', 'widget-plan'].every(p => !has(env3.calls, p)),
  'aucune phase coûteuse rejouée (Sweep/Plan/Extract/Verify/Widgets tous sautés)');
ok(has(env3.calls, 'compose') && has(env3.calls, 'build'), 'Compose+Build tournent quand même (déterministes)');
ok(r3 && r3.claims && r3.claims.total === 6, 'résultat complet : 6 claims');

console.log(failures === 0 ? '\n✅ TOUS LES TESTS PASSENT' : `\n❌ ${failures} test(s) en échec`);
process.exit(failures === 0 ? 0 : 1);
