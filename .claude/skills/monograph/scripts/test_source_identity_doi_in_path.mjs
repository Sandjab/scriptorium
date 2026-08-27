// Test de l'IDENTITÉ DES SOURCES quand le DOI vit dans le CHEMIN de l'éditeur.
// Couvre les trois workflows (monograph, frugalmonograph, leanmonograph).
//
// Lancer :  node .claude/skills/monograph/scripts/test_source_identity_doi_in_path.mjs
//
// CE QUE CES TESTS PROTÈGENT, ET POURQUOI
//
//   Symétrique du bug du 43e run (cf. test_source_identity_query_string.mjs, qui protège contre
//   la FAUSSE DÉPENDANCE : deux documents distincts écrasés en un). Ici c'est l'autre erreur, la
//   FAUSSE INDÉPENDANCE : un SEUL article compté pour DEUX sources, ce qui fait franchir le
//   seuil ≥2 à un claim qui n'a en réalité qu'une source.
//
//   Bug du 45e run (microdosage-psychedeliques, claim:41) : `docKeys` savait déjà rapprocher
//   les variantes de rendu d'arXiv (/abs/, /html/, /pdf/) et n'extrayait le DOI que derrière
//   « doi.org/ ». Or les éditeurs posent le DOI dans LEUR propre chemin, derrière un segment de
//   rendu qui change d'une citation à l'autre :
//
//       journals.sagepub.com/doi/pdf/10.1177/0269881119857204   ← un juré cite le PDF
//       journals.sagepub.com/doi/10.1177/0269881119857204       ← l'autre cite la page
//
//   Aucune clé commune : ni arxiv:, ni doi: (pas de doi.org), ni url: (les chemins diffèrent),
//   et le titre suffisait rarement à rattraper. Le compteur lisait 2 sources là où il n'y a
//   qu'un article. Le claim passait le seuil sans l'avoir atteint.
//
//   Ces tests encodent la FRONTIÈRE : le DOI identifie le document où qu'il apparaisse, mais
//   deux DOI distincts restent deux documents. Ils doivent tomber si l'un des deux côtés se
//   relâche — sur-fusionner serait aussi grave que sur-compter.
//
// Technique : identique à test_source_identity_query_string.mjs — on extrait le bloc de
// fonctions pures de chaque workflow.js et on l'importe (le workflow entier n'est pas
// exécutable ici, idiome `return` top-level, cf. workflow-js-verification).

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

async function loadPure(name) {
  const src = readFileSync(join(skills, name, 'workflow.js'), 'utf8');
  const trackAt = src.search(/^const TRACKING_PARAMS\b/m);
  const nuAt = src.search(/^const normUrl\b/m);
  const normAt = trackAt >= 0 ? trackAt : nuAt;
  let normEnd = -1;
  if (nuAt >= 0) {
    const brace = src.indexOf('{', nuAt), eol = src.indexOf('\n', nuAt);
    if (brace < 0 || brace > eol) normEnd = eol;              // forme mono-ligne (historique)
    else { let d = 0;
      for (let j = brace; j < src.length; j++) {
        if (src[j] === '{') d++;
        else if (src[j] === '}') { d--; if (d === 0) { normEnd = src.indexOf(';', j) + 1; break; } }
      } }
  }
  const start = src.indexOf('const docKeys');
  const fnAt = src.indexOf('function collectSources', start);
  if (normAt < 0 || normEnd < 0 || start < 0 || fnAt < 0) throw new Error(`${name} : bloc d'identité introuvable`);
  let i = src.indexOf('{', fnAt), depth = 0, end = -1;
  for (; i < src.length; i++) {
    if (src[i] === '{') depth++;
    else if (src[i] === '}') { depth--; if (depth === 0) { end = i + 1; break; } }
  }
  if (end < 0) throw new Error(`${name} : fin de collectSources introuvable`);
  const modPath = join(tmpdir(), `srcid_doi_under_test_${name}_${process.pid}.mjs`);
  writeFileSync(modPath,
    `${src.slice(normAt, normEnd)}\n${src.slice(start, end)}\nexport { normUrl, docKeys, collectSources };\n`, 'utf8');
  try { return await import(pathToFileURL(modPath).href); }
  finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }
}

