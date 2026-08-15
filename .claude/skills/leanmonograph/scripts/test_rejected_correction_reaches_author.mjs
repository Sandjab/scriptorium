// Test du CÂBLAGE « garde-fous » de ../workflow.js (leanmonograph).
//
// Lancer :  node .claude/skills/leanmonograph/scripts/test_rejected_correction_reaches_author.mjs
//           (exit ≠ 0 si échec)
//
// Ce qu'il protège, et POURQUOI :
//
//   Classe d'échec trouvée le 2026-08-15 sur `cafeine-ergogene` (37e run). Quand un claim est
//   rejeté sur le SEUIL DE SOURCES, l'énoncé corrigé produit par un juré était jeté avec lui :
//   il ne survivait ni dans le checkpoint ni nulle part ailleurs. L'auteur de prose, qui ne voit
//   jamais les claims rejetés, réécrivait ensuite le fait depuis les NOTES de section — donc
//   dans sa version FAUTIVE, celle que le council venait précisément d'identifier comme fausse.
//   Deux erreurs du document sont nées de là, dont une fausse attribution d'auteur que `lint.py`
//   ne pouvait pas voir (aucun chiffre en cause, et le nom fautif n'était pas écrit).
//
//   Le test vérifie donc UNE chose, de bout en bout : une correction trouvée par un juré sur un
//   claim rejeté ARRIVE jusqu'au prompt de l'auteur. Il tombe si quelqu'un retire le champ
//   `rejected_correction`, cesse de le transmettre dans `garde_fous`, ou supprime la consigne.
//   Il vérifie AUSSI que le claim rejeté n'est pas ressuscité en claim porteur au passage.
//
// Technique : on enveloppe une COPIE TEMPORAIRE du workflow dans un module ESM recevant les
// globals du harness, comme test_resume.mjs — le vrai workflow.js n'est jamais modifié
// (l'envelopper romprait son idiome `return` top-level, cf. mémoire workflow-js-verification).
// Les agents sont mockés ; on ne teste PAS le comportement LLM, seulement le câblage, qui est
// la partie cassable en silence.

import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
const src = readFileSync(join(here, '..', 'workflow.js'), 'utf8').replace(/^export const meta/m, 'const meta');
const modPath = join(tmpdir(), `lean_under_test_${process.pid}.mjs`);
writeFileSync(modPath,
  'export default async function __run(__env) {\n' +
  '  const { agent, parallel, pipeline, phase, log, args, budget } = __env;\n' + src + '\n}\n', 'utf8');
let runWorkflow;
try { ({ default: runWorkflow } = await import(pathToFileURL(modPath).href)); }
finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }

// ── Fixtures ────────────────────────────────────────────────────────────────
const FAUTIF = "L'essai croisé de 2020 est signé du même premier auteur que l'étude princeps.";
const EXACT  = "L'essai croisé de 2020 est conduit par Carswell et ses coauteurs.";
const SRC_A = { title: 'source A', url: 'https://exemple.test/a' };
const SRC_B = { title: 'source B', url: 'https://exemple.test/b' };

const OUTLINE = [
  { id: 's1', heading: 'S1', angle: 'a', kind: 'normal', angle_key: 'foundations' },
  { id: 's2', heading: 'S2', angle: 'a', kind: 'normal', angle_key: 'theory' },
];

// claim 0 : un juré le tient, l'autre le CORRIGE, et les deux ne citent qu'un seul travail
//           → seuil ≥2 sources non atteint → REJETÉ, mais avec une correction en main.
// claims 1 et 2 : deux sources distinctes → confirmés (il en faut 2 pour que la section survive).
const verdictsFor = (lens) => ({
  verdicts: [
    lens === 'soutien'
      ? { claim_index: 0, holds: false, corrected_statement: EXACT, independent_sources: [SRC_A], note: '', search_exhausted: false, document_source: false }
      : { claim_index: 0, holds: true,  corrected_statement: '',    independent_sources: [SRC_A], note: '', search_exhausted: false, document_source: false },
    { claim_index: 1, holds: true, corrected_statement: '', independent_sources: [lens === 'soutien' ? SRC_A : SRC_B], note: '', search_exhausted: false, document_source: false },
    { claim_index: 2, holds: true, corrected_statement: '', independent_sources: [lens === 'soutien' ? SRC_A : SRC_B], note: '', search_exhausted: false, document_source: false },
  ],
});

