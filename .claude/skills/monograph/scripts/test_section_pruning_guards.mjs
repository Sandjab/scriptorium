// Test des GARDES DE SURVIE DE SECTION des workflows leanmonograph et frugalmonograph.
//
// Lancer :  node .claude/skills/monograph/scripts/test_section_pruning_guards.mjs   (exit ≠ 0 si échec)
//
// Ce que ces tests protègent, et POURQUOI :
//
//   39e run (nootropiques-stimulants-prescrits, 2026-08-15), deux classes d'échec jumelles,
//   toutes deux découvertes APRÈS un `build.success: true` :
//
//   1. L'élagage déterministe coupe toute section normale sous SECTION_CLAIM_QUOTA claims
//      survivants — SILENCIEUSEMENT. Quand un des rejets qui font tomber la section est un
//      FAUX REJET PROBABLE (tous les jurés tiennent l'énoncé, rejet au seul seuil de sources),
//      le run perd une section entière que personne ne voit disparaître : le garde-fou
//      « prose manquante » ne mord pas (la section sort du plan AVANT l'Author) et le
//      relecteur de continuité camoufle le trou. L'élagage doit donc S'ARRÊTER BRUYAMMENT
//      quand un tel rejet est DÉCISIF (la section survivrait si on le gardait) — un ré-audit
//      ciblé d'un agent suffit alors à trancher, pour presque rien.
//
//   2. Le compte « sections retenues » annoncé par le workflow est calculé sur l'élagage,
//      jamais sur le manifeste que Compose écrit réellement : « 11/11 » annoncé, 10 dans le
//      document. Le contrôle doit vivre dans build.py (seul lecteur du fichier écrit) :
//      buildPrompt doit passer les ids post-élagage via --expect-sections.
//
//   Ces tests doivent tomber si : le garde-fou d'arrêt disparaît ou s'élargit (arrêt sur des
//   rejets NON décisifs ou réellement réfutés = fausses alertes qui feraient désactiver le
//   garde), ou si buildPrompt cesse de transmettre les sections attendues.
//
// Technique : extraction du bloc « Élagage déterministe » et de buildPrompt de chaque
// workflow.js vers un module temporaire — même procédé que test_audit_document_source.mjs
// (le workflow entier n'est pas exécutable ici : idiome `return` top-level).

import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
const skills = join(here, '..', '..');
const WORKFLOWS = ['leanmonograph', 'frugalmonograph'];

let failures = 0;
const ok = (cond, label) => {
  if (!cond) { failures++; console.error(`  ✗ ${label}`); } else { console.log(`  ✓ ${label}`); }
};

async function loadModule(name, body) {
  const modPath = join(tmpdir(), `pruning_under_test_${name}_${process.pid}_${Math.floor(Math.random() * 1e6)}.mjs`);
  writeFileSync(modPath, body, 'utf8');
  try { return await import(pathToFileURL(modPath).href); }
  finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }
}

async function loadElagage(name) {
  const src = readFileSync(join(skills, name, 'workflow.js'), 'utf8');
  const startM = src.match(/^\/\/ ── .?lagage d.terministe.*$/mi);
  if (!startM) throw new Error(`${name} : bloc d'élagage introuvable`);
  const start = src.indexOf(startM[0]);
  const endMark = 'sections retenues.`);';
  const end = src.indexOf(endMark, start);
  if (end < 0) throw new Error(`${name} : fin du bloc d'élagage introuvable`);
  const block = src.slice(start, end + endMark.length);
  const mod = await loadModule(name,
    'const SECTION_CLAIM_QUOTA = 2;\n' +
    'export function elagage(sectionData, log = () => {}) {\n' +
    block + '\nreturn liveSections;\n}\n');
  return mod.elagage;
}

async function loadBuildPrompt(name) {
  const src = readFileSync(join(skills, name, 'workflow.js'), 'utf8');
  const start = src.indexOf('const buildPrompt');
  if (start < 0) throw new Error(`${name} : buildPrompt introuvable`);
  const endMark = "].join('\\n');";
  const end = src.indexOf(endMark, start);
  if (end < 0) throw new Error(`${name} : fin de buildPrompt introuvable`);
  const mod = await loadModule(name,
    "const buildScript = '/B/build.py', lintScript = '/B/lint.py', themeDir = '/T';\n" +
    src.slice(start, end + endMark.length) + '\nexport { buildPrompt };\n');
  return { buildPrompt: mod.buildPrompt, src };
}

// ── Fixtures ────────────────────────────────────────────────────────────────
// C(audit, corroborés, réfutés) : le tally est la trace des votes que porte chaque claim.
const C = (audit, corrob, refut, statement = 'fait') => ({
  audit, statement, original_statement: statement,
  sources: [], examples: [], tally: { corroborated: corrob, refuted: refut },
});
const S = (id, kind, claims, pointers = []) => ({
  section: { id, heading: `H-${id}`, kind }, claims, pointers, notes: [],
});
const SURVIVANTE = S('sv', 'normal', [C('confirmed', 2, 0), C('confirmed', 2, 0)]);

