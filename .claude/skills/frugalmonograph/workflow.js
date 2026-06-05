export const meta = {
  name: 'frugalmonograph',
  description: "Variante FRUGALE de monograph : même pipeline vérifié (Sweep→Plan→Extract→Verify→Author→Widgets→Compose→Build), mais modèles moins chers sur la recherche/vérification, council réduit (2 jurés) et plafonds durs — pour produire une monographie HTML à coût réduit.",
  whenToUse: "Lancé par le skill /frugalmonograph. Reçoit args:{subject, slug, themeDir} et peuple themeDir/ avant build.py (réutilise build.py/charte de monograph).",
  phases: [
    { title: 'Sweep',   detail: 'recherche web multi-angles ; collecte de sources', model: 'sonnet' },
    { title: 'Plan',    detail: 'plan du document depuis les sources' },
    { title: 'Extract', detail: 'claims candidats + prose par section', model: 'sonnet' },
    { title: 'Verify',  detail: 'council adversarial par claim ; ≥2 sources indépendantes', model: 'sonnet' },
    { title: 'Author',  detail: 'écrit knowledge/glossary/tldr' },
    { title: 'Widgets', detail: 'sélection des concepts (planner) puis fan-out codeurs + critic' },
    { title: 'Compose', detail: 'écrit le manifeste unique (best-of)' },
    { title: 'Build',   detail: 'python3 build.py → 1 HTML + auto-vérifs' },
  ],
};

// ─────────────────────────────────────────────────────────────────────────────
// Contrainte d'architecture : un script Workflow n'a AUCUN accès filesystem.
// Donc phases 1-3 (jugement de recherche) retournent des données structurées AU
// script ; les FAITS vérifiés sont assemblés en JS (frontière code/jugement) ;
// phases 4-6 sont des agents qui ÉCRIVENT les fichiers du thème (ils ont Write/Bash).
// build.py (phase 6) reste le seul assembleur déterministe HTML.
// ─────────────────────────────────────────────────────────────────────────────

// args peut arriver objet OU chaîne JSON selon le marshalling — tolère les deux.
const A0 = (typeof args === 'string') ? JSON.parse(args) : (args || {});
const { subject, slug, themeDir } = A0;
if (!subject || !slug || !themeDir)
  throw new Error('args manquants : attendu {subject, slug, themeDir}. Reçu : ' + JSON.stringify(args));
const repoRoot = themeDir.replace(/\/themes\/[^/]+\/?$/, '');
const buildScript = repoRoot + '/.claude/skills/monograph/scripts/build.py';
// Reprise disque (Fix 2) : survit à /clear et au changement de session, contrairement au cache
// moteur (resumeFromRunId, same-session, historiquement peu fiable). args.resume=true → on RELIT
// les checkpoints incrémentaux de themeDir/.monograph/ et on saute le travail déjà fait (Sweep+Plan,
// sections déjà auditées, widgets). Un run FRAIS (sans resume) les IGNORE et les RÉÉCRIT : l'intention
// fraîche-vs-reprise est portée par args.resume, jamais devinée.
const RESUME = (A0.resume === true) || (String(A0.resume) === 'true');
const ckptDir = themeDir + '/.frugalmonograph';   // checkpoints isolés de /monograph : pas de collision de reprise sur un même thème

const WEB = 'Utilise WebSearch et WebFetch (charge-les via ToolSearch "select:WebSearch,WebFetch" si absents). Cite des URL réelles, jamais inventées.';

// Politique terminologique : éviter la francisation systématique des termes dont la forme
// anglaise fait référence. Injectée dans les prompts qui RÉDIGENT (Plan, Extract, Author).
const TERMINO = `TERMINOLOGIE (anglais en tête) : pour tout concept dont la littérature emploie une forme anglaise de référence — Y COMPRIS quand un calque français circule — mets le TERME ANGLAIS EN TÊTE et donne la forme française en glose à la 1re occurrence SEULEMENT, puis emploie l'anglais seul. Ex. : « chain rule (dérivation des fonctions composées) », « backpropagation (rétropropagation) », « forward pass / backward pass », « learning rate », « vanishing / exploding gradient », « gradient clipping ». NUANCE GRAMMATICALE : seul le NOM bascule en anglais ; garde les formes VERBALES/participes françaises (« rétropropagé », « rétropropage ») — n'anglicise jamais un verbe au milieu d'une phrase. BANNIS les calques (ni vrai français ni anglais : « règle de la chaîne », « écrêtage de gradient »…). N'anglicise PAS le vocabulaire français naturalisé et non-calque (descente de gradient, couche, poids, perte, dérivée, fonction d'activation, connexions résiduelles, graphe de calcul). Les termes déjà anglais (ReLU, Adam, ResNet, batch normalization, internal covariate shift…) restent tels quels. Glossaire : le champ "term" = la forme anglaise canonique (glose française dans la définition).`;

// Tous les agents tournent en general-purpose (Tools: *) → WebSearch/WebFetch/Write/Bash garantis.
const A = (prompt, opts) => agent(prompt, { agentType: 'general-purpose', ...opts });

// FRUGALITÉ — modèles par classe de tâche. C'est le levier de coût principal : les phases de
// RECHERCHE et de VÉRIFICATION (Sweep, Extract, Verify, pointeurs) dominent le volume et ne
// requièrent pas Opus (lire des sources et juger qu'un énoncé tient). Le JUGEMENT STRUCTURANT
// garde le modèle hérité (Opus) : Plan (cerveau du doc), Author/Compose (rédaction), Widgets
// (code interactif), Build. Les agents d'I/O (écritures verbatim, lecture des checkpoints) sont
// de simples passthrough sans jugement → modèle bon marché.
const M_RESEARCH = 'sonnet';   // Sweep, Extract, Verify, vérification des pointeurs
const M_IO       = 'sonnet';   // écritures verbatim + checkpoints de reprise (knowledge/sections/research/sec-*/widgets)

// ── Schémas (forcent une sortie structurée validée) ──────────────────────────
const S_SWEEP = { type:'object', additionalProperties:false, required:['sources','findings'], properties:{
  sources:{ type:'array', items:{ type:'object', additionalProperties:false, required:['title','url','kind'],
    properties:{ title:{type:'string'}, url:{type:'string'}, kind:{type:'string'}, note:{type:'string'} } } },
  findings:{ type:'array', items:{ type:'object', additionalProperties:false, required:['point','url'],
    properties:{ point:{type:'string'}, url:{type:'string'} } } } } };

const S_ARCH = { type:'object', additionalProperties:false, required:['title','kicker','outline'], properties:{
  title:{type:'string'}, kicker:{type:'string'},
  outline:{ type:'array', items:{ type:'object', additionalProperties:false, required:['id','heading','angle'],
    properties:{ id:{type:'string'}, heading:{type:'string'}, angle:{type:'string'},
      kind:{ type:'string', enum:['normal','ecosystem'] },
      angle_key:{ type:'string', enum:['foundations','theory','variants','applications','misconceptions','ecosystem'] }
    } } } } };

const S_SECTION = { type:'object', additionalProperties:false, required:['id','heading','prose','claims'], properties:{
  id:{type:'string'}, heading:{type:'string'}, prose:{type:'string'},
  claims:{ type:'array', items:{ type:'object', additionalProperties:false, required:['statement','candidate_sources'],
    properties:{ statement:{type:'string'},
      candidate_sources:{ type:'array', items:{type:'string'} },
      examples:{ type:'array', items:{type:'string'} },
      kind:{ type:'string', enum:['established','contestable'] } } } },
  pointers:{ type:'array', items:{ type:'object', additionalProperties:false, required:['name','url'],
    properties:{ name:{type:'string'}, url:{type:'string'},
      kind:{ type:'string', enum:['library','package','tool','reading','implementation'] },
      blurb:{type:'string'} } } } } };

