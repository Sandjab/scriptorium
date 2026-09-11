"""Tests du générateur de BASCULE SOMBRE (bascule_sombre.py).

Lancer :  python3 -m pytest .claude/skills/monograph/scripts/test_bascule_sombre.py

CE QUE CES TESTS PROTÈGENT, ET POURQUOI

  Ce script écrit du CSS dans 108 widgets d'un coup. Une erreur de dérivation ne casse pas un
  document, elle en casse soixante — et le lint de contraste ne la verrait pas : un fond bleu
  nuit au lieu d'un gris ardoise contraste parfaitement, il est juste faux. La mesure ne
  protège que la lisibilité ; ces tests protègent la JUSTESSE.

  Trois intentions :

  1. La dérivation respecte ce que la couleur EST. Un blanc cassé reste neutre, un wash vert
     reste vert. C'est `test_le_blanc_casse_ne_devient_pas_bleu` qui tient ce point, et il
     documente le piège qui l'a motivé.
  2. Le CSS généré ne s'applique QU'en sombre. Un sélecteur mal préfixé, une règle sortie de
     son `@media`, et le script casse le thème clair — c'est-à-dire les 96 documents, y compris
     les 12 qui allaient bien.
  3. Le script se tait là où il ne sait pas. Le cas « encre littérale sans fond » est laissé au
     lint : `test_une_encre_sans_fond_est_laissee_au_lint` échouerait si quelqu'un décidait un
     jour de le deviner.
"""
import pytest
import bascule_sombre as B

JETONS = {"--blue": ("#23537f", "#6fa8d8"),    # s'éclaircit en sombre
          "--card": ("#ffffff", "#16212e"),    # s'assombrit
          "--paper": ("#f4f6fa", "#0e1620")}


# --- la dérivation des couleurs --------------------------------------------

def test_le_blanc_casse_ne_devient_pas_bleu():
    """#FBFCFE est le fond de carte le plus répandu du corpus : 200 règles à lui seul.

    Sa saturation HLS vaut 0,60 — un artefact du modèle quand la clarté frôle 1 — alors qu'il
    est visuellement gris. S'y fier teintait 200 fonds en bleu nuit. La neutralité se juge donc
    au CHROMA (écart max-min des canaux), et ce test est la trace de ce piège.
    """
    assert B.fond_sombre("#FBFCFE") == "#16212E"
    assert B.fond_sombre("#FFFFFF") == "#16212E"


def test_un_wash_teinte_garde_sa_teinte():
    """Un fond vert pâle dit quelque chose (« ce bloc est le cas favorable ») : le perdre en
    sombre, c'est perdre l'information, pas seulement la couleur."""
    vert = B.fond_sombre("#EAF4EE")
    r, g, b = (int(vert[i:i + 2], 16) for i in (1, 3, 5))
    assert g > r and g > b, f"{vert} devrait rester verdâtre"
    rose = B.fond_sombre("#FBEDEF")
    r, g, b = (int(rose[i:i + 2], 16) for i in (1, 3, 5))
    assert r > g and r > b, f"{rose} devrait rester rosé"


def test_les_trois_surfaces_neutres_preservent_la_hierarchie():
    """Le widget distinguait une carte d'un liseré gris : les écraser en une seule surface
    sombre aplatirait une hiérarchie que l'auteur avait posée exprès."""
    assert len({B.fond_sombre("#FBFCFE"), B.fond_sombre("#F1F3F6"), B.fond_sombre("#E3E3E3")}) == 3


def test_une_encre_accent_reste_un_accent():
    """Un bordeaux d'encre ne doit pas devenir l'encre grise commune : la charte elle-même
    remonte --bordeaux de #7C2A38 à #C86F7B plutôt que de le neutraliser."""
    clair = B.encre_claire("#7E2734")
    r, g, b = (int(clair[i:i + 2], 16) for i in (1, 3, 5))
    assert r > g and r > b and B.luminance(clair) > B.luminance("#7E2734")