for (const name of WORKFLOWS) {
  console.log(`\n── ${name} ──`);
  const elagage = await loadElagage(name);

  // 1. Faux rejet probable DÉCISIF (le cas du 39e run) → arrêt bruyant.
  let err = null;
  try { elagage([S('s1', 'normal', [C('confirmed', 2, 0), C('rejected', 2, 0, 'ÉNONCÉ TENU PAR TOUS')]), SURVIVANTE]); }
  catch (e) { err = e; }
  ok(!!err, 'section coupée par un rejet tenu par TOUS les jurés → le run S\'ARRÊTE');
  ok(!!err && /H-s1/.test(err.message), 'l\'erreur NOMME la section perdue');
  ok(!!err && /ÉNONCÉ TENU PAR TOUS/.test(err.message), 'l\'erreur NOMME l\'énoncé du rejet suspect');
  ok(!!err && /ré-audit|re-audit|2e source/i.test(err.message), 'l\'erreur prescrit la réparation (ré-audit ciblé)');

  // 2. Rejet AUTHENTIQUE (un juré réfute) → coupe silencieuse, comme avant.
  let live = null; err = null;
  try { live = elagage([S('s1', 'normal', [C('confirmed', 2, 0), C('rejected', 1, 1)]), SURVIVANTE]); }
  catch (e) { err = e; }
  ok(!err, 'rejet réellement réfuté → pas d\'arrêt (sinon fausses alertes → garde désactivé)');
  ok(!!live && live.length === 1 && live[0].section.id === 'sv', 'la section sous quota est bien coupée');

  // 3. Rejet suspect NON décisif (la section tomberait même en le gardant) → pas d'arrêt.
  err = null;
  try { live = elagage([S('s1', 'normal', [C('rejected', 2, 0)]), SURVIVANTE]); }
  catch (e) { err = e; }
  ok(!err && live.length === 1, 'rejet suspect non décisif (0 + 1 < quota) → coupe silencieuse');

  // 4. Section AU-DESSUS du quota avec un rejet suspect → elle vit, pas d'arrêt.
  err = null;
  try { live = elagage([S('s1', 'normal', [C('confirmed', 2, 0), C('confirmed', 2, 0), C('rejected', 2, 0)])]); }
  catch (e) { err = e; }
  ok(!err && live.length === 1 && live[0].section.id === 's1', 'section survivante avec rejet suspect → aucune alerte');

  // 5. Écosystème vidé par un rejet suspect décisif (1 claim l'aurait sauvé) → arrêt.
  err = null;
  try { elagage([S('e1', 'ecosystem', [C('rejected', 2, 0)]), SURVIVANTE]); }
  catch (e) { err = e; }
  ok(!!err, 'écosystème sans pointeur, vidé par un rejet tenu par tous → le run s\'arrête');

  // 6. Écosystème sauvé par ses pointeurs → il vit, pas d'arrêt.
  err = null;
  try { live = elagage([S('e1', 'ecosystem', [C('rejected', 2, 0)], [{ name: 'x' }])]); }
  catch (e) { err = e; }
  ok(!err && live.length === 1, 'écosystème avec pointeurs → vit, aucune alerte');

  // 7. Verdict unique (un seul juré a répondu) → preuve trop mince pour arrêter.
  err = null;
  try { live = elagage([S('s1', 'normal', [C('confirmed', 2, 0), C('rejected', 1, 0)]), SURVIVANTE]); }
  catch (e) { err = e; }
  ok(!err && live.length === 1, 'rejet corroboré par UN seul juré → pas assez pour arrêter, coupe silencieuse');

  // ── buildPrompt : les sections attendues voyagent jusqu'à build.py ──────────
  const { buildPrompt, src } = await loadBuildPrompt(name);
  const withIds = buildPrompt(['s1', 's2']);
  ok(withIds.includes('--expect-sections s1,s2'), 'buildPrompt(ids) passe --expect-sections id1,id2 à build.py');
  ok(!buildPrompt().includes('--expect-sections'), 'buildPrompt() sans ids (top-up sans élagage) n\'impose rien');
  // Câblage du site d'appel (tripwire textuel) : le run principal passe les ids post-élagage.
  ok(/buildPrompt\(\s*(?:liveOutline|liveSections)\.map\(/.test(src),
     'le run principal appelle buildPrompt(<sections vivantes>.map(...))');
}

console.log(failures ? `\n${failures} échec(s)` : '\nTous les tests passent.');
process.exit(failures ? 1 : 0);
