// Test structurel du câblage super-widget de ../workflow.js (champ kind + variantes process).
// Lancer : node .claude/skills/monograph/scripts/test_superwidget.mjs   (exit ≠ 0 si échec)
// Même technique que test_resume.mjs : copie temporaire enveloppée en ESM, globals harness mockés,
// agent mocké par label + CAPTURE des prompts. Ne teste pas le LLM — seulement le contrôle de flux.
import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
// Enveloppe une COPIE TEMPORAIRE d'un workflow dans un module ESM recevant les globals harness.
// Suffixe unique par chargement : sinon le cache de modules ESM de Node renverrait le 1er fichier importé.
let _loadN = 0;
async function loadWorkflow(srcPath) {
  const src = readFileSync(srcPath, 'utf8').replace(/^export const meta/m, 'const meta');
  const wrapped =
    'export default async function __run(__env) {\n' +
    '  const { agent, parallel, pipeline, phase, log, args, budget } = __env;\n' +
    src + '\n}\n';
  const modPath = join(tmpdir(), `wf_sw_${process.pid}_${_loadN++}.mjs`);
  writeFileSync(modPath, wrapped, 'utf8');
  try { const m = await import(pathToFileURL(modPath).href); return m.default; }
  finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }
}
// Les deux workflows jumeaux : monograph (scénarios A-C, E) et frugalmonograph (scénario D = garde-fou de parité).
const runWorkflow = await loadWorkflow(join(here, '..', 'workflow.js'));
const runFrugal   = await loadWorkflow(join(here, '..', '..', 'frugalmonograph', 'workflow.js'));

// ── Mock agent (full pipeline + top-up), capture {label, prompt} ──────────────
function makeEnv(disk, planWidgets, envOpts = {}) {
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
    if (label.startsWith('widget-critic:')) return Promise.resolve({
      ok: envOpts.criticOk !== false, issues: envOpts.criticOk === false ? ['phases manquantes'] : [] });
    if (label.startsWith('figure-code:') || label.startsWith('figure-recode:'))
      return Promise.resolve({ ref: 'fig-x', after_section_id: 's1', caption: 'légende', kind: 'figure' });
    if (label.startsWith('figure-critic:')) return Promise.resolve({ ok: true, issues: [] });
    if (label === 'manifest-insert') return Promise.resolve(envOpts.insertReturns || { inserted: ['w-process'], already_present: [] });
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
  ok(/probe.*process|kind \("probe"\|"process"\)/.test(env.prompts['widget-plan'] || ''),
     'le prompt planner expose les deux kinds (probe|process)');
  ok(/PROCESSUS DE BOUT EN BOUT|super-widget|SUPER-WIDGET/i.test(env.prompts['widget-plan'] || ''),
     'le prompt planner décrit la rubrique process');
  const codeKey = Object.keys(env.prompts).find(k => k.startsWith('widget-code:'));
  ok(!!codeKey, 'un widget-code a été appelé');
  ok(/Vue d'ensemble/.test(env.prompts[codeKey] || ''), 'le prompt codeur process exige l\'en-tête « Vue d\'ensemble »');
  ok(/jusqu'à convergence|PAS-À-PAS|INSTANCE JOUET/i.test(env.prompts[codeKey] || ''),
     'le prompt codeur process exige pas-à-pas + continu sur instance jouet');
  const critKey = Object.keys(env.prompts).find(k => k.startsWith('widget-critic:'));
  ok(!!critKey && /PROCESSUS COMPLET|ENCHAÎNEMENT|toutes les phases/i.test(env.prompts[critKey] || ''),
     'le prompt critic process ajoute le contrôle d\'enchaînement complet');
  const wjson = disk['widgets.json'] || '';
  ok(/"kind"\s*:\s*"process"/.test(wjson), 'le checkpoint widgets.json porte kind=process');
}