# --- la garantie de contraste ----------------------------------------------

def test_le_couple_ecrit_atteint_toujours_la_cible():
    """La raison d'être de `ajuste` : un script qui répare un défaut de contraste et peut en
    produire un autre ne vaut pas la peine d'être lancé sur 108 fichiers."""
    for encre in ("#11283F", "#8A5E1B", "#666666", "#1F5C3F"):
        for fond in ("#16212E", "#1E3829", "#38301E"):
            ajustee = B.ajuste(B.encre_claire(encre), fond, 4.5)
            assert B.contraste(ajustee, fond) >= 4.5, f"{ajustee} sur {fond}"


# --- ce que le script décide, règle par règle -------------------------------

def test_un_fond_clair_litteral_bascule():
    out = B.bascule_regle({"background": "#FBFCFE"}, JETONS, 4.5)
    assert out == {"background": "#16212E"}


def test_un_fond_deja_sombre_est_laisse_tranquille():
    """Un bandeau déjà sombre en clair fonctionne dans les deux thèmes : le « réparer »
    l'inverserait sans raison."""
    assert B.bascule_regle({"background": "#11283F", "color": "#fff"}, JETONS, 4.5) == {}


def test_le_miroir_recoit_une_encre_sombre():
    """`color:#fff` sur `var(--blue)` : le jeton s'éclaircit en sombre, le blanc lâche. C'est
    l'encre qu'on reprend, jamais le fond — le fond, lui, est correct."""
    out = B.bascule_regle({"background": "var(--blue)", "color": "#fff"}, JETONS, 4.5)
    assert "background" not in out
    assert B.contraste(out["color"], "#6fa8d8") >= 4.5


def test_une_encre_sombre_sur_un_jeton_qui_s_assombrit_est_eclaircie():
    out = B.bascule_regle({"background": "var(--card)", "color": "#11283F"}, JETONS, 4.5)
    assert B.contraste(out["color"], "#16212e") >= 4.5


def test_une_regle_seule_ne_decide_pas_d_une_encre_sans_fond():
    """Une règle ignore sur quoi elle s'écrit : la décision remonte à la feuille (voir
    `test_une_encre_sans_fond_bascule_si_le_widget_s_assombrit`)."""
    assert B.bascule_regle({"color": "#11283F"}, JETONS, 4.5) == {}


def test_une_encre_sans_fond_bascule_si_le_widget_s_assombrit():
    """Le défaut mesuré sur `synopsis-best-of-n-verificateur` : réparer les 4 fonds d'un widget
    sans toucher aux `<b>` qui s'y écrivent transformait 19 occurrences illisibles en 6 autres,
    l'encre sombre se retrouvant sur la surface sombre neuve. Réparer doit FERMER le défaut,
    pas le déplacer."""
    bloc, n = B.bloc_genere(".q{background:#FBFCFE} .q b{color:#0A1521}", JETONS, 4.5)
    assert n == 2
    assert 'html[data-theme="dark"] .q b{color:' in bloc
    encre = bloc.split('html[data-theme="dark"] .q b{color:')[1].split(";")[0]
    assert B.contraste(encre, "#16212E") >= 4.5


def test_une_encre_claire_sans_fond_est_laissee_tranquille():
    """Elle a été écrite POUR un fond coloré (un badge, un bouton) : l'éclaircir encore la
    ferait disparaître sur ce fond-là, qui, lui, n'a pas bougé."""
    bloc, _ = B.bloc_genere(".q{background:#FBFCFE} .q .badge{color:#fff}", JETONS, 4.5)
    assert ".badge" not in bloc


def test_sans_fond_assombri_aucune_encre_ne_bascule():
    """Dans un widget qui tire tout des jetons, les encres littérales sombres sont rares et
    volontaires : rien ne justifie d'y toucher sans preuve."""
    _, n = B.bloc_genere(".q b{color:#0A1521}", JETONS, 4.5)
    assert n == 0


