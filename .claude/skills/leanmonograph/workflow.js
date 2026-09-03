export const meta = {
  name: 'leanmonograph',
  description: "Variante LEAN de monograph : vérifier d'abord, écrire une fois. Council par SECTION (2 jurés adversariaux batch + 1 juré dédié par claim contestable), prose rédigée APRÈS l'audit par un auteur unique (voix cohérente), lint déterministe (claims rejetés, chiffres prose-only) — mêmes garanties, moins de tokens.",
  whenToUse: "Lancé par le skill /leanmonograph. Reçoit args:{subject, slug, themeDir} et peuple themeDir/ avant build.py (réutilise build.py/charte de monograph).",
  phases: [
    { title: 'Sweep',       detail: 'recherche web multi-angles ; collecte de sources', model: 'sonnet' },
    { title: 'Plan',        detail: 'plan du document + fil rouge narratif' },
    { title: 'Extract',     detail: 'notes factuelles sourcées + claims candidats (PAS de prose)', model: 'sonnet' },
    { title: 'Verify',      detail: 'council par SECTION (soutien + réfutation) + juré dédié par claim contestable', model: 'sonnet' },
    { title: 'Author',      detail: 'prose rédigée APRÈS audit, en tranches séquentielles à voix unique' },
    { title: 'Relecture',   detail: 'éditeur de continuité : transitions, répétitions inter-tranches' },
    { title: 'Audit-prose', detail: 'lint.py --pre + vérification des chiffres prose-only contre leurs sources', model: 'sonnet' },
    { title: 'Widgets',     detail: 'sélection des concepts (planner) puis fan-out codeurs + critic' },
    { title: 'Compose',     detail: 'écrit le manifeste unique (best-of)' },
    { title: 'Verdicts',    detail: "tableau efficacité/sécurité par indication (thème santé, si args.verdicts) — écrit verdicts.json + insère l'élément au manifeste" },
    { title: 'Style',       detail: 'relecture accents/calques du texte visible des widgets', model: 'sonnet' },
    { title: 'Build',       detail: 'build.py + lint.py (adjudication des flags) → 1 HTML + auto-vérifs' },
  ],
};

// ─────────────────────────────────────────────────────────────────────────────
// LEAN — deux renversements d'architecture vs monograph/frugalmonograph :
// 1. VÉRIFIER D'ABORD, ÉCRIRE UNE FOIS : Extract produit des NOTES (pas de prose) ;
//    la prose est rédigée APRÈS le council, depuis les claims FINAUX — la classe
//    de bugs « prose pré-council » (dérives, claims rejetés affirmés) disparaît
//    par construction ; les passes Réconcilie et Style-prose disparaissent avec.
// 2. COUNCIL PAR SECTION : 2 jurés adversariaux auditent les ≤4 claims d'une
//    section en UNE passe chacun (les claims d'une section citent les mêmes
//    papiers → fetchs amortis) ; chaque claim `contestable` reçoit EN PLUS un
//    juré dédié (source primaire). Le seuil ≥2 sources indépendantes par claim
//    reste inchangé, en code (decideAudit/collectSources identiques).
// Un script Workflow n'a AUCUN accès filesystem : les données transitent par le
// script, les fichiers sont écrits par des agents (Write/Bash), build.py reste
// le seul assembleur déterministe.
// ─────────────────────────────────────────────────────────────────────────────

// args peut arriver objet OU chaîne JSON selon le marshalling — tolère les deux.
const A0 = (typeof args === 'string') ? JSON.parse(args) : (args || {});
const { subject, slug, themeDir } = A0;
if (!subject || !slug || !themeDir)
  throw new Error('args manquants : attendu {subject, slug, themeDir}. Reçu : ' + JSON.stringify(args));
const repoRoot = themeDir.replace(/\/themes\/[^/]+\/?$/, '');
const buildScript = repoRoot + '/.claude/skills/monograph/scripts/build.py';
const lintScript = repoRoot + '/.claude/skills/leanmonograph/scripts/lint.py';
const RESUME = (A0.resume === true) || (String(A0.resume) === 'true');
const WANT_VERDICTS = (A0.verdicts === true) || (String(A0.verdicts) === 'true');
const ckptDir = themeDir + '/.leanmonograph';   // checkpoints isolés de /monograph et /frugalmonograph

const WEB = 'Utilise WebSearch et WebFetch (charge-les via ToolSearch "select:WebSearch,WebFetch" si absents). Cite des URL réelles, jamais inventées.';

const TERMINO = `TERMINOLOGIE (anglais en tête) : pour tout concept dont la littérature emploie une forme anglaise de référence — Y COMPRIS quand un calque français circule — mets le TERME ANGLAIS EN TÊTE et donne la forme française en glose à la 1re occurrence SEULEMENT, puis emploie l'anglais seul. Ex. : « chain rule (dérivation des fonctions composées) », « backpropagation (rétropropagation) », « forward pass / backward pass », « learning rate », « vanishing / exploding gradient », « gradient clipping ». NUANCE GRAMMATICALE : seul le NOM bascule en anglais ; garde les formes VERBALES/participes françaises (« rétropropagé », « rétropropage ») — n'anglicise jamais un verbe au milieu d'une phrase. BANNIS les calques (ni vrai français ni anglais : « règle de la chaîne », « écrêtage de gradient »…). N'anglicise PAS le vocabulaire français naturalisé et non-calque (descente de gradient, couche, poids, perte, dérivée, fonction d'activation, connexions résiduelles, graphe de calcul). Les termes déjà anglais (ReLU, Adam, ResNet, batch normalization, internal covariate shift…) restent tels quels. Glossaire : le champ "term" = la forme anglaise canonique (glose française dans la définition). SIGLES & TERMES SPÉCIFIQUES : développe tout sigle ou terme technique propre au sujet à sa 1re occurrence — forme longue entre parenthèses (« RoPE (Rotary Position Embedding) »), ou glose fonctionnelle quand le sigle n'a pas d'expansion canonique (« GPTQ (méthode de quantification post-entraînement) ») ; n'INVENTE JAMAIS une forme longue. N'applique PAS cette règle aux sigles bibliographiques — conférences, revues, institutions (NeurIPS, SIGIR, EMNLP, IEEE, W3C…) — ni aux sigles ubiquitaires (CPU, GPU, API, LLM, JSON…), laissés tels quels.`;

const STYLE = `STYLE FRANÇAIS (complète TERMINOLOGIE) : (1) ACCENTS — tout texte français visible PORTE ses diacritiques (é è ê à â î ï ô û ù ç œ…) ; n'écris JAMAIS en ASCII dé-accentué, y compris dans les libellés/légendes/boutons/messages et le texte SVG affiché des widgets, et dans les blurbs de pointeurs. (2) LISIBILITÉ — phrases fluides : sujet et verbe rapprochés, pas de ponctuation cassée (« — : »), pas d'apposition non liée par deux-points, pas de participes empilés ; allège plutôt que de délayer. (3) FAUX-AMIS à proscrire : « library »→bibliothèque (jamais « librairie ») ; « to attend to »→prêter attention / regarder (jamais « attendre ») ; « consistent »→régulier / cohérent (jamais « consistant ») ; « to support (une fonctionnalité) »→prendre en charge ; « to address (un problème) »→traiter / aborder ; « paper »→article. Ne dé-accentue JAMAIS un nom propre ni un mot français pour « faire simple ».`;

// Charte de voix — la prose est écrite par UN auteur, après vérification. C'est le levier
// « plus agréable à lire » : une seule voix, un arc, pas de ré-introductions.
const VOICE = `VOIX D'AUTEUR (un seul auteur pour tout le document) : (1) ARC — suis le fil rouge fourni ; chaque section ouvre en reliant à ce qui précède (une phrase de transition suffit, pas de résumé) et referme en tendant vers la suite. (2) PREMIÈRE OCCURRENCE GLOBALE — un concept, un sigle, un système (BLINK, CRF…) ne se présente qu'UNE fois dans tout le document, à sa première apparition ; ensuite emploie-le nu. Consulte le récapitulatif « déjà posé » fourni : ce qui y figure est déjà introduit. (3) RYTHME, ET IL SE MESURE — vise 18 à 22 mots par phrase en MÉDIANE sur chaque section, et au plus une phrase sur douze au-dessus de 45 mots ; le lint mesure les deux, section par section (« prose_style »). Le levier n'est jamais de couper un fait, c'est de les répartir : une phrase porte UN fait, et sa population, son intervalle ou sa réserve suivent en phrases propres au lieu de s'empiler en incises — au plus UNE rupture (—, ;, :) par phrase. Une énumération de trois éléments ou plus s'écrit en phrases séparées, jamais en une seule phrase à points-virgules. Alterne vraiment les longueurs (une courte après une longue vaut mieux que trois moyennes) ; jamais deux paragraphes consécutifs construits sur le même moule ; pas de paragraphe entier bâti sur un moule unique répété (« X fait Y. Z fait W. ») ; pas plus d'UN chiffre secondaire par phrase — hiérarchise : le fait porteur en phrase principale, les chiffres d'appoint en incise ou dans la carte de fait. (4) REGISTRE — essai technique français : précis, direct, sans emphase ni remplissage (« il est important de noter », « dans le monde de », « véritable »… bannis). Bannis aussi le méta-discours, qui commente l'écriture au lieu d'écrire (« il faut ici nommer », « la phrase mérite qu'on s'y arrête », « et il faut le dire tel quel », « tient en une phrase »), et l'auto-référence au corpus (« ce document », « cette monographie ») partout ailleurs que dans la section écosystème, où le renvoi est l'objet : un thème voisin se nomme par son sujet, pas par sa place dans la fabrique. (5) HONNÊTETÉ — n'affirme QUE ce que la matière fournie établit ; les controverses restent des controverses.`;

// Tous les agents tournent en general-purpose (Tools: *) → WebSearch/WebFetch/Write/Bash garantis.
const A = (prompt, opts) => agent(prompt, { agentType: 'general-purpose', ...opts });

// Modèles par classe de tâche (profil hérité de frugal) : recherche/vérification/I-O en Sonnet ;
// jugement structurant (Plan, Author, Relecture, Widgets, Compose, Build) en modèle hérité (Opus).
const M_RESEARCH = 'sonnet';
const M_IO       = 'sonnet';

// ── Schémas ──────────────────────────────────────────────────────────────────
const S_SWEEP = { type:'object', additionalProperties:false, required:['sources','findings'], properties:{
  sources:{ type:'array', items:{ type:'object', additionalProperties:false, required:['title','url','kind'],
    properties:{ title:{type:'string'}, url:{type:'string'}, kind:{type:'string'}, note:{type:'string'} } } },
  findings:{ type:'array', items:{ type:'object', additionalProperties:false, required:['point','url'],
    properties:{ point:{type:'string'}, url:{type:'string'} } } } } };

const S_ARCH = { type:'object', additionalProperties:false, required:['title','kicker','fil_rouge','outline'], properties:{
  title:{type:'string'}, kicker:{type:'string'},
  fil_rouge:{type:'string'},   // l'arc narratif du document (2-3 phrases) — injecté dans CHAQUE prompt d'auteur
  outline:{ type:'array', items:{ type:'object', additionalProperties:false, required:['id','heading','angle'],
    properties:{ id:{type:'string'}, heading:{type:'string'}, angle:{type:'string'},
      kind:{ type:'string', enum:['normal','ecosystem'] },
      angle_key:{ type:'string', enum:['foundations','theory','variants','applications','misconceptions','ecosystem'] }
    } } } } };

// Extract LEAN : des NOTES sourcées, pas de prose (la prose vient après le council).
const S_NOTES = { type:'object', additionalProperties:false, required:['id','heading','notes','claims'], properties:{
  id:{type:'string'}, heading:{type:'string'},
  notes:{ type:'array', items:{ type:'object', additionalProperties:false, required:['point','url'],
    properties:{ point:{type:'string'}, url:{type:'string'} } } },
  claims:{ type:'array', items:{ type:'object', additionalProperties:false, required:['statement','candidate_sources'],
    properties:{ statement:{type:'string'},
      candidate_sources:{ type:'array', items:{type:'string'} },
      examples:{ type:'array', items:{type:'string'} },
      kind:{ type:'string', enum:['established','contestable'] } } } },
  pointers:{ type:'array', items:{ type:'object', additionalProperties:false, required:['name','url'],
    properties:{ name:{type:'string'}, url:{type:'string'},
      kind:{ type:'string', enum:['library','package','tool','reading','implementation'] },
      blurb:{type:'string'} } } } } };

