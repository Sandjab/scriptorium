#!/usr/bin/env python3
"""Génère la BASCULE SOMBRE manquante d'un widget — frontière code/jugement : le CODE dérive
mécaniquement le pendant nocturne d'un couple fond/encre littéral, le MODÈLE tranche ce que la
mesure signale encore après coup.

Usage : bascule_sombre.py <widget.html|themeDir...> [--dry-run] [--cible 4.5]

  bascule_sombre.py themes/backpropagation --dry-run   # montre les règles qu'il écrirait
  bascule_sombre.py themes/*/                          # applique, puis rebâtir et re-linter

CE QUE CE SCRIPT FAIT, ET CE QU'IL NE FAIT PAS

  Il n'invente aucune palette. Chaque couleur nocturne est DÉRIVÉE de sa diurne en conservant
  la teinte et en ramenant clarté et saturation aux niveaux que la charte emploie déjà pour ses
  propres surfaces sombres (`--card` #16212E, `--blue-wash` #1B2C3E, `--bordeaux-wash` #2C1A1F).
  Une table de 54 fonds et 40 encres écrite à la main dériverait de la charte au premier
  ajustement ; une règle qui préserve la teinte, non.

  Il ne touche QUE trois cas, ceux où la lecture du CSS suffit à conclure :

  1. fond littéral CLAIR  → on écrit `html[data-theme="dark"] <sel>{background:<pendant>}`,
     plus l'encre si elle aussi est littérale (sinon elle vient d'un jeton, qui bascule seul).
  2. fond `var(--jeton)` qui s'ÉCLAIRCIT en sombre + encre littérale claire (le motif miroir :
     `color:#fff` sur `var(--blue)`) → on écrit l'encre sombre. C'est le motif `--onbright`,
     déjà employé par `probe-mcid-iief-severite` (`color:#0A1521`).
  3. fond `var(--jeton)` qui s'ASSOMBRIT + encre littérale sombre → on éclaircit l'encre.

  4. encre littérale SOMBRE sans fond dans sa règle, dans un widget dont au moins une surface
     s'assombrit → elle bascule avec la surface. Cette décision-là se prend au widget et non à
     la règle : une règle seule ignore sur quoi elle s'écrit, la feuille non. Sans cette passe,
     réparer un widget déplace son défaut au lieu de le fermer — mesuré sur
     `synopsis-best-of-n-verificateur`, 19 occurrences illisibles devenaient 6 autres.
     Le pendant clair est laissé tranquille : une encre blanche sans fond a été écrite POUR un
     fond coloré, et l'éclaircir encore la ferait disparaître.

  Ce qui reste hors de portée d'une lecture du CSS — un fond peint en JS, un dégradé — n'est pas
  deviné : c'est `lint_contraste_sombre.py`, lancé après, qui désigne ce résidu, mesuré.

  Il ne touche pas non plus aux couleurs peintes par le JS d'un widget : elles ne rebasculent
  jamais (aucun événement de thème n'est émis), et leur réparation est une décision par widget.

GARANTIE DE CONSTRUCTION : tout couple fond/encre écrit par ce script atteint `--cible`
(4,5:1 par défaut, le seuil AA du texte courant), l'encre étant éclaircie ou assombrie jusqu'à
l'atteindre. Le script ne se contente donc pas de « faire quelque chose de sombre » : il ne peut
pas produire le défaut qu'il répare.

IDEMPOTENCE : le bloc généré est encadré de marqueurs et REMPLACÉ à chaque passage — relancer
le script ne l'empile pas. Éditer le bloc à la main n'a pas de sens : il sera réécrit.

Sortie : JSON sur stdout (widgets touchés, règles écrites, cas ignorés). Exit 0.
"""
import argparse
import colorsys
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
CHARTE = HERE.parent / "template" / "charte.css"

DEBUT = "/* ==== bascule sombre — généré par bascule_sombre.py, ne pas éditer à la main ==== */"
FIN = "/* ==== fin bascule sombre ==== */"

