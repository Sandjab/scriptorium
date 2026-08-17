// Test de CÂBLAGE bout-en-bout du garde d'élagage de ../workflow.js (leanmonograph).
//
// Lancer :  node .claude/skills/leanmonograph/scripts/test_elagage_stops_before_prose.mjs
//           (exit ≠ 0 si échec)
//
// Ce qu'il protège, et POURQUOI :
//
//   39e run (nootropiques-stimulants-prescrits, 2026-08-15). Un claim que les DEUX jurés
//   tenaient (rejet au seul seuil de sources) a fait tomber sa section sous le quota
//   d'élagage : section coupée en silence, prose écrite sans elle, relecteur de continuité
//   camouflant le trou, « 11/11 sections retenues » annoncé sur un document qui n'en avait
//   que 10. Réparation réelle : ~1,9 M tokens de resume. Détection au bon endroit : ~0.
//
//   test_section_pruning_guards.mjs teste la LOGIQUE du garde (bloc extrait) ; celui-ci
//   teste le CÂBLAGE dans le vrai flux : (A) l'arrêt survient AVANT l'Author — aucune prose
//   n'est payée sur un plan amputé — et (B) sur un run sain, les ids de sections
//   POST-élagage voyagent jusqu'à la ligne de commande de build.py (--expect-sections),
//   seul lecteur du manifeste réellement écrit par Compose.
//
// Technique : copie temporaire du workflow enveloppée en module ESM, agents mockés —
// même procédé que test_rejected_correction_reaches_author.mjs (le vrai workflow.js
// n'est jamais modifié : l'envelopper romprait son idiome `return` top-level).

import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
const src = readFileSync(join(here, '..', 'workflow.js'), 'utf8').replace(/^export const meta/m, 'const meta');
const modPath = join(tmpdir(), `lean_elagage_under_test_${process.pid}.mjs`);
writeFileSync(modPath,
  'export default async function __run(__env) {\n' +
  '  const { agent, parallel, pipeline, phase, log, args, budget } = __env;\n' + src + '\n}\n', 'utf8');
let runWorkflow;
try { ({ default: runWorkflow } = await import(pathToFileURL(modPath).href)); }
finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }

// ── Fixtures ────────────────────────────────────────────────────────────────
const TENU = 'Le sous-groupe à charge élevée localise l\'effet.';
const SRC_A = { title: 'source A', url: 'https://exemple.test/a' };
const SRC_B = { title: 'source B', url: 'https://exemple.test/b' };

const OUTLINE = [
  { id: 's1', heading: 'S1', angle: 'a', kind: 'normal', angle_key: 'foundations' },
  { id: 's2', heading: 'S2', angle: 'a', kind: 'normal', angle_key: 'theory' },
];

// s1, claim 0 — le cas du 39e run, piloté par scénario :
//   'faux-rejet' : les DEUX jurés tiennent l'énoncé mais ne citent que le même travail
//                  → rejeté au seuil de sources, tenu par tous → le garde doit ARRÊTER.
//   'vrai-rejet' : un juré réfute → rejet authentique → coupe silencieuse, run complet.
// s1, claim 1 et s2 : confirmés (2 sources indépendantes).
const verdictsFor = (scenario, secId, lens) => ({
  verdicts: [
    (secId === 's1'
      ? (scenario === 'faux-rejet' || lens === 'refutation'
          ? { claim_index: 0, holds: true,  corrected_statement: '', independent_sources: [SRC_A], note: '', search_exhausted: true, document_source: false }
          : { claim_index: 0, holds: false, corrected_statement: '', independent_sources: [SRC_A], note: '', search_exhausted: false, document_source: false })
      : { claim_index: 0, holds: true, corrected_statement: '', independent_sources: [lens === 'soutien' ? SRC_A : SRC_B], note: '', search_exhausted: false, document_source: false }),
    { claim_index: 1, holds: true, corrected_statement: '', independent_sources: [lens === 'soutien' ? SRC_A : SRC_B], note: '', search_exhausted: false, document_source: false },
  ],
});