const S_VERDICT = { type:'object', additionalProperties:false, required:['holds','corrected_statement','independent_sources','note'], properties:{
  holds:{type:'boolean'},
  corrected_statement:{type:'string'},        // "" si rien à corriger
  independent_sources:{ type:'array', items:{ type:'object', additionalProperties:false, required:['title','url'],
    properties:{ title:{type:'string'}, url:{type:'string'} } } },
  note:{type:'string'} } };

const S_POINTERS = { type:'object', additionalProperties:false, required:['pointers'], properties:{
  pointers:{ type:'array', items:{ type:'object', additionalProperties:false, required:['name','url','blurb'],
    properties:{ name:{type:'string'}, url:{type:'string'},
      kind:{ type:'string' }, blurb:{type:'string'} } } } } };

const S_AUTHOR = { type:'object', additionalProperties:false, required:['files_written'], properties:{
  files_written:{ type:'array', items:{type:'string'} } } };

const S_COMPOSE = { type:'object', additionalProperties:false, required:['files_written','element_counts'], properties:{
  files_written:{ type:'array', items:{type:'string'} },
  element_counts:{ type:'object', additionalProperties:false, required:['document'],
    properties:{ document:{type:'integer'} } } } };

const S_WIDGET_PLAN = { type:'object', additionalProperties:false, required:['widgets'], properties:{
  widgets:{ type:'array', items:{ type:'object', additionalProperties:false,
    required:['concept','after_section_id','brief','kind'],
    properties:{ concept:{type:'string'}, after_section_id:{type:'string'}, brief:{type:'string'},
      kind:{ type:'string', enum:['probe','process'] } } } } } };

const S_WIDGET_CODE = { type:'object', additionalProperties:false,
  required:['ref','title','after_section_id','kind'],
  properties:{ ref:{type:'string'}, title:{type:'string'}, after_section_id:{type:'string'},
    kind:{ type:'string', enum:['probe','process'] } } };

const S_WIDGET_CRITIC = { type:'object', additionalProperties:false, required:['ok','issues'],
  properties:{ ok:{type:'boolean'}, issues:{ type:'array', items:{type:'string'} } } };

const S_BUILD = { type:'object', additionalProperties:false, required:['success','files','acceptance','errors'], properties:{
  success:{type:'boolean'},
  files:{ type:'array', items:{type:'string'} },
  build_output:{type:'string'},
  acceptance:{ type:'object', additionalProperties:false, required:['confirmed_claims','all_confirmed_have_2plus_sources','audit_categories_present'],
    properties:{ confirmed_claims:{type:'integer'}, all_confirmed_have_2plus_sources:{type:'boolean'},
      audit_categories_present:{ type:'array', items:{type:'string'} } } },
  errors:{ type:'array', items:{type:'string'} } } };

// Reprise disque (Fix 2) : sortie d'écriture de checkpoint + sonde de chargement.
const S_CKPT = { type:'object', additionalProperties:false, required:['written'], properties:{ written:{type:'boolean'} } };
const S_LOAD = { type:'object', additionalProperties:false, required:['research','sections','widgets'], properties:{
  research:{type:'string'},   // contenu verbatim de research.json ("" si absent)
  widgets:{type:'string'},    // contenu verbatim de widgets.json ("" si absent)
  sections:{ type:'array', items:{ type:'object', additionalProperties:false, required:['id','content'],
    properties:{ id:{type:'string'}, content:{type:'string'} } } } } };

