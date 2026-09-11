"""Tests du lint de CONTRASTE EN THÈME SOMBRE (lint_contraste_sombre.py).

Lancer :  python3 -m pytest .claude/skills/monograph/scripts/test_lint_contraste_sombre.py

CE QUE CES TESTS PROTÈGENT, ET POURQUOI

  Le lint ouvre un navigateur ; ses tests, non. La frontière est posée exprès dans le code :
  la sonde injectée dans la page RELÈVE (couleur d'encre, fond effectivement peint), et tout
  le VERDICT — rapport de contraste, famille, seuil, tri — est calculé en Python. C'est cette
  moitié-là qui décide ce qu'on répare, et c'est elle qui est testée ici. Un test qui aurait
  besoin d'un navigateur ne serait pas lancé, donc ne protégerait rien.

  Deux intentions, et la seconde compte autant que la première :

  1. Le nombre doit être JUSTE. Tout le chantier se chiffre en rapports de contraste ; une
     formule qui dérive de quelques pourcents déclasse silencieusement des centaines
     d'occurrences d'un côté ou de l'autre du seuil.
  2. Les FAMILLES ne doivent pas se confondre. Elles ne décrivent pas une gravité mais un
     mécanisme, et chaque mécanisme a sa réparation : une règle `data-theme` pour un fond
     littéral, un jeton `--onbright` pour le miroir, une encre à retirer pour le symétrique.
     Ranger une occurrence dans la mauvaise famille envoie la réparation au mauvais endroit —
     c'est `test_le_miroir_n_est_pas_confondu_avec_un_fond_en_dur` qui tient cette frontière.
"""
import pathlib, pytest
import lint_contraste_sombre as L

CHARTE = pathlib.Path(__file__).resolve().parent.parent / "template" / "charte.css"


# --- le nombre -------------------------------------------------------------

def test_le_rapport_de_contraste_suit_wcag():
    """Les deux bornes de l'échelle : elles ancrent tout le reste du chantier."""
    assert L.contraste("#000000", "#ffffff") == pytest.approx(21.0, abs=0.01)
    assert L.contraste("#7c2a38", "#7c2a38") == pytest.approx(1.0, abs=0.001)


def test_le_temoin_mesure_le_2026_09_11_reste_sous_le_seuil():
    """`.bnv-q` de reasoning-test-time-compute : encre #E4EBF3 sur fond #FBFCFE, mesuré 1,17:1.

    C'est LE cas qui a chiffré le chantier — du texte clair sur du texte clair, invisible.
    Si ce test passe un jour au-dessus de 3, ce n'est pas le document qui a guéri : c'est la
    formule qui a dérivé.
    """
    assert L.contraste("#E4EBF3", "#FBFCFE") == pytest.approx(1.17, abs=0.02)


def test_une_couleur_illisible_echoue_bruyamment():
    """Une couleur tronquée ne doit pas produire un contraste plausible mais faux."""
    with pytest.raises(SystemExit):
        L.luminance("#abc")


# --- les jetons, lus dans la charte ---------------------------------------

def test_les_jetons_sont_lus_dans_la_charte_avec_leurs_DEUX_valeurs():
    """La charte est la source unique : une table de jetons recopiée dans le lint divergerait
    au premier ajustement de palette, et le lint classerait alors des jetons en « fond en dur ».

    Les deux valeurs sont nécessaires, pas seulement la sombre : c'est leur ÉCART qui distingue
    le miroir du reste.
    """
    jetons = L.jetons_charte(CHARTE.read_text(encoding="utf-8"))
    assert jetons["--blue"] == ("#23537f", "#6fa8d8")
    assert jetons["--paper"] == ("#f4f6fa", "#0e1620")
    assert "--maxw" not in jetons, "une longueur n'est pas une couleur de fond"


def test_un_jeton_precede_d_un_commentaire_est_quand_meme_lu():
    """`--paper` et `--blue` sont précédés d'un commentaire dans le bloc sombre de la charte.
    Un parseur qui ne les retire pas perd justement les jetons les plus utilisés, et range
    leurs occurrences dans « fond codé en dur » : un chantier fantôme."""
    css = ':root{--blue:#23537F;}\nhtml[data-theme="dark"]{/* on éclaircit */ --blue:#6FA8D8;}'
    assert L.jetons_charte(css)["--blue"] == ("#23537f", "#6fa8d8")


