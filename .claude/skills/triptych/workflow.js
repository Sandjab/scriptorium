export const meta = {
  name: 'triptych',
  description: 'Recherche vérifiée d’un sujet puis assemblage déterministe du triptyque (référence / publication / pédagogique)',
  whenToUse: 'Lancé par le skill /triptych. Reçoit args:{subject, slug, themeDir} et peuple themeDir/ avant build.py.',
  phases: [
    { title: 'Sweep',   detail: 'recherche web multi-angles ; collecte de sources' },
    { title: 'Plan',    detail: 'plan du document depuis les sources' },
    { title: 'Extract', detail: 'claims candidats + prose par section' },
    { title: 'Verify',  detail: 'council adversarial par claim ; ≥2 sources indépendantes' },
    { title: 'Author',  detail: 'écrit knowledge/glossary/tldr (+widget)' },
    { title: 'Compose', detail: 'écrit les 3 manifestes-vues' },
    { title: 'Build',   detail: 'python3 build.py → 3 HTML + auto-vérifs' },
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
const buildScript = repoRoot + '/.claude/skills/triptych/scripts/build.py';

const WEB = 'Utilise WebSearch et WebFetch (charge-les via ToolSearch "select:WebSearch,WebFetch" si absents). Cite des URL réelles, jamais inventées.';

// Tous les agents tournent en general-purpose (Tools: *) → WebSearch/WebFetch/Write/Bash garantis.
const A = (prompt, opts) => agent(prompt, { agentType: 'general-purpose', ...opts });

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
      kind:{ type:'string', enum:['normal','ecosystem'] } } } } } };

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

const S_AUTHOR = { type:'object', additionalProperties:false, required:['files_written','has_widget'], properties:{
  files_written:{ type:'array', items:{type:'string'} },
  has_widget:{type:'boolean'},
  widget:{ type:'object', additionalProperties:false, required:['ref','title','after_section_id'],
    properties:{ ref:{type:'string'}, title:{type:'string'}, after_section_id:{type:'string'} } } } };

const S_COMPOSE = { type:'object', additionalProperties:false, required:['files_written','element_counts'], properties:{
  files_written:{ type:'array', items:{type:'string'} },
  element_counts:{ type:'object', additionalProperties:false, required:['reference','publication','pedagogique'],
    properties:{ reference:{type:'integer'}, publication:{type:'integer'}, pedagogique:{type:'integer'} } } } };

const S_BUILD = { type:'object', additionalProperties:false, required:['success','files','acceptance','errors'], properties:{
  success:{type:'boolean'},
  files:{ type:'array', items:{type:'string'} },
  build_output:{type:'string'},
  acceptance:{ type:'object', additionalProperties:false, required:['confirmed_claims','all_confirmed_have_2plus_sources','audit_categories_present'],
    properties:{ confirmed_claims:{type:'integer'}, all_confirmed_have_2plus_sources:{type:'boolean'},
      audit_categories_present:{ type:'array', items:{type:'string'} } } },
  errors:{ type:'array', items:{type:'string'} } } };