// ── Helpers JS (transformations déterministes — pas de jugement) ─────────────
const normUrl = u => (u||'').trim().replace(/^https?:\/\//i,'').replace(/[#?].*$/,'').replace(/\/+$/,'').toLowerCase();
const SECTION_CLAIM_QUOTA = 2;  // claims survivants (audit ≠ rejected) requis pour qu'une section NORMALE survive à l'élagage
// FRUGALITÉ — plafonds durs (garde-fous coût) : bornent un Plan/Extract qui déraille AVANT
// d'engager le council coûteux. Alignés sur ce que les prompts demandent déjà ('typiquement 4 à 9'
// sections, '2 à 4' claims) : ils ne mordent qu'en cas d'emballement, pas sur le cas nominal.
const MAX_SECTIONS = 9;             // sections traitées (Extract + Verify) au maximum
const MAX_CLAIMS_PER_SECTION = 4;   // claims soumis au council par section au maximum

function dedupSources(list) {
  const seen = new Map();
  for (const s of list) { const k = normUrl(s.url); if (k && !seen.has(k)) seen.set(k, s); }
  return [...seen.values()];
}

// Sources de SOUTIEN uniquement : on n'agrège QUE les independent_sources des verdicts passés.
// Le juré réfutateur (lentille 0) ramène des sources CONTRADICTOIRES — ne jamais les compter
// comme « sources indépendantes » du claim. On ne lui passe donc que les verdicts soutenants.
function collectSources(verdicts) {
  const out = [], seen = new Set();
  for (const v of verdicts) for (const s of (v.independent_sources || [])) {
    const k = normUrl(s.url);
    if (k && !seen.has(k)) { seen.add(k); out.push({ title: s.title || s.url, url: s.url }); }
  }
  return out;
}

// Décision d'audit : le SEUIL est en code ; l'INDÉPENDANCE des sources est jugée par les jurés.
// Le décompte de sources se fait par branche, sur les SEULS verdicts qui appuient le claim
// (confirment, ou corrigent) — d'où un audit strictement plus conservateur qu'avant ce fix.
function decideAudit(claim, verdicts) {
  const holds = verdicts.filter(v => v.holds);
  const corrected = verdicts.filter(v => !v.holds && v.corrected_statement && v.corrected_statement.trim());
  if (holds.length >= 2) {
    const sources = collectSources(holds);                      // confirmé : sources des seuls jurés qui tiennent l'énoncé
    if (sources.length >= 2)
      return { audit:'confirmed', statement: claim.statement, sources,
               note: `Confirmé : ${holds.length}/${verdicts.length} jurés, ${sources.length} sources indépendantes.` };
  }
  if ((holds.length + corrected.length) >= 2) {
    const sources = collectSources([...holds, ...corrected]);   // corrigé : sources de ceux qui confirment OU corrigent
    if (sources.length >= 2)
      return { audit:'corrected', statement: corrected[0].corrected_statement.trim(), sources,
               note: `Énoncé d'origine imprécis, corrigé après vérification (${sources.length} sources indépendantes). Origine : « ${claim.statement} »` };
  }
  const sources = collectSources([...holds, ...corrected]);     // rejeté : on garde le soutien réel (souvent 0-1) pour l'audit
  return { audit:'rejected', statement: claim.statement, sources,
           note: `Rejeté : ${holds.length} confirmation(s), ${sources.length} source(s) indépendante(s) — seuil ≥2 non atteint ou réfuté.` };
}

// ── Prompts (le JUGEMENT du modèle vit ici) ──────────────────────────────────
const ANGLES = [
  { key:'foundations',   label:'définition, origine et principe de fonctionnement' },
  { key:'theory',        label:'propriétés formelles, garanties et limites mathématiques' },
  { key:'variants',      label:'variantes, extensions et état de l’art' },
  { key:'applications',  label:'applications concrètes et systèmes réels qui l’utilisent' },
  { key:'misconceptions',label:'critiques, pièges et idées reçues fréquentes' },
  { key:'ecosystem',     label:'outils, bibliothèques, packages, implémentations de référence et lectures pour aller plus loin' },
];

const sweepPrompt = a => [
  `Sujet : « ${subject} ».`,
  `Angle de recherche : ${a.label}.`,
  WEB,
  `Recherche large puis ouvre 2 à 4 sources sérieuses (papiers, docs officielles, ouvrages, références reconnues — pas de fermes de contenu).`,
  `Rends : (a) "sources" = les sources ouvertes (title, url, kind ∈ paper|docs|book|reference|article) ; (b) "findings" = points factuels précis, chacun avec l'url EXACTE d'où il vient. Un point par fait. Privilégie chiffres, formules, dates, noms.`,
].join('\n');

const archPrompt = (findings, sources) => [
  `Sujet : « ${subject} ». Tu conçois le PLAN d'un document de référence à partir des données de recherche.`,
  TERMINO,
  `Findings (point → url, champ _angle = angle de sweep d'origine) :\n${JSON.stringify(findings)}`,
  `Sources :\n${JSON.stringify(sources.map(s => ({ title:s.title, url:s.url, kind:s.kind })))}`,
  `Rends : title (titre du document, sans suffixe d'édition), kicker (sur-titre court), et outline = AUTANT de sections que la matière trouvée le justifie (typiquement 4 à 9). Propose LARGE : une section par sous-thème réellement documenté. Les sections sans matière vérifiable seront élaguées automatiquement — ne t'autocensure pas, mais n'invente pas de section creuse.`,
  `Chaque section : id (kebab-case ascii, unique), heading, angle (ce qu'elle couvre), angle_key (clé de l'angle de sweep qui l'a principalement documentée, parmi : foundations, theory, variants, applications, misconceptions, ecosystem — si kind="ecosystem" alors angle_key="ecosystem").`,
  `Couvre fondations → propriétés → variantes/applications → limites. Si le sujet a un écosystème d'outils/bibliothèques/packages/lectures, AJOUTE une section finale kind="ecosystem" (heading type « Écosystème & pour aller plus loin »). Les autres sections : kind="normal". Pas de section "glossaire"/"biblio" (ajoutées à la composition).`,
].join('\n');

const extractPrompt = (sec, findings) => [
  `Sujet : « ${subject} ». Section « ${sec.heading} » — angle : ${sec.angle}.`,
  `Findings disponibles (point → url) :\n${JSON.stringify(findings)}`,
  WEB + ' (autorisé pour compléter/préciser une source.)',
  TERMINO,
  `Produis pour CETTE section :`,
  `- prose : autant de paragraphes HTML (<p>…</p>) que la matière de la section l'exige, sans délayer. Prose d'auteur, claire, sans inventer. Pas de titre (le heading est ajouté à l'assemblage).`,
  `- claims : 2 à 4 énoncés factuels vérifiables portés par la section. Pour CHAQUE claim : statement (une phrase nette), candidate_sources (urls qui l'étayent), examples (0-2 exemples concrets), kind.`,
  `IMPORTANT pour exercer la vérification : inclure au moins UN claim kind="contestable" — un énoncé fréquemment affirmé mais possiblement imprécis ou faux (idée reçue), à départager par les jurés. Les autres = kind="established".`,
  `Si CETTE section concerne l'écosystème (outils/bibliothèques/packages/lectures) : remplis "pointers" = liste {name, url (lien officiel réel), kind ∈ library|package|tool|reading|implementation, blurb (1 phrase)}. Les pointeurs ne sont PAS des claims (pas de seuil ≥2 sources) : ce sont des renvois curés. N'invente jamais d'URL.`,
].join('\n');

const LENSES = [
  'RÉFUTATION : cherche activement à INVALIDER l\'énoncé. Trouve des contre-exemples, des nuances, des sources qui le contredisent. Sois sévère.',
  'INDÉPENDANCE : trouve des sources qui CONFIRMENT l\'énoncé MAIS indépendantes entre elles et de l\'origine du claim (pas deux pages qui citent le même papier, pas miroir/repost). Ne liste que des sources réellement indépendantes.',
  'SOURCE PRIMAIRE : remonte à la source faisant autorité (papier original, spécification, manuel) et vérifie que l\'énoncé y correspond EXACTEMENT, sans déformation.',
];
// Noms courts des lentilles (index aligné sur LENSES) — pour le rapport d'audit.
const LENS_NAMES = ['réfutation', 'indépendance', 'source-primaire'];

const verifyPrompt = (claim, lensIdx) => [
  `Énoncé à vérifier : « ${claim.statement} »`,
  `Sources candidates DÉJÀ trouvées en amont — COMMENCE par celles-ci (ouvre-les via WebFetch AVANT toute nouvelle recherche) : ${JSON.stringify(claim.candidate_sources || [])}`,
  `Ton rôle de juré — ${LENSES[lensIdx]}`,
  `MÉTHODE (économie) : examine d'abord les sources candidates ci-dessus ; ne lance une NOUVELLE recherche que si elles sont insuffisantes pour ton rôle, ou pour établir l'indépendance / remonter à la source primaire. ` + WEB,
  `Rends un verdict HONNÊTE : holds (true si l'énoncé tient TEL QUEL), corrected_statement ("" si rien à corriger ; sinon l'énoncé corrigé minimal qui serait vrai), independent_sources (UNIQUEMENT les sources que TOI tu as vérifiées et qui sont indépendantes — title+url réels), note (1-2 phrases justifiant).`,
  `N'invente jamais d'URL. En cas de doute sur l'indépendance ou la véracité, penche vers holds=false.`,
].join('\n');

const pointersPrompt = (candidates) => [
  `Voici des pointeurs candidats (outils/bibliothèques/packages/lectures) extraits de la recherche : ${JSON.stringify(candidates).slice(0, 8000)}`,
  WEB,
  `Pour CHAQUE pointeur, VÉRIFIE que l'URL existe réellement et pointe l'outil/la ressource annoncé(e). GARDE uniquement ceux dont l'URL résout et correspond. Corrige l'URL vers le lien officiel si nécessaire ; n'en invente aucun.`,
  `Rends : pointers = liste finale {name, url (réel), kind, blurb (1 phrase factuelle)}. Liste vide si aucun ne tient.`,
].join('\n');

const authorPrompt = (sectionsBrief) => [
  `Tu es l'auteur. Tu ÉCRIS des fichiers dans le dossier de thème : ${themeDir}`,
  TERMINO,
  `${themeDir}/knowledge.json a été écrit par l'étape précédente — lis-le pour connaître les claims vérifiés avant de rédiger le glossaire et le tldr.`,
  `Assure-toi que le dossier existe (mkdir -p si besoin), puis ÉCRIS exactement ces fichiers :`,
  ``,
  `1) ${themeDir}/glossary.json — un tableau JSON de 4 à 7 termes du sujet : {term, definition, see_also?}. « term » = forme canonique du concept (garde l'anglais si c'est la référence, ex. « embedding ») ; la traduction FR éventuelle va dans « definition ». Définitions exactes, propres au sujet « ${subject} ». "see_also" est une CHAÎNE (jamais une liste) : pour renvoyer vers plusieurs termes, une seule chaîne séparée par ", " — ex. "see_also": "Triplet, Property graph".`,
  ``,
  `2) ${themeDir}/tldr.json — { "these": "<la thèse du document en 1 phrase>", "part1": ["…","…"], "part2": ["…","…"] }. part1 et part2 = 2-4 puces chacune (idées clés ; part1 = principe, part2 = garanties/limites). Ce fichier alimente le RÉSUMÉ (abstract) en tête du document — sois complet.`,
  ``,
  `Sections du document (pour cohérence de ton glossaire/tldr) :\n${sectionsBrief}`,
  ``,
  `Rends : files_written (chemins écrits).`,
].join('\n');

const widgetPlanPrompt = (secs) => [
  `Sujet : « ${subject} ». Sections RETENUES du document (id, heading, prose, faits clés) :`,
  JSON.stringify(secs),
  `Décide quels CONCEPTS/MÉCANISMES méritent un widget interactif démonstratif, et de quel TYPE (champ "kind").`,
  `• "probe" — illustre UN mécanisme ISOLÉ. Rubrique STRICTE : seulement si NON TRIVIAL et plus clair MONTRÉ qu'expliqué. Rien pour le trivial/déclaratif. UN seul probe par mécanisme (déduplique).`,
  `• "process" — un SUPER-WIDGET synoptique montrant un PROCESSUS DE BOUT EN BOUT assemblé sur une instance jouet. Rubrique STRICTE (c'est le SEUL frein — il n'y a PAS de plafond) : seulement un VRAI processus multi-étapes — soit ITÉRATIF (une boucle d'étapes répétée jusqu'à convergence, ex. avant→arrière→mise à jour→répéter), soit un PIPELINE d'AU MOINS 3 étapes chaînées sur un cas concret. JAMAIS pour un mécanisme isolé (ça reste un probe). Déduplique : un seul process par processus distinct. Dans "brief", NOMME explicitement les étapes enchaînées (ou la boucle) ; si tu ne peux pas nommer ≥3 étapes ou la boucle, ce n'est PAS un process.`,
  `Un "process" s'ancre sur la section de SYNTHÈSE après laquelle l'enchaînement est complet (after_section_id).`,
  `Rends : widgets = liste {concept, after_section_id (id EXACT d'une section ci-dessus), brief (ce que le widget fait voir/manipuler ; pour un process, nomme les étapes), kind ("probe"|"process")}. Liste VIDE si rien ne le justifie.`,
].join('\n');

const widgetCodePrompt = (w) => [
  (w.kind === 'process')
    ? `Tu CODES un SUPER-WIDGET synoptique illustrant un PROCESSUS DE BOUT EN BOUT du sujet « ${subject} » : ${w.concept}.`
    : `Tu CODES un widget interactif autonome illustrant ce mécanisme du sujet « ${subject} » : ${w.concept}.`,
  `Objectif pédagogique (brief) : ${w.brief}`,
  (w.kind === 'process')
    ? `EXIGENCES SUPER-WIDGET : montre le PROCESSUS COMPLET sur une INSTANCE JOUET (pas un fragment) ; chaque PHASE distinctement ; DEUX pilotages — PAS-À-PAS (une phase à la fois) ET lecture continue « jusqu'à convergence » ; un INDICATEUR DE PROGRESSION (ex. courbe/compteur d'étape) ; relie visuellement les mécanismes déjà introduits ; en-tête interne « Vue d'ensemble ». Tout DÉTERMINISTE (aucun aléa), calculé exactement.`
    : null,
  `Écris le fichier ${themeDir}/widgets/<ref>.html (mkdir -p ${themeDir}/widgets si besoin). Choisis un <ref> kebab-case ascii unique (probe-… pour un mécanisme ; synopsis-… pour un process).`,
  `CONTRAINTES STRICTES (sinon le build échoue bruyamment) : un seul bloc <div class="widget">…</div> + <style>…</style> + <script>…</script> ; AUCUNE ressource externe, AUCUN file:///, AUCUN alert/confirm/prompt ; balises <section>/<details>/<script> ÉQUILIBRÉES ; préfixe TOUS les id/classes par le ref pour éviter les collisions avec la charte.`,
  `Le widget doit VRAIMENT démontrer le mécanisme : interactif et manipulable, pas décoratif ni statique. Aussi complexe que nécessaire, mais pas au-delà de sa valeur explicative.`,
  `Rends : ref (sans .html), title (titre court du widget), after_section_id = "${w.after_section_id}", kind = "${w.kind || 'probe'}".`,
].filter(Boolean).join('\n');

const widgetCriticPrompt = (coded) => [
  `Relis le widget : ${themeDir}/widgets/${coded.ref}.html (fais Read).`,
  `Juge HONNÊTEMENT : (1) tourne-t-il plausiblement (pas d'erreur JS évidente, pas de référence indéfinie, balises équilibrées) ; (2) est-il réellement INTERACTIF et DÉMONSTRATIF du mécanisme « ${coded.title} » (pas décoratif, pas statique) ; (3) respecte-t-il les contraintes (un seul <div class="widget">, aucune ressource externe / file:/// / alert|confirm|prompt, id/classes préfixés).`,
  (coded.kind === 'process')
    ? `(4) SUPER-WIDGET : montre-t-il le PROCESSUS COMPLET — toutes les phases distinctes, l'ITÉRATION jusqu'à convergence visible, pilotage pas-à-pas ET continu — et est-ce bien l'ENCHAÎNEMENT (pas un mécanisme isolé) ?`
    : null,
  `Rends : ok (true SEULEMENT si tous les points tiennent), issues (liste des problèmes précis à corriger ; vide si ok).`,
].filter(Boolean).join('\n');

const widgetRecodePrompt = (coded, issues) => [
  `Le widget ${themeDir}/widgets/${coded.ref}.html a été relu et DOIT être corrigé. Problèmes relevés :`,
  JSON.stringify(issues),
  `Réécris (Write) le fichier ${themeDir}/widgets/${coded.ref}.html en corrigeant ces points, en gardant les MÊMES contraintes strictes (un seul <div class="widget">, aucune ressource externe / file:/// / alert|confirm|prompt, balises équilibrées, id/classes préfixés, vraiment démonstratif).`,
  (coded.kind === 'process')
    ? `RAPPEL SUPER-WIDGET : garde le processus COMPLET (phases distinctes, itération jusqu'à convergence, pilotage pas-à-pas ET continu, en-tête « Vue d'ensemble ») — ne le rabaisse pas en simple sonde.`
    : null,
  `Rends : ref="${coded.ref}", title="${coded.title}", after_section_id="${coded.after_section_id}", kind="${coded.kind || 'probe'}".`,
].filter(Boolean).join('\n');

// ── Top-up super-widget (retrofit) : chargement persistant + insertion chirurgicale ──
const topupLoadPrompt = [
  `Lis ${themeDir}/sections_draft.json (liste d'objets {id, heading, prose, claims}) et ${themeDir}/knowledge.json.`,
  `Les "claims" de sections_draft sont des IDS (ex. "claim:1"). Pour chaque section, REMPLACE chaque id par l'ÉNONCÉ correspondant : dans knowledge.json, "claims" est une liste d'objets {id, statement, …} ; prends le "statement" du claim dont l'"id" == cet id. Id introuvable ⇒ garde l'id tel quel.`,
  `N'écris, ne crée, ne modifie RIEN sur le disque.`,
  `Rends : sections = [{id, heading, prose, claims:[énoncés]}].`,
].join('\n');
const S_TOPUP_LOAD = { type:'object', additionalProperties:false, required:['sections'], properties:{
  sections:{ type:'array', items:{ type:'object', additionalProperties:false, required:['id','heading','prose','claims'],
    properties:{ id:{type:'string'}, heading:{type:'string'}, prose:{type:'string'},
      claims:{ type:'array', items:{type:'string'} } } } } } };

const manifestInsertPrompt = (inserts) => [
  `Tu fais une édition CHIRURGICALE de ${themeDir}/manifest.json. Fais Read d'abord.`,
  `Le manifeste a "elements": [ … ] ordonnés. Pour CHAQUE super-widget ci-dessous, insère l'élément {"type":"widget","ref":"<ref>"} IMMÉDIATEMENT APRÈS le DERNIER élément {"type":"widget"} consécutif déjà présent juste après l'élément {"type":"section","id":"<after_section_id>"} (s'il n'y en a aucun, directement après la section).`,
  `Super-widgets à insérer : ${JSON.stringify(inserts)}`,
  `IDEMPOTENT : si un élément {"type":"widget","ref":"<ref>"} existe déjà dans le manifeste, NE L'AJOUTE PAS une seconde fois.`,
  `Ne modifie AUCUN autre élément (faits, sections, prose, biblio, pointers, meta : INTACTS). Réécris (Write) le fichier complet avec UNIQUEMENT ces insertions.`,
  `Si l'élément {"type":"section","id":"<after_section_id>"} est INTROUVABLE dans le manifeste, n'insère PAS ce widget : ne mets son ref ni dans inserted ni dans already_present (il restera non placé — volontaire, pas une erreur).`,
  `Rends : inserted (refs effectivement insérés), already_present (refs déjà présents).`,
].join('\n');
const S_INSERT = { type:'object', additionalProperties:false, required:['inserted','already_present'], properties:{
  inserted:{ type:'array', items:{type:'string'} }, already_present:{ type:'array', items:{type:'string'} } } };

const ELEMENT_CHEATSHEET = [
  `Types d'éléments valides (rendus par build.py) et leurs champs requis :`,
  `- {"type":"section","id":<kebab>,"heading":<str>,"level":3,"prose":<html>,"claims":[<claim ids>]}`,
  `- {"type":"abstract"}                      (tire de tldr.json : these+part1+part2)`,
  `- {"type":"exercise","part":<str>,"question":<html>,"answer":<html>}`,
  `- {"type":"widget","ref":<widget ref>}`,
  `- {"type":"callout","kind":"callout","title":<str>,"body":<html>}`,
  `- {"type":"biblio","entries":[{"label":<str>,"href":<url>}]}`,
  `- {"type":"pointers","title":<str>,"items":[{"name":<str>,"url":<url>,"kind":<str>,"blurb":<str>}]}`,
  `- {"type":"glossary"}                       (tire de glossary.json)`,
  `Un manifeste = {"edition":<ed>,"slug":"${slug}","meta":{"title","kicker","h1","lede","meta_chips":[…],"footer"},"elements":[…ordonnés…]}`,
  `meta.title/kicker/h1/lede sont OBLIGATOIRES. Les claims référencés doivent exister ; le widget ref doit exister.`,
].join('\n');

const composePrompt = (title, biblioEntries, widgets, pointers) => [
  `Tu composes LE manifeste unique de la monographie « ${title} » (slug ${slug}). Tu ÉCRIS (Write) UN fichier : ${themeDir}/manifest.json.`,
  `IMPÉRATIF — RÉÉCRITURE OBLIGATOIRE : un manifest.json peut déjà exister (sortie PÉRIMÉE d'un run précédent) alors que le knowledge.json courant a changé. Tu DOIS l'écraser intégralement avec le manifeste ci-dessous. Ne le considères JAMAIS comme la source de vérité. Si un Write échoue avec « File has not been read yet », fais d'abord Read sur ce fichier PUIS refais le Write — n'abandonne pas. À la fin, manifest.json DOIT avoir été (ré)écrit par toi dans CE run.`,
  ELEMENT_CHEATSHEET,
  ``,
  `Matériel partagé (réutilise la prose telle quelle ; ne ré-écris pas les faits) :`,
  `- sections (id, heading, prose HTML à réutiliser tel quel, claims = liste d'ids) : lis ${themeDir}/sections_draft.json`,
  `- entrées biblio (depuis les sources vérifiées) : ${JSON.stringify(biblioEntries)}`,
  `- widgets à placer (chacun APRÈS la section dont l'id == after_section_id) : ${widgets && widgets.length ? JSON.stringify(widgets) : 'aucun'}`,
  `- pointeurs « pour aller plus loin » : ${pointers && pointers.length ? JSON.stringify(pointers) : 'aucun'}`,
  ``,
  `Layout du document (superset best-of, dense et complet) — ordre des elements :`,
  `1. {"type":"abstract"}  — résumé exécutif (tiré de tldr.json : thèse + tous les points).`,
  `2. TOUTES les sections (avec leurs claims) dans l'ordre. Après une section dont l'id == after_section_id d'un widget, insère {"type":"widget","ref":<ce ref>}.`,
  `3. 1 à 2 {"type":"exercise","part":<str>,"question":<html>,"answer":<html>} que TU rédiges (auto-évaluation sur les points clés du document).`,
  `4. {"type":"biblio","entries":[…depuis les entrées biblio ci-dessus…]}`,
  (pointers && pointers.length) ? `5. {"type":"pointers","title":"Pour aller plus loin","items":[…depuis les pointeurs ci-dessus…]}` : `(pas d'élément pointers : aucun pointeur)`,
  `6. {"type":"glossary"}`,
  ``,
  `meta OBLIGATOIRE : title = "${title}", kicker = "<sujet court> · monographie", h1 = "${title}", lede = 1 phrase d'accroche, meta_chips = ["Monographie"], footer = "${title} · scriptorium".`,
  `Les claims référencés doivent exister dans knowledge.json ; chaque widget ref doit exister. Crée le dossier si besoin (mkdir -p ${themeDir}). Rends files_written + element_counts:{document:<nb total d'elements>}.`,
].join('\n');

const buildPrompt = () => [
  `Assemble la monographie de façon déterministe puis vérifie l'acceptation.`,
  `1) Exécute : python3 "${buildScript}" "${themeDir}"`,
  `   build.py échoue bruyamment (référence manquante, type inconnu, balise déséquilibrée, file:/// résiduel, jeton non substitué).`,
  `   S'il échoue pour une référence corrigeable (ex. claim id absent, widget ref erroné, clé meta manquante), CORRIGE le manifeste/fichier fautif dans ${themeDir} puis relance — UNE seule tentative de réparation, puis rapporte.`,
  `2) Lis ${themeDir}/knowledge.json et vérifie l'acceptation Phase 2 :`,
  `   - chaque claim "audit":"confirmed" a AU MOINS 2 entrées dans "sources" → all_confirmed_have_2plus_sources ;`,
  `   - quelles catégories d'audit sont présentes parmi confirmed/corrected/rejected → audit_categories_present ;`,
  `   - confirmed_claims = nombre de claims confirmés.`,
  `Rends : success (build OK et acceptation OK), files (fichiers de dist/), build_output (sortie de build.py), acceptance{…}, errors[] (vide si tout va bien).`,
].join('\n');

// ── Orchestration ────────────────────────────────────────────────────────────

// ── Reprise disque (Fix 2) : helpers ─────────────────────────────────────────
const safeParse = (s, what) => { try { return s ? JSON.parse(s) : null; }
  catch (e) { log(`[resume] ${what} illisible (${e.message}) → ignoré`); return null; } };
// Écriture best-effort d'un artefact de reprise. Son échec (ex. rate-limit) ne doit JAMAIS tuer un
// run par ailleurs réussi : on log et on continue (cette unité ne sera simplement pas reprenable).
async function ckptWrite(relName, obj, phaseName, labelName) {
  try {
    await A(`Crée le dossier si besoin (mkdir -p ${ckptDir}) puis écris VERBATIM, sans modification, le fichier suivant.\nChemin : ${ckptDir}/${relName}\nContenu :\n${JSON.stringify(obj)}`,
      { schema: S_CKPT, model: M_IO, phase: phaseName, label: labelName });
  } catch (e) { log(`[resume] checkpoint ${relName} non écrit (${e.message}) — unité non reprenable, run continue.`); }
}

// ── Mode top-up super-widget (retrofit) ──────────────────────────────────────
// Gardé par args.superwidgetOnly : n'exécute QUE planner-process → codeur → critic →
// insertion chirurgicale → build, à partir des fichiers DÉJÀ persistés du thème (pas de
// .monograph/ requis, pas de re-vérification factuelle). Réutilise les prompts canoniques.
async function runSuperwidgetTopUp() {
  phase('Synopsis');
  const L = await A(topupLoadPrompt, { schema: S_TOPUP_LOAD, phase: 'Synopsis', label: 'topup-load' });
  const sectionsBrief = L.sections || [];
  const ids = new Set(sectionsBrief.map(s => s.id));
  const plan = await A(widgetPlanPrompt(sectionsBrief), { schema: S_WIDGET_PLAN, phase: 'Synopsis', label: 'widget-plan' });
  const wanted = (plan.widgets || []).filter(w => w.kind === 'process' && ids.has(w.after_section_id));
  if (!wanted.length) {
    log('Synopsis : aucun super-widget process éligible — thème laissé inchangé.');
    return { slug, themeDir, mode: 'superwidgetOnly', superwidgets: [], inserted: [], already_present: [], build: null };
  }
  const coded = (await pipeline(
    wanted,
    (w) => A(widgetCodePrompt(w), { schema: S_WIDGET_CODE, phase: 'Synopsis', label: `widget-code:${w.after_section_id}` }),
    async (c) => {
      if (!c) return null;
      const verdict = await A(widgetCriticPrompt(c), { schema: S_WIDGET_CRITIC, phase: 'Synopsis', label: `widget-critic:${c.ref}` });
      if (verdict.ok) return c;
      log(`[superwidget] ${c.ref} recodé : ${(verdict.issues || []).join('; ')}`);
      const fixed = await A(widgetRecodePrompt(c, verdict.issues || []), { schema: S_WIDGET_CODE, phase: 'Synopsis', label: `widget-recode:${c.ref}` });
      return fixed || c;
    }
  )).filter(Boolean);
  if (!coded.length) {
    log('Synopsis : aucun super-widget codé.');
    return { slug, themeDir, mode: 'superwidgetOnly', superwidgets: [], inserted: [], already_present: [], build: null };
  }
  const inserts = coded.map(c => ({ ref: c.ref, after_section_id: c.after_section_id }));
  const ins = await A(manifestInsertPrompt(inserts), { schema: S_INSERT, phase: 'Synopsis', label: 'manifest-insert' });
  const placed = new Set([...(ins.inserted || []), ...(ins.already_present || [])]);
  const notPlaced = coded.map(c => c.ref).filter(r => !placed.has(r));   // section d'ancrage introuvable dans le manifeste
  if (notPlaced.length) log(`[superwidget] non placé(s) (section d'ancrage introuvable dans le manifeste) : ${notPlaced.join(', ')}`);
  const built = await A(buildPrompt(), { schema: S_BUILD, phase: 'Build', label: 'build' });
  return { slug, themeDir, mode: 'superwidgetOnly',
    superwidgets: coded.map(c => ({ ref: c.ref, title: c.title, after_section_id: c.after_section_id })),
    inserted: ins.inserted, already_present: ins.already_present, not_placed: notPlaced, build: built };
}
// resume n'a aucun effet ici : le top-up est sans état (relit les fichiers persistés, aucun checkpoint .monograph/ à reprendre).
if (String(A0.superwidgetOnly) === 'true') return await runSuperwidgetTopUp();

// Chargement des checkpoints (UNIQUEMENT en reprise). Échec/illisible ⇒ traité comme absent (run frais, loggé).
let loadedResearch = null, savedSections = {}, loadedWidgets = null;
if (RESUME) {
  try {
    const L = await A([
      `Lis l'état de reprise dans ${ckptDir}/ (ce dossier peut ne pas exister — alors tout est vide).`,
      `- research : si ${ckptDir}/research.json existe, rends son contenu EXACT (verbatim) ; sinon "".`,
      `- widgets : si ${ckptDir}/widgets.json existe, rends son contenu EXACT ; sinon "".`,
      `- sections : pour CHAQUE fichier ${ckptDir}/sec-*.json (liste-les via ls/Bash), un objet {id, content} où id = la partie <id> du nom (sec-<id>.json) et content = le contenu EXACT du fichier. Tableau vide si aucun.`,
      `N'écris, ne crée, ne modifie RIEN. Verbatim : ne reformate pas, ne tronque pas.`,
    ].join('\n'), { schema: S_LOAD, model: M_IO, phase: 'Sweep', label: 'resume-load' });
    loadedResearch = safeParse(L.research, 'research.json');
    loadedWidgets = safeParse(L.widgets, 'widgets.json');
    for (const s of (L.sections || [])) { const o = safeParse(s.content, `sec-${s.id}.json`); if (o) savedSections[s.id] = o; }
    log(`[resume] chargé : research=${loadedResearch ? 'oui' : 'non'}, sections=${Object.keys(savedSections).length}, widgets=${loadedWidgets ? 'oui' : 'non'}`);
  } catch (e) { log(`[resume] chargement échoué (${e.message}) → run frais`); }
}

// ── Sweep + Plan (sautés si repris du disque) ────────────────────────────────
let allFindings, allSources, arch;
if (loadedResearch && Array.isArray(loadedResearch.allFindings) && loadedResearch.arch) {
  ({ allFindings, allSources, arch } = loadedResearch);
  phase('Plan');
  log(`[resume] Sweep+Plan repris du disque : « ${arch.title} », ${arch.outline.length} sections, ${allFindings.length} findings.`);
} else {
  phase('Sweep');
  log(`Sujet : ${subject} — recherche multi-angles (${ANGLES.length} angles)`);
  const sweepResults = await parallel(ANGLES.map(a => () =>
    A(sweepPrompt(a), { schema: S_SWEEP, model: M_RESEARCH, phase: 'Sweep', label: `sweep:${a.key}` })
  ));
  // Tag chaque finding avec son angle d'origine (pour filtrage ciblé en Extract)
  const sweepsByAngle = ANGLES.map((a, i) => ({ key: a.key, sweep: sweepResults[i] })).filter(({sweep}) => sweep);
  allFindings = sweepsByAngle.flatMap(({key, sweep}) => (sweep.findings || []).map(f => ({ ...f, _angle: key })));
  allSources = dedupSources(sweepsByAngle.flatMap(({sweep}) => sweep.sources || []));
  log(`Sweep : ${allFindings.length} findings, ${allSources.length} sources uniques`);

  phase('Plan');
  arch = await A(archPrompt(allFindings, allSources), { schema: S_ARCH, phase: 'Plan', label: 'plan' });
  log(`Plan : « ${arch.title} » — ${arch.outline.length} sections`);
  await ckptWrite('research.json', { allFindings, allSources, arch }, 'Plan', 'ckpt:research');
}

// FRUGALITÉ (plafond dur) : on ne traite jamais plus de MAX_SECTIONS (Extract+Verify = le coût).
// Placé APRÈS la résolution de arch (frais ou repris du disque) pour s'appliquer dans les deux cas ;
// déterministe, donc une reprise re-tronque à l'identique. Ordre du plan conservé.
if (arch.outline.length > MAX_SECTIONS) {
  log(`[frugal] plan à ${arch.outline.length} sections → tronqué aux ${MAX_SECTIONS} premières (ordre du plan).`);
  arch.outline = arch.outline.slice(0, MAX_SECTIONS);
}

// Extract → Verify en pipeline (pas de barrière entre sections)
const sectionResults = await pipeline(
  arch.outline,
  (sec) => {
    if (savedSections[sec.id]) return { __saved: savedSections[sec.id] };   // section déjà auditée (reprise) → saute Extract+Verify
    // Filtre les findings sur l'angle de la section — réduit le bruit et le volume injecté
    const secFindings = sec.angle_key
      ? allFindings.filter(f => f._angle === sec.angle_key)
      : allFindings;
    return A(extractPrompt(sec, secFindings), { schema: S_SECTION, model: M_RESEARCH, phase: 'Extract', label: `extract:${sec.id}` });
  },
  async (ext, sec) => {
    if (ext && ext.__saved) { log(`[resume] section « ${sec.heading} » reprise du disque (audit conservé).`); return ext.__saved; }
    let claims = ext.claims || [];
    // FRUGALITÉ (plafond dur) : ne jamais soumettre plus de MAX_CLAIMS_PER_SECTION claims au council.
    if (claims.length > MAX_CLAIMS_PER_SECTION) {
      log(`[frugal] section « ${sec.heading} » : ${claims.length} claims → ${MAX_CLAIMS_PER_SECTION} soumis au council.`);
      claims = claims.slice(0, MAX_CLAIMS_PER_SECTION);
    }
    const auditedClaims = (await parallel(claims.map((c, ci) => async () => {
      // FRUGALITÉ — council réduit : 2 lentilles par claim, jamais 3 (Verify domine le coût).
      // 'established' → [réfutation, indépendance] (la source primaire est de trop pour un énoncé
      // déjà admis). 'contestable'/kind absent (idée reçue à départager) → [réfutation, source
      // primaire] : c'est la confrontation au texte faisant autorité qui tranche, pas l'accumulation
      // de soutiens. Le seuil ≥2 sources indépendantes reste GARANTI par collectSources/decideAudit
      // (inchangés). Effet de bord inchangé : 'confirmed' exige holds≥2, donc 2 jurés = unanimité.
      const lenses = (c.kind === 'established') ? [0, 1] : [0, 2];
      // On garde la lentille d'origine attachée à chaque verdict (le .filter casserait l'index).
      const lensVerdicts = (await parallel(lenses.map(j => () =>
        A(verifyPrompt(c, j), { schema: S_VERDICT, model: M_RESEARCH, phase: 'Verify', label: `verify:${sec.id}#${ci}/${j}` })
          .then(v => ({ lens: j, v }))
      ))).filter(x => x && x.v);
      if (lensVerdicts.length === 0) return null;
      const verdicts = lensVerdicts.map(x => x.v);   // entrée de decideAudit INCHANGÉE → audit identique
      const d = decideAudit(c, verdicts);
      // Capture des votes (vue de diagnostic ; voyage dans le checkpoint de section → reprise OK).
      const tally = { kind: c.kind || 'unspecified',
        corroborated: verdicts.filter(v => v.holds).length,
        refuted: verdicts.filter(v => !v.holds).length,
        corrected: verdicts.filter(v => !v.holds && v.corrected_statement && v.corrected_statement.trim()).length,
        jurors: lensVerdicts.map(({ lens, v }) => ({ lens: LENS_NAMES[lens] || String(lens),
          holds: !!v.holds, corrected: !!(v.corrected_statement && v.corrected_statement.trim()),
          n_sources: (v.independent_sources || []).length, note: v.note || '' })) };
      return { sectionId: sec.id, statement: d.statement, original_statement: c.statement,
               audit: d.audit, note: d.note, examples: c.examples || [], sources: d.sources, tally };
    }))).filter(Boolean);
    const result = { section: { id: sec.id, heading: sec.heading, prose: ext.prose, kind: sec.kind || 'normal' },
                     claims: auditedClaims, pointers: ext.pointers || [] };
    await ckptWrite(`sec-${sec.id}.json`, result, 'Verify', `ckpt:sec:${sec.id}`);   // persiste cette section pour une reprise future
    return result;
  }
);
const sectionData = sectionResults.filter(Boolean);
const audited = sectionData.flatMap(r => r.claims);
log(`Verify : ${audited.length} claims audités (${audited.filter(c=>c.audit==='confirmed').length} confirmés, ${audited.filter(c=>c.audit==='corrected').length} corrigés, ${audited.filter(c=>c.audit==='rejected').length} rejetés)`);

// ── ÉLAGAGE déterministe (frontière code) : la longueur = matière survivante ──
const enriched = sectionData.map(r => ({
  ...r, kept: r.claims.filter(c => c.audit !== 'rejected'),
}));
const liveSet = new Set(enriched.filter(s =>
  (s.section.kind === 'ecosystem')
    ? ((s.pointers && s.pointers.length > 0) || s.kept.length > 0)   // écosystème : ≥1 pointeur OU ≥1 claim
    : (s.kept.length >= SECTION_CLAIM_QUOTA)                          // normale : quota de faits
));
const liveSections = enriched.filter(s => liveSet.has(s));
enriched.filter(s => !liveSet.has(s)).forEach(s =>
  log(`[élagage] section « ${s.section.heading} » coupée : ${s.kept.length} claim(s) survivant(s) < ${SECTION_CLAIM_QUOTA}`));
if (liveSections.length === enriched.length) log('[élagage] aucune section coupée — toute la matière survit.');
log(`[élagage] ${liveSections.length}/${enriched.length} sections retenues.`);

// Vérification légère des pointeurs (sur sections vivantes), pas de council ≥2 sources
const liveOutlineIds = new Set(liveSections.map(s => s.section.id));
const pointerCandidates = liveSections.flatMap(s => s.pointers || []);
let verifiedPointers = [];
if (pointerCandidates.length > 0) {
  const pv = await A(pointersPrompt(pointerCandidates), { schema: S_POINTERS, model: M_RESEARCH, phase: 'Verify', label: 'verify:pointers' });
  const seenP = new Set();
  for (const p of (pv.pointers || [])) {
    const k = normUrl(p.url);
    if (k && !seenP.has(k)) { seenP.add(k); verifiedPointers.push({ name: p.name, url: p.url, kind: p.kind || 'reading', blurb: p.blurb || '' }); }
  }
  log(`[pointeurs] ${verifiedPointers.length}/${pointerCandidates.length} vérifiés.`);
}
const liveClaims = liveSections.flatMap(r => r.claims);  // knowledge.json = audit COMPLET des sections retenues (rejected inclus) ; les vues filtrent ensuite

// Assemblage déterministe de knowledge.json (frontière code/jugement)
const srcId = new Map();
const sources = [];
function ensureSrc(s) {
  const k = normUrl(s.url);
  if (!k) return null;
  if (!srcId.has(k)) {
    const id = 'src:' + (sources.length + 1);
    srcId.set(k, id);
    sources.push({ id, title: s.title || s.url, url: s.url, kind: s.kind || 'reference' });
  }
  return srcId.get(k);
}
const claims = liveClaims.map((ac, i) => ({
  id: 'claim:' + (i + 1),
  statement: ac.statement,
  sources: (ac.sources || []).map(ensureSrc).filter(Boolean),
  audit: ac.audit,
  audit_note: ac.note,
  examples: ac.examples || [],
  _section: ac.sectionId,
}));
const sectionClaims = {};
for (const c of claims) {
  if (c.audit === 'rejected') continue;             // les vues ne référencent que confirmed/corrected
  (sectionClaims[c._section] || (sectionClaims[c._section] = [])).push(c.id);
}
const knowledge = {
  theme: { slug, title: arch.title },
  sources,
  claims: claims.map(({ _section, ...c }) => c),    // knowledge.json conserve l'audit complet des sections RETENUES (y c. rejected) ; sections élaguées retirées
};
const knowledgeJson = JSON.stringify(knowledge, null, 2);

// ── Rapport d'audit (vue de diagnostic dérivée — PAS la source de vérité) ─────
// Resitue ce qui s'est passé : par claim, combien de jurés l'ont corroboré / réfuté / corrigé,
// l'audit final, et s'il a été retenu. Couvre TOUTES les sections auditées (élaguées incluses).
const retainedSectionIds = new Set(liveSections.map(s => s.section.id));
const idByClaimObj = new Map();
liveClaims.forEach((ac, i) => idByClaimObj.set(ac, 'claim:' + (i + 1)));   // même indexation que knowledge.json
const reportClaims = sectionData.flatMap(s => (s.claims || []).map(ac => {
  const sectionRetained = retainedSectionIds.has(ac.sectionId);
  const t = ac.tally || null;   // null = section reprise d'un checkpoint antérieur à cette instrumentation
  return { id: idByClaimObj.get(ac) || null, section: ac.sectionId, section_retained: sectionRetained,
    retained: sectionRetained && ac.audit !== 'rejected', audit: ac.audit, kind: t ? t.kind : 'unknown',
    statement: ac.statement, original_statement: ac.original_statement || ac.statement,
    corroborated: t ? t.corroborated : null, refuted: t ? t.refuted : null, corrected: t ? t.corrected : null,
    n_sources: (ac.sources || []).length, jurors: t ? t.jurors : [], audit_note: ac.note || '' };
}));
const auditReport = {
  generator: 'frugalmonograph', theme: { slug, title: arch.title },
  summary: { sections_total: enriched.length, sections_retained: liveSections.length,
    claims_total: reportClaims.length,
    confirmed: reportClaims.filter(c => c.audit === 'confirmed').length,
    corrected: reportClaims.filter(c => c.audit === 'corrected').length,
    rejected: reportClaims.filter(c => c.audit === 'rejected').length,
    retained: reportClaims.filter(c => c.retained).length },
  claims: reportClaims,
};
const _esc = v => String(v == null ? '' : v).replace(/\|/g, '\\|').replace(/\s*\n+\s*/g, ' ').trim();
const _num = v => v == null ? '?' : v;
const auditReportMd = [
  `# Rapport d'audit — ${_esc(auditReport.theme.title)} (${auditReport.generator})`, ``,
  `Thème : \`${_esc(slug)}\``, ``,
  `## Synthèse`,
  `- Sections : ${auditReport.summary.sections_retained}/${auditReport.summary.sections_total} retenues`,
  `- Claims : ${auditReport.summary.claims_total} audités → **${auditReport.summary.confirmed} confirmed**, ${auditReport.summary.corrected} corrected, ${auditReport.summary.rejected} rejected ; ${auditReport.summary.retained} retenus dans le document`,
  ``, `Légende jurés : \`lentille✓\` corrobore · \`lentille✗\` réfute · \`~\` propose une correction.`, ``,
  `## Par claim`, ``,
  `| id | section | kind | audit | corrob. | réfut. | corrig. | sources | jurés | énoncé |`,
  `|---|---|---|---|---|---|---|---|---|---|`,
  ...auditReport.claims.map(c => {
    const jur = (c.jurors || []).map(j => `${j.lens}${j.holds ? '✓' : '✗'}${j.corrected ? '~' : ''}`).join(' ');
    return `| ${c.id || '—'} | ${_esc(c.section)} | ${c.kind} | ${c.audit}${c.retained ? '' : ' (non retenu)'} | ${_num(c.corroborated)} | ${_num(c.refuted)} | ${_num(c.corrected)} | ${c.n_sources} | ${_esc(jur)} | ${_esc(c.statement)} |`;
  }),
].join('\n');

phase('Author');
// Écriture de knowledge.json via un agent dédié (le script workflow n'a pas d'accès disque)
await A(
  `Crée le dossier si besoin (mkdir -p ${themeDir}) puis écris VERBATIM, sans aucune modification, le fichier suivant.\nChemin : ${themeDir}/knowledge.json\nContenu :\n${knowledgeJson}`,
  { schema: { type:'object', additionalProperties:false, required:['written'], properties:{ written:{type:'boolean'} } },
    model: M_IO, phase: 'Author', label: 'write:knowledge' }
);
// Écriture du rapport d'audit (2 fichiers annexes : JSON réexploitable + MD lisible). Best-effort :
// son échec ne doit pas tuer un run par ailleurs réussi → try/catch.
try {
  await A(
    `Crée le dossier si besoin (mkdir -p ${themeDir}) puis écris VERBATIM ces DEUX fichiers (un Write chacun, sans rien modifier).\n` +
    `--- Fichier 1 : ${themeDir}/audit-report.json ---\n${JSON.stringify(auditReport, null, 2)}\n` +
    `--- Fichier 2 : ${themeDir}/audit-report.md ---\n${auditReportMd}`,
    { schema: { type:'object', additionalProperties:false, required:['files_written'], properties:{ files_written:{ type:'array', items:{type:'string'} } } },
      model: M_IO, phase: 'Author', label: 'write:audit-report' }
  );
} catch (e) { log(`[audit] rapport non écrit (${e.message}) — run continue.`); }
const sectionsBrief = arch.outline.filter(o => liveOutlineIds.has(o.id)).map(o => `- ${o.id} : ${o.heading}`).join('\n');
const authored = await A(authorPrompt(sectionsBrief), { schema: S_AUTHOR, phase: 'Author', label: 'author' });
log(`Author : ${authored.files_written.length} fichiers écrits`);

phase('Widgets');
let widgets = [];
if (Array.isArray(loadedWidgets)) {                 // reprise : décision widgets déjà prise (même []) → saute le 2e fan-out
  widgets = loadedWidgets;
  log(`[resume] ${widgets.length} widget(s) repris du disque — phase Widgets sautée.`);
} else {
  const liveSectionsBrief = liveSections.map(s => ({
    id: s.section.id, heading: s.section.heading, prose: s.section.prose,
    claims: (s.kept || []).map(c => c.statement),
  }));
  const wantWidgets = String(A0.widget) !== 'false';
  if (wantWidgets && liveSectionsBrief.length) {
    const plan = await A(widgetPlanPrompt(liveSectionsBrief), { schema: S_WIDGET_PLAN, phase: 'Widgets', label: 'widget-plan' });
    const liveIds = new Set(liveSections.map(s => s.section.id));
    const wanted = (plan.widgets || []).filter(w => liveIds.has(w.after_section_id));  // garde-fou : ancrage sur une section vivante
    widgets = (await pipeline(
      wanted,
      (w) => A(widgetCodePrompt(w), { schema: S_WIDGET_CODE, phase: 'Widgets', label: `widget-code:${w.after_section_id}` }),
      async (coded) => {
        if (!coded) return null;
        const verdict = await A(widgetCriticPrompt(coded), { schema: S_WIDGET_CRITIC, phase: 'Widgets', label: `widget-critic:${coded.ref}` });
        if (verdict.ok) return coded;
        log(`[widget] ${coded.ref} recodé : ${(verdict.issues || []).join('; ')}`);
        const fixed = await A(widgetRecodePrompt(coded, verdict.issues || []), { schema: S_WIDGET_CODE, phase: 'Widgets', label: `widget-recode:${coded.ref}` });
        return fixed || coded;   // 1 SEULE re-passe ; au pire on garde la version critiquée
      }
    )).filter(Boolean);
    log(`Widgets : ${widgets.length}/${(plan.widgets || []).length} retenus.`);
  } else {
    log(wantWidgets ? 'Widgets : aucune section vivante.' : 'Widgets : désactivés (widget=false).');
  }
  // Persiste la décision widgets (même vide) pour ne pas re-payer ce 2e fan-out sur une reprise ultérieure.
  await ckptWrite('widgets.json', widgets, 'Widgets', 'ckpt:widgets');
}

phase('Compose');
const proseById = {};
sectionData.forEach(r => { proseById[r.section.id] = r.section.prose; });
const liveOutline = arch.outline.filter(o => liveOutlineIds.has(o.id));
const sectionsForCompose = liveOutline.map(o => ({
  id: o.id, heading: o.heading,
  prose: proseById[o.id] || '',
  claims: sectionClaims[o.id] || [],
}));
// Écriture des sections sur disque — Compose lit depuis le fichier (pas d'injection inline volumineuse)
await A(
  `Crée le dossier si besoin (mkdir -p ${themeDir}) puis écris VERBATIM le fichier suivant.\nChemin : ${themeDir}/sections_draft.json\nContenu :\n${JSON.stringify(sectionsForCompose, null, 2)}`,
  { schema: { type:'object', additionalProperties:false, required:['written'], properties:{ written:{type:'boolean'} } },
    model: M_IO, phase: 'Compose', label: 'write:sections' }
);
const biblioEntries = sources.map(s => ({ label: s.title, href: s.url }));
const composed = await A(
  composePrompt(arch.title, biblioEntries, widgets, verifiedPointers),
  { schema: S_COMPOSE, phase: 'Compose', label: 'compose' }
);
log(`Compose : ${composed.files_written.length} manifeste(s) écrit(s)`);

// Garde fail-loud : manifest.json DOIT avoir été (ré)écrit dans ce run.
// Sinon build.py assemblerait un manifeste périmé (refs claim:N pointant des faits différents) → corruption silencieuse.
const _wroteManifest = (composed.files_written || []).some(p => /(^|\/)manifest\.json$/.test(p));
if (!_wroteManifest) throw new Error(
  `Compose n'a pas (ré)écrit ${themeDir}/manifest.json. files_written=${JSON.stringify(composed.files_written)}. ` +
  `Abandon AVANT build pour ne pas assembler un manifeste périmé sur le knowledge.json courant.`);

phase('Build');
const built = await A(buildPrompt(), { schema: S_BUILD, phase: 'Build', label: 'build' });

return {
  slug, title: arch.title, themeDir,
  claims: { total: claims.length,
    confirmed: claims.filter(c => c.audit === 'confirmed').length,
    corrected: claims.filter(c => c.audit === 'corrected').length,
    rejected: claims.filter(c => c.audit === 'rejected').length },
  sources: sources.length,
  widgets: { kept: widgets.length },
  audit: auditReport.summary,
  build: built,
};