def test_un_degrade_n_est_pas_touche():
    """Un `linear-gradient` porte plusieurs couleurs : en réécrire une seule le défigure."""
    assert B.bascule_regle({"background": "linear-gradient(#FBFCFE,#EAF4EE)"}, JETONS, 4.5) == {}


# --- le CSS produit ---------------------------------------------------------

def test_chaque_selecteur_d_une_liste_est_prefixe():
    """`a, b{}` préfixé une seule fois donnerait `html[…] a, b{}` : la seconde moitié
    s'appliquerait AUSSI en thème clair, et le script casserait ce qu'il vient réparer."""
    bloc, n = B.bloc_genere(".a, .b{background:#FBFCFE}", JETONS, 4.5)
    assert n == 1
    assert 'html[data-theme="dark"] .a, html[data-theme="dark"] .b{' in bloc


def test_une_regle_sous_media_reste_sous_son_media():
    """Sortie de son `@media`, la bascule s'appliquerait à toutes les largeurs."""
    bloc, n = B.bloc_genere("@media (max-width:600px){.a{background:#FBFCFE}}", JETONS, 4.5)
    assert n == 1
    assert "@media (max-width:600px){" in bloc
    assert bloc.index("@media") < bloc.index('html[data-theme="dark"] .a')


def test_une_regle_deja_sombre_n_est_pas_retraitee():
    """Sinon chaque passage empilerait une bascule de la bascule."""
    _, n = B.bloc_genere('html[data-theme="dark"] .a{background:#FBFCFE}', JETONS, 4.5)
    assert n == 0


def test_le_passage_est_idempotent(tmp_path):
    """On relance ce script après chaque retouche d'un widget : deux passages doivent donner
    le même fichier, pas deux blocs empilés."""
    w = tmp_path / "w.html"
    w.write_text('<div class="widget"><style>.a{background:#FBFCFE}</style></div>', encoding="utf-8")
    jetons = B.jetons_charte(B.CHARTE.read_text(encoding="utf-8"))
    assert B.bascule_widget(w, jetons, 4.5, dry_run=False) == 1
    une_fois = w.read_text(encoding="utf-8")
    assert B.bascule_widget(w, jetons, 4.5, dry_run=False) == 1
    assert w.read_text(encoding="utf-8") == une_fois
    assert une_fois.count(B.DEBUT) == 1


def test_le_dry_run_n_ecrit_rien(tmp_path):
    w = tmp_path / "w.html"
    avant = '<div class="widget"><style>.a{background:#FBFCFE}</style></div>'
    w.write_text(avant, encoding="utf-8")
    jetons = B.jetons_charte(B.CHARTE.read_text(encoding="utf-8"))
    assert B.bascule_widget(w, jetons, 4.5, dry_run=True) == 1
    assert w.read_text(encoding="utf-8") == avant


def test_le_bloc_est_ecrit_dans_le_style_pas_apres(tmp_path):
    """Hors du `<style>`, le CSS généré serait du texte affiché dans le document."""
    w = tmp_path / "w.html"
    w.write_text('<div class="widget"><style>.a{background:#FBFCFE}</style><p>texte</p></div>',
                 encoding="utf-8")
    jetons = B.jetons_charte(B.CHARTE.read_text(encoding="utf-8"))
    B.bascule_widget(w, jetons, 4.5, dry_run=False)
    rendu = w.read_text(encoding="utf-8")
    assert rendu.index(B.FIN) < rendu.index("</style>")


def test_les_jetons_viennent_de_la_charte_reelle():
    """Le miroir ne se décide que si l'on sait quels jetons s'éclaircissent vraiment."""
    jetons = B.jetons_charte(B.CHARTE.read_text(encoding="utf-8"))
    assert jetons["--blue"] == ("#23537f", "#6fa8d8")
    assert B.luminance(jetons["--blue"][1]) > B.luminance(jetons["--blue"][0])