// ── Scénario A2 : recode process exercé (critic rejette → recode) ──────────────
console.log('Scénario A2 — recode process exercé (critic ko → widget-recode) :');
{
  const disk = {};
  const env = makeEnv(disk, [{ concept: 'c', after_section_id: 's1', brief: 'b', kind: 'process' }], { criticOk: false });
  await run(env, ARGS);
  const recodeKey = Object.keys(env.prompts).find(k => k.startsWith('widget-recode:'));
  ok(!!recodeKey, 'un widget-recode a été appelé (critic a rejeté)');
  ok(/RAPPEL SUPER-WIDGET/.test(env.prompts[recodeKey] || ''),
     'le prompt recode process rappelle de garder le super-widget');
  ok(/Vue d'ensemble|jusqu'à convergence/i.test(env.prompts[recodeKey] || ''),
     'le prompt recode process réénonce les exigences (Vue d\'ensemble / jusqu\'à convergence)');
}
// ── Scénario B : mode superwidgetOnly (retrofit) ──────────────────────────────
console.log('Scénario B — superwidgetOnly : seules les phases process tournent :');
{
  const disk = {};
  const env = makeEnv(disk, [
    { concept: 'p', after_section_id: 's1', brief: 'avant→arrière→maj', kind: 'process' },
    { concept: 'q', after_section_id: 's1', brief: 'isolé', kind: 'probe' },          // doit être ignoré
  ]);
  const r = await run(env, { ...ARGS, superwidgetOnly: true });
  ok(['sweep:', 'plan', 'extract:', 'verify:', 'author', 'compose'].every(p => !has(env.calls, p)),
     'aucune phase de recherche/auteur/compose complète n\'est exécutée');
  ok(has(env.calls, 'topup-load'), 'chargement des fichiers persistés (topup-load)');
  ok(has(env.calls, 'widget-plan'), 'planner exécuté');
  ok(env.calls.filter(c => c.startsWith('widget-code:')).length === 1, 'un seul widget codé (le probe est filtré)');
  ok(env.calls.some(c => c.startsWith('widget-critic:')), 'le critic est exécuté en top-up');
  ok(has(env.calls, 'manifest-insert'), 'insertion chirurgicale dans le manifeste');
  ok(/IMMÉDIATEMENT APRÈS|IDEMPOTENT|Ne modifie AUCUN autre/i.test(env.prompts['manifest-insert'] || ''),
     'le prompt d\'insertion est chirurgical + idempotent');
  ok(has(env.calls, 'build'), 'build relancé');
  ok(r && r.mode === 'superwidgetOnly' && Array.isArray(r.superwidgets) && r.superwidgets.length === 1,
     'rapport top-up : 1 super-widget');
}

// ── Scénario C : superwidgetOnly mais aucun process éligible → no-op ───────────
console.log('Scénario C — superwidgetOnly sans process éligible : thème inchangé :');
{
  const disk = {};
  const env = makeEnv(disk, [{ concept: 'q', after_section_id: 's1', brief: 'isolé', kind: 'probe' }]);
  const r = await run(env, { ...ARGS, superwidgetOnly: true });
  ok(!has(env.calls, 'widget-code:'), 'aucun widget codé');
  ok(!has(env.calls, 'manifest-insert') && !has(env.calls, 'build'), 'ni insertion ni build (no-op)');
  ok(r && r.mode === 'superwidgetOnly' && r.superwidgets.length === 0, 'rapport : 0 super-widget');
}

// ── Scénario D : frugalmonograph — le top-up superwidgetOnly fonctionne aussi (garde-fou de parité) ──
console.log('Scénario D — frugalmonograph : top-up superwidgetOnly opérationnel :');
{
  const disk = {};
  const env = makeEnv(disk, [{ concept: 'p', after_section_id: 's1', brief: 'avant→arrière→maj', kind: 'process' }]);
  const r = await runFrugal({ ...env, args: { ...ARGS, superwidgetOnly: true } });
  ok(['sweep:', 'plan', 'extract:', 'verify:', 'author', 'compose'].every(p => !has(env.calls, p)),
     'frugal : aucune phase de recherche/auteur/compose');
  ok(has(env.calls, 'topup-load') && has(env.calls, 'manifest-insert') && has(env.calls, 'build'),
     'frugal : top-up load → insertion → build');
  ok(r && r.mode === 'superwidgetOnly' && r.superwidgets.length === 1, 'frugal : rapport top-up 1 super-widget');
}

// ── Scénario E : section d'ancrage introuvable dans le manifeste → ref rapporté non placé (M2) ──
console.log('Scénario E — section d\'ancrage absente du manifeste : ref rapporté non placé :');
{
  const disk = {};
  const env = makeEnv(disk, [{ concept: 'p', after_section_id: 's1', brief: 'b', kind: 'process' }],
    { insertReturns: { inserted: [], already_present: [] } });
  const r = await run(env, { ...ARGS, superwidgetOnly: true });
  ok(Array.isArray(r.not_placed) && r.not_placed.includes('w-process'),
     'le ref non inséré est rapporté dans not_placed');
}

// ── Scénario F : kind=figure routé vers le codeur de figure (en série), sections_draft écrit avant ──
console.log('Scénario F — figure : routage + sections_draft écrit AVANT la phase visuelle :');
{
  const disk = {};
  const env = makeEnv(disk, [
    { concept: 'c', after_section_id: 's1', brief: 'b', kind: 'figure', anchor: '…' },
    { concept: 'd', after_section_id: 's2', brief: 'b', kind: 'probe' },
  ]);
  await run(env, ARGS);
  const iWrite = env.calls.indexOf('write:sections');
  const iPlan = env.calls.indexOf('widget-plan');
  ok(iWrite >= 0 && iPlan >= 0 && iWrite < iPlan, 'sections_draft.json écrit AVANT le planner visuel');
  ok(env.calls.some(c => c.startsWith('figure-code:')), 'le codeur de figure est appelé');
  ok(env.calls.some(c => c.startsWith('figure-critic:')), 'le critic de figure est appelé');
  ok(env.calls.some(c => c.startsWith('widget-code:')), 'le widget (probe) est aussi codé');
}

console.log(failures === 0 ? '\n✅ TOUS LES TESTS PASSENT' : `\n❌ ${failures} test(s) en échec`);
process.exit(failures === 0 ? 0 : 1);
