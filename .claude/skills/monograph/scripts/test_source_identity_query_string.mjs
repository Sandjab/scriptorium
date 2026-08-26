// Test de l'IDENTITÉ DES SOURCES quand l'identifiant du document vit dans la QUERY STRING.
// Couvre les trois workflows (monograph, frugalmonograph, leanmonograph).
//
// Lancer :  node .claude/skills/monograph/scripts/test_source_identity_query_string.mjs
//
// CE QUE CES TESTS PROTÈGENT, ET POURQUOI
//
//   `normUrl` sert à décider si deux entrées désignent le MÊME travail. Il doit trancher dans
//   les deux sens, et les deux erreurs coûtent cher :
//
//     — Sur-compter (FAUSSE INDÉPENDANCE) : la même page citée sous deux titres, ou un miroir,
//       comptée pour deux sources → le seuil ≥2 se contourne sans qu'on le veuille. C'est le
//       bug du 32e run, réparé en posant TOUJOURS une clé d'URL.
//     — Sous-compter (FAUSSE DÉPENDANCE) : deux documents RÉELLEMENT distincts écrasés en un
//       seul → faux rejets. C'est le bug trouvé au 43e run (inhibiteurs-pde5) : `normUrl`
//       supprimait toute la query string par `.replace(/[#?].*$/,'')`, or DailyMed identifie
//       chaque notice par `?setid=`. Les étiquetages FDA du sildénafil, du tadalafil et du
//       vardénafil — trois médicaments, trois documents — se normalisaient tous en
//       « dailymed.nlm.nih.gov/dailymed/druginfo.cfm » et ne valaient qu'UNE source.
//       Conséquence mesurée : deux claims de la section sécurité (délais avant nitré, seuils de
//       priapisme) rejetés à tort, puis re-cassés à l'assemblage après réparation manuelle.
//
//   Ces tests encodent la FRONTIÈRE entre les deux : la query string porte l'identité et doit
//   être conservée, SAUF les paramètres de suivi, qui ne désignent pas un document mais la
//   façon dont on y est arrivé. Ils doivent tomber si l'un des deux côtés se relâche.
//
// Technique : on extrait le bloc de fonctions pures (normUrl, docKeys, collectSources) de chaque
// workflow.js et on l'importe — même procédé que test_audit_document_source.mjs. Le workflow
// entier n'est pas exécutable ici (idiome `return` top-level, cf. workflow-js-verification).

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
  // normUrl s'étend sur plusieurs lignes depuis le correctif du 43e run (query string
  // conservée, paramètres de suivi retirés). On prend sa DÉCLARATION SEULE, accolades
  // équilibrées : le segment jusqu'à docKeys embarquerait au passage des constantes qui lisent
  // les `args` du harness (MAX_SECTIONS dans leanmonograph) et le module ne chargerait pas.
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
  const modPath = join(tmpdir(), `srcid_under_test_${name}_${process.pid}.mjs`);
  writeFileSync(modPath,
    `${src.slice(normAt, normEnd)}\n${src.slice(start, end)}\nexport { normUrl, docKeys, collectSources };\n`, 'utf8');
  try { return await import(pathToFileURL(modPath).href); }
  finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }
}

// ── Fixtures : les trois étiquetages réellement en cause au 43e run ─────────
const DM = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=';
const sildenafil = { title: 'VIAGRA (sildenafil) — FDA label', url: `${DM}4d60822d-1c9b-494d-adb3-20fe921d9c58` };
const tadalafil  = { title: 'CIALIS (tadalafil) — FDA label',  url: `${DM}ebddb745-81f9-4b25-8739-b2886032ed26` };
const vardenafil = { title: 'LEVITRA (vardénafil) — FDA label', url: `${DM}b3bbc16e-8305-469a-9dc3-8e698339a98b` };

// Le même document, cité autrement : ne doit JAMAIS compter deux fois (garde du 32e run).
const sildenafilAutreTitre = { title: 'Notice du citrate de sildénafil', url: sildenafil.url };
const sildenafilAvecSuivi  = { title: 'VIAGRA via une newsletter', url: `${sildenafil.url}&utm_source=nl&utm_medium=email` };
const sildenafilAvecAncre  = { title: 'VIAGRA, section interactions', url: `${sildenafil.url}#nitrates` };

const verdict = (sources) => ({ holds: true, independent_sources: sources });

const CASES = [
  {
    label: 'trois notices DailyMed de trois médicaments → TROIS sources (le bug du 43e run)',
    run: ({ collectSources }) => collectSources([verdict([sildenafil, tadalafil, vardenafil])]).length === 3,
  },
  {
    label: 'deux notices réparties sur deux jurés → DEUX sources, le seuil ≥2 est atteint',
    run: ({ collectSources }) => collectSources([verdict([sildenafil]), verdict([tadalafil])]).length === 2,
  },
  {
    label: 'même URL sous deux titres différents → UNE source (garde du 32e run)',
    run: ({ collectSources }) => collectSources([verdict([sildenafil, sildenafilAutreTitre])]).length === 1,
  },
  {
    label: 'paramètres de suivi (utm_*) → UNE source : ils disent le chemin, pas le document',
    run: ({ collectSources }) => collectSources([verdict([sildenafil, sildenafilAvecSuivi])]).length === 1,
  },
  {
    label: "ancre de section (#nitrates) → UNE source : c'est un endroit dans le document",
    run: ({ collectSources }) => collectSources([verdict([sildenafil, sildenafilAvecAncre])]).length === 1,
  },
  {
    label: 'normUrl conserve un setid distinct',
    run: ({ normUrl }) => normUrl(sildenafil.url) !== normUrl(tadalafil.url),
  },
  {
    label: 'normUrl ignore la casse et le slash final',
    run: ({ normUrl }) => normUrl('HTTPS://Example.ORG/Doc/') === normUrl('http://example.org/doc'),
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