@pytest.mark.parametrize("couleur", ["#FBFCFE", "#EAF4EE", "#FBF3E3", "#E7EEF6"])
def test_tout_fond_derive_est_bien_sombre(couleur):
    """La condition minimale : sur un fond dérivé, l'encre de la charte (--ink) doit tenir."""
    assert B.contraste("#E4EBF3", B.fond_sombre(couleur)) >= 4.5


# --- la résolution des alias -----------------------------------------------

def test_un_repli_de_var_n_est_pas_pris_pour_la_couleur():
    """`var(--blue,#23537F)` porte une couleur sans en être une.

    Prendre le repli pour la valeur, c'est lire la teinte DIURNE d'un jeton qui bascule — donc
    conclure que rien ne change en sombre, et ne rien réparer. Le bug a laissé passer tous les
    boutons `color:#fff` du corpus : les widgets n'écrivent presque jamais un jeton sans repli.
    """
    jetons = {"--blue": ("#23537f", "#6fa8d8")}
    assert B._litteral("var(--blue,#23537F)") is None
    assert B.paire("var(--blue,#23537F)", jetons) == ("#23537f", "#6fa8d8")


def test_un_alias_de_widget_est_suivi_jusqu_au_jeton():
    """Les widgets posent une couche à eux — `--bnv-blue:var(--blue,#23537F)` — et n'emploient
    plus que ces alias. Sans suivre la chaîne, on ne voit aucune des couleurs réelles."""
    jetons = {"--blue": ("#23537f", "#6fa8d8")}
    locaux = {"--bnv-blue": "var(--blue,#23537F)"}
    assert B.paire("var(--bnv-blue)", jetons, locaux) == ("#23537f", "#6fa8d8")
    out = B.bascule_regle({"background": "var(--bnv-blue)", "color": "#fff"},
                          jetons, 4.5, locaux, {})
    assert B.contraste(out["color"], "#6fa8d8") >= 4.5


def test_une_surcharge_sombre_deja_posee_est_respectee():
    """Un widget qui a déjà écrit sa bascule pour un alias ne doit pas être contredit."""
    jetons = {"--blue": ("#23537f", "#6fa8d8")}
    assert B.paire("var(--w-x)", jetons, {"--w-x": "#EAF4EE"}, {"--w-x": "#1E3829"}) \
        == ("#EAF4EE", "#1E3829")


def test_un_alias_inconnu_ne_produit_aucune_decision():
    """Ne rien dire vaut mieux que réparer au jugé : le lint mesurera."""
    assert B.paire("var(--inconnu)", {"--blue": ("#23537f", "#6fa8d8")}) is None


def test_la_reference_est_la_pire_surface_pour_l_encre_consideree():
    """Un widget pose plusieurs surfaces neuves ; l'encre doit tenir sur TOUTES.

    Comparer à un extrême fixe sous-déclenche : une encre sombre souffre sur la surface la plus
    sombre, une encre claire sur la plus claire. Choisir « la plus claire » laissait 67
    occurrences après le premier passage corpus.
    """
    css = ".a{background:#FBFCFE} .b{background:#FBF3E3} .c{color:#0A1521}"
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    assert 'html[data-theme="dark"] .c{color:' in bloc
    encre = bloc.split('html[data-theme="dark"] .c{color:')[1].split(";")[0]
    for fond in (B.fond_sombre("#FBFCFE"), B.fond_sombre("#FBF3E3")):
        assert B.contraste(encre, fond) >= 4.5, f"{encre} lâche sur {fond}"


