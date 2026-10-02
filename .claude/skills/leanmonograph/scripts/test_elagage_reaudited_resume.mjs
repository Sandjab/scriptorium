// Test de la garde d'élagage en REPRISE, face à un rejet déjà ré-audité à la main.
//
// Lancer :  node .claude/skills/leanmonograph/scripts/test_elagage_reaudited_resume.mjs
//           (exit ≠ 0 si échec)
//
// Ce qu'il protège, et POURQUOI :
//
//   65e run (generalisation-double-descent-grokking, 2026-10-02). La garde « faux rejet
//   probable » arrête le run quand une section tomberait à cause d'un claim tenu par TOUS ses
//   jurés mais rejeté au seul seuil de sources : c'est un rejet qu'on n'a pas encore jugé.
//   Après un ré-audit manuel qui CONFIRME ce rejet (aucune 2e source honnête), la reprise
//   s'arrêtait pourtant au même endroit, en boucle : la garde ne savait pas que le rejet avait
//   été jugé. Le marqueur `reaudited: true`, posé dans sec-<id>.json, le lui dit.
//
//   Les deux sens comptent : (A) sans marqueur, la garde doit TOUJOURS arrêter — sinon le
//   marqueur aurait affaibli le garde-fou du 39e run ; (B) avec marqueur, la section tombe
//   proprement et build.py n'attend plus qu'elle.
//
// Technique : celle de test_elagage_stops_before_prose.mjs (copie du workflow enveloppée en
// module ESM, agents mockés), mais par la branche `args.resume`, où les sections viennent
// des checkpoints relus par les loaders.

import { readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

const here = dirname(fileURLToPath(import.meta.url));
const src = readFileSync(join(here, '..', 'workflow.js'), 'utf8').replace(/^export const meta/m, 'const meta');
const modPath = join(tmpdir(), `lean_reaudited_under_test_${process.pid}.mjs`);
writeFileSync(modPath,
  'export default async function __run(__env) {\n' +
  '  const { agent, parallel, pipeline, phase, log, args, budget } = __env;\n' + src + '\n}\n', 'utf8');
let runWorkflow;
try { ({ default: runWorkflow } = await import(pathToFileURL(modPath).href)); }
finally { try { unlinkSync(modPath); } catch { /* déjà parti */ } }

// ── Fixtures ────────────────────────────────────────────────────────────────
const SRC_A = { title: 'source A', url: 'https://exemple.test/a' };
const SRC_B = { title: 'source B', url: 'https://exemple.test/b' };
const OUTLINE = [
  { id: 's1', heading: 'S1', angle: 'a', kind: 'normal', angle_key: 'foundations' },
  { id: 's2', heading: 'S2', angle: 'a', kind: 'normal', angle_key: 'theory' },
];
const jurors = [{ lens: 'soutien', holds: true }, { lens: 'réfutation', holds: true }];
const confirmed = (sid, s) => ({ sectionId: sid, statement: s, original_statement: s, audit: 'confirmed',
  note: 'Confirmé', examples: [], sources: [SRC_A, SRC_B],
  tally: { kind: 'established', corroborated: 2, refuted: 0, corrected: 0, jurors } });
// Tenu par tous les jurés, rejeté au seul seuil de sources : le profil exact que la garde vise.
const suspect = (reaudited) => ({ sectionId: 's1', statement: 'résultat mono-source', original_statement: 'résultat mono-source',
  audit: 'rejected', note: 'Rejeté', examples: [], sources: [SRC_A],
  tally: { kind: 'established', corroborated: 2, refuted: 0, corrected: 0, jurors },
  ...(reaudited ? { reaudited: true } : {}) });
// s1 : 1 claim retenu + 1 suspect → tombe sous le quota de 2, mais vivrait en gardant le suspect.
const checkpoints = (reaudited) => ({
  s1: { section: { id: 's1', heading: 'S1', kind: 'normal' }, notes: [], pointers: [],
        claims: [confirmed('s1', 'fait retenu de s1'), suspect(reaudited)] },
  s2: { section: { id: 's2', heading: 'S2', kind: 'normal' }, notes: [], pointers: [],
        claims: [confirmed('s2', 'fait A de s2'), confirmed('s2', 'fait B de s2')] },
});

function makeAgent(reaudited, seen) {
  const ck = checkpoints(reaudited);
  return function agent(prompt, opts) {
    const label = (opts && opts.label) || '';
    seen.push({ label, prompt });
    if (/Chemin\s*:/.test(prompt)) return Promise.resolve({ written: true, files_written: ['x'] });
    if (label === 'resume-index') return Promise.resolve({ sec_ids: ['s1', 's2'], widgets: '', prose: '' });
    if (label === 'resume-research:arch') return Promise.resolve({ content: JSON.stringify({ title: 'T', kicker: 'k', fil_rouge: 'f', outline: OUTLINE }) });
    if (label.startsWith('resume-research:')) return Promise.resolve({ content: '[]' });
    if (label.startsWith('resume-sec:')) return Promise.resolve({ content: JSON.stringify(ck[label.slice(11)]) });
    if (label.startsWith('prose:')) return Promise.resolve({
      sections: OUTLINE.map(o => ({ id: o.id, prose: '<p>x</p>' })), summary: 's' });
    if (label === 'compose') return Promise.resolve({ files_written: ['/repo/themes/demo/manifest.json'], element_counts: { document: 6 } });
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

async function run(reaudited) {
  const seen = [];
  let error = null;
  try {
    await runWorkflow({ agent: makeAgent(reaudited, seen), parallel: parallelMock, pipeline: pipelineMock,
      phase: () => {}, log: () => {},
      args: { subject: 'Sujet', slug: 'demo', themeDir: '/repo/themes/demo', resume: true },
      budget: { total: null, spent: () => 0, remaining: () => Infinity } });
  } catch (e) { error = e; }
  return { seen, error };
}

// ── Assertions ──────────────────────────────────────────────────────────────
let failures = 0;
const ok = (cond, label) => { if (!cond) { failures++; console.error(`  ✗ ${label}`); } else console.log(`  ✓ ${label}`); };

// Témoin : la reprise relit bien les checkpoints (sinon les deux cas suivants ne prouvent rien).
const a = await run(false);
ok(a.seen.some(s => s.label === 'resume-sec:s1'), 'la reprise relit le checkpoint de s1');
ok(!a.seen.some(s => s.label.startsWith('extract:') || s.label.startsWith('verify:')), 'aucune section n\'est ré-extraite ni ré-auditée');

// (A) suspect NON ré-audité → la garde arrête toujours, avant toute prose.
ok(!!a.error && /faux rejet/i.test(String(a.error && a.error.message)), 'sans marqueur : la garde arrête (« faux rejet »)');
ok(!a.seen.some(s => s.label.startsWith('prose:')), 'sans marqueur : aucune prose payée');

// (B) suspect marqué `reaudited: true` → la section tombe, le run va au bout sans elle.
const b = await run(true);
ok(!b.error, `avec marqueur : le run va au bout (erreur : ${b.error ? b.error.message : '—'})`);
const build = b.seen.find(s => s.label === 'build');
ok(!!build && build.prompt.includes('--expect-sections s2'), 'avec marqueur : build.py n\'attend que la section survivante s2');
ok(!!build && !build.prompt.includes('s1'), 'avec marqueur : la section coupée s1 n\'est pas attendue');

console.log(failures ? `\n${failures} échec(s)` : '\nTous les tests passent.');
process.exit(failures ? 1 : 0);