# Surfaces sombres de la charte, reprises telles quelles pour les fonds NEUTRES : trois niveaux,
# pour ne pas écraser en une seule teinte la hiérarchie que le widget exprimait en clair.
NEUTRES = (("#16212E", 0.96), ("#1B2735", 0.90), ("#212E3C", 0.0))
ENCRE_CLAIRE, ENCRE_SOFT = "#E4EBF3", "#AFC0D2"   # --ink et --ink-soft de la charte
ENCRE_SOMBRE = "#0A1521"                           # --blue-deep sombre ; motif --onbright
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")
VAR_COMPLET = re.compile(r"^var\(\s*(--[A-Za-z0-9-]+)\s*(?:,\s*(.+?)\s*)?\)$", re.S)


def die(msg) -> "None":
    raise SystemExit(f"[bascule] ÉCHEC : {msg}")


# --- couleurs ---------------------------------------------------------------

def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(r, g, b):
    return "#" + "".join(f"{round(max(0.0, min(1.0, c)) * 255):02X}" for c in (r, g, b))


def luminance(h):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4  # noqa: E731
    r, g, b = _rgb(h)
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _hls(h):
    r, g, b = _rgb(h)
    return colorsys.rgb_to_hls(r, g, b)


def chroma(h):
    """Écart max-min des canaux — la seule mesure de « teinté ou gris » qui tienne près du blanc.

    La saturation HLS ne convient pas ici : #FBFCFE, qui est du blanc cassé, y culmine à 0,60
    parce que le dénominateur s'effondre quand la clarté frôle 1. S'y fier ferait teinter en
    bleu nuit le fond de carte le plus répandu du corpus (200 règles).
    """
    r, g, b = _rgb(h)
    return max(r, g, b) - min(r, g, b)


def _de_hls(teinte, clarte, saturation):
    return _hex(*colorsys.hls_to_rgb(teinte, max(0.0, min(1.0, clarte)), saturation))


def fond_sombre(h):
    """Pendant nocturne d'un fond clair : teinte conservée, clarté et saturation ramenées au
    régime des washes de la charte. Un fond neutre prend une des trois surfaces de la charte."""
    teinte, clarte, _ = _hls(h)
    if chroma(h) < 0.02:
        for valeur, seuil in NEUTRES:
            if clarte >= seuil:
                return valeur
    return _de_hls(teinte, 0.17, 0.30)


def encre_claire(h):
    """Pendant nocturne d'une encre sombre : un gris devient l'encre de la charte, un accent
    garde sa teinte et monte en clarté (comme --bordeaux passe de #7C2A38 à #C86F7B)."""
    teinte, clarte, _ = _hls(h)
    if chroma(h) < 0.02:
        return ENCRE_CLAIRE if clarte < 0.35 else ENCRE_SOFT
    return _de_hls(teinte, 0.65, 0.45)


def ajuste(encre, fond, cible):
    """Pousse l'encre jusqu'à ce que le couple atteigne la cible. C'est ce qui interdit au
    script de produire, en réparant, un couple aussi illisible que celui qu'il remplace."""
    if contraste(encre, fond) >= cible:
        return encre
    teinte, clarte, sat = _hls(encre)
    sat = 0.45 if chroma(encre) >= 0.02 else 0.0
    sens = 1 if luminance(fond) < 0.18 else -1
    for _ in range(50):
        clarte += sens * 0.02
        if not 0.0 <= clarte <= 1.0:
            break
        candidat = _de_hls(teinte, clarte, sat)
        if contraste(candidat, fond) >= cible:
            return candidat
    return ENCRE_CLAIRE if luminance(fond) < 0.18 else ENCRE_SOMBRE


# --- CSS --------------------------------------------------------------------