// ── Helpers JS (transformations déterministes — pas de jugement) ─────────────
const normUrl = u => (u||'').trim().replace(/^https?:\/\//i,'').replace(/[#?].*$/,'').replace(/\/+$/,'').toLowerCase();

function dedupSources(list) {
  const seen = new Map();
  for (const s of list) { const k = normUrl(s.url); if (k && !seen.has(k)) seen.set(k, s); }
  return [...seen.values()];
}

// Décision d'audit : le SEUIL est en code ; l'INDÉPENDANCE des sources est jugée par les jurés.
function decideAudit(claim, verdicts) {
  const supportive = [];
  const seen = new Set();
  for (const v of verdicts) for (const s of (v.independent_sources || [])) {
    const k = normUrl(s.url);
    if (k && !seen.has(k)) { seen.add(k); supportive.push({ title: s.title || s.url, url: s.url }); }
  }
  const nSrc = supportive.length;
  const holds = verdicts.filter(v => v.holds);
  const corrected = verdicts.filter(v => !v.holds && v.corrected_statement && v.corrected_statement.trim());
  if (holds.length >= 2 && nSrc >= 2)
    return { audit:'confirmed', statement: claim.statement, sources: supportive,
             note: `Confirmé : ${holds.length}/${verdicts.length} jurés, ${nSrc} sources indépendantes.` };
  if ((holds.length + corrected.length) >= 2 && nSrc >= 2)
    return { audit:'corrected', statement: corrected[0].corrected_statement.trim(), sources: supportive,
             note: `Énoncé d'origine imprécis, corrigé après vérification (${nSrc} sources indépendantes). Origine : « ${claim.statement} »` };
  return { audit:'rejected', statement: claim.statement, sources: supportive,
           note: `Rejeté : ${holds.length} confirmation(s), ${nSrc} source(s) indépendante(s) — seuil ≥2 non atteint ou réfuté.` };
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
  `Findings (point → url) :\n${JSON.stringify(findings).slice(0, 12000)}`,
  `Sources :\n${JSON.stringify(sources.map(s => ({ title:s.title, url:s.url, kind:s.kind }))).slice(0, 6000)}`,
  `Rends : title (titre du document, sans suffixe d'édition), kicker (sur-titre court), et outline = AUTANT de sections que la matière trouvée le justifie (typiquement 4 à 9). Propose LARGE : une section par sous-thème réellement documenté. Les sections sans matière vérifiable seront élaguées automatiquement — ne t'autocensure pas, mais n'invente pas de section creuse.`,
  `Chaque section : id (kebab-case ascii, unique), heading, angle (ce qu'elle couvre).`,
  `Couvre fondations → propriétés → variantes/applications → limites. Si le sujet a un écosystème d'outils/bibliothèques/packages/lectures, AJOUTE une section finale kind="ecosystem" (heading type « Écosystème & pour aller plus loin »). Les autres sections : kind="normal". Pas de section "glossaire"/"biblio" (ajoutées à la composition).`,
].join('\n');

const extractPrompt = (sec, findings) => [
  `Sujet : « ${subject} ». Section « ${sec.heading} » — angle : ${sec.angle}.`,
  `Findings disponibles (point → url) :\n${JSON.stringify(findings).slice(0, 12000)}`,
  WEB + ' (autorisé pour compléter/préciser une source.)',
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

const verifyPrompt = (claim, lensIdx) => [
  `Énoncé à vérifier : « ${claim.statement} »`,
  `Sources candidates fournies : ${JSON.stringify(claim.candidate_sources || [])}`,
  `Ton rôle de juré — ${LENSES[lensIdx]}`,
  WEB,
  `Rends un verdict HONNÊTE : holds (true si l'énoncé tient TEL QUEL), corrected_statement ("" si rien à corriger ; sinon l'énoncé corrigé minimal qui serait vrai), independent_sources (UNIQUEMENT les sources que TOI tu as vérifiées et qui sont indépendantes — title+url réels), note (1-2 phrases justifiant).`,
  `N'invente jamais d'URL. En cas de doute sur l'indépendance ou la véracité, penche vers holds=false.`,
].join('\n');

const authorPrompt = (knowledgeJson, sectionsBrief, wantWidget) => [
  `Tu es l'auteur. Tu ÉCRIS des fichiers dans le dossier de thème : ${themeDir}`,
  `Assure-toi que le dossier existe (mkdir -p si besoin), puis ÉCRIS exactement ces fichiers :`,
  ``,
  `1) ${themeDir}/knowledge.json — écris VERBATIM ce contenu, SANS rien modifier (c'est la base de faits vérifiée, déjà assemblée) :`,
  knowledgeJson,
  ``,
  `2) ${themeDir}/glossary.json — un tableau JSON de 4 à 7 termes du sujet : {term, definition, see_also?}. Définitions exactes, propres au sujet « ${subject} ». "see_also" est une CHAÎNE (jamais une liste) : pour renvoyer vers plusieurs termes, une seule chaîne séparée par ", " — ex. "see_also": "Triplet, Property graph".`,
  ``,
  `3) ${themeDir}/tldr.json — { "these": "<la thèse du document en 1 phrase>", "part1": ["…","…"], "part2": ["…","…"] }. part1 et part2 = 2-4 puces chacune (idées clés ; part1 = principe, part2 = garanties/limites).`,
  ``,
  wantWidget
    ? `4) ${themeDir}/widgets/<ref>.html — UN widget interactif autonome illustrant le sujet. Contraintes STRICTES : un seul bloc <div class="widget">…</div> + <style>…</style> + <script>…</script> ; AUCUNE ressource externe, AUCUN file:///, AUCUN alert/confirm/prompt ; balises <section>/<details>/<script> équilibrées ; préfixe TOUS les id/classes pour éviter les collisions avec la charte. Choisis un ref kebab-case (ex. probe-…). Le widget doit vraiment démontrer un mécanisme du sujet (interactif, pas décoratif).`
    : `(Pas de widget pour ce thème.)`,
  ``,
  `Sections du document (pour cohérence de ton glossaire/tldr/widget) :\n${sectionsBrief}`,
  ``,
  `Rends : files_written (chemins écrits), has_widget, et si widget → widget:{ref, title, after_section_id (l'id de section après laquelle l'insérer)}.`,
].join('\n');

const ELEMENT_CHEATSHEET = [
  `Types d'éléments valides (rendus par build.py) et leurs champs requis :`,
  `- {"type":"section","id":<kebab>,"heading":<str>,"level":3,"prose":<html>,"claims":[<claim ids>]}`,
  `- {"type":"abstract"}                      (tire de tldr.json : these+part1+part2)`,
  `- {"type":"tldr","key":"part1"|"part2","title":<str>}`,
  `- {"type":"onramp","steps":["<li>…</li>","<li>…</li>"]}`,
  `- {"type":"exercise","part":<str>,"question":<html>,"answer":<html>}`,
  `- {"type":"widget","ref":<widget ref>}`,
  `- {"type":"callout","kind":"callout","title":<str>,"body":<html>}`,
  `- {"type":"biblio","entries":[{"label":<str>,"href":<url>}]}`,
  `- {"type":"glossary"}                       (tire de glossary.json)`,
  `Un manifeste = {"edition":<ed>,"slug":"${slug}","meta":{"title","kicker","h1","lede","meta_chips":[…],"footer"},"elements":[…ordonnés…]}`,
  `meta.title/kicker/h1/lede sont OBLIGATOIRES. Les claims référencés doivent exister ; le widget ref doit exister.`,
].join('\n');

const composePrompt = (title, sections, biblioEntries, widget) => [
  `Tu composes les 3 manifestes-vues du thème « ${title} » (slug ${slug}). Tu ÉCRIS 3 fichiers JSON.`,
  ELEMENT_CHEATSHEET,
  ``,
  `Matériel partagé (réutilise la prose telle quelle ; ne ré-écris pas les faits) :`,
  `- sections, ordre logique — chacune : id, heading, prose (HTML à réutiliser tel quel), claims (ids à mettre dans section.claims) :`,
  `  ${JSON.stringify(sections)}`,
  `- entrées biblio (depuis les sources vérifiées) : ${JSON.stringify(biblioEntries)}`,
  `- widget : ${widget ? JSON.stringify(widget) : 'aucun'}`,
  ``,
  `Politique d'édition (guide de rédaction, pas une règle du code) :`,
  `- ${themeDir}/editions/reference.manifest.json : tldr(part1) → toutes les sections (avec leurs claims)${widget ? ' → widget (après sa section)' : ''} → biblio → glossary. Édition dense, superset.`,
  `- ${themeDir}/editions/publication.manifest.json : abstract → toutes les sections → biblio → glossary. Lecture suivie.`,
  `- ${themeDir}/editions/pedagogique.manifest.json : onramp (tu rédiges 3-4 étapes) → sections${widget ? ' → widget' : ''} → 1-2 exercise (tu rédiges question+réponse) → biblio → glossary. Apprentissage.`,
  ``,
  `meta par édition : title = "${title} — <référence|publication|pédagogique>", kicker = "<sujet court> · édition <…>", h1 = "${title}", lede = 1 phrase d'accroche propre à l'édition, meta_chips = ["Référence"]/["Publication"]/["Pédagogique"], footer = "${title} · scriptorium".`,
  `Crée le dossier editions/ si besoin (mkdir -p). Rends files_written + element_counts.`,
].join('\n');

const buildPrompt = () => [
  `Assemble le triptyque de façon déterministe puis vérifie l'acceptation.`,
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
phase('Sweep');
log(`Sujet : ${subject} — recherche multi-angles (${ANGLES.length} angles)`);
const sweeps = (await parallel(ANGLES.map(a => () =>
  A(sweepPrompt(a), { schema: S_SWEEP, phase: 'Sweep', label: `sweep:${a.key}` })
))).filter(Boolean);
const allFindings = sweeps.flatMap(s => s.findings || []);
const allSources = dedupSources(sweeps.flatMap(s => s.sources || []));
log(`Sweep : ${allFindings.length} findings, ${allSources.length} sources uniques`);

phase('Plan');
const arch = await A(archPrompt(allFindings, allSources), { schema: S_ARCH, phase: 'Plan', label: 'plan' });
log(`Plan : « ${arch.title} » — ${arch.outline.length} sections`);

// Extract → Verify en pipeline (pas de barrière entre sections)
const sectionResults = await pipeline(
  arch.outline,
  (sec) => A(extractPrompt(sec, allFindings), { schema: S_SECTION, phase: 'Extract', label: `extract:${sec.id}` }),
  async (ext, sec) => {
    const claims = ext.claims || [];
    const auditedClaims = (await parallel(claims.map((c, ci) => async () => {
      const verdicts = (await parallel([0, 1, 2].map(j => () =>
        A(verifyPrompt(c, j), { schema: S_VERDICT, phase: 'Verify', label: `verify:${sec.id}#${ci}/${j}` })
      ))).filter(Boolean);
      if (verdicts.length === 0) return null;
      const d = decideAudit(c, verdicts);
      return { sectionId: sec.id, statement: d.statement, audit: d.audit, note: d.note,
               examples: c.examples || [], sources: d.sources };
    }))).filter(Boolean);
    return { section: { id: sec.id, heading: sec.heading, prose: ext.prose }, claims: auditedClaims };
  }
);
const sectionData = sectionResults.filter(Boolean);
const audited = sectionData.flatMap(r => r.claims);
log(`Verify : ${audited.length} claims audités (${audited.filter(c=>c.audit==='confirmed').length} confirmés, ${audited.filter(c=>c.audit==='corrected').length} corrigés, ${audited.filter(c=>c.audit==='rejected').length} rejetés)`);

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
const claims = audited.map((ac, i) => ({
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
  claims: claims.map(({ _section, ...c }) => c),    // knowledge.json conserve TOUT l'audit (y c. rejected)
};
const knowledgeJson = JSON.stringify(knowledge, null, 2);

phase('Author');
const sectionsBrief = arch.outline.map(o => `- ${o.id} : ${o.heading}`).join('\n');
const wantWidget = String(A0.widget) !== 'false';   // widget par défaut, sauf widget === false
const authored = await A(authorPrompt(knowledgeJson, sectionsBrief, wantWidget), { schema: S_AUTHOR, phase: 'Author', label: 'author' });
log(`Author : ${authored.files_written.length} fichiers écrits${authored.has_widget ? ' (widget inclus)' : ''}`);

phase('Compose');
const proseById = {};
sectionData.forEach(r => { proseById[r.section.id] = r.section.prose; });
const sectionsForCompose = arch.outline.map(o => ({
  id: o.id, heading: o.heading,
  prose: proseById[o.id] || '',
  claims: sectionClaims[o.id] || [],
}));
const biblioEntries = sources.map(s => ({ label: s.title, href: s.url }));
const widget = (authored.has_widget && authored.widget) ? authored.widget : null;
const composed = await A(
  composePrompt(arch.title, sectionsForCompose, biblioEntries, widget),
  { schema: S_COMPOSE, phase: 'Compose', label: 'compose' }
);
log(`Compose : ${composed.files_written.length} manifestes écrits`);

phase('Build');
const built = await A(buildPrompt(), { schema: S_BUILD, phase: 'Build', label: 'build' });

return {
  slug, title: arch.title, themeDir,
  claims: { total: claims.length,
    confirmed: claims.filter(c => c.audit === 'confirmed').length,
    corrected: claims.filter(c => c.audit === 'corrected').length,
    rejected: claims.filter(c => c.audit === 'rejected').length },
  sources: sources.length,
  build: built,
};