function makeAgent(scenario, seen) {
  return function agent(prompt, opts) {
    const label = (opts && opts.label) || '';
    seen.push({ label, prompt });
    if (/Chemin\s*:/.test(prompt)) return Promise.resolve({ written: true, files_written: ['x'] });
    if (label === 'plan') return Promise.resolve({ title: 'T', kicker: 'k', fil_rouge: 'f', outline: JSON.parse(JSON.stringify(OUTLINE)) });
    if (label.startsWith('sweep:')) return Promise.resolve({ sources: [SRC_A], findings: [{ point: 'p', url: SRC_A.url }] });
    if (label.startsWith('extract:')) {
      const id = label.slice(8);
      return Promise.resolve({ id, heading: id.toUpperCase(), notes: [{ point: 'n', url: SRC_A.url }],
        claims: [
          { statement: id === 's1' ? TENU : 'fait A', candidate_sources: [SRC_A.url], kind: 'established' },
          { statement: `fait B de ${id}`, candidate_sources: [SRC_A.url], kind: 'established' },
        ], pointers: [] });
    }
    if (label.startsWith('verify:')) {
      const secId = label.slice(7).split('/')[0].split('#')[0];
      return Promise.resolve(verdictsFor(scenario, secId, label.endsWith('soutien') ? 'soutien' : 'refutation'));
    }
    if (label.startsWith('prose:')) return Promise.resolve({
      sections: OUTLINE.map(o => ({ id: o.id, prose: '<p>x</p>' })), summary: 's' });
    if (label === 'compose') return Promise.resolve({ files_written: ['/repo/themes/demo/manifest.json'], element_counts: { document: 6 } });
    // défaut permissif pour les étapes non discriminantes du test
    return Promise.resolve({ files_written: ['tldr.json', 'glossary.json'], sections: [], widgets: [], pointers: [],
      edits: [], ok: true, issues: [], success: true, files: [], errors: [], element_counts: {},
      checked: 0, fixed: 0, hedged: 0, n_substances: 0, n_rows: 0, note: '' });
  };
}

const parallelMock = (thunks) => Promise.all(thunks.map(t => Promise.resolve().then(t).catch(() => null)));
const pipelineMock = async (items, ...stages) => Promise.all(items.map(async (it, i) => {
  let v = it;
  for (const st of stages) { try { v = await st(v, it, i); } catch { return null; } }
  return v;
}));

async function run(scenario) {
  const seen = [];
  let error = null;
  try {
    await runWorkflow({ agent: makeAgent(scenario, seen), parallel: parallelMock, pipeline: pipelineMock,
      phase: () => {}, log: () => {},
      args: { subject: 'Sujet', slug: 'demo', themeDir: '/repo/themes/demo' },
      budget: { total: null, spent: () => 0, remaining: () => Infinity } });
  } catch (e) { error = e; }
  return { seen, error };
}

// ── Assertions ──────────────────────────────────────────────────────────────
let failures = 0;
const ok = (cond, label) => { if (!cond) { failures++; console.error(`  ✗ ${label}`); } else console.log(`  ✓ ${label}`); };

// (A) faux rejet décisif → arrêt AVANT toute prose.
const a = await run('faux-rejet');
ok(!!a.error, 'faux rejet décisif : le run s\'arrête (erreur levée)');
ok(!!a.error && /faux rejet/i.test(String(a.error && a.error.message)), 'l\'erreur nomme la classe d\'échec (« faux rejet »)');
ok(!a.seen.some(s => s.label.startsWith('prose:')), 'AUCUNE prose n\'a été payée sur le plan amputé');

// (B) rejet authentique → run complet, ids post-élagage transmis à build.py.
const b = await run('vrai-rejet');
ok(!b.error, `rejet authentique : le run va au bout (erreur : ${b.error ? b.error.message : '—'})`);
const build = b.seen.find(s => s.label === 'build');
ok(!!build, 'le Build a bien été appelé');
const bp = build ? build.prompt : '';
ok(bp.includes('--expect-sections s2'), 'la ligne de commande de build.py porte --expect-sections avec les sections POST-élagage');
ok(!bp.includes('s1'), 'la section coupée (s1) n\'est PAS dans les sections attendues');

console.log(failures ? `\n${failures} échec(s)` : '\nTous les tests passent.');
process.exit(failures ? 1 : 0);