def test_une_variante_qui_gerait_son_cas_ne_se_fait_pas_voler_son_encre():
    """`html[data-theme="dark"] .btn` est PLUS SPÉCIFIQUE que `.btn.ghost`.

    Réparer le bouton plein imposait donc son encre sombre au bouton fantôme, qui n'avait rien
    demandé et devenait illisible : 51 occurrences du corpus étaient un défaut CRÉÉ par la
    réparation. Toute variante qui déclare sa propre encre doit la réaffirmer en sombre.
    """
    css = (".btn{background:var(--blue);color:#fff}"
           ".btn.ghost{background:transparent;color:var(--blue)}")
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    assert 'html[data-theme="dark"] .btn{color:' in bloc
    assert 'html[data-theme="dark"] .btn.ghost{color:var(--blue)' in bloc, \
        "la variante doit réaffirmer SA déclaration, verbatim tant qu'elle tient"


def test_une_variante_dont_l_encre_ne_tient_pas_est_ajustee():
    """Réaffirmer ne suffit pas si la déclaration d'origine échoue elle aussi en sombre —
    mais seulement quand la variante porte SON propre fond, donc qu'on sait contre quoi juger."""
    css = ".btn{background:var(--blue);color:#fff}.btn.plat{background:#FBFCFE;color:#11283F}"
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    encre = bloc.split('html[data-theme="dark"] .btn.plat{')[1].split("}")[0]
    valeur = [d for d in encre.split(";") if d.startswith("color:")][0][6:]
    assert B.contraste(valeur, B.fond_sombre("#FBFCFE")) >= 4.5


def test_un_selecteur_voisin_n_est_pas_pris_pour_une_variante():
    """`.hns-btns` contient `.hns-btn` comme texte sans en être une variante : réaffirmer une
    encre là serait toucher une règle que rien ne menace."""
    css = ".btn{background:var(--blue);color:#fff}.btns{color:#11283F}"
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    assert '.btns{' not in bloc


def test_une_variante_sans_fond_propre_est_restituee_verbatim():
    """On ne sait pas sur quoi elle s'écrit. Lui inventer une référence a fermé 18 occurrences
    du corpus et en a ouvert 12 ailleurs : réaffirmer doit RESTITUER, jamais re-décider."""
    css = ".btn{background:var(--blue);color:#fff}.btn.ghost{color:#11283F}"
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    assert 'html[data-theme="dark"] .btn.ghost{color:#11283F;}' in bloc


def test_la_passe_d_encre_ne_sort_pas_du_perimetre_des_surfaces_qu_on_assombrit():
    """Elle ne juge QUE sur les surfaces que la bascule a créées elle-même.

    L'élargir aux fonds tirés des jetons la fait tourner dans des widgets qu'elle n'avait jamais
    touchés, où elle éclaircit des encres qui atterrissent ensuite sur une surface claire : le
    corpus y perd plus qu'il n'y gagne. Un widget qui tire tous ses fonds des jetons relève de la
    passe PALETTE (`test_une_palette_categorielle_bascule_par_ses_jetons`), pas de celle-ci.
    """
    _, n = B.bloc_genere(".card{background:var(--card)} .card b{color:#9B3443}", JETONS, 4.5)
    assert n == 0


def test_une_encre_est_jugee_sur_la_pire_des_surfaces_sombres_du_widget():
    """Dans un widget dont toutes les surfaces sont sombres, l'encre se juge sur la pire d'elles.

    N'agir que si elle échoue contre TOUTES serait plus rigoureux et c'est empiriquement pire :
    `named-entity-recognition-sequence-labeling` passe alors de 13 à 26 occurrences. (Si le
    widget peint aussi du clair, rien ne se déclenche — voir
    `test_aucune_passe_a_l_aveugle_dans_un_widget_qui_peint_aussi_du_clair`.)
    """
    css = ".carte{background:#FBFCFE} .liseré{background:#F1F3F6} .x{color:#0A1521}"
    bloc, n = B.bloc_genere(css, JETONS, 4.5)
    encre = bloc.split('html[data-theme="dark"] .x{color:')[1].split(";")[0]
    for fond in (B.fond_sombre("#FBFCFE"), B.fond_sombre("#F1F3F6")):
        assert B.contraste(encre, fond) >= 4.5


