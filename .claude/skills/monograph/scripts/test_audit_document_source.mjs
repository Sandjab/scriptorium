// Test de la DÉCISION D'AUDIT des trois workflows (monograph, frugalmonograph, leanmonograph).
//
// Lancer :  node .claude/skills/monograph/scripts/test_audit_document_source.mjs   (exit ≠ 0 si échec)
//
// Ce que ces tests protègent, et POURQUOI :
//
//   Le seuil « ≥ 2 sources indépendantes » est la garantie centrale du scriptorium (CLAUDE.md).
//   Le 2026-08-10 (berberine) puis le 2026-08-15 (cafeine-ergogene), il a produit des FAUX REJETS
//   sur une classe précise d'énoncés : ceux qui décrivent le contenu d'un document de référence
//   (« la position stand ISSN retient 3-6 mg/kg »). Ces énoncés n'ont qu'une source PAR NATURE —
//   on ne corrobore pas « ce document dit X » par un second document. L'exception « document-source »
//   a donc été ouverte, mais elle est DANGEREUSE : mal bornée, elle rouvre le seuil pour tout.
//
//   Ces tests encodent les BORNES, pas seulement le comportement nominal. Ils doivent tomber si :
//     — le seuil général se relâche (cas « seuil mordant ») ;
//     — l'exception cesse d'exiger l'UNANIMITÉ des jurés (cas « fail closed ») ;
//     — un claim RÉFUTÉ par un juré passe malgré tout (cas « réfutation ») ;
//     — la note d'audit se remet à prétendre plusieurs sources (cas « note honnête »),
//       ce qui était précisément le contournement silencieux trouvé sur berberine.
//
// Technique : on extrait le bloc de fonctions PURES (normUrl → decideAudit) de chaque workflow.js,
// on l'écrit dans un module temporaire qui l'exporte, et on l'importe — même procédé que
// test_resume.mjs. Le workflow entier n'est pas exécutable ici (idiome `return` top-level,
// cf. mémoire workflow-js-verification) et n'a pas besoin de l'être : la règle testée est pure.

import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
const skills = join(here, '..', '..');
const WORKFLOWS = ['monograph', 'frugalmonograph', 'leanmonograph'];

let failures = 0;
const ok = (cond, label) => {
  if (!cond) { failures++; console.error(`  ✗ ${label}`); } else { console.log(`  ✓ ${label}`); }
};

// ── Extraction du bloc pur, puis import d'un module temporaire ───────────────
async function loadDecider(name) {
  const src = readFileSync(join(skills, name, 'workflow.js'), 'utf8');
  // On ne prend QUE les fonctions pures dont dépend decideAudit : la ligne normUrl, puis le bloc
  // docKeys → decideAudit. Prendre l'intervalle complet embarquerait au passage des constantes
  // qui lisent les `args` du harness (MAX_SECTIONS dans leanmonograph) et le module ne chargerait pas.
  const normLine = src.match(/^const normUrl = .*$/m);
  const start = src.indexOf('const docKeys');
  const fnAt = src.indexOf('function decideAudit', start);
  if (!normLine || start < 0 || fnAt < 0) throw new Error(`${name} : bloc d'audit introuvable`);
  let i = src.indexOf('{', fnAt), depth = 0, end = -1;
  for (; i < src.length; i++) {
    if (src[i] === '{') depth++;
    else if (src[i] === '}') { depth--; if (depth === 0) { end = i + 1; break; } }
  }
  if (end < 0) throw new Error(`${name} : fin de decideAudit introuvable`);
  const modPath = join(tmpdir(), `audit_under_test_${name}_${process.pid}.mjs`);
  writeFileSync(modPath, `${normLine[0]}\n${src.slice(start, end)}\nexport { decideAudit };\n`, 'utf8');
  try { return (await import(pathToFileURL(modPath).href)).decideAudit; }
  finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }
}