def test_une_charte_sans_bloc_sombre_echoue_bruyamment():
    with pytest.raises(SystemExit):
        L.jetons_charte(":root{--ink:#15202E;}")


# --- les familles ----------------------------------------------------------

JETONS = {"--blue": ("#23537f", "#6fa8d8"),   # s'éclaircit en sombre
          "--card": ("#ffffff", "#16212e"),   # s'assombrit
          "--paper": ("#f4f6fa", "#0e1620")}


def test_le_miroir_n_est_pas_confondu_avec_un_fond_en_dur():
    """Les deux donnent du texte illisible, et se réparent à l'opposé l'un de l'autre.

    #6FA8D8 EST un jeton — la valeur sombre de --blue, PLUS CLAIRE que sa valeur diurne :
    c'est l'encre blanche posée dessus qu'il faut reprendre (jeton --onbright). #FBFCFE n'est
    aucun jeton : c'est le FOND qu'il faut doubler d'une règle sombre. Confondre les deux fait
    réécrire ce qui allait.

    Le piège est qu'en luminance absolue #6FA8D8 (0,36) est plus SOMBRE que la moitié de
    l'échelle : un classement au seuil absolu le rangerait avec les fonds corrects.
    """
    assert L.famille("#6FA8D8", JETONS) == "miroir"
    assert L.famille("#FBFCFE", JETONS) == "fond_clair_en_dur"


def test_l_encre_en_dur_sur_fond_sombre_correct_a_sa_propre_famille():
    """Le fond est le bon jeton sombre : rien à corriger côté fond, tout côté encre."""
    assert L.famille("#16212E", JETONS) == "encre_en_dur"


def test_un_fond_sombre_inconnu_reste_a_adjuger():
    """Ni jeton ni fond clair : le lint ne devine pas, il range dans `autre` pour qu'un humain
    (ou un agent) tranche — plutôt que d'inventer une famille et une réparation avec."""
    assert L.famille("#1a0f05", JETONS) == "autre"


# --- le seuil et le tri ----------------------------------------------------

def _rec(encre, fond, ou="div.x"):
    return {"encre": encre, "fond": fond, "ou": ou, "fondDe": ou, "texte": "un texte"}


def test_seules_les_occurrences_sous_le_seuil_sont_relevees():
    """Un lint qui liste aussi ce qui va bien ne se lit plus : 2 872 occurrences se noieraient
    dans 90 000 lignes conformes."""
    records = [_rec("#E4EBF3", "#FBFCFE"), _rec("#E4EBF3", "#0E1620")]
    fautes = L.analyse(records, JETONS, seuil=3.0)
    assert len(fautes) == 1
    assert fautes[0]["fond"] == "#FBFCFE"


def test_le_seuil_est_bien_une_borne_reglable():
    """Le défaut 3.0 marque le « cassé », pas la conformité AA (4,5 pour du texte courant) :
    le seuil doit donc pouvoir monter sans toucher au code."""
    records = [_rec("#ffffff", "#6FA8D8")]  # miroir mesuré à 2,54:1
    assert L.analyse(records, JETONS, seuil=2.0) == []
    assert len(L.analyse(records, JETONS, seuil=3.0)) == 1


def test_la_pire_occurrence_sort_en_premier():
    """On répare en descendant la liste : le texte invisible d'abord, le texte pâle ensuite."""
    fautes = L.analyse([_rec("#ffffff", "#6FA8D8"), _rec("#E4EBF3", "#FBFCFE")],
                       JETONS, seuil=3.0)
    assert [f["fond"] for f in fautes] == ["#FBFCFE", "#6FA8D8"]


def test_un_document_propre_ne_produit_rien():
    """Les 12 documents mesurés propres le 2026-09-11 doivent rendre une liste vide, pas un
    rapport vide-mais-non-nul : c'est ce que le code de sortie 0 promet."""
    assert L.analyse([_rec("#E4EBF3", "#0E1620"), _rec("#15202E", "#FFFFFF")],
                     JETONS, seuil=3.0) == []