def test_une_palette_categorielle_bascule_par_ses_jetons():
    """Un widget qui distingue des entités par couleur pose sa palette en jetons littéraux et
    laisse le JS poser les classes. Aucune règle de couleur n'est alors atteignable : c'est le
    JETON qu'on bascule, une fois pour toutes ses utilisations. 12 occurrences de
    `coreference-resolution` tenaient à cela."""
    css = (".crm{--crm-A:#2C77B6;--crm-B:#9B3443}"
           " .crm-card{background:var(--card)} .crm-a{color:var(--crm-A)}"
           " .crm-b{color:var(--crm-B)}")
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    assert 'html[data-theme="dark"] .crm{' in bloc
    surcharge = bloc.split('html[data-theme="dark"] .crm{')[1].split("}")[0]
    for nom in ("--crm-A", "--crm-B"):
        valeur = [d for d in surcharge.split(";") if d.startswith(nom + ":")][0].split(":")[1]
        assert B.contraste(valeur, "#16212e") >= 4.5, f"{nom} = {valeur}"


def test_un_jeton_de_palette_servant_de_fond_est_assombri_pas_eclairci():
    """Le rôle ne se lit pas dans le jeton mais dans son usage : éclaircir un fond, c'est
    l'inverse de ce qu'il faut."""
    css = ".w{--w-wash:#EAF4EE} .w-box{background:var(--w-wash)}"
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    valeur = bloc.split("--w-wash:")[1].split(";")[0]
    assert B.luminance(valeur) < B.luminance("#EAF4EE")


def test_un_jeton_a_double_role_n_est_pas_bascule():
    """Une seule valeur ne peut pas servir d'encre ET de fond en sombre. Laisser l'encre
    l'emporter éclaircissait des surfaces : `named-entity-recognition-sequence-labeling`
    passait de 13 à 26 occurrences, dont 17 fonds devenus clairs."""
    css = ".w{--w-x:#9B3443} .card{background:var(--card)} .a{color:var(--w-x)} .b{background:var(--w-x)}"
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    assert "--w-x:" not in bloc


def test_un_jeton_que_le_css_n_utilise_jamais_est_quand_meme_bascule():
    """Il est appliqué par le JS (`style.color=COL[r]`), qui pose `var(--crm-A)` et non une
    valeur figée : surcharger le jeton est la seule prise qu'on ait, et elle suffit."""
    css = ".w{--w-A:#9B3443} .card{background:var(--card)}"
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    assert "--w-A:" in bloc


def test_un_jeton_en_capitales_reste_distinct_de_son_homonyme_minuscule():
    """Les custom properties CSS sont sensibles à la casse. Les normaliser en minuscules comme
    les propriétés ordinaires rendait invisible toute palette écrite en capitales — jamais
    résolue, donc jamais basculée."""
    d = B.declarations("--crm-A:#2C77B6;--crm-a:#000000;COLOR:#fff")
    assert d["--crm-A"] == "#2C77B6" and d["--crm-a"] == "#000000"
    assert d["color"] == "#fff", "une propriété ordinaire, elle, se normalise"


def test_aucune_passe_a_l_aveugle_dans_un_widget_qui_peint_aussi_du_clair():
    """Une encre éclaircie sans savoir où elle atterrit tombe sur la surface claire du widget.
    Trois documents PROPRES — `ejaculation-precoce`, `masse-maigre-sous-glp1`, `peptides-gris` —
    y ont gagné 9 occurrences. Casser un document propre coûte plus que ne rapporte une
    réparation à l'aveugle."""
    css = (".card{background:var(--card)} .btn{background:var(--blue);color:#fff}"
           " .lab{color:#11283F}")
    bloc, _ = B.bloc_genere(css, JETONS, 4.5)
    assert ".lab" not in bloc