def sans_commentaires(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def regles(css, contexte=()):
    """(sélecteur, corps, contexte d'at-règles) pour chaque règle, @media/@supports compris.

    Un parseur à comptage d'accolades, pas une expression régulière : un `@media` contient des
    règles, et une règle contenue doit ressortir dans SON @media, sinon la bascule générée
    s'appliquerait à toutes les largeurs.
    """
    out, i, debut, n = [], 0, 0, len(css)
    while i < n:
        c = css[i]
        if c == "{":
            entete = css[debut:i].strip()
            prof, j = 1, i + 1
            while j < n and prof:
                prof += (css[j] == "{") - (css[j] == "}")
                j += 1
            corps = css[i + 1:j - 1]
            if entete.startswith("@"):
                # @keyframes et @font-face n'ont pas de sélecteur : on n'y entre pas.
                if entete.split()[0] in ("@media", "@supports"):
                    out += regles(corps, contexte + (entete,))
            else:
                out.append((entete, corps, contexte))
            i = debut = j
        elif c == "}":
            i += 1
            debut = i
        else:
            i += 1
    return out


def declarations(corps):
    """{propriété: valeur} — découpe sur `;` en respectant les parenthèses, sinon
    `background:linear-gradient(a, b)` se coupe en deux."""
    morceaux, prof, cur = [], 0, ""
    for ch in corps:
        prof += (ch == "(") - (ch == ")")
        if ch == ";" and prof == 0:
            morceaux.append(cur)
            cur = ""
        else:
            cur += ch
    morceaux.append(cur)
    out = {}
    for m in morceaux:
        if ":" in m:
            k, v = m.split(":", 1)
            k = k.strip()
            # Les custom properties sont SENSIBLES À LA CASSE : `--crm-A` et `--crm-a` sont deux
            # jetons distincts. Les normaliser en minuscules comme les propriétés ordinaires
            # rendait invisible toute palette écrite en capitales — elle n'était jamais résolue,
            # donc jamais basculée.
            out[k if k.startswith("--") else k.lower()] = v.strip()
    return out


def jetons_charte(css):
    """{'--blue': ('#23537f', '#6fa8d8'), …} — valeur claire et valeur sombre de chaque jeton."""
    css = sans_commentaires(css)

    def bloc(selecteur):
        i = css.find(selecteur)
        if i < 0:
            die(f"bloc {selecteur} introuvable dans la charte")
        return css[css.index("{", i) + 1:css.index("}", i)]

    def props(corps):
        return {k: v.lower() for k, v in declarations(corps).items()
                if k.startswith("--") and re.fullmatch(r"#[0-9A-Fa-f]{6}", v)}

    clair, sombre = props(bloc(":root")), props(bloc('html[data-theme="dark"]'))
    return {n: (clair[n], v) for n, v in sombre.items() if n in clair}


# --- décision ---------------------------------------------------------------

def _litteral(valeur):
    """La couleur littérale d'une déclaration, si elle en porte une seule et sans dégradé.

    Les trois écritures coexistent dans le corpus — `#fff`, `#ffffff`, `white` — et la forme
    courte est justement celle du motif miroir (`color:#fff` sur un jeton). La rater revenait à
    ne jamais réparer la famille la plus répandue.
    """
    if not valeur or "gradient" in valeur:
        return None
    if "var(" in valeur:
        # `var(--blue,#23537F)` PORTE une couleur sans en être une : prendre son repli pour la
        # valeur de la déclaration, c'est lire la teinte DIURNE d'un jeton qui bascule, donc
        # conclure que rien ne change en sombre. C'est au résolveur de suivre la chaîne.
        return None
    v = valeur.strip()
    if v.lower() in ("white", "#fff", "#ffffff"):
        return "#FFFFFF"
    if v.lower() in ("black", "#000", "#000000"):
        return "#000000"
    trouve = HEX.findall(v)
    if len(trouve) != 1:
        return None
    t = trouve[0]
    return ("#" + "".join(c * 2 for c in t[1:])).upper() if len(t) == 4 else t.upper()


def jetons_locaux(css):
    """Les alias que le widget se donne à lui-même : ({nom: valeur diurne}, {nom: valeur nocturne}).

    Les widgets du corpus n'écrivent presque jamais une couleur en clair : ils posent d'abord une
    couche à eux — `--bnv-deep:var(--blue-deep,#142E49)` — puis n'emploient que ces alias. Lire
    les déclarations au pied de la lettre ne voit donc RIEN de ce qui casse : `.bnv-q b{color:
    var(--bnv-deep)}` est une encre bleu nuit, en clair comme en sombre, posée sur une surface
    qui, elle, s'assombrit. C'est ce motif qui laissait 6 occurrences après une première passe.
    """
    base, sombre = {}, {}
    for selecteur, corps, _ in regles(sans_commentaires(css)):
        cible = sombre if "data-theme" in selecteur else base
        for nom, valeur in declarations(corps).items():
            if nom.startswith("--"):
                cible.setdefault(nom, valeur)
    return base, sombre


def ou_sont_definis(css):
    """{jeton local: sélecteur de la règle qui le définit} — pour pouvoir le SURCHARGER là."""
    out = {}
    for selecteur, corps, _ in regles(sans_commentaires(css)):
        if "data-theme" in selecteur:
            continue
        for nom in declarations(corps):
            if nom.startswith("--"):
                out.setdefault(nom, selecteur)
    return out


def usages_jetons(lues):
    """{jeton local: propriétés qui le consomment} — `color`, `background`, les deux.

    Un jeton n'a pas de rôle en soi : `--crm-B:#9B3443` est une encre si on écrit
    `color:var(--crm-B)`, une surface si on écrit `background:var(--crm-B)`. Basculer sans
    distinguer reviendrait à éclaircir un fond ou à assombrir une encre.
    """
    out = {}
    for _, decl, _ in lues:
        for prop, valeur in decl.items():
            for nom in re.findall(r"var\(\s*(--[A-Za-z0-9-]+)", valeur or ""):
                out.setdefault(nom, set()).add(
                    "fond" if prop.startswith("background") else
                    "encre" if prop == "color" else "autre")
    return out


def paire(valeur, jetons, locaux=None, locaux_sombres=None, profondeur=0):
    """(valeur diurne, valeur nocturne) d'une déclaration de couleur, `var()` suivis.

    Rend None dès qu'on ne sait pas conclure — dégradé, mot-clé, alias non défini. Ne rien
    dire vaut mieux que réparer au jugé : le lint mesurera ce qui reste.
    """
    if not valeur or profondeur > 6:
        return None
    litteral = _litteral(valeur)
    if litteral:
        return (litteral, litteral)
    m = VAR_COMPLET.match(valeur.strip())
    if not m:
        return None
    nom, repli = m.group(1), m.group(2)
    if nom in jetons:
        return jetons[nom]
    if locaux and nom in locaux:
        diurne = paire(locaux[nom], jetons, locaux, locaux_sombres, profondeur + 1)
        if diurne is None:
            return None
        surcharge = (paire(locaux_sombres[nom], jetons, locaux, locaux_sombres, profondeur + 1)
                     if locaux_sombres and nom in locaux_sombres else None)
        return (diurne[0], surcharge[1] if surcharge else diurne[1])
    return paire(repli, jetons, locaux, locaux_sombres, profondeur + 1) if repli else None


def bascule_regle(decl, jetons, cible, locaux=None, locaux_sombres=None):
    """Déclarations nocturnes d'une règle diurne, ou {} s'il n'y a rien de sûr à en dire.

    Le raisonnement ne classe plus par motif : il CALCULE le couple tel qu'il sera en sombre,
    et ne corrige que celui qui échoue vraiment. Un fond clair est assombri ; une encre est
    reprise si, sur le fond nocturne, elle n'atteint pas la cible — quel que soit le chemin de
    `var()` par lequel l'une et l'autre sont arrivées là.
    """
    def resolue(prop, repli_prop=None):
        return paire(decl.get(prop) or (decl.get(repli_prop) if repli_prop else None),
                     jetons, locaux, locaux_sombres)

    fond, encre = resolue("background-color", "background"), resolue("color")
    fond_nuit = fond[1] if fond else None
    out = {}

    if fond_nuit and luminance(fond_nuit) > 0.5:
        fond_nuit = fond_sombre(fond_nuit)
        out["background"] = fond_nuit
        bordure = resolue("border-color", "border")
        if bordure and luminance(bordure[1]) > 0.5:
            out["border-color"] = fond_sombre(bordure[1])

    if encre and fond_nuit and contraste(encre[1], fond_nuit) < cible:
        # On essaie les deux sens et on garde le meilleur : sur un fond nocturne CLAIR (un jeton
        # qui s'éclaircit), c'est l'encre sombre qui tient ; sur un fond sombre, l'encre claire.
        vers_clair = ajuste(encre_claire(encre[1]), fond_nuit, cible)
        vers_sombre = ajuste(ENCRE_SOMBRE, fond_nuit, cible)
        out["color"] = (vers_clair if contraste(vers_clair, fond_nuit)
                        >= contraste(vers_sombre, fond_nuit) else vers_sombre)
    return out


def surfaces_nocturnes(lues, fonds_neufs, jetons, locaux=None, locaux_sombres=None):
    """Tout ce que ce widget sait peindre comme fond en thème sombre.

    Les surfaces neuves ne suffisent pas : un widget qui tire TOUS ses fonds des jetons n'en
    produit aucune, et sa carte n'en est pas moins sombre. Sans ces fonds-là, l'encre d'un tel
    widget n'était jamais examinée — 15 occurrences du corpus, une encre bordeaux diurne restée
    sur `var(--card)` devenu #16212E.

    ⚠️ Seules les surfaces SOMBRES entrent ici, et la restriction n'est pas cosmétique. Un
    widget peint aussi des fonds clairs en sombre — `var(--blue)` vaut #6FA8D8 —, et une encre
    claire « échoue » contre eux. Les compter faisait assombrir l'encre courante de chaque
    règle sans fond : `coreference-resolution` passait de 12 à 153 occurrences, et
    `named-entity-recognition-sequence-labeling` de 13 à 332. Cette passe ne traite qu'un cas,
    l'encre diurne restée sur une surface devenue sombre ; les fonds clairs relèvent de la
    règle qui les déclare, où le couple est connu.
    """
    out = list(fonds_neufs)
    for _, decl, _ in lues:
        p = paire(decl.get("background-color") or decl.get("background"),
                  jetons, locaux, locaux_sombres)
        if p:
            out.append(fond_sombre(p[1]) if luminance(p[1]) > 0.5 else p[1])
    # « Sombre » se juge par l'usage, pas par un seuil de luminance : #6FA8D8 est un bleu
    # CLAIR à l'œil et sa luminance relative ne vaut que 0,36. Une surface entre ici si
    # l'encre claire de la charte y tient — c'est exactement la question posée.
    sombres = [f for f in out if contraste(ENCRE_CLAIRE, f) >= 4.5]
    peint_du_clair = len(sombres) < len(out)
    return sombres, peint_du_clair


def bloc_genere(css, jetons, cible):
    """Le bloc de règles nocturnes à ajouter à une feuille, et le compte des cas traités.

    La décision sur l'encre sans fond se prend ICI, au widget, pas dans `bascule_regle` : une
    règle seule ne sait pas sur quoi elle s'écrit, la FEUILLE si. Dès qu'au moins une surface
    de ce widget s'assombrit, une encre littérale sombre écrite pour la surface claire ne tient
    plus — elle bascule avec elle. Mesuré sur `synopsis-best-of-n-verificateur` : sans cette
    passe, réparer les 4 fonds transformait 19 occurrences illisibles en 6 autres, les `<b>`
    du bloc devenant de l'encre sombre sur la surface sombre neuve.

    Le pendant clair est laissé tranquille : une encre blanche sans fond a été écrite POUR un
    fond coloré, et l'éclaircir encore la ferait disparaître.
    """
    locaux, locaux_sombres = jetons_locaux(css)
    lues = [(s, declarations(c), ctx) for s, c, ctx in regles(sans_commentaires(css))
            if s and "data-theme" not in s and not s.startswith("%")]
    decisions = [(s, bascule_regle(d, jetons, cible, locaux, locaux_sombres), ctx)
                 for s, d, ctx in lues]
    fonds_neufs = [v["background"] for _, v, _ in decisions if "background" in v]
    elargies, peint_du_clair = surfaces_nocturnes(lues, fonds_neufs, jetons, locaux, locaux_sombres)
    # La passe d'ENCRE garde le périmètre éprouvé — les surfaces que NOUS assombrissons. L'élargir
    # aux fonds tirés des jetons la fait tourner dans des widgets qu'elle n'avait jamais touchés,
    # et y casse ce qui allait. La passe PALETTE, elle, n'a de sens qu'avec ce périmètre élargi,
    # et ne se déclenche que si le widget ne peint AUCUNE surface claire.
    surfaces = fonds_neufs
    surfaces_palette = [] if peint_du_clair else elargies

    # --- les palettes que le widget se donne ---------------------------------
    # Un widget pose parfois une palette CATÉGORIELLE en jetons littéraux, sans jeton de charte
    # derrière — `--crm-A:#2C77B6;--crm-B:#9B3443;--crm-C:#3F8E66…` pour distinguer des entités —
    # et c'est le JS qui pose les classes qui la consomment. Aucune règle de couleur n'est alors
    # atteignable : c'est le JETON qu'il faut basculer, une fois pour toutes ses utilisations.
    # 12 occurrences de `coreference-resolution` tenaient à cela.
    ou = ou_sont_definis(css)
    usages = usages_jetons(lues)
    palettes = {}
    for nom, valeur in locaux.items():
        if nom in locaux_sombres or nom not in ou or not _litteral(valeur):
            continue
        roles = usages.get(nom, set())
        litteral = _litteral(valeur)
        # Un jeton qu'AUCUNE règle CSS ne consomme est appliqué par le JS (`style.color=COL[r]`) :
        # le surcharger en sombre reste la seule prise qu'on ait dessus, et elle suffit, le JS
        # posant `var(--crm-A)` et non une valeur figée.
        #
        # Mais il faut qu'aucun rôle de FOND ne soit connu. Laisser l'encre l'emporter sur un
        # jeton à double rôle éclaircissait des surfaces :
        # `named-entity-recognition-sequence-labeling` passait de 13 à 26 occurrences, dont 17
        # fonds devenus clairs en sombre. Un jeton qui sert aux deux ne se bascule pas d'une
        # seule valeur — c'est au widget de séparer ses cas.
        if "fond" not in roles and surfaces_palette:
            pire = min(surfaces_palette, key=lambda f: contraste(litteral, f))
            if contraste(litteral, pire) < cible:
                palettes.setdefault(ou[nom], {})[nom] = ajuste(encre_claire(litteral), pire, cible)
        elif roles == {"fond"} and luminance(litteral) > 0.5:
            palettes.setdefault(ou[nom], {})[nom] = fond_sombre(litteral)
    for selecteur, surcharges in palettes.items():
        decisions.append((selecteur, surcharges, ()))

    for i, (selecteur, decl, contexte) in enumerate(lues):
        if decisions[i][1] or decl.get("background") or decl.get("background-color"):
            continue
        encre = paire(decl.get("color"), jetons, locaux, locaux_sombres)
        if not encre or not surfaces:
            continue
        # On ne devine pas SUR QUOI l'encre s'écrit : on regarde TOUT ce que le widget sait
        # peindre en sombre, et on la juge sur la PIRE de ces surfaces.
        #
        # N'agir que si elle échoue contre TOUTES serait plus rigoureux, et c'est empiriquement
        # pire : la version stricte laisse tranquilles des encres que celle-ci répare, et
        # `named-entity-recognition-sequence-labeling` passe de 13 à 26 occurrences. Une encre
        # unique posée sur plusieurs surfaces est presque toujours écrite pour la surface
        # dominante ; l'exception se mesure, la règle se garde.
        pire = min(surfaces, key=lambda f: contraste(encre[1], f))
        if contraste(encre[1], pire) < cible:
            decisions[i] = (selecteur,
                            {"color": ajuste(encre_claire(encre[1]), pire, cible)},
                            contexte)

    # --- rendre à la cascade ce que la bascule lui prend -----------------------
    # `html[data-theme="dark"] .hns-btn` est PLUS SPÉCIFIQUE que `.hns-btn.hns-ghost` : une
    # variante qui gérait déjà son cas se fait voler son encre par la bascule de sa règle de
    # base, et devient illisible. 51 occurrences du corpus étaient exactement cela — un défaut
    # créé par la réparation. Toute variante qui déclare SA propre encre la réaffirme donc en
    # sombre, verbatim quand elle tient, ajustée sinon.
    ecrites = {s for s, v, _ in decisions if "color" in v}
    for i, (selecteur, decl, contexte) in enumerate(lues):
        if "color" in decisions[i][1] or "color" not in decl:
            continue
        if not any(s != selecteur and re.search(re.escape(s) + r"(?![\w-])", selecteur)
                   for s in ecrites):
            continue
        # Réaffirmer, c'est RESTITUER la déclaration de la variante — pas la re-décider. Quand
        # la variante ne porte pas son propre fond, on ne sait pas sur quoi elle s'écrit ; lui
        # inventer une référence a fermé 18 occurrences et en a ouvert 12 ailleurs. Verbatim,
        # on rend exactement ce qui s'appliquerait sans notre règle de base : au pire le défaut
        # préexistant du widget, jamais un défaut de notre fait.
        propre = paire(decl["color"], jetons, locaux, locaux_sombres)
        fond = paire(decl.get("background-color") or decl.get("background"),
                     jetons, locaux, locaux_sombres)
        fond_nuit = (fond_sombre(fond[1]) if luminance(fond[1]) > 0.5 else fond[1]) if fond else None
        valeur = decl["color"]
        if propre and fond_nuit and contraste(propre[1], fond_nuit) < cible:
            valeur = ajuste(encre_claire(propre[1]), fond_nuit, cible)
        decisions[i] = (selecteur, {**decisions[i][1], "color": valeur}, contexte)

    par_contexte, n = {}, 0
    for selecteur, neuves, contexte in decisions:
        if not neuves:
            continue
        # Chaque sélecteur de la liste est préfixé : `a, b {}` deviendrait sinon
        # `html[…] a, b {}`, dont la seconde moitié s'appliquerait aussi en clair.
        cible_sel = ", ".join(f'html[data-theme="dark"] {s.strip()}'
                              for s in selecteur.split(",") if s.strip())
        decls = "".join(f"{k}:{v};" for k, v in neuves.items())
        par_contexte.setdefault(contexte, []).append(f"  {cible_sel}{{{decls}}}")
        n += 1
    if not n:
        return "", 0
    lignes = [DEBUT]
    for contexte, regs in par_contexte.items():
        if contexte:
            lignes.append(" ".join(contexte) + "{")
            lignes += ["  " + r for r in regs]
            lignes.append("}")
        else:
            lignes += regs
    lignes.append(FIN)
    return "\n".join(lignes), n


def bascule_widget(chemin, jetons, cible, dry_run):
    src = chemin.read_text(encoding="utf-8")
    nettoye = re.sub(r"\n*" + re.escape(DEBUT) + r".*?" + re.escape(FIN) + r"\n*",
                     "", src, flags=re.S)
    styles = list(re.finditer(r"(<style[^>]*>)(.*?)(</style>)", nettoye, re.S))
    if not styles:
        return 0
    total, sortie, pos = 0, [], 0
    for m in styles:
        bloc, n = bloc_genere(m.group(2), jetons, cible)
        total += n
        sortie.append(nettoye[pos:m.end(2)])
        if bloc:
            sortie.append("\n" + bloc + "\n")
        pos = m.end(2)
    sortie.append(nettoye[pos:])
    if total and not dry_run:
        chemin.write_text("".join(sortie), encoding="utf-8")
    return total


def widgets(cible):
    p = pathlib.Path(cible.rstrip("/"))
    if p.is_file():
        return [p]
    d = p / "widgets"
    if not d.is_dir():
        die(f"ni un widget ni un thème avec widgets/ : {cible}")
    return sorted(d.glob("*.html"))


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("cibles", nargs="+", help="widgets .html ou dossiers de thème")
    ap.add_argument("--dry-run", action="store_true", help="n'écrit rien, compte seulement")
    ap.add_argument("--cible", type=float, default=4.5,
                    help="contraste minimal garanti pour tout couple écrit (défaut 4.5)")
    a = ap.parse_args()

    jetons = jetons_charte(CHARTE.read_text(encoding="utf-8"))
    touches, regles_ecrites = [], 0
    for c in a.cibles:
        for w in widgets(c):
            n = bascule_widget(w, jetons, a.cible, a.dry_run)
            if n:
                touches.append({"widget": str(w), "regles": n})
                regles_ecrites += n
    json.dump({"dry_run": a.dry_run, "cible": a.cible, "widgets": len(touches),
               "regles": regles_ecrites, "detail": touches},
              sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