// Verdict d'un juré BATCH : un verdict PAR claim de la section (claim_index aligné).
const S_BATCH = { type:'object', additionalProperties:false, required:['verdicts'], properties:{
  verdicts:{ type:'array', items:{ type:'object', additionalProperties:false,
    required:['claim_index','holds','corrected_statement','independent_sources','note','search_exhausted','document_source'],
    properties:{ claim_index:{type:'integer'}, holds:{type:'boolean'}, search_exhausted:{type:'boolean'}, document_source:{type:'boolean'},
      corrected_statement:{type:'string'},
      independent_sources:{ type:'array', items:{ type:'object', additionalProperties:false, required:['title','url'],
        properties:{ title:{type:'string'}, url:{type:'string'} } } },
      note:{type:'string'} } } } } };

// Verdict du juré DÉDIÉ (un claim contestable, lentille source primaire).
const S_VERDICT = { type:'object', additionalProperties:false, required:['holds','corrected_statement','independent_sources','note','search_exhausted','document_source'], properties:{
  holds:{type:'boolean'}, search_exhausted:{type:'boolean'}, document_source:{type:'boolean'},
  corrected_statement:{type:'string'},
  independent_sources:{ type:'array', items:{ type:'object', additionalProperties:false, required:['title','url'],
    properties:{ title:{type:'string'}, url:{type:'string'} } } },
  note:{type:'string'} } };

const S_POINTERS = { type:'object', additionalProperties:false, required:['pointers'], properties:{
  pointers:{ type:'array', items:{ type:'object', additionalProperties:false, required:['name','url','blurb'],
    properties:{ name:{type:'string'}, url:{type:'string'},
      kind:{ type:'string' }, blurb:{type:'string'} } } } } };

const S_AUTHOR = { type:'object', additionalProperties:false, required:['files_written'], properties:{
  files_written:{ type:'array', items:{type:'string'} } } };

// Une tranche de prose : les sections rédigées + le récapitulatif pour la tranche suivante.
const S_PROSE = { type:'object', additionalProperties:false, required:['sections','summary'], properties:{
  sections:{ type:'array', minItems:1, items:{ type:'object', additionalProperties:false, required:['id','prose'],
    properties:{ id:{type:'string'}, prose:{type:'string'} } } },
  summary:{type:'string'} } };

// Relecture de continuité : des ÉDITIONS ponctuelles (find→replace), appliquées en JS —
// jamais une réécriture intégrale (diff minimal par construction, pas de plafond de sortie).
const S_EDITS = { type:'object', additionalProperties:false, required:['edits'], properties:{
  edits:{ type:'array', items:{ type:'object', additionalProperties:false,
    required:['section_id','find','replace'],
    properties:{ section_id:{type:'string'}, find:{type:'string'}, replace:{type:'string'},
      reason:{type:'string'} } } } } };

const S_PROSEAUDIT = { type:'object', additionalProperties:false, required:['checked','fixed','hedged','note'], properties:{
  checked:{type:'integer'}, fixed:{type:'integer'}, hedged:{type:'integer'}, note:{type:'string'} } };

const S_COMPOSE = { type:'object', additionalProperties:false, required:['files_written','element_counts'], properties:{
  files_written:{ type:'array', items:{type:'string'} },
  element_counts:{ type:'object', additionalProperties:false, required:['document'],
    properties:{ document:{type:'integer'} } } } };

const S_VERDICTS = { type:'object', additionalProperties:false, required:['files_written','n_substances','n_rows'], properties:{
  files_written:{ type:'array', items:{type:'string'} },
  n_substances:{type:'integer'}, n_rows:{type:'integer'} } };

const S_WIDGET_PLAN = { type:'object', additionalProperties:false, required:['widgets'], properties:{
  widgets:{ type:'array', items:{ type:'object', additionalProperties:false,
    required:['concept','after_section_id','brief','kind'],
    properties:{ concept:{type:'string'}, after_section_id:{type:'string'}, brief:{type:'string'},
      kind:{ type:'string', enum:['probe','process','figure'] }, anchor:{type:'string'} } } } } };

const S_WIDGET_CODE = { type:'object', additionalProperties:false,
  required:['ref','title','after_section_id','kind'],
  properties:{ ref:{type:'string'}, title:{type:'string'}, after_section_id:{type:'string'},
    kind:{ type:'string', enum:['probe','process'] } } };

const S_WIDGET_CRITIC = { type:'object', additionalProperties:false, required:['ok','issues'],
  properties:{ ok:{type:'boolean'}, issues:{ type:'array', items:{type:'string'} } } };

const S_FIGURE_CODE = { type:'object', additionalProperties:false,
  required:['ref','after_section_id','caption','kind'],
  properties:{ ref:{type:'string'}, after_section_id:{type:'string'}, caption:{type:'string'},
    kind:{ type:'string', enum:['figure'] } } };

const S_BUILD = { type:'object', additionalProperties:false, required:['success','files','acceptance','errors'], properties:{
  success:{type:'boolean'},
  files:{ type:'array', items:{type:'string'} },
  build_output:{type:'string'},
  lint_flags:{type:'integer'},      // flags non hedgés remontés par lint.py (post)
  lint_fixed:{type:'integer'},      // flags adjugés « affirmation » et corrigés
  lint_note:{type:'string'},
  acceptance:{ type:'object', additionalProperties:false, required:['confirmed_claims','all_confirmed_have_2plus_sources','audit_categories_present'],
    properties:{ confirmed_claims:{type:'integer'}, all_confirmed_have_2plus_sources:{type:'boolean'},
      audit_categories_present:{ type:'array', items:{type:'string'} } } },
  errors:{ type:'array', items:{type:'string'} } } };

const S_CKPT = { type:'object', additionalProperties:false, required:['written'], properties:{ written:{type:'boolean'} } };
// Reprise granulaire : un index (noms de fichiers + petits artefacts), puis UN loader PAR
// section — évite le plafond de sortie 32k du loader monolithique sur les gros thèmes.
// I/O interne (recopie verbatim de gros fichiers) : additionalProperties TOLÉRÉ — un champ
// parasite émis en fin de génération ne doit pas invalider 79 Ko de contenu correct.
const S_LOAD_INDEX = { type:'object', additionalProperties:true, required:['sec_ids','research','widgets','prose'], properties:{
  sec_ids:{ type:'array', items:{type:'string'} },   // ids extraits des noms sec-<id>.json
  research:{type:'string'},                           // contenu verbatim de research.json ("" si absent)
  widgets:{type:'string'},                            // contenu verbatim de widgets.json ("" si absent)
  prose:{type:'string'} } };                          // contenu verbatim de prose.json ("" si absent)
const S_LOAD_ONE = { type:'object', additionalProperties:true, required:['content'], properties:{ content:{type:'string'} } };