// ── Fixtures ─────────────────────────────────────────────────────────────────
const claim = { statement: 'La position stand ISSN 2021 retient une plage de 3 à 6 mg/kg.' };
const srcA = { title: 'ISSN position stand: caffeine and exercise performance', url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7777221/' };
const srcB = { title: 'Grgic et al., umbrella review of caffeine meta-analyses', url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6839090/' };

const juror = (o = {}) => ({
  holds: true, corrected_statement: '', independent_sources: [srcA],
  note: '', search_exhausted: false, document_source: false, ...o,
});

const CASES = [
  {
    label: 'nominal — 2 jurés, 2 sources distinctes → confirmed par le seuil normal',
    verdicts: [juror({ independent_sources: [srcA] }), juror({ independent_sources: [srcB] })],
    expect: v => v.audit === 'confirmed' && /2 sources indépendantes/.test(v.note),
  },
  {
    label: 'seuil mordant — 2 jurés mais 1 SEULE source, sans document_source → rejected',
    verdicts: [juror(), juror()],
    expect: v => v.audit === 'rejected',
  },
  {
    label: 'exception — 2 jurés unanimes + document_source, 1 source → confirmed',
    verdicts: [juror({ document_source: true }), juror({ document_source: true })],
    expect: v => v.audit === 'confirmed' && /UNIQUE PAR NATURE/.test(v.note),
  },
  {
    label: "note honnête — l'exception ne prétend JAMAIS plusieurs sources indépendantes",
    verdicts: [juror({ document_source: true }), juror({ document_source: true })],
    expect: v => !/\d+ sources indépendantes/.test(v.note),
  },
  {
    label: 'fail closed — un seul juré qualifie document_source → rejected',
    verdicts: [juror({ document_source: true }), juror({ document_source: false })],
    expect: v => v.audit === 'rejected',
  },
  {
    label: "réfutation — 2 jurés document_source mais un 3e réfute → pas d'unanimité → rejected",
    verdicts: [juror({ document_source: true }), juror({ document_source: true }),
               juror({ holds: false, document_source: false, independent_sources: [] })],
    expect: v => v.audit === 'rejected',
  },
  {
    label: 'rien de vérifié — document_source unanime mais AUCUNE source → rejected',
    verdicts: [juror({ document_source: true, independent_sources: [] }),
               juror({ document_source: true, independent_sources: [] })],
    expect: v => v.audit === 'rejected',
  },
  {
    label: 'chemin corrigé intact — 1 tient + 1 corrige, 2 sources → corrected',
    verdicts: [juror({ independent_sources: [srcA] }),
               juror({ holds: false, corrected_statement: 'Énoncé corrigé.', independent_sources: [srcB] })],
    expect: v => v.audit === 'corrected' && v.statement === 'Énoncé corrigé.',
  },
  {
    label: 'la même URL sous deux titres ne vaut pas 2 sources (régression 32e run)',
    verdicts: [juror({ independent_sources: [srcA] }),
               juror({ independent_sources: [{ title: 'Autre titre pour la même page', url: srcA.url }] })],
    expect: v => v.audit === 'rejected',
  },
];

// ── Exécution ────────────────────────────────────────────────────────────────
const verdictsByWorkflow = {};
for (const name of WORKFLOWS) {
  console.log(`\n${name} :`);
  const decideAudit = await loadDecider(name);
  verdictsByWorkflow[name] = CASES.map(c => decideAudit(claim, c.verdicts));
  CASES.forEach((c, i) => ok(c.expect(verdictsByWorkflow[name][i]), c.label));
}

console.log('\nles trois workflows :');
CASES.forEach((c, i) => {
  const audits = WORKFLOWS.map(w => verdictsByWorkflow[w][i].audit);
  ok(new Set(audits).size === 1, `verdict identique sur « ${c.label.split(' —')[0]} » (${audits.join(', ')})`);
});

console.log(failures ? `\n${failures} échec(s)` : '\nTous les tests passent.');
process.exit(failures ? 1 : 0);
