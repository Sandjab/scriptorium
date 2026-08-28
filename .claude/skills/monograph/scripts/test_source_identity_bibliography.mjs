// Test de l'IDENTITÉ DES SOURCES au moment de l'ASSEMBLAGE de knowledge.json (`ensureSrc`).
// Couvre les trois workflows (monograph, frugalmonograph, leanmonograph).
//
// Lancer :  node .claude/skills/monograph/scripts/test_source_identity_bibliography.mjs
//
// CE QUE CES TESTS PROTÈGENT, ET POURQUOI
//
//   Il y a DEUX endroits où l'identité d'une source est décidée, et jusqu'au 46e run ils ne
//   suivaient pas la même règle :
//
//     collectSources()  — le SEUIL ≥2 par claim, indexé par `docKeys` (identité de DOCUMENT) ;
//     ensureSrc()       — la LISTE GLOBALE des sources, indexée par `normUrl` (identité d'URL).
//
//   Conséquence observée au 46e run (nootropiques-panorama) : Jędrejko et al. 2023 figurait
//   DEUX fois dans `knowledge.json` et donc deux fois en bibliographie —
//
//       doi.org/10.1002/dta.3529                                            ← cité par un claim
//       analyticalsciencejournals.onlinelibrary.wiley.com/doi/abs/10.1002/dta.3529  ← par un autre
//
//   `docKeys` rapprochait pourtant déjà correctement ces deux URLs (même clé `doi:`), si bien
//   qu'AUCUN claim ne comptait le travail deux fois : le seuil ≥2 n'a jamais été en danger.
//   Le défaut est resté invisible au council, au lint et au contrôle d'acceptation, et n'a été
//   trouvé qu'en passant la bibliographie au crible après un build vert. Un lecteur qui compte
//   les sources d'un document de référence y lisait deux travaux là où il n'y en a qu'un.
//
//   LA FRONTIÈRE QUE CES TESTS ENCODENT — et pourquoi la fusion est VOLONTAIREMENT étroite :
//   `ensureSrc` ne fusionne que sur un IDENTIFIANT FORT (arxiv:, doi:), jamais sur le titre.
//   Sur-fusionner ici ne ferait pas rejeter un claim (comme dans collectSources) : cela ferait
//   DISPARAÎTRE une source réelle de la bibliographie, en silence. Deux documents distincts qui
//   partagent un titre tronqué doivent donc rester deux entrées.

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

// Extrait le bloc d'identité (TRACKING_PARAMS/normUrl → docKeys) puis le bloc d'assemblage
// (srcId/sources/ensureSrc), et en fait un module importable. Le workflow entier n'est pas
// exécutable ici (idiome `return` top-level, cf. workflow-js-verification).
//
// ⚠ Le chemin du module est UNIQUE à chaque chargement : `srcId`/`sources` sont un état de
// module, et Node met les modules en cache par URL. Réutiliser le même chemin rendrait les
// comptages cumulatifs d'un cas à l'autre — le test passerait ou échouerait pour de mauvaises
// raisons, ce qui est pire que pas de test.
let loadSeq = 0;
async function loadPure(name) {
  const src = readFileSync(join(skills, name, 'workflow.js'), 'utf8');
  const trackAt = src.search(/^const TRACKING_PARAMS\b/m);
  const nuAt = src.search(/^const normUrl\b/m);
  const normAt = trackAt >= 0 ? trackAt : nuAt;
  let normEnd = -1;
  if (nuAt >= 0) {
    const brace = src.indexOf('{', nuAt), eol = src.indexOf('\n', nuAt);
    if (brace < 0 || brace > eol) normEnd = eol;
    else { let d = 0;
      for (let j = brace; j < src.length; j++) {
        if (src[j] === '{') d++;
        else if (src[j] === '}') { d--; if (d === 0) { normEnd = src.indexOf(';', j) + 1; break; } }
      } }
  }
  const dkAt = src.indexOf('const docKeys');
  const dkEnd = src.indexOf('};', dkAt) + 2;
  const asmAt = src.indexOf('const srcId = new Map();');
  const esAt = src.indexOf('function ensureSrc', asmAt);
  if (normAt < 0 || normEnd < 0 || dkAt < 0 || asmAt < 0 || esAt < 0)
    throw new Error(`${name} : bloc d'assemblage introuvable`);
  let i = src.indexOf('{', esAt), depth = 0, esEnd = -1;
  for (; i < src.length; i++) {
    if (src[i] === '{') depth++;
    else if (src[i] === '}') { depth--; if (depth === 0) { esEnd = i + 1; break; } }
  }
  if (esEnd < 0) throw new Error(`${name} : fin de ensureSrc introuvable`);
  const modPath = join(tmpdir(), `srcid_biblio_under_test_${name}_${process.pid}_${++loadSeq}.mjs`);
  writeFileSync(modPath,
    `${src.slice(normAt, normEnd)}\n${src.slice(dkAt, dkEnd)}\n${src.slice(asmAt, esEnd)}\n` +
    `export { normUrl, docKeys, ensureSrc, sources };\n`, 'utf8');
  try { return await import(pathToFileURL(modPath).href); }
  finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }
}