// ── Fixtures : l'article réellement en cause au 45e run, et son voisin d'éditeur ────────────
// Kuypers et al. 2019, « Microdosing psychedelics: More questions than answers? », J Psychopharmacol.
const SAGE = 'https://journals.sagepub.com/doi';
const kuypersPdf  = { title: 'Microdosing psychedelics: more questions than answers? (PDF)', url: `${SAGE}/pdf/10.1177/0269881119857204` };
const kuypersPage = { title: 'Kuypers et al. 2019, J Psychopharmacol',                        url: `${SAGE}/10.1177/0269881119857204` };
const kuypersFull = { title: 'Kuypers 2019 — texte intégral',                                 url: `${SAGE}/full/10.1177/0269881119857204` };
const kuypersExt  = { title: 'Kuypers 2019 — fichier',                                        url: `${SAGE}/pdf/10.1177/0269881119857204.pdf` };
// Deux AUTRES articles du même éditeur, réellement cités par le même thème : DOI distincts.
const halman      = { title: 'Halman et al. 2024, interactions des psychédéliques classiques', url: `${SAGE}/10.1177/02698811231211219` };
const valvulo     = { title: 'Microdosage chronique et valvulopathie (2024)',                  url: `${SAGE}/10.1177/02698811231225609` };
// Le DOI derrière doi.org doit continuer de marcher (non-régression).
const parDoiOrg   = { title: 'Kuypers 2019 via doi.org', url: 'https://doi.org/10.1177/0269881119857204' };
// Non-régression du 43e run : identité portée par la query string, sans aucun DOI.
const DM = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=';
const sildenafil = { title: 'VIAGRA (sildenafil) — FDA label', url: `${DM}4d60822d-1c9b-494d-adb3-20fe921d9c58` };
const tadalafil  = { title: 'CIALIS (tadalafil) — FDA label',  url: `${DM}ebddb745-81f9-4b25-8739-b2886032ed26` };

const verdict = (sources) => ({ holds: true, independent_sources: sources });

const CASES = [
  {
    label: 'PDF et page du MÊME article SAGE → UNE source (le bug du 45e run)',
    run: ({ collectSources }) => collectSources([verdict([kuypersPdf, kuypersPage])]).length === 1,
  },
  {
    label: 'les deux formes réparties sur DEUX jurés → UNE source : le seuil ≥2 N\'est PAS atteint',
    run: ({ collectSources }) => collectSources([verdict([kuypersPdf]), verdict([kuypersPage])]).length === 1,
  },
  {
    label: '/pdf/, /full/ et l\'URL nue du même DOI → UNE source',
    run: ({ collectSources }) => collectSources([verdict([kuypersPdf, kuypersFull, kuypersPage])]).length === 1,
  },
  {
    label: 'extension finale (« …204.pdf ») → même document que « …204 »',
    run: ({ collectSources }) => collectSources([verdict([kuypersExt, kuypersPage])]).length === 1,
  },
  {
    label: 'même DOI via doi.org et via le chemin de l\'éditeur → UNE source',
    run: ({ collectSources }) => collectSources([verdict([parDoiOrg, kuypersPage])]).length === 1,
  },
  {
    label: 'FRONTIÈRE : deux DOI distincts du même éditeur → DEUX sources (ne pas sur-fusionner)',
    run: ({ collectSources }) => collectSources([verdict([halman, valvulo])]).length === 2,
  },
  {
    label: 'FRONTIÈRE : trois articles SAGE distincts → TROIS sources',
    run: ({ collectSources }) => collectSources([verdict([kuypersPage, halman, valvulo])]).length === 3,
  },
  {
    label: 'docKeys pose bien une clé doi: pour une URL d\'éditeur',
    run: ({ docKeys }) => docKeys(kuypersPage).some(k => k === 'doi:10.1177/0269881119857204'),
  },
  {
    label: 'non-régression 43e run : deux notices DailyMed (query string, sans DOI) → DEUX sources',
    run: ({ collectSources }) => collectSources([verdict([sildenafil, tadalafil])]).length === 2,
  },
];

for (const name of WORKFLOWS) {
  console.log(`\n${name} :`);
  let pure;
  try { pure = await loadPure(name); }
  catch (e) { failures++; console.error(`  ✗ chargement impossible — ${e.message}`); continue; }
  for (const c of CASES) {
    let got;
    try { got = c.run(pure); } catch (e) { got = false; console.error(`    (exception : ${e.message})`); }
    ok(got, c.label);
  }
}

console.log(failures ? `\n${failures} échec(s)` : '\nTous les tests passent.');
process.exit(failures ? 1 : 0);