// ── Helpers JS (transformations déterministes — pas de jugement) ─────────────
// L'identifiant d'un document vit PARFOIS DANS LA QUERY : DailyMed adresse chaque étiquetage
// par `?setid=…`. Supprimer la query entière (ce que faisait ce code jusqu'au 43e run) écrasait
// donc les notices du sildénafil, du tadalafil et du vardénafil — trois médicaments, trois
// documents — en UNE seule source, et fabriquait des faux rejets sur la section sécurité.
// On garde la query, en retirant les seuls paramètres de SUIVI : ceux-là disent par quel chemin
// on est arrivé, jamais de quel document il s'agit. Le fragment (#section) désigne un endroit
// DANS le document : il tombe. Les paires sont triées pour que l'ordre ne crée pas deux clés.
// Casse : hôte et chemin sont normalisés, la query NON — un identifiant peut y être sensible.
const TRACKING_PARAMS = /^(utm_[a-z_]+|fbclid|gclid|msclkid|igshid|mc_cid|mc_eid|_ga)$/i;
const normUrl = u => {
  const s = (u||'').trim().replace(/^https?:\/\//i,'').replace(/#.*$/,'');
  const q = s.indexOf('?');
  const base = (q < 0 ? s : s.slice(0, q)).replace(/\/+$/,'').toLowerCase();
  if (q < 0) return base;
  const kept = s.slice(q + 1).split('&')
    .filter(p => p && !TRACKING_PARAMS.test(p.split('=')[0]))
    .sort();
  return kept.length ? base + '?' + kept.join('&') : base;
};
const SECTION_CLAIM_QUOTA = 2;      // claims survivants requis pour qu'une section NORMALE survive
// DISJONCTEUR, pas garde-fou de coût : l'architecte ne voit JAMAIS cette valeur (son prompt dit
// « typiquement 4 à 9 », en dur), donc la relever ne peut pas le pousser à proposer davantage —
// elle décide seulement de ce qu'on JETTE. Sur les 32 plans de l'historique (médiane 10, max 14),
// un plafond de 9 coupait 27 sections ; à 16 il n'en coupe aucune et ne coûte rien de plus sur
// les plans qui tiennent en dessous. La sobriété éditoriale est portée par le prompt ; ce nombre
// n'est là que pour arrêter un vrai déraillement. Surchargeable par args.maxSections.
const MAX_SECTIONS = Number(A0.maxSections) > 0 ? Number(A0.maxSections) : 16;
const MAX_CLAIMS_PER_SECTION = 4;
const PROSE_CHUNK = 3;              // sections rédigées par tranche d'auteur (séquentiel, voix continue)
const MAX_EDITS = 40;               // plafond d'éditions de la relecture de continuité

function dedupSources(list) {
  const seen = new Map();
  for (const s of list) { const k = normUrl(s.url); if (k && !seen.has(k)) seen.set(k, s); }
  return [...seen.values()];
}

// Identité du DOCUMENT, pas de l'URL. Un même travail se présente sous plusieurs entrées —
// arxiv /abs/ vs /html/ vs /pdf/, préprint vs actes de conférence, blog ou dataset card des
// mêmes auteurs — et ne vaut qu'UNE source pour le seuil ≥2. Sans ça le seuil se contourne
// sans le vouloir : un juré cite le PDF, un autre la page abs, le compteur lit 2.
// Chaque source produit PLUSIEURS clés (identifiant + titre) : deux entrées sont le même
// travail dès qu'UNE clé coïncide — l'identifiant seul rate le blog, le titre seul rate
// les entrées dont le nom varie.
const docKeys = s => {
  const u = normUrl(s.url), t = (s.title || '').toLowerCase();
  const keys = [];
  const arx = (u.match(/arxiv\.org\/(?:abs|html|pdf)\/(\d{4}\.\d{4,5})/) ||
               t.match(/arxiv:\s*(\d{4}\.\d{4,5})/) || [])[1];
  if (arx) keys.push('arxiv:' + arx);
  // Le DOI identifie le document où qu'il apparaisse dans l'URL, pas seulement derrière
  // doi.org : les éditeurs le posent dans LEUR propre chemin, précédé d'un segment de rendu
  // qui varie pour un même article (« /doi/pdf/10.1177/… » et « /doi/10.1177/… » chez SAGE,
  // « /doi/full/ », « /doi/epub/ » ailleurs). Sans cette clé, les deux formes ne partagent
  // aucune clé et le MÊME article compte pour DEUX sources indépendantes — bug du 45e run
  // (microdosage-psychedeliques, claim:41). L'extension finale est retirée : « …204.pdf » et
  // « …204 » sont le même DOI.
  const doi = (u.match(/(10\.\d{4,9}\/[^\s?&#]+)/) || [])[1];
  if (doi) keys.push('doi:' + doi.replace(/\.(pdf|epub|full|html?|xml)$/, ''));
  // titre dépouillé de son suffixe d'édition : « … — NeurIPS 2023 PDF », « … (blog HF) »
  const base = t.split(/\s+[—–-]\s+|\s*\(/)[0].replace(/[^a-z0-9]+/g, '');
  if (base.length >= 12) keys.push('title:' + base);
  // Une URL = UN document : clé d'URL TOUJOURS posée, sinon la même page citée sous deux
  // titres différents produit deux clés `title:` et compte pour deux sources indépendantes,
  // alors que ensureSrc (indexé par normUrl) la ramène à un seul id (bug du 32e run).
  if (u) keys.push('url:' + u);
  if (!keys.length) keys.push('url:' + u);
  return keys;
};

// Sources de SOUTIEN uniquement : on n'agrège QUE les independent_sources des verdicts passés.
function collectSources(verdicts) {
  const out = [], seen = new Set();
  for (const v of verdicts) for (const s of (v.independent_sources || [])) {
    const keys = docKeys(s);
    if (keys.some(k => seen.has(k))) continue;       // même travail sous une autre forme
    keys.forEach(k => seen.add(k));
    out.push({ title: s.title || s.url, url: s.url });
  }
  return out;
}

// Décision d'audit : le SEUIL est en code ; l'INDÉPENDANCE des sources est jugée par les jurés.
// IDENTIQUE à monograph/frugalmonograph — le profil lean ne touche pas cette règle.
function decideAudit(claim, verdicts) {
  const holds = verdicts.filter(v => v.holds);
  const corrected = verdicts.filter(v => !v.holds && v.corrected_statement && v.corrected_statement.trim());
  if (holds.length >= 2) {
    const sources = collectSources(holds);
    if (sources.length >= 2)
      return { audit:'confirmed', statement: claim.statement, sources,
               note: `Confirmé : ${holds.length}/${verdicts.length} jurés, ${sources.length} sources indépendantes.` };
  }
  // Exception « document-source » : un énoncé qui décrit le CONTENU d'un document de référence
  // (position de société savante, avis d'agence, fiche officielle) n'a qu'UNE source par nature —
  // on ne corrobore pas « ce document dit X » par un second document. Le lui refuser au décompte
  // fabrique un faux rejet (règle adoptée le 2026-08-10 sur berberine, reconfirmée le 2026-08-15
  // sur cafeine-ergogene ; jusque-là appliquée à la main APRÈS le build, deux fois).
  // Garde-fous, dans cet ordre : (1) elle ne se déclenche QUE si le seuil normal a échoué, la
  // branche ci-dessus étant essayée d'abord ; (2) UNANIMITÉ — tous les jurés tiennent l'énoncé ET
  // le qualifient de document-source, un seul oubli et on retombe sur le rejet (fail closed) ;
  // (3) la note DIT que la source est unique par nature, elle ne prétend jamais 2 sources.
  // Elle ne couvre PAS un résultat empirique mono-source : cette distinction est portée par le
  // prompt du juré, c'est un jugement, pas un test.
  if (holds.length >= 2 && holds.length === verdicts.length &&
      holds.every(v => v.document_source === true)) {
    const sources = collectSources(holds);
    if (sources.length >= 1)
      return { audit:'confirmed', statement: claim.statement, sources,
               note: `Confirmé sur lecture directe (règle document-source) : ${holds.length}/${verdicts.length} jurés. Ce claim décrit le contenu d'un document de référence — SA SOURCE EST UNIQUE PAR NATURE, le seuil ≥2 ne s'y applique pas.` };
  }
  if ((holds.length + corrected.length) >= 2) {
    const sources = collectSources([...holds, ...corrected]);
    if (sources.length >= 2)
      return { audit:'corrected', statement: corrected[0].corrected_statement.trim(), sources,
               note: `Énoncé d'origine imprécis, corrigé après vérification (${sources.length} sources indépendantes). Origine : « ${claim.statement} »` };
  }
  const sources = collectSources([...holds, ...corrected]);
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
  STYLE,
  `Findings (point → url, champ _angle = angle de sweep d'origine) :\n${JSON.stringify(findings)}`,
  `Sources :\n${JSON.stringify(sources.map(s => ({ title:s.title, url:s.url, kind:s.kind })))}`,
  `Rends : title (titre du document, sans suffixe d'édition), kicker (sur-titre court), fil_rouge (l'ARC NARRATIF du document en 2-3 phrases : ce que le lecteur comprend progressivement, de la question d'ouverture à la conclusion — il guidera CHAQUE section), et outline = AUTANT de sections que la matière trouvée le justifie (typiquement 4 à 9). Propose LARGE : une section par sous-thème réellement documenté. Les sections sans matière vérifiable seront élaguées automatiquement — ne t'autocensure pas, mais n'invente pas de section creuse.`,
  `Chaque section : id (kebab-case ascii, unique), heading, angle (ce qu'elle couvre ET son rôle dans l'arc), angle_key (clé de l'angle de sweep qui l'a principalement documentée, parmi : foundations, theory, variants, applications, misconceptions, ecosystem — si kind="ecosystem" alors angle_key="ecosystem").`,
  `Couvre fondations → propriétés → variantes/applications → limites. Si le sujet a un écosystème d'outils/bibliothèques/packages/lectures, AJOUTE une section finale kind="ecosystem" (heading type « Écosystème & pour aller plus loin »). Les autres sections : kind="normal". Pas de section "glossaire"/"biblio" (ajoutées à la composition).`,
].join('\n');

// Extract LEAN : notes sourcées + claims — AUCUNE prose (rédigée après le council).
const extractPrompt = (sec, findings) => [
  `Sujet : « ${subject} ». Section « ${sec.heading} » — angle : ${sec.angle}.`,
  `Findings disponibles (point → url) :\n${JSON.stringify(findings)}`,
  WEB + ' (autorisé pour compléter/préciser une source.)',
  `Produis pour CETTE section — PAS de prose (elle sera rédigée plus tard, après vérification) :`,
  `- notes : 6 à 15 points factuels PRÉCIS et sourcés (point net + url exacte d'où il vient), la matière brute de la future prose. Reprends les findings pertinents et complète-les au besoin. Chiffres, mécanismes, attributions, dates — un fait par note. N'invente rien.`,
  `- claims : 2 à 4 énoncés factuels vérifiables, LES PLUS PORTEURS de la section (ceux qui méritent le council). Pour CHAQUE claim : statement (une phrase nette), candidate_sources (urls qui l'étayent), examples (0-2 exemples concrets), kind.`,
  `IMPORTANT pour exercer la vérification : inclure au moins UN claim kind="contestable" — un énoncé fréquemment affirmé mais possiblement imprécis ou faux (idée reçue), à départager par les jurés. Les autres = kind="established".`,
  `Si CETTE section concerne l'écosystème (outils/bibliothèques/packages/lectures) : remplis "pointers" = liste {name, url (lien officiel réel), kind ∈ library|package|tool|reading|implementation, blurb (1 phrase)}. Les pointeurs ne sont PAS des claims (pas de seuil ≥2 sources) : ce sont des renvois curés. N'invente jamais d'URL.`,
  `Rends : id="${sec.id}", heading="${sec.heading}", notes, claims, pointers (si écosystème).`,
].join('\n');

// Council par SECTION — 2 lentilles adversariales, chacune audite TOUS les claims en une passe.
const BATCH_LENSES = [
  `SOUTIEN & INDÉPENDANCE : pour chaque claim, trouve des sources qui le CONFIRMENT mais indépendantes entre elles et de l'origine du claim (pas deux pages qui citent le même papier, pas miroir/repost — arXiv et ar5iv sont le MÊME document). Remonte à la source primaire quand c'est elle qui fait foi. Ne liste que des sources réellement indépendantes que TOI tu as ouvertes.`,
  `RÉFUTATION : pour chaque claim, cherche activement à l'INVALIDER. Contre-exemples, nuances, sources qui le contredisent, chiffres qui ne collent pas avec la source primaire. Sois sévère : un claim qui sur-généralise, sur-restreint ou déforme sa source ne tient PAS tel quel.`,
];
const BATCH_LENS_NAMES = ['soutien', 'réfutation'];

const batchVerifyPrompt = (sec, claims, lensIdx) => [
  `Sujet : « ${subject} ». Tu es juré du council pour la section « ${sec.heading} » — tu audites ${claims.length} claim(s) EN UNE PASSE.`,
  `Ton rôle — ${BATCH_LENSES[lensIdx]}`,
  `Claims (claim_index → énoncé + sources candidates déjà trouvées en amont) :`,
  ...claims.map((c, i) => `[${i}] « ${c.statement} »\n    candidates : ${JSON.stringify(c.candidate_sources || [])}`),
  `MÉTHODE (économie) : les claims d'une même section citent souvent LES MÊMES papiers — ouvre chaque source candidate UNE seule fois (WebFetch) et évalue à cette occasion TOUS les claims qu'elle concerne. Ne lance une NOUVELLE recherche que si les candidates sont insuffisantes pour ton rôle. ` + WEB,
  `Rends : verdicts = UN verdict PAR claim (claim_index aligné sur la numérotation ci-dessus, tous présents) : holds (true si l'énoncé tient TEL QUEL), corrected_statement ("" si rien à corriger ; sinon l'énoncé corrigé minimal qui serait vrai), independent_sources (UNIQUEMENT les sources que TOI tu as vérifiées et qui sont indépendantes — title+url réels), note (1-2 phrases justifiant), search_exhausted (true UNIQUEMENT si tes moyens de recherche étaient épuisés ou indisponibles pendant cet audit — sinon false).`,
  `N'invente jamais d'URL. holds juge l'EXACTITUDE seule : true si le contenu tient tel quel, vérifié à la source — un claim qui sur-généralise, sur-restreint ou déforme sa source ne tient PAS. L'indépendance et le seuil ≥2 sources sont tranchés par le code à partir des independent_sources de tous les jurés : ne vote JAMAIS false pour un simple doute d'indépendance — en cas de doute sur une source, ne la liste pas, c'est tout. En cas de doute sur la VÉRACITÉ, penche vers holds=false. Si tes moyens de recherche sont épuisés (quota, outil indisponible), renseigne search_exhausted=true et dis-le dans note. Chaque verdict est INDIVIDUEL : ne laisse pas la solidité d'un claim déteindre sur son voisin.`,
  `document_source : true UNIQUEMENT si l'énoncé décrit le CONTENU d'un DOCUMENT DE RÉFÉRENCE que tu as lu toi-même — position de société savante, recommandation, avis d'agence, fiche officielle, norme — et dont le contenu EST le fait énoncé (« la position stand ISSN retient 3-6 mg/kg », « l'EFSA fixe le seuil à 400 mg/j »). Un tel énoncé n'a qu'une source PAR NATURE : on ne corrobore pas « ce document dit X » par un second document, et le code lui appliquera une exception au seuil ≥2 — mais SEULEMENT si TOUS les jurés le qualifient ainsi. Sinon false. En particulier false pour un RÉSULTAT EMPIRIQUE (« une méta-analyse de 13 études trouve un gradient SMD 0,30 », « cet essai mesure +4,9 % »), même publié dans une revue de rang fort et même s'il n'existe qu'une seule publication au monde : ce fait-là reste soumis au seuil ≥2 sources, et la réserve « source unique, non corroborée » en prose est le bon traitement. Dans le doute, false.`,
].join('\n');

// Juré DÉDIÉ pour un claim contestable : confrontation au texte faisant autorité.
const extraJurorPrompt = (claim) => [
  `Énoncé CONTESTABLE à vérifier : « ${claim.statement} »`,
  `Sources candidates DÉJÀ trouvées en amont — COMMENCE par celles-ci (ouvre-les via WebFetch AVANT toute nouvelle recherche) : ${JSON.stringify(claim.candidate_sources || [])}`,
  `Ton rôle de juré — SOURCE PRIMAIRE : remonte à la source faisant autorité (papier original, spécification, manuel) et vérifie que l'énoncé y correspond EXACTEMENT, sans déformation (chiffres, périmètre, causalité, attribution).`,
  WEB,
  `Rends un verdict HONNÊTE : holds (true si l'énoncé tient TEL QUEL), corrected_statement ("" si rien à corriger ; sinon l'énoncé corrigé minimal qui serait vrai), independent_sources (UNIQUEMENT les sources que TOI tu as vérifiées — title+url réels), note (1-2 phrases justifiant), search_exhausted (true UNIQUEMENT si tes moyens de recherche étaient épuisés ou indisponibles pendant cet audit — sinon false).`,
  `N'invente jamais d'URL. holds juge l'EXACTITUDE seule : l'indépendance des sources est tranchée par le code — ne vote JAMAIS false pour un simple doute d'indépendance ; en cas de doute sur la VÉRACITÉ, penche vers holds=false. Si tes moyens de recherche sont épuisés, renseigne search_exhausted=true et dis-le dans note.`,
  `document_source : true UNIQUEMENT si l'énoncé décrit le CONTENU d'un DOCUMENT DE RÉFÉRENCE que tu as lu toi-même — position de société savante, recommandation, avis d'agence, fiche officielle, norme — et dont le contenu EST le fait énoncé (« la position stand ISSN retient 3-6 mg/kg », « l'EFSA fixe le seuil à 400 mg/j »). Un tel énoncé n'a qu'une source PAR NATURE : on ne corrobore pas « ce document dit X » par un second document, et le code lui appliquera une exception au seuil ≥2 — mais SEULEMENT si TOUS les jurés le qualifient ainsi. Sinon false. En particulier false pour un RÉSULTAT EMPIRIQUE (« une méta-analyse de 13 études trouve un gradient SMD 0,30 », « cet essai mesure +4,9 % »), même publié dans une revue de rang fort et même s'il n'existe qu'une seule publication au monde : ce fait-là reste soumis au seuil ≥2 sources, et la réserve « source unique, non corroborée » en prose est le bon traitement. Dans le doute, false.`,
].join('\n');

const pointersPrompt = (candidates) => [
  `Voici des pointeurs candidats (outils/bibliothèques/packages/lectures) extraits de la recherche : ${JSON.stringify(candidates).slice(0, 8000)}`,
  WEB,
  `Pour CHAQUE pointeur, VÉRIFIE que l'URL existe réellement et pointe l'outil/la ressource annoncé(e). GARDE uniquement ceux dont l'URL résout et correspond. Corrige l'URL vers le lien officiel si nécessaire ; n'en invente aucun.`,
  `Rends : pointers = liste finale {name, url (réel), kind, blurb (1 phrase factuelle)}. Liste vide si aucun ne tient.`,
].join('\n');

const authorTldrGlossPrompt = (sectionsBrief) => [
  `Tu es l'auteur. Tu ÉCRIS des fichiers dans le dossier de thème : ${themeDir}`,
  TERMINO,
  STYLE,
  `${themeDir}/knowledge.json a été écrit par l'étape précédente — lis-le pour connaître les claims vérifiés avant de rédiger le glossaire et le tldr.`,
  `Assure-toi que le dossier existe (mkdir -p si besoin), puis ÉCRIS exactement ces fichiers :`,
  ``,
  `1) ${themeDir}/glossary.json — un tableau JSON de 4 à 7 termes du sujet : {term, definition, see_also?}. « term » = forme canonique du concept (garde l'anglais si c'est la référence, ex. « embedding ») ; la traduction FR éventuelle va dans « definition ». Définitions exactes, propres au sujet « ${subject} ». "see_also" est une CHAÎNE (jamais une liste) : pour renvoyer vers plusieurs termes, une seule chaîne séparée par ", ". Les entrées doivent couvrir les termes et sigles PIVOTS du sujet (concepts porteurs, récurrents) : aucun terme central ne doit manquer au glossaire.`,
  ``,
  `2) ${themeDir}/tldr.json — { "these": "<accroche en 1 phrase>", "part1": ["…","…"], "part2": ["…","…"] }. part1 et part2 = 2-4 puces chacune (part1 = ce que le lecteur va comprendre ; part2 = garanties et limites). Ce fichier alimente le RÉSUMÉ (abstract) en tête du document — le passage le PLUS LU : il doit se lire sans effort. RÈGLE D'OR : le résumé donne envie et oriente, les preuves vivent dans le corps.`,
  `   - THÈSE : une seule phrase de 30 mots au plus, UNE idée, une incise au maximum. Une accroche, pas une table des matières compressée.`,
  `   - PUCES : une phrase par puce, sujet et verbe rapprochés, même registre que la prose.`,
  `   - INTERDITS dans tout le tldr : chiffres et nombres (années, pourcentages, scores — un chiffre n'est toléré que dans un nom propre : « 1-WL », « D3PM ») ; citations (auteurs, venues) ; comparaisons chiffrées ; points-virgules en série ; sigles non déployés.`,
  `   - VÉRACITÉ : chaque puce reste FONDÉE sur un claim vérifié de knowledge.json (jamais sur ta mémoire) — reformule l'idée SANS embarquer la preuve ; n'affirme rien que le document n'établit.`,
  ``,
  `Sections du document (pour cohérence de ton glossaire/tldr) :\n${sectionsBrief}`,
  ``,
  `Rends : files_written (chemins écrits).`,
].join('\n');

// Rédaction d'une TRANCHE de prose (≤ PROSE_CHUNK sections), APRÈS l'audit.
const prosePrompt = (title, filRouge, outline, prevSummaries, chunkSecs) => [
  `Tu rédiges la prose du document « ${title} » (sujet : « ${subject} »). La vérification factuelle est DÉJÀ faite : tu écris depuis une matière auditée, tu n'as RIEN à vérifier — et rien à inventer.`,
  VOICE,
  TERMINO,
  STYLE,
  `FIL ROUGE du document : ${filRouge}`,
  `PLAN COMPLET (pour situer tes sections dans l'arc) :\n${outline.map(o => `- ${o.id} : ${o.heading} — ${o.angle}`).join('\n')}`,
  prevSummaries.length
    ? `DÉJÀ POSÉ par les sections précédentes (ne ré-introduis RIEN de ce qui suit ; enchaîne) :\n${prevSummaries.join('\n')}`
    : `Tu ouvres le document : la première section pose le problème et les notions de base.`,
  ``,
  `TES SECTIONS (dans l'ordre). Pour chacune : ses CLAIMS VÉRIFIÉS (l'ossature factuelle — leur énoncé fait foi) et ses NOTES sourcées (matière d'appoint).`,
  JSON.stringify(chunkSecs),
  ``,
  `RÈGLES DURES SUR LES FAITS :`,
  `- Chaque fait PRÉCIS et falsifiable (chiffre, pourcentage, date, attribution d'auteurs, nom de système, benchmark) de ta prose provient des claims (priorité — leur énoncé exact fait foi) ou des notes fournies. N'introduis AUCUN fait précis de ta propre mémoire : si un point te semble manquer, formule-le qualitativement ou omets-le.`,
  `- Tisse les claims dans le récit (le lecteur verra aussi leur carte de fait sous la section : la prose CONTEXTUALISE, elle ne les recopie pas mot à mot).`,
  `- GARDE-FOUS : si une section porte un champ "garde_fous", chaque entrée signale un point sur lequel un juré a vérifié à la source qu'une formulation candidate était FAUSSE ("version_fautive"), avec la formulation exacte ("version_exacte"). Ces énoncés n'ont PAS passé le council : n'en fais jamais un fait porteur, et ne les mets pas en avant. Mais les NOTES ci-dessus peuvent porter le même fait dans sa version fautive — si tu l'emploies malgré tout, emploie la VERSION EXACTE ; si elle ne te suffit pas, omets le fait. Ne recopie jamais la version fautive.`,
  `- Ne délaye pas : autant de paragraphes que la matière l'exige, pas plus.`,
  `Format : pour chaque section, prose = paragraphes HTML (<p>…</p>) uniquement, sans titre (le heading est ajouté à l'assemblage).`,
  `Rends : sections = [{id, prose}] (tes sections, dans l'ordre) ; summary = récapitulatif COMPACT pour l'auteur de la tranche suivante — concepts/sigles/systèmes introduits (avec la formulation de 1re occurrence utilisée), exemples filés, notations posées. 5-10 lignes.`,
].join('\n');

// Relecture de continuité : UN relecteur, TOUT le document, éditions ponctuelles seulement.
const editorPrompt = (title, filRouge, sectionsAll) => [
  `Tu es le relecteur de CONTINUITÉ du document « ${title} ». La prose a été rédigée en ${Math.ceil(sectionsAll.length / PROSE_CHUNK)} tranches par le même cahier des charges — ta mission : la faire lire comme UN texte.`,
  `FIL ROUGE : ${filRouge}`,
  `Sections (id, heading, prose HTML) :\n${JSON.stringify(sectionsAll)}`,
  `CHERCHE UNIQUEMENT : (1) ré-introductions — un concept/sigle/système présenté une 2e fois (garde la 1re occurrence, allège les suivantes) ; (2) transitions absentes ou cassées aux frontières de tranches ; (3) répétitions de formulation (même tournure d'ouverture, même connecteur) entre sections voisines ; (4) incohérences de terminologie (deux noms pour la même chose).`,
  `NE TOUCHE PAS aux faits : aucun chiffre, date, nom propre, attribution, URL ne change. Pas de réécriture de fond — des retouches de couture.`,
  TERMINO,
  STYLE,
  `Rends : edits = liste d'éditions ponctuelles {section_id, find (extrait EXACT et UNIQUE de la prose de cette section, avec ses balises), replace, reason (courte)}. "find" doit apparaître UNE seule fois dans la section visée — prends assez de contexte. Maximum ${MAX_EDITS} éditions ; liste vide si le texte coule déjà.`,
].join('\n');

// Audit-prose : lint --pre + vérification des chiffres prose-only contre leurs sources.
const proseAuditPrompt = (notesBySection) => [
  `AUDIT DE PROSE avant assemblage. Répertoire du thème : ${themeDir}`,
  `1) Exécute : python3 "${lintScript}" "${themeDir}" --pre`,
  `   Le rapport JSON liste : "novel_numbers" (chiffres significatifs de la prose/tldr/glossaire ABSENTS de knowledge.json — candidats faits non vérifiés) et "rejected_flags" (pivots de claims rejetés — attendu vide ici, la prose est écrite sans eux).`,
  `2) Pour CHAQUE novel_number : retrouve sa source dans les notes ci-dessous (le chiffre vient normalement d'une note sourcée) et VÉRIFIE-le en ouvrant l'URL (WebFetch). S'il n'apparaît dans aucune note, vérifie-le par une recherche web courte. ${WEB}`,
  `3) Verdicts et actions (Edit CHIRURGICAL de ${themeDir}/sections_draft.json — ou tldr.json/glossary.json si le chiffre y vit) :`,
  `   - EXACT (la source le confirme tel quel) → ne touche à rien.`,
  `   - FAUX/DÉFORMÉ → corrige le chiffre/l'attribution vers la valeur de la source.`,
  `   - INVÉRIFIABLE (source inaccessible, chiffre introuvable) → retire le chiffre ou reformule qualitativement. Ne laisse JAMAIS un chiffre invérifiable affirmé.`,
  `   Ne modifie QUE les passages concernés ; garde un JSON valide ; n'ajoute aucun fait.`,
  `4) S'il y a des rejected_flags non hedgés : lis le contexte ; si le passage AFFIRME le contenu rejeté, corrige-le (retrait ou réserve « source unique, non corroborée ») ; s'il le CRITIQUE ou le cite en biblio, laisse.`,
  `5) STYLE (signalé, jamais bloquant) : le rapport porte « prose_style » — médiane des longueurs de phrase et part de phrases de plus de 45 mots, par section. Pour CHAQUE section listée dans "sections_over", découpe : une phrase-liste redevient une liste de phrases, une incise qui porte un fait autonome redevient une phrase. Ne retire AUCUN chiffre, AUCUNE attribution, AUCUNE réserve — et laisse chaque réserve à moins de 350 caractères du chiffre qu'elle qualifie, sinon le check des claims rejetés la perd de vue. Si une section reste au-dessus du seuil après découpage, dis-le dans ta note plutôt que de sacrifier un fait.`,
  `6) INDÉPENDANCE DES SÉRIES : partout où la prose présente deux séries chiffrées comme INDÉPENDANTES (« deux études distinctes », « deux recrutements différents », « une revue distincte »), compare leurs effectifs et valeurs secondaires et vérifie que les deux URLs décrivent des TRAVAUX différents — pas un résumé et sa source primaire. Corrige UNIQUEMENT sur preuve de duplication (mêmes effectifs, mêmes valeurs des deux côtés) : c'est alors UNE seule source, et l'argument d'indépendance disparaît de la prose. Si les valeurs diffèrent, ne touche à rien — un hedge injustifié est une erreur au même titre qu'une affirmation fausse. Un doute d'attribution que TU soulèves n'est jamais « hors périmètre » : tranche-le avant de rendre.`,
  ``,
  `NOTES SOURCÉES par section (point → url) :\n${JSON.stringify(notesBySection)}`,
  ``,
  `Rends : checked (chiffres vérifiés), fixed (corrections appliquées), hedged (retraits/réserves), note (résumé court, mentionne tout chiffre resté douteux et tout doute d'attribution tranché).`,
].join('\n');

const widgetPlanPrompt = (secs) => [
  `Sujet : « ${subject} ». Sections RETENUES du document (id, heading, prose, faits clés) :`,
  JSON.stringify(secs),
  `Décide quels CONCEPTS/MÉCANISMES méritent un APPUI VISUEL, et de quel TYPE (champ "kind") : "probe", "process" ou "figure". Choisis UN SEUL outil visuel par concept (anti-surcharge) ; rien pour le trivial.`,
  `• "probe" — widget interactif d'UN mécanisme ISOLÉ. Seulement si NON TRIVIAL et plus clair MONTRÉ qu'expliqué. UN seul probe par mécanisme.`,
  `• "process" — SUPER-WIDGET synoptique d'un PROCESSUS DE BOUT EN BOUT sur une instance jouet. Seulement un VRAI processus multi-étapes — ITÉRATIF (boucle jusqu'à convergence) ou PIPELINE d'AU MOINS 3 étapes chaînées. JAMAIS un mécanisme isolé. Dans "brief", NOMME les étapes (ou la boucle) ; sinon ce n'est pas un process. Ancre sur la section de SYNTHÈSE.`,
  `• "figure" — ILLUSTRATION STATIQUE (SVG fixe : courbe, organigramme, taxonomie, schéma). Seulement quand VOIR suffit et que manipuler n'apporterait rien — pour une STRUCTURE, une ALLURE ou un SCHÉMA. JAMAIS pour le trivial/déclaratif, JAMAIS en doublon d'un widget. Pour une figure, fournis "anchor" : un court extrait VERBATIM de fin du paragraphe (dans la prose de la section) après lequel la figure doit se poser (ou "début"/"fin" de section).`,
  `Une figure peut compléter un widget seulement s'ils sont vraiment complémentaires (figure = vue fixe ; widget = exploration).`,
  `Rends : widgets = liste {concept, after_section_id (id EXACT d'une section ci-dessus), brief, kind ("probe"|"process"|"figure"), anchor (UNIQUEMENT pour les figures)}. Liste VIDE si rien ne le justifie.`,
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
  STYLE + ' WIDGET : tout le texte VISIBLE (libellés, boutons, légendes, messages, texte SVG affiché) est en français correctement ACCENTUÉ — jamais en ASCII ; applique aussi la règle TERMINOLOGIE.',
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

const figureCodePrompt = (f) => [
  `Tu produis une FIGURE STATIQUE illustrant ce point du sujet « ${subject} » : ${f.concept}.`,
  `Objectif (brief) : ${f.brief}`,
  `Fais Read de ${themeDir}/sections_draft.json. Repère la section d'id "${f.after_section_id}" et, dans sa "prose" (HTML), le paragraphe visé par ce repère : « ${f.anchor || 'fin de section'} ».`,
  `INSÈRE, par un Edit CHIRURGICAL de ${themeDir}/sections_draft.json, le bloc figure JUSTE APRÈS la balise </p> de ce paragraphe (ne modifie RIEN d'autre de la prose ; n'altère aucun fait ni aucune phrase). Forme EXACTE du bloc :`,
  `<figure class='fig'><svg viewBox='0 0 W H' role='img' aria-label='…'>…</svg><figcaption><span class='fcap-k'></span>LÉGENDE</figcaption></figure>`,
  `CONTRAINTES STRICTES : SVG autoporteur DÉTERMINISTE (aucun aléa) ; couleurs via variables de charte avec fallback (var(--blue,#23537F), var(--ink,#15202E), var(--bordeaux,#7C2A38), var(--ink-faint,#7A889B)…) ; AUCUN <script>, AUCUNE ressource externe, AUCUN file:/// ; balises équilibrées. Le <span class='fcap-k'> reste VIDE (« Figure N » est ajouté par le build). LÉGENDE = une phrase concise.`,
  `IMPORTANT — la prose est stockée dans un JSON : utilise des APOSTROPHES SIMPLES pour TOUS les attributs du bloc figure (class='fig', viewBox='…', fill='…', stroke='…', role='img', aria-label='…', class='fcap-k', etc.). Ainsi l'insertion par Edit n'introduit AUCUN guillemet " à échapper, le JSON reste valide. Le TEXTE de la légende peut contenir des apostrophes françaises sans souci.`,
  `La figure doit VRAIMENT illustrer (structure/allure/schéma), pas décorer. Choisis un <ref> kebab-case ascii unique (ex. fig-…).`,
  `Rends : ref, after_section_id = "${f.after_section_id}", caption (la légende), kind = "figure".`,
].join('\n');

const figureCriticPrompt = (coded) => [
  `Fais Read de ${themeDir}/sections_draft.json. Dans la prose de la section "${coded.after_section_id}", relis la figure insérée (légende « ${coded.caption} »).`,
  `Juge HONNÊTEMENT : (1) un seul bloc <figure class='fig'> bien formé : un <svg> équilibré, un <figcaption> avec <span class='fcap-k'> VIDE ; (2) AUCUN <script>, aucune ressource externe / file:/// ; attributs du SVG en APOSTROPHES SIMPLES (aucun guillemet droit, pour ne pas casser le JSON) ; (3) la figure ILLUSTRE vraiment (structure/allure/schéma, pas décorative) ; (4) insertion CHIRURGICALE : la prose n'a gagné QUE cette figure (le texte autour intact), et la figure suit bien une balise </p>.`,
  `Rends : ok (true SEULEMENT si les 4 tiennent), issues (problèmes précis ; vide si ok).`,
].join('\n');

const figureRecodePrompt = (coded, issues) => [
  `La figure (section "${coded.after_section_id}", légende « ${coded.caption} ») dans ${themeDir}/sections_draft.json DOIT être corrigée. Problèmes :`,
  JSON.stringify(issues),
  `Corrige par un Edit CHIRURGICAL de ${themeDir}/sections_draft.json : un seul bloc <figure class='fig'> bien formé (SVG déterministe équilibré, attributs en apostrophes simples (JSON-safe), AUCUN <script>/ressource externe/file:///, <span class='fcap-k'> VIDE, légende = une phrase concise) ; ne touche à RIEN d'autre de la prose.`,
  `Rends : ref="${coded.ref}", after_section_id="${coded.after_section_id}", caption (la légende), kind="figure".`,
].join('\n');

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
  `3. 1 à 2 {"type":"exercise","part":<str>,"question":<html>,"answer":<html>} que TU rédiges (auto-évaluation sur les points clés du document). Chaque question/réponse S'APPUIE sur les claims vérifiés de knowledge.json — aucun fait de mémoire.`,
  `4. {"type":"biblio","entries":[…depuis les entrées biblio ci-dessus…]}`,
  (pointers && pointers.length) ? `5. {"type":"pointers","title":"Pour aller plus loin","items":[…depuis les pointeurs ci-dessus…]}` : `(pas d'élément pointers : aucun pointeur)`,
  `6. {"type":"glossary"}`,
  ``,
  `meta OBLIGATOIRE : title = "${title}", kicker = "<sujet court> · monographie", h1 = "${title}", lede = 1 phrase d'accroche, meta_chips = ["Monographie"], footer = "${title} · scriptorium".`,
  `Les claims référencés doivent exister dans knowledge.json ; chaque widget ref doit exister. Crée le dossier si besoin (mkdir -p ${themeDir}). Rends files_written + element_counts:{document:<nb total d'elements>}.`,
].join('\n');

const verdictsPrompt = () => [
  `Tu produis le TABLEAU DE VERDICTS de la monographie santé « ${slug} » : ${themeDir}/verdicts.json, puis tu insères son élément au manifeste.`,
  `LIS d'abord : ${themeDir}/knowledge.json (statements + audit de chaque claim) et ${themeDir}/manifest.json (ids de sections).`,
  `SCHÉMA EXACT de verdicts.json : {"theme":"${slug}","substances":[{"id":<kebab>,"label":<nom affiché>,"safety":{"status":<autorise|interdit|restreint|pas-avis>,"label":<phrase courte>,"claims":[ids]},"adverse":{"text":<phrase>,"claims":[ids]},"rows":[{"indication":<indication discutée>,"efficacy":<nulle|faible|modeste|bonne|tres-bonne|indeterminee>,"ci":<optionnel>,"official":<optionnel>,"note":<optionnel>,"claims":[ids],"anchor":<id de section, optionnel>}]}]}`,
  `RÈGLES NON NÉGOCIABLES : (1) une ligne par indication/allégation réellement discutée dans le document ; (2) chaque ligne, safety et adverse citent UNIQUEMENT des claims dont audit vaut confirmed ou corrected — jamais rejected ; (3) "ci" recopie un intervalle/taille d'effet présent DANS le statement d'un claim cité — jamais depuis ta mémoire ; (4) sans donnée exploitable : efficacy "indeterminee", pas d'invention ; (5) "anchor" = l'id exact de la section du manifeste qui détaille la ligne ; (6) une monographie multi-substances → une entrée "substances" par substance traitée.`,
  `PUIS insère {"type":"verdicts"} dans ${themeDir}/manifest.json en position 1 de "elements" (juste après {"type":"abstract"}) : Read du fichier, puis Edit/Write en préservant le formatage (indent 2).`,
  `build.py validera derrière toi (claims vérifiés, enums, ancres) et échouera bruyamment sur toute entorse : ne compte pas sur lui pour rattraper, rends un fichier déjà conforme.`,
  `Rends : files_written (chemins écrits), n_substances, n_rows.`,
].join('\n');

const buildPrompt = (expectIds) => [
  `Assemble la monographie de façon déterministe puis vérifie l'acceptation et le lint.`,
  `1) Exécute : python3 "${buildScript}" "${themeDir}"${expectIds && expectIds.length ? ` --expect-sections ${expectIds.join(',')}` : ''}`,
  `   build.py échoue bruyamment (référence manquante, type inconnu, balise déséquilibrée, file:/// résiduel, jeton non substitué${expectIds && expectIds.length ? ', section attendue absente du manifeste' : ''}).`,
  `   S'il échoue pour une référence corrigeable (ex. claim id absent, widget ref erroné, clé meta manquante), CORRIGE le manifeste/fichier fautif dans ${themeDir} puis relance — UNE seule tentative de réparation, puis rapporte.`,
  ...(expectIds && expectIds.length ? [
    `   Si l'échec est « sections du manifeste ≠ sections attendues » : réinsère la/les section(s) manquante(s) dans manifest.json à leur place dans l'ordre du plan, en recopiant {"type":"section","id","heading","level":3,"prose","claims"} depuis ${themeDir}/sections_draft.json (écrit par CE run), puis relance. Ne retire JAMAIS le flag --expect-sections pour faire passer le build.`,
  ] : []),
  `2) Exécute : python3 "${lintScript}" "${themeDir}"`,
  `   Traite aussi "low_rank_sources" : le lint y liste les claims RETENUS dont l'appareil de preuve`,
  `   repose sur des sources sans valeur probante (encyclopédie collaborative, marchand, blog, dépôt social,`,
  `   reprise de presse). Pour chaque entrée "blocking": true — un claim CONFIRMÉ sans deux sources de rang`,
  `   réel et sans exception document-source déclarée — CORRIGE l'appareil : trouve deux vraies sources et`,
  `   remplace-les dans knowledge.json, ou invoque l'exception document-source sur le document OFFICIEL en la`,
  `   déclarant dans l'audit_note. Ne déclasse JAMAIS le claim en "corrected" pour faire passer le lint, et`,
  `   ne retire jamais le contrôle. Les entrées "blocking": false sont à LIRE : un claim méthodologique ou`,
  `   un claim d'absence peut légitimement citer ces sources — vérifier que l'énoncé ne REPOSE pas sur elles.`,
  `   (exit 0 = propre, exit 2 = flags à adjuger, jamais bloquant en soi). Pour CHAQUE entrée de "rejected_flags" avec hedged=false : lis le contexte ; si le passage AFFIRME le contenu d'un claim rejeté comme un fait, corrige ${themeDir}/manifest.json (retrait, ou réserve explicite « source unique, non corroborée par une source indépendante ») puis relance build.py ET lint.py (une seule passe de réparation) ; si le passage CRITIQUE/RÉFUTE ce contenu, ou n'est qu'une entrée bibliographique, laisse-le (adjugé OK).`,
  `3) Lis ${themeDir}/knowledge.json et vérifie l'acceptation :`,
  `   - chaque claim "audit":"confirmed" a AU MOINS 2 entrées dans "sources" → all_confirmed_have_2plus_sources ;`,
  `   - et ces entrées VALENT comme preuve : compter le RANG, pas seulement le NOMBRE. Ne comptent PAS`,
  `     une encyclopédie collaborative (Wikipédia, Wiktionary), un site marchand ou de marque, un blog, un`,
  `     dépôt social (ResearchGate, Academia), un forum, une reprise de presse ni un fil de communiqués`,
  `     (PR Newswire, Business Wire) — deux sources de rang nul ne confirment rien, même indépendantes.`,
  `     Un communiqué publié PAR l'autorité qui l'émet (fda.gov, ftc.gov, ANSM, HAS) est en revanche le`,
  `     document officiel, donc recevable. Tout claim confirmé qui n'a pas 2 sources recevables est un`,
  `     DÉFAUT à signaler dans errors[] (avec son id) : le re-sourcer, ou — si l'énoncé décrit le contenu`,
  `     d'un document de référence — invoquer l'exception document-source sur le document OFFICIEL et non`,
  `     sur un miroir de presse, en la DÉCLARANT dans son audit_note. Ne jamais déclasser un claim en`,
  `     "corrected" pour faire passer ce contrôle.`,
  `   - quelles catégories d'audit sont présentes parmi confirmed/corrected/rejected → audit_categories_present ;`,
  `   - confirmed_claims = nombre de claims confirmés.`,
  `Rends : success (build OK et acceptation OK), files (fichiers de dist/), build_output (sortie de build.py), lint_flags (nb de flags non hedgés au 1er lint), lint_fixed (nb corrigés), lint_note (adjudications, 1 ligne), acceptance{…}, errors[] (vide si tout va bien).`,
].join('\n');

const S_STYLE = { type:'object', additionalProperties:false, required:['file','n_changes'],
  properties:{ file:{type:'string'}, n_changes:{type:'integer'}, note:{type:'string'} } };
const stylePassPrompt = (path) => [
  `PASSE DE RELECTURE STYLE sur UN widget : ${path}. Fais Read d'abord, puis applique des éditions CHIRURGICALES (Edit). Le SENS est préservé partout.`,
  `Trois axes : (1) calques / faux-amis ; (2) formulations lourdes ; (3) accents manquants dans le TEXTE VISIBLE (element→élément, modele→modèle, reponse→réponse, methode→méthode…).`,
  STYLE,
  `WIDGET HTML : édite UNIQUEMENT le texte VISIBLE (libellés, légendes, boutons, messages, texte SVG <text>/<tspan> affiché). NE TOUCHE PAS les aria-label/alt (accessibilité), ni les identifiants/variables/commentaires JS, ni les id/classes/sélecteurs. Le <script> doit rester syntaxiquement valide.`,
  `CONTRAINTES DURES : NE modifie JAMAIS un chiffre, une date, un nom propre, une citation, un id arXiv, une URL, un slug/id/ref. ⚠ Homographes : n'accentue « a/à », « ou/où », « des/dès », « la/là » que si le contexte l'impose — le VERBE « a » (avoir) reste « a ». Dans le doute, ne change pas.`,
  `Rends : file="${path}", n_changes (entier), note (résumé court ; "déjà propre" si rien).`,
].join('\n');

// ── Orchestration ────────────────────────────────────────────────────────────

const safeParse = (s, what) => { try { return s ? JSON.parse(s) : null; }
  catch (e) { log(`[resume] ${what} illisible (${e.message}) → ignoré`); return null; } };
// Écriture best-effort d'un artefact de reprise (son échec ne tue jamais le run).
async function ckptWrite(relName, obj, phaseName, labelName) {
  try {
    await A(`Crée le dossier si besoin (mkdir -p ${ckptDir}) puis écris VERBATIM, sans modification, le fichier suivant.\nChemin : ${ckptDir}/${relName}\nContenu :\n${JSON.stringify(obj)}`,
      { schema: S_CKPT, model: M_IO, phase: phaseName, label: labelName });
  } catch (e) { log(`[resume] checkpoint ${relName} non écrit (${e.message}) — unité non reprenable, run continue.`); }
}
const _writeVerbatim = async (path, content, phaseName, label) => {
  try {
    await A(
      `Crée le dossier si besoin (mkdir -p ${themeDir}) puis écris VERBATIM, sans aucune modification, le fichier suivant.\nChemin : ${path}\nContenu :\n${content}`,
      { schema: S_CKPT, model: M_IO, phase: phaseName, label }
    );
  } catch (e) { log(`[io] ${path} non écrit (${e.message}) — run continue.`); }
};

// Chargement des checkpoints (UNIQUEMENT en reprise) — index léger puis UN loader PAR section
// (le loader monolithique dépassait le plafond de sortie 32k sur les gros thèmes → re-Sweep).
let loadedResearch = null, savedSections = {}, loadedWidgets = null, loadedProse = null;
if (RESUME) {
  try {
    const idx = await A([
      `Lis l'état de reprise dans ${ckptDir}/ (ce dossier peut ne pas exister — alors tout est vide).`,
      `- sec_ids : liste (via ls/Bash) les fichiers ${ckptDir}/sec-*.json et rends la partie <id> de chaque nom (sec-<id>.json). Tableau vide si aucun.`,
      `- research : si ${ckptDir}/research.json existe, rends son contenu EXACT (verbatim) ; sinon "".`,
      `- widgets : si ${ckptDir}/widgets.json existe, rends son contenu EXACT ; sinon "".`,
      `- prose : si ${ckptDir}/prose.json existe, rends son contenu EXACT ; sinon "".`,
      `N'écris, ne crée, ne modifie RIEN. Verbatim : ne reformate pas, ne tronque pas.`,
    ].join('\n'), { schema: S_LOAD_INDEX, model: M_IO, phase: 'Sweep', label: 'resume-index' });
    loadedResearch = safeParse(idx.research, 'research.json');
    loadedWidgets = safeParse(idx.widgets, 'widgets.json');
    loadedProse = safeParse(idx.prose, 'prose.json');
    const secIds = idx.sec_ids || [];
    if (secIds.length) {
      // Un checkpoint existe sur le disque mais n'est relisible QUE par un agent (le script n'a
      // aucun accès filesystem). Si sa sortie ne se parse pas, la section repartait en Extract +
      // council SANS RIEN DIRE — et ÉCRASAIT le checkpoint, donc toute ré-adjudication faite à la
      // main. Constaté deux fois au 43e run (une section perdue par reprise, à chaque reprise).
      // Deux garde-fous : on redemande une fois, puis on le DIT bruyamment. Le ré-audit reste le
      // comportement de repli — il produit un résultat valide — mais il n'est plus silencieux.
      const readOne = (id) =>
        A(`Rends le contenu EXACT (verbatim, sans reformater ni tronquer) du fichier ${ckptDir}/sec-${id}.json. N'écris rien.`,
          { schema: S_LOAD_ONE, model: M_IO, phase: 'Sweep', label: `resume-sec:${id}` });
      const contents = await parallel(secIds.map(id => () => readOne(id)));
      const perdues = [];
      for (let i = 0; i < secIds.length; i++) {
        const id = secIds[i];
        let o = contents[i] && safeParse(contents[i].content, `sec-${id}.json`);
        if (!o) {
          log(`[resume] sec-${id}.json illisible au 1er essai → nouvelle tentative.`);
          const retry = await readOne(id);
          o = retry && safeParse(retry.content, `sec-${id}.json (retry)`);
        }
        if (o) savedSections[id] = o; else perdues.push(id);
      }
      if (perdues.length)
        log(`⚠️ [resume] ${perdues.length} checkpoint(s) NON rechargé(s) après retry : ${perdues.join(', ')}. ` +
            `Ces sections vont être RÉ-AUDITÉES et leur checkpoint RÉÉCRIT : toute correction manuelle ` +
            `qu'elles portaient sera perdue. Sauvegarde : ${ckptDir} avant toute nouvelle reprise.`);
    }
    log(`[resume] chargé : research=${loadedResearch ? 'oui' : 'non'}, sections=${Object.keys(savedSections).length}, prose=${loadedProse ? 'oui' : 'non'}, widgets=${loadedWidgets ? 'oui' : 'non'}`);
  } catch (e) { log(`[resume] chargement échoué (${e.message}) → run frais`); }
}

// ── Sweep + Plan ─────────────────────────────────────────────────────────────
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
  const sweepsByAngle = ANGLES.map((a, i) => ({ key: a.key, sweep: sweepResults[i] })).filter(({sweep}) => sweep);
  allFindings = sweepsByAngle.flatMap(({key, sweep}) => (sweep.findings || []).map(f => ({ ...f, _angle: key })));
  allSources = dedupSources(sweepsByAngle.flatMap(({sweep}) => sweep.sources || []));
  log(`Sweep : ${allFindings.length} findings, ${allSources.length} sources uniques`);

  phase('Plan');
  arch = await A(archPrompt(allFindings, allSources), { schema: S_ARCH, phase: 'Plan', label: 'plan' });
  log(`Plan : « ${arch.title} » — ${arch.outline.length} sections. Fil rouge : ${arch.fil_rouge}`);
  await ckptWrite('research.json', { allFindings, allSources, arch }, 'Plan', 'ckpt:research');
}
if (arch.outline.length > MAX_SECTIONS) {
  // La section « écosystème » est TOUJOURS placée en dernier par l'architecte (son prompt le lui
  // demande), donc un slice des N premières la décapite systématiquement : sur les 17 thèmes
  // réellement tronqués du corpus au 2026-08-10, 15 avaient perdu exactement cette section.
  // On la met de côté avant la coupe et on la réattache après — le plafond reste tenu.
  const eco = arch.outline.filter(o => o.kind === 'ecosystem');
  const rest = arch.outline.filter(o => o.kind !== 'ecosystem');
  const keep = rest.slice(0, Math.max(0, MAX_SECTIONS - eco.length));
  const dropped = rest.slice(keep.length).map(o => o.heading);
  log(`[lean] plan à ${arch.outline.length} sections → ${keep.length + eco.length} retenues ` +
      `(plafond ${MAX_SECTIONS}${eco.length ? `, dont la section écosystème préservée` : ''}). ` +
      `Écartées : ${dropped.join(' · ') || 'aucune'}`);
  arch.outline = [...keep, ...eco];
}

// ── Extract (notes) → Verify (council par section) en pipeline ───────────────
const LENS_NAMES = [...BATCH_LENS_NAMES, 'source-primaire'];
const sectionResults = await pipeline(
  arch.outline,
  (sec) => {
    if (savedSections[sec.id]) return { __saved: savedSections[sec.id] };
    const secFindings = sec.angle_key
      ? allFindings.filter(f => f._angle === sec.angle_key)
      : allFindings;
    return A(extractPrompt(sec, secFindings), { schema: S_NOTES, model: M_RESEARCH, phase: 'Extract', label: `extract:${sec.id}` });
  },
  async (ext, sec) => {
    if (ext && ext.__saved) { log(`[resume] section « ${sec.heading} » reprise du disque (audit conservé).`); return ext.__saved; }
    let claims = ext.claims || [];
    if (claims.length > MAX_CLAIMS_PER_SECTION) {
      log(`[lean] section « ${sec.heading} » : ${claims.length} claims → ${MAX_CLAIMS_PER_SECTION} soumis au council.`);
      claims = claims.slice(0, MAX_CLAIMS_PER_SECTION);
    }
    if (!claims.length) {
      const empty = { section: { id: sec.id, heading: sec.heading, kind: sec.kind || 'normal' },
                      notes: ext.notes || [], claims: [], pointers: ext.pointers || [] };
      await ckptWrite(`sec-${sec.id}.json`, empty, 'Verify', `ckpt:sec:${sec.id}`);
      return empty;
    }
    // Council par SECTION : 2 jurés batch (soutien / réfutation) sur TOUS les claims,
    // + 1 juré dédié (source primaire) par claim `contestable` — tous en parallèle.
    const contestableIdx = claims.map((_, i) => i).filter(i => claims[i].kind !== 'established');
    const tasks = [
      () => A(batchVerifyPrompt(sec, claims, 0), { schema: S_BATCH, model: M_RESEARCH, phase: 'Verify', label: `verify:${sec.id}/soutien` }),
      () => A(batchVerifyPrompt(sec, claims, 1), { schema: S_BATCH, model: M_RESEARCH, phase: 'Verify', label: `verify:${sec.id}/refutation` }),
      ...contestableIdx.map(i => () =>
        A(extraJurorPrompt(claims[i]), { schema: S_VERDICT, model: M_RESEARCH, phase: 'Verify', label: `verify:${sec.id}#${i}/primaire` })
          .then(v => v && { claim_index: i, ...v })),
    ];
    const results = await parallel(tasks);
    const batchA = results[0], batchB = results[1];
    const extras = results.slice(2).filter(Boolean);
    const byClaim = claims.map((_, i) => {
      const vs = [];
      const a = batchA && (batchA.verdicts || []).find(v => v.claim_index === i);
      const b = batchB && (batchB.verdicts || []).find(v => v.claim_index === i);
      if (a) vs.push({ lens: 0, v: a });
      if (b) vs.push({ lens: 1, v: b });
      const x = extras.find(v => v.claim_index === i);
      if (x) vs.push({ lens: 2, v: x });
      return vs;
    });
    const auditedClaims = claims.map((c, ci) => {
      const lensVerdicts = byClaim[ci];
      if (!lensVerdicts.length) { log(`[verify] ${sec.id}#${ci} : aucun verdict — claim abandonné.`); return null; }
      const verdicts = lensVerdicts.map(x => x.v);
      const d = decideAudit(c, verdicts);
      const tally = { kind: c.kind || 'unspecified',
        corroborated: verdicts.filter(v => v.holds).length,
        refuted: verdicts.filter(v => !v.holds).length,
        corrected: verdicts.filter(v => !v.holds && v.corrected_statement && v.corrected_statement.trim()).length,
        jurors: lensVerdicts.map(({ lens, v }) => ({ lens: LENS_NAMES[lens] || String(lens),
          holds: !!v.holds, corrected: !!(v.corrected_statement && v.corrected_statement.trim()),
          // Le TEXTE, pas seulement le booléen : sur un claim rejeté au seuil de sources, la
          // correction du juré était jusqu'ici perdue ici même (classe d'échec du 37e run).
          corrected_statement: (v.corrected_statement || '').trim(),
          search_exhausted: !!v.search_exhausted,
          n_sources: (v.independent_sources || []).length, note: v.note || '' })) };
      // Sur un claim REJETÉ, la correction proposée par un juré était jusqu'ici jetée avec le
      // claim : l'auteur, qui ne voit pas les rejets, réécrivait ensuite le fait depuis les NOTES
      // — dans sa version fautive (classe d'échec du 37e run, cf. cafeine-ergogene). On la garde
      // pour la lui transmettre comme garde-fou, sans jamais en refaire un fait porteur.
      const rejectedFix = verdicts.map(v => (v.corrected_statement || '').trim()).find(Boolean) || '';
      return { sectionId: sec.id, statement: d.statement, original_statement: c.statement,
               audit: d.audit, note: d.note, examples: c.examples || [], sources: d.sources, tally,
               ...(d.audit === 'rejected' && rejectedFix ? { rejected_correction: rejectedFix } : {}) };
    }).filter(Boolean);
    const result = { section: { id: sec.id, heading: sec.heading, kind: sec.kind || 'normal' },
                     notes: ext.notes || [], claims: auditedClaims, pointers: ext.pointers || [] };
    await ckptWrite(`sec-${sec.id}.json`, result, 'Verify', `ckpt:sec:${sec.id}`);
    return result;
  }
);
const sectionData = sectionResults.filter(Boolean);
const audited = sectionData.flatMap(r => r.claims);
log(`Verify : ${audited.length} claims audités (${audited.filter(c=>c.audit==='confirmed').length} confirmés, ${audited.filter(c=>c.audit==='corrected').length} corrigés, ${audited.filter(c=>c.audit==='rejected').length} rejetés)`);

// ── Élagage déterministe ─────────────────────────────────────────────────────
const enriched = sectionData.map(r => ({
  ...r, kept: r.claims.filter(c => c.audit !== 'rejected'),
}));
const liveSet = new Set(enriched.filter(s =>
  (s.section.kind === 'ecosystem')
    ? ((s.pointers && s.pointers.length > 0) || s.kept.length > 0)
    : (s.kept.length >= SECTION_CLAIM_QUOTA)
));
const liveSections = enriched.filter(s => liveSet.has(s));
// Garde « faux rejet probable » (39e run) : un claim rejeté au SEUL seuil de sources alors que
// TOUS les jurés le tiennent ne doit jamais coûter une section en silence — quand il est
// DÉCISIF (la section survivrait en le gardant), on s'arrête ICI, avant de payer la prose.
const suspectLosses = enriched.filter(s => !liveSet.has(s)).map(s => {
  const susp = s.claims.filter(c => c.audit === 'rejected' && c.tally
    && c.tally.refuted === 0 && c.tally.corroborated >= 2);
  if (!susp.length) return null;
  const keptWith = s.kept.length + susp.length;
  const wouldLive = (s.section.kind === 'ecosystem')
    ? ((s.pointers && s.pointers.length > 0) || keptWith > 0)
    : (keptWith >= SECTION_CLAIM_QUOTA);
  return wouldLive ? { s, susp } : null;
}).filter(Boolean);
if (suspectLosses.length) throw new Error(
  `[élagage] ARRÊT — faux rejet probable décisif : ` +
  suspectLosses.map(({ s, susp }) =>
    `la section « ${s.section.heading} » (${s.section.id}) tomberait à cause de ${susp.map(c => `« ${c.original_statement || c.statement} »`).join(' ; ')}`).join(' | ') +
  `. Chaque énoncé listé est tenu par TOUS ses jurés (rejet au seul seuil de sources). ` +
  `Réparation : ré-audit ciblé (1 agent) pour chercher la 2e source indépendante — souvent le texte intégral d'une étude primaire citée par la revue — ` +
  `puis corriger le checkpoint sec-<id>.json et relancer avec args.resume=true.`);
enriched.filter(s => !liveSet.has(s)).forEach(s =>
  log(`[élagage] section « ${s.section.heading} » coupée : ${s.kept.length} claim(s) survivant(s) < ${SECTION_CLAIM_QUOTA}`));
log(`[élagage] ${liveSections.length}/${enriched.length} sections retenues.`);

// Vérification légère des pointeurs (sur sections vivantes)
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
const liveClaims = liveSections.flatMap(r => r.claims);

// ── Assemblage déterministe de knowledge.json ────────────────────────────────
const srcId = new Map();
const sources = [];
function ensureSrc(s) {
  const k = normUrl(s.url);
  if (!k) return null;
  // Identité de DOCUMENT, pas d'URL. `collectSources` tranche déjà le seuil ≥2 par `docKeys` ;
  // ici, indexer par la seule URL faisait entrer le MÊME travail deux fois dans la liste des
  // sources, donc deux fois en bibliographie — Jędrejko et al. 2023 sous `doi.org/…` et sous
  // `…wiley.com/doi/abs/…` au 46e run. Le seuil n'était pas en danger, mais le lecteur qui
  // compte les sources d'un document de référence en lisait deux là où il n'y en a qu'une.
  // Fusion volontairement ÉTROITE — identifiant fort (doi:, arxiv:) UNIQUEMENT, jamais le
  // titre : à cet endroit, sur-fusionner ne ferait pas rejeter un claim, cela ferait
  // DISPARAÎTRE une source réelle de la bibliographie, en silence.
  const strong = docKeys(s).filter(x => x.startsWith('doi:') || x.startsWith('arxiv:'));
  for (const x of strong) if (srcId.has(x)) { const id = srcId.get(x); srcId.set(k, id); return id; }
  if (!srcId.has(k)) {
    const id = 'src:' + (sources.length + 1);
    srcId.set(k, id);
    strong.forEach(x => srcId.set(x, id));
    sources.push({ id, title: s.title || s.url, url: s.url, kind: s.kind || 'reference' });
  }
  return srcId.get(k);
}
const claims = liveClaims.map((ac, i) => ({
  id: 'claim:' + (i + 1),
  statement: ac.statement,
  sources: [...new Set((ac.sources || []).map(ensureSrc).filter(Boolean))],  // défense en profondeur : jamais deux fois le même id
  audit: ac.audit,
  audit_note: ac.note,
  examples: ac.examples || [],
  _section: ac.sectionId,
}));
const sectionClaims = {};
for (const c of claims) {
  if (c.audit === 'rejected') continue;
  (sectionClaims[c._section] || (sectionClaims[c._section] = [])).push(c.id);
}
const knowledge = {
  theme: { slug, title: arch.title },
  sources,
  claims: claims.map(({ _section, ...c }) => c),
};
const knowledgeJson = JSON.stringify(knowledge, null, 2);

// ── Rapport d'audit (vue de diagnostic dérivée) ──────────────────────────────
const retainedSectionIds = new Set(liveSections.map(s => s.section.id));
const idByClaimObj = new Map();
liveClaims.forEach((ac, i) => idByClaimObj.set(ac, 'claim:' + (i + 1)));
const reportClaims = sectionData.flatMap(s => (s.claims || []).map(ac => {
  const sectionRetained = retainedSectionIds.has(ac.sectionId);
  const t = ac.tally || null;
  return { id: idByClaimObj.get(ac) || null, section: ac.sectionId, section_retained: sectionRetained,
    retained: sectionRetained && ac.audit !== 'rejected', audit: ac.audit, kind: t ? t.kind : 'unknown',
    statement: ac.statement, original_statement: ac.original_statement || ac.statement,
    corroborated: t ? t.corroborated : null, refuted: t ? t.refuted : null, corrected: t ? t.corrected : null,
    n_sources: (ac.sources || []).length, jurors: t ? t.jurors : [], audit_note: ac.note || '' };
}));
const auditReport = {
  generator: 'leanmonograph', theme: { slug, title: arch.title },
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

// ── Author : knowledge + (tldr/glossaire ∥ prose séquentielle) ───────────────
phase('Author');
// knowledge.json = source de vérité : son écriture échoue BRUYAMMENT (pas de best-effort),
// contrairement aux rapports annexes ci-dessous.
await A(
  `Crée le dossier si besoin (mkdir -p ${themeDir}) puis écris VERBATIM, sans aucune modification, le fichier suivant.\nChemin : ${themeDir}/knowledge.json\nContenu :\n${knowledgeJson}`,
  { schema: S_CKPT, model: M_IO, phase: 'Author', label: 'write:knowledge' }
);
await _writeVerbatim(`${themeDir}/audit-report.json`, JSON.stringify(auditReport, null, 2), 'Author', 'write:audit-report.json');
await _writeVerbatim(`${themeDir}/audit-report.md`, auditReportMd, 'Author', 'write:audit-report.md');

const liveOutline = arch.outline.filter(o => liveOutlineIds.has(o.id));
const sectionsBrief = liveOutline.map(o => `- ${o.id} : ${o.heading}`).join('\n');

// La prose n'est fournie à l'auteur QUE depuis les claims RETENUS (les rejetés n'existent
// pas pour lui — ils ne peuvent donc pas être affirmés) + les notes sourcées.
const bySecId = new Map(liveSections.map(s => [s.section.id, s]));
// tldr/glossaire : TOUJOURS (ré)écrits — knowledge.json est recalculé à chaque run, un
// tldr/glossaire d'un run antérieur peut décrire des claims disparus (désalignement silencieux).
const tldrThunk = () => A(authorTldrGlossPrompt(sectionsBrief), { schema: S_AUTHOR, phase: 'Author', label: 'tldr-glossaire' });
const guardTldr = (r) => {
  const fw = (r && r.files_written) || [];
  if (!fw.some(p => /tldr\.json$/.test(p)) || !fw.some(p => /glossary\.json$/.test(p)))
    throw new Error(`Author : tldr.json/glossary.json non écrits (files_written=${JSON.stringify(fw)}) — abandon avant assemblage (l'abstract et le glossaire en dépendent).`);
};
let proseById = {};
if (loadedProse && loadedProse.proseById) {
  proseById = loadedProse.proseById;
  log(`[resume] prose reprise du disque (${Object.keys(proseById).length} sections) — Author/Relecture sautés, tldr/glossaire rejoués sur le knowledge courant.`);
  guardTldr(await tldrThunk());
} else {
  const chunks = [];
  for (let i = 0; i < liveOutline.length; i += PROSE_CHUNK) chunks.push(liveOutline.slice(i, i + PROSE_CHUNK));
  const proseChain = async () => {
    const summaries = [];
    for (let ci = 0; ci < chunks.length; ci++) {
      const chunkSecs = chunks[ci].map(o => {
        const s = bySecId.get(o.id);
        return { id: o.id, heading: o.heading, angle: o.angle,
          claims: (s.kept || []).map(c => ({ statement: c.statement, examples: c.examples || [] })),
          notes: s.notes || [],
          garde_fous: (s.claims || [])
            .filter(c => c.audit === 'rejected' && c.rejected_correction)
            .map(c => ({ version_fautive: c.original_statement, version_exacte: c.rejected_correction })) };
      });
      const askTranche = (again) => A(prosePrompt(arch.title, arch.fil_rouge, liveOutline, summaries, chunkSecs),
        { schema: S_PROSE, phase: 'Author', label: `prose:${ci + 1}/${chunks.length}${again ? ':retry' : ''}` });
      const harvest = (r) => { if (r && Array.isArray(r.sections))
        for (const s of r.sections) if (s.id && s.prose) proseById[s.id] = s.prose; };
      let r = await askTranche(false);
      harvest(r);
      let missingIds = chunks[ci].filter(o => !proseById[o.id]);
      if (missingIds.length) {
        log(`[author] tranche ${ci + 1} incomplète (${missingIds.map(o => o.id).join(', ')}) — un nouvel essai.`);
        r = await askTranche(true);
        harvest(r);
        missingIds = chunks[ci].filter(o => !proseById[o.id]);
      }
      if (missingIds.length) {
        log(`[author] tranche ${ci + 1} encore incomplète après retry (${missingIds.map(o => o.id).join(', ')}) — chaîne de prose arrêtée ; réparation : relancer avec args.resume=true.`);
        break;
      }
      summaries.push((r && r.summary) || '');
    }
  };
  // tldr/glossaire (lit knowledge.json, indépendant de la prose) en PARALLÈLE de la chaîne de prose.
  const [, tldrRes] = await parallel([proseChain, tldrThunk]);
  guardTldr(tldrRes);
  const missing = liveOutline.filter(o => !proseById[o.id]);
  if (missing.length) throw new Error(`Author : prose manquante pour ${missing.map(o => o.id).join(', ')} — abandon avant assemblage.`);

  // Relecture de continuité : éditions ponctuelles, appliquées en JS (diff minimal garanti).
  phase('Relecture');
  const sectionsAll = liveOutline.map(o => ({ id: o.id, heading: o.heading, prose: proseById[o.id] }));
  const ed = await A(editorPrompt(arch.title, arch.fil_rouge, sectionsAll), { schema: S_EDITS, phase: 'Relecture', label: 'continuite' });
  let applied = 0, skipped = 0;
  for (const e of (ed && ed.edits || []).slice(0, MAX_EDITS)) {
    const p = proseById[e.section_id];
    if (p && e.find && p.split(e.find).length === 2) { proseById[e.section_id] = p.replace(e.find, () => e.replace); applied++; }
    else { skipped++; }
  }
  log(`[relecture] ${applied} édition(s) appliquée(s)${skipped ? `, ${skipped} ignorée(s) (extrait introuvable/ambigu)` : ''}.`);
  await ckptWrite('prose.json', { proseById }, 'Relecture', 'ckpt:prose');
}

// sections_draft.json — écrit AVANT la phase visuelle (les codeurs de figure l'éditent en ligne).
// Garde resume : si la phase visuelle est reprise, le fichier porte déjà les figures → ne pas écraser.
if (!Array.isArray(loadedWidgets)) {
  // Invariant commun frais/reprise : CHAQUE section vivante a une prose. Une reprise divergente
  // (sec-*.json corrompu → ré-audit → pruning différent ; research.json perdu → nouveaux ids)
  // laisserait sinon des sections à prose VIDE, silencieusement (build.py ne les voit pas).
  const noProse = liveOutline.filter(o => !proseById[o.id]);
  if (noProse.length) throw new Error(
    `Prose manquante pour ${noProse.map(o => o.id).join(', ')} (reprise divergente ?). ` +
    `Relancer SANS resume, ou effacer ${ckptDir}/prose.json pour ré-écrire la prose sur l'audit courant.`);
  const sectionsForCompose = liveOutline.map(o => ({
    id: o.id, heading: o.heading, prose: proseById[o.id], claims: sectionClaims[o.id] || [],
  }));
  await _writeVerbatim(`${themeDir}/sections_draft.json`, JSON.stringify(sectionsForCompose, null, 2), 'Relecture', 'write:sections');

  // ── Audit-prose : lint --pre + vérification des chiffres prose-only à la source ──
  phase('Audit-prose');
  const notesBySection = liveSections.map(s => ({ id: s.section.id, notes: s.notes || [] }));
  const pa = await A(proseAuditPrompt(notesBySection), { schema: S_PROSEAUDIT, model: M_RESEARCH, phase: 'Audit-prose', label: 'audit-prose' });
  // Passe QUALITÉ best-effort : son échec (rate-limit web) ne doit pas avorter un run abouti —
  // le lint post-build du Build reste le filet.
  if (pa) log(`[audit-prose] ${pa.checked} chiffre(s) vérifié(s), ${pa.fixed} corrigé(s), ${pa.hedged} retiré(s)/réservé(s). ${pa.note || ''}`);
  else log('[audit-prose] agent sans sortie — passe sautée (le lint post-build reste le filet).');
}

// ── Widgets / figures ────────────────────────────────────────────────────────
phase('Widgets');
let visual = [];
if (Array.isArray(loadedWidgets)) {
  visual = loadedWidgets;
  log(`[resume] ${visual.length} élément(s) visuel(s) repris du disque — phase visuelle sautée.`);
} else {
  const liveSectionsBrief = liveOutline.map(o => ({
    id: o.id, heading: o.heading, prose: proseById[o.id] || '',
    claims: (bySecId.get(o.id).kept || []).map(c => c.statement),
  }));
  const wantWidgets = String(A0.widget) !== 'false';
  if (wantWidgets && liveSectionsBrief.length) {
    const plan = await A(widgetPlanPrompt(liveSectionsBrief), { schema: S_WIDGET_PLAN, phase: 'Widgets', label: 'widget-plan' });
    const wanted = (plan.widgets || []).filter(w => liveOutlineIds.has(w.after_section_id));
    const widgetItems = wanted.filter(w => w.kind !== 'figure');
    const figureItems = wanted.filter(w => w.kind === 'figure');
    const codedWidgets = (await pipeline(
      widgetItems,
      (w) => A(widgetCodePrompt(w), { schema: S_WIDGET_CODE, phase: 'Widgets', label: `widget-code:${w.after_section_id}` }),
      async (coded) => {
        if (!coded) return null;
        const verdict = await A(widgetCriticPrompt(coded), { schema: S_WIDGET_CRITIC, phase: 'Widgets', label: `widget-critic:${coded.ref}` });
        if (verdict.ok) return coded;
        log(`[widget] ${coded.ref} recodé : ${(verdict.issues || []).join('; ')}`);
        const fixed = await A(widgetRecodePrompt(coded, verdict.issues || []), { schema: S_WIDGET_CODE, phase: 'Widgets', label: `widget-recode:${coded.ref}` });
        return fixed || coded;
      }
    )).filter(Boolean);
    // Figures : codées EN SÉRIE (elles éditent toutes le même sections_draft.json → pas de course).
    const codedFigures = [];
    for (const f of figureItems) {
      const coded = await A(figureCodePrompt(f), { schema: S_FIGURE_CODE, phase: 'Widgets', label: `figure-code:${f.after_section_id}` });
      if (!coded) continue;
      const verdict = await A(figureCriticPrompt(coded), { schema: S_WIDGET_CRITIC, phase: 'Widgets', label: `figure-critic:${coded.ref}` });
      if (verdict.ok) { codedFigures.push(coded); continue; }
      log(`[figure] ${coded.ref} recodée : ${(verdict.issues || []).join('; ')}`);
      const fixed = await A(figureRecodePrompt(coded, verdict.issues || []), { schema: S_FIGURE_CODE, phase: 'Widgets', label: `figure-recode:${coded.ref}` });
      codedFigures.push(fixed || coded);
    }
    visual = [...codedWidgets, ...codedFigures];
    log(`Visuel : ${codedWidgets.length} widget(s) + ${codedFigures.length} figure(s) retenus.`);
  } else {
    log(wantWidgets ? 'Visuel : aucune section vivante.' : 'Visuel : désactivé (widget=false).');
  }
  await ckptWrite('widgets.json', visual, 'Widgets', 'ckpt:widgets');
}
const widgets = visual.filter(v => v.kind !== 'figure');

// ── Compose ──────────────────────────────────────────────────────────────────
phase('Compose');
const biblioEntries = sources.map(s => ({ label: s.title, href: s.url }));
const composed = await A(
  composePrompt(arch.title, biblioEntries, widgets, verifiedPointers),
  { schema: S_COMPOSE, phase: 'Compose', label: 'compose' }
);
log(`Compose : ${composed.files_written.length} manifeste(s) écrit(s)`);
const _wroteManifest = (composed.files_written || []).some(p => /(^|\/)manifest\.json$/.test(p));
if (!_wroteManifest) throw new Error(
  `Compose n'a pas (ré)écrit ${themeDir}/manifest.json. files_written=${JSON.stringify(composed.files_written)}. ` +
  `Abandon AVANT build pour ne pas assembler un manifeste périmé sur le knowledge.json courant.`);

// ── Verdicts (thème santé : flag explicite args.verdicts) ────────────────────
if (WANT_VERDICTS) {
  phase('Verdicts');
  const v = await A(verdictsPrompt(), { schema: S_VERDICTS, phase: 'Verdicts', label: 'verdicts' });
  if (!(v.files_written || []).some(p => /(^|\/)verdicts\.json$/.test(p)))
    throw new Error(`Verdicts n'a pas écrit ${themeDir}/verdicts.json. files_written=${JSON.stringify(v.files_written)}`);
  log(`Verdicts : ${v.n_substances} substance(s), ${v.n_rows} indication(s).`);
}

// ── Style : widgets uniquement (la prose est née stylée + relue en continuité) ──
if (widgets.length) {
  phase('Style');
  const styleRes = (await parallel(widgets.map(w => () =>
    A(stylePassPrompt(`${themeDir}/widgets/${w.ref}.html`), { schema: S_STYLE, model: M_RESEARCH, phase: 'Style', label: `style:${w.ref}` })
  ))).filter(Boolean);
  log(`Style : ${styleRes.reduce((n, r) => n + (r.n_changes || 0), 0)} correction(s) sur ${styleRes.length} widget(s).`);
}

// ── Build (+ lint post & adjudication) ───────────────────────────────────────
phase('Build');
// Les ids POST-élagage voyagent jusqu'à build.py : le manifeste réellement écrit par Compose
// est comparé au plan vivant (39e run : « 11/11 retenues » annoncé, 10 dans le document).
const built = await A(buildPrompt(liveOutline.map(o => o.id)), { schema: S_BUILD, phase: 'Build', label: 'build' });

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