const seen = [];   // { label, prompt }

function agent(prompt, opts) {
  const label = (opts && opts.label) || '';
  seen.push({ label, prompt });
  if (/Chemin\s*:/.test(prompt)) return Promise.resolve({ written: true, files_written: ['x'] });
  if (label === 'plan') return Promise.resolve({ title: 'T', kicker: 'k', fil_rouge: 'f', outline: JSON.parse(JSON.stringify(OUTLINE)) });
  if (label.startsWith('sweep:')) return Promise.resolve({ sources: [SRC_A], findings: [{ point: 'p', url: SRC_A.url }] });
  if (label.startsWith('extract:')) return Promise.resolve({
    id: label.slice(8), heading: 'h',
    notes: [{ point: FAUTIF, url: SRC_A.url }],           // la NOTE porte la version fautive
    claims: [
      { statement: FAUTIF, candidate_sources: [SRC_A.url], kind: 'established' },
      { statement: 'fait B', candidate_sources: [SRC_A.url], kind: 'established' },
      { statement: 'fait C', candidate_sources: [SRC_A.url], kind: 'established' },
    ], pointers: [] });
  if (label.startsWith('verify:')) return Promise.resolve(verdictsFor(label.endsWith('soutien') ? 'soutien' : 'refutation'));
  if (label.startsWith('prose:')) return Promise.resolve({ sections: OUTLINE.map(o => ({ id: o.id, prose: '<p>x</p>' })), summary: 's' });
  // défaut permissif : le test n'a besoin que d'aller jusqu'à l'auteur.
  return Promise.resolve({ files_written: ['tldr.json', 'glossary.json'], sections: [], widgets: [], pointers: [],
    edits: [], ok: true, issues: [], success: true, files: [], errors: [], element_counts: {},
    checked: 0, fixed: 0, hedged: 0, n_substances: 0, n_rows: 0 });
}

const parallel = (thunks) => Promise.all(thunks.map(t => Promise.resolve().then(t).catch(() => null)));
const pipeline = async (items, ...stages) => Promise.all(items.map(async (it, i) => {
  let v = it;
  for (const st of stages) { try { v = await st(v, it, i); } catch { return null; } }
  return v;
}));

try {
  await runWorkflow({ agent, parallel, pipeline, phase: () => {}, log: () => {},
    args: { subject: 'Sujet', slug: 'demo', themeDir: '/repo/themes/demo' },
    budget: { total: null, spent: () => 0, remaining: () => Infinity } });
} catch { /* le workflow peut échouer plus loin : seul le prompt de l'auteur nous intéresse */ }

// ── Assertions ──────────────────────────────────────────────────────────────
let failures = 0;
const ok = (cond, label) => { if (!cond) { failures++; console.error(`  ✗ ${label}`); } else console.log(`  ✓ ${label}`); };

const prose = seen.find(s => s.label.startsWith('prose:'));
ok(!!prose, "l'auteur de prose a bien été appelé");
const p = prose ? prose.prompt : '';

ok(/"garde_fous":\[/.test(p), 'les DONNÉES transmises portent un champ "garde_fous" (et pas seulement la consigne)');
ok(p.includes(EXACT), 'la VERSION EXACTE trouvée par le juré atteint l\'auteur');
ok(/"version_exacte":/.test(p) && /"version_fautive":/.test(p), 'les deux versions sont étiquetées dans les données sérialisées');
ok(/GARDE-FOUS/.test(p), 'la consigne d\'usage des garde-fous est présente dans le prompt');

// le claim rejeté ne doit PAS être ressuscité en claim porteur
const claimsBlock = (p.match(/"claims":\[.*?\]/s) || [''])[0];
ok(!claimsBlock.includes(FAUTIF), 'le claim rejeté n\'est PAS remonté parmi les claims porteurs');

// le checkpoint de section doit conserver le texte de la correction, pas un simple booléen
const ckpt = seen.find(s => /sec-s1\.json/.test(s.prompt) && /Chemin\s*:/.test(s.prompt));
ok(!!ckpt && ckpt.prompt.includes(EXACT), 'le checkpoint de section conserve le texte de la correction');
ok(!!ckpt && /rejected_correction/.test(ckpt.prompt), 'le checkpoint expose le champ rejected_correction');

console.log(failures ? `\n${failures} échec(s)` : '\nTous les tests passent.');
process.exit(failures ? 1 : 0);