// ── Fixtures : le doublon réellement observé au 46e run, et ses voisins ────────────────────
// Jędrejko et al. 2023, « Unauthorized ingredients in "nootropic" dietary supplements »,
// Drug Testing and Analysis — cité par deux claims sous deux formes.
const jedrejkoDoiOrg = { title: 'Jędrejko K. et al. — Unauthorized ingredients in « nootropic » dietary supplements (Drug Test Anal 2023)',
                         url: 'https://doi.org/10.1002/dta.3529' };
const jedrejkoWiley  = { title: 'Jędrejko et al. 2023, Drug Testing and Analysis — revue des ingrédients non autorisés',
                         url: 'https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/abs/10.1002/dta.3529' };
// Un AUTRE article, DOI distinct : doit rester une entrée séparée.
const vanhee = { title: 'Vanhee C. et al. — The Occurrence of Illicit Smart Drugs or Nootropics in Europe and Australia (J Xenobiot 2025)',
                 url: 'https://doi.org/10.3390/jox15030088' };
// Non-régression du 43e run : deux notices distinctes identifiées par la QUERY STRING, sans DOI.
const DM = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=';
const sildenafil = { title: 'VIAGRA (sildenafil) — FDA label', url: `${DM}4d60822d-1c9b-494d-adb3-20fe921d9c58` };
const tadalafil  = { title: 'CIALIS (tadalafil) — FDA label',  url: `${DM}ebddb745-81f9-4b25-8739-b2886032ed26` };
// Non-régression du 32e run : la MÊME page citée sous deux titres → un seul id.
const memePage1 = { title: 'Cochrane CD001011 — piracetam pour la démence', url: 'https://www.cochrane.org/evidence/CD001011' };
const memePage2 = { title: 'Revue Cochrane sur le piracétam',                url: 'https://www.cochrane.org/evidence/CD001011' };
// FRONTIÈRE de sur-fusion : deux rapports DIFFÉRENTS dont le titre tronqué coïncide, sans
// identifiant fort commun. Ils doivent rester DEUX entrées — fusionner par titre ferait
// disparaître une source réelle de la bibliographie.
const rapportA = { title: 'Rapport annuel de pharmacovigilance — édition 2023', url: 'https://agence.example.org/rapports/2023' };
const rapportB = { title: 'Rapport annuel de pharmacovigilance — édition 2024', url: 'https://agence.example.org/rapports/2024' };

const CASES = [
  {
    label: 'doi.org et /doi/abs/ du MÊME article → UNE entrée de bibliographie (doublon du 46e run)',
    run: ({ ensureSrc, sources }) => {
      ensureSrc(jedrejkoDoiOrg); ensureSrc(jedrejkoWiley);
      return sources.length === 1;
    },
  },
  {
    label: 'les deux formes reçoivent le MÊME id de source',
    run: ({ ensureSrc }) => ensureSrc(jedrejkoDoiOrg) === ensureSrc(jedrejkoWiley),
  },
  {
    label: 'FRONTIÈRE : deux DOI distincts → DEUX entrées (ne pas sur-fusionner)',
    run: ({ ensureSrc, sources }) => {
      ensureSrc(jedrejkoDoiOrg); ensureSrc(vanhee);
      return sources.length === 2;
    },
  },
  {
    label: 'non-régression 43e run : deux notices DailyMed (query string, sans DOI) → DEUX entrées',
    run: ({ ensureSrc, sources }) => {
      ensureSrc(sildenafil); ensureSrc(tadalafil);
      return sources.length === 2;
    },
  },
  {
    label: 'non-régression 32e run : même URL sous deux titres → UNE entrée',
    run: ({ ensureSrc, sources }) => {
      ensureSrc(memePage1); ensureSrc(memePage2);
      return sources.length === 1;
    },
  },
  {
    label: 'FRONTIÈRE : deux documents au titre tronqué identique, sans identifiant commun → DEUX entrées',
    run: ({ ensureSrc, sources }) => {
      ensureSrc(rapportA); ensureSrc(rapportB);
      return sources.length === 2;
    },
  },
  {
    label: 'une source sans URL ne produit aucune entrée',
    run: ({ ensureSrc, sources }) => ensureSrc({ title: 'sans url', url: '' }) === null && sources.length === 0,
  },
];

for (const name of WORKFLOWS) {
  console.log(`\n${name} :`);
  for (const c of CASES) {
    // Chaque cas repart d'un module FRAIS : `sources` est un état de module, il ne doit pas
    // fuir d'un cas à l'autre (sinon les comptages deviennent cumulatifs et le test ment).
    let pure;
    try { pure = await loadPure(name); }
    catch (e) { failures++; console.error(`  ✗ chargement impossible — ${e.message}`); break; }
    let res;
    try { res = c.run(pure); }
    catch (e) { res = false; console.error(`    (exception : ${e.message})`); }
    ok(res, c.label);
  }
}

console.log(failures ? `\n${failures} échec(s)` : '\nOK — identité de bibliographie tenue');
process.exit(failures ? 1 : 0);
