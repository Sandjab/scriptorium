import html, json, pathlib, pytest
import portal


def _write_portal(tmp_path, domain_id, **overrides):
    """Écrit un portail valide à 2 thèmes, surchargeable champ par champ."""
    data = {
        "domain": domain_id,
        "intro": "Ce que le domaine couvre.",
        "parcours": [
            {"slug": "alpha", "pourquoi": "pose le vocabulaire"},
            {"slug": "beta", "pourquoi": "en tire les conséquences"},
        ],
        "aretes": [{"de": "alpha", "vers": "beta", "lien": "l'un précède l'autre"}],
        "delimitations": [{"a": "alpha", "b": "beta", "frontiere": "l'un mesure, l'autre agit"}],
    }
    data.update(overrides)
    p = tmp_path / f"{domain_id}.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def _tldr(themes_dir, slug, these="Thèse vérifiée du thème."):
    d = pathlib.Path(themes_dir) / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "tldr.json").write_text(json.dumps({"these": these}), encoding="utf-8")


SLUGS = ["alpha", "beta"]


def test_load_portal_valid(tmp_path):
    p = _write_portal(tmp_path, "d1")
    data = portal.load_portal(p, "d1", SLUGS)
    assert [s["slug"] for s in data["parcours"]] == ["alpha", "beta"]
    assert data["aretes"][0]["lien"] == "l'un précède l'autre"


def test_portal_omitting_a_theme_fails(tmp_path):
    """Couverture exhaustive : un thème publié ne doit jamais devenir invisible dans
    le portail de son domaine — l'oubli doit casser le build, pas passer inaperçu."""
    p = _write_portal(tmp_path, "d1", parcours=[{"slug": "alpha", "pourquoi": "seul"}])
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_portal_citing_foreign_slug_fails(tmp_path):
    """Un parcours qui cite un thème d'un autre domaine trahit un déplacement de
    taxonomie non répercuté : le portail doit suivre /arrange, pas diverger."""
    p = _write_portal(tmp_path, "d1", parcours=[
        {"slug": "alpha", "pourquoi": "ok"},
        {"slug": "beta", "pourquoi": "ok"},
        {"slug": "gamma", "pourquoi": "hors domaine"},
    ])
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_portal_duplicate_step_fails(tmp_path):
    """Un slug répété fausse la numérotation du parcours et signale une fusion ratée."""
    p = _write_portal(tmp_path, "d1", parcours=[
        {"slug": "alpha", "pourquoi": "une fois"},
        {"slug": "alpha", "pourquoi": "deux fois"},
        {"slug": "beta", "pourquoi": "ok"},
    ])
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_portal_edge_outside_domain_fails(tmp_path):
    """Une arête vers un thème absent du domaine produirait un libellé introuvable
    au rendu : mieux vaut échouer au chargement."""
    p = _write_portal(tmp_path, "d1",
                      aretes=[{"de": "alpha", "vers": "gamma", "lien": "x"}])
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_portal_delimitation_outside_domain_fails(tmp_path):
    p = _write_portal(tmp_path, "d1",
                      delimitations=[{"a": "gamma", "b": "beta", "frontiere": "x"}])
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_portal_domain_mismatch_fails(tmp_path):
    """Le nom du fichier déclare le domaine ; un champ 'domain' divergent signale un
    copier-coller entre portails."""
    p = _write_portal(tmp_path, "d1", domain="autre")
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_portal_empty_intro_fails(tmp_path):
    p = _write_portal(tmp_path, "d1", intro="   ")
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_portal_step_without_pourquoi_fails(tmp_path):
    """Sans le 'pourquoi', une étape n'apporte rien que la home ne donne déjà."""
    p = _write_portal(tmp_path, "d1", parcours=[
        {"slug": "alpha", "pourquoi": ""},
        {"slug": "beta", "pourquoi": "ok"},
    ])
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_portal_invalid_json_fails(tmp_path):
    p = tmp_path / "d1.json"
    p.write_text("{pas du json", encoding="utf-8")
    with pytest.raises(SystemExit):
        portal.load_portal(p, "d1", SLUGS)


def test_thesis_missing_tldr_fails(tmp_path):
    """La thèse est dérivée, pas stockée : si la source disparaît, le portail ne doit
    pas se rendre avec un trou silencieux."""
    with pytest.raises(SystemExit):
        portal.thesis_of(tmp_path, "alpha")


def test_thesis_empty_fails(tmp_path):
    _tldr(tmp_path, "alpha", these="  ")
    with pytest.raises(SystemExit):
        portal.thesis_of(tmp_path, "alpha")


def _entries(*slugs, titre=None):
    """Imite les entrées d'un domaine produites par build_site.group_by_domain()."""
    return [(s, s.title(), [(f"{s}/{s}.html", s, titre or s)]) for s in slugs]


# Méta-domaine porteur du domaine rendu : build_site le fournit toujours (taxonomie v2).
META = {"id": "meta-un", "label": "Méta Un"}


def test_short_title_drops_subtitle():
    """Dans une arête, le titre complet noierait la relation qu'on veut montrer."""
    assert portal.short_title("Décodage et sampling : des logits aux tokens") \
        == "Décodage et sampling"


def test_short_title_handles_em_dash_separator():
    """Le corpus sépare le sous-titre par ':' ou par un tiret cadratin ; ignorer le
    second laissait passer des noms de plus de 70 caractères dans une arête."""
    assert portal.short_title("Approximate Nearest Neighbor search — HNSW, IVF, PQ") \
        == "Approximate Nearest Neighbor search"


def test_short_title_keeps_title_without_subtitle():
    assert portal.short_title("Mixture of Experts (MoE)") == "Mixture of Experts (MoE)"


def test_render_uses_document_title_not_slug(tmp_path):
    """Le titre de la monographie est lisible ('IA agentique : …') là où le slug
    donnerait 'Agentic Ai' : le portail affiche le titre, pas le libellé dérivé."""
    p = _write_portal(tmp_path, "d1")
    data = portal.load_portal(p, "d1", SLUGS)
    for s in SLUGS:
        _tldr(tmp_path, s)
    entries = [("alpha", "Alpha", [("alpha/alpha.html", "alpha", "Vrai titre : sous-titre")]),
               ("beta", "Beta", [("beta/beta.html", "beta", "Autre titre : et sa suite")])]

    out = html.unescape(portal.render({"id": "d1", "label": "D1"}, data, entries,
                                      tmp_path, "2026-01-01 00:00 UTC", META))

    assert "Vrai titre : sous-titre" in out        # étape = titre complet
    assert "<b>Vrai titre</b>" in out              # arête = titre court
    assert "Alpha" not in out                      # jamais le libellé dérivé du slug


def test_render_derives_thesis_and_links(tmp_path):
    """Le corps du portail est dérivé : la thèse vient de tldr.json (jamais recopiée
    dans le portail) et chaque étape pointe vers la monographie."""
    p = _write_portal(tmp_path, "d1")
    data = portal.load_portal(p, "d1", SLUGS)
    _tldr(tmp_path, "alpha", these="Thèse de alpha.")
    _tldr(tmp_path, "beta", these="Thèse de beta.")

    out = portal.render({"id": "d1", "label": "Domaine 1"}, data,
                        _entries(*SLUGS), tmp_path, "2026-01-01 00:00 UTC", META)
    texte = html.unescape(out)  # l'apostrophe est échappée comme sur la home

    assert "Thèse de alpha." in texte and "Thèse de beta." in texte
    assert 'href="../alpha/alpha.html"' in out          # remonte depuis domaines/
    assert 'href="../index.html"' in out                # retour home
    assert "pose le vocabulaire" in texte               # couche éditoriale
    assert "l'un précède l'autre" in texte              # arête
    assert "l'un mesure, l'autre agit" in texte         # délimitation


def test_render_breadcrumb_traverses_meta_domain(tmp_path):
    """La taxonomie a deux étages : un portail est DANS un méta-domaine, et le
    lecteur doit pouvoir remonter à celui-ci. Un fil d'Ariane qui ne propose que
    le hub fait sauter un niveau — on redescend alors par la home, sans savoir
    d'où l'on vient."""
    p = _write_portal(tmp_path, "d1")
    data = portal.load_portal(p, "d1", SLUGS)
    for s in SLUGS:
        _tldr(tmp_path, s)

    out = portal.render({"id": "d1", "label": "D1"}, data, _entries(*SLUGS),
                        tmp_path, "2026-01-01 00:00 UTC", META)

    assert 'href="../meta-un.html"' in out          # l'étage intermédiaire est atteignable
    assert "Méta Un" in html.unescape(out)          # et nommé, pas seulement lié
    assert out.index('../index.html') < out.index('../meta-un.html')  # hub, puis méta


def test_render_escapes_editorial_text(tmp_path):
    """La couche éditoriale est écrite par un modèle : elle doit être échappée."""
    p = _write_portal(tmp_path, "d1", intro="Tension <script>alert(1)</script>")
    data = portal.load_portal(p, "d1", SLUGS)
    _tldr(tmp_path, "alpha")
    _tldr(tmp_path, "beta")

    out = portal.render({"id": "d1", "label": "D1"}, data,
                        _entries(*SLUGS), tmp_path, "2026-01-01 00:00 UTC", META)

    assert "<script>alert(1)</script>" not in out
    assert "&lt;script&gt;" in out


def test_render_omits_empty_sections(tmp_path):
    """Un domaine sans arêtes ni délimitations ne doit pas afficher de rubriques vides."""
    p = _write_portal(tmp_path, "d1", aretes=[], delimitations=[])
    data = portal.load_portal(p, "d1", SLUGS)
    _tldr(tmp_path, "alpha")
    _tldr(tmp_path, "beta")

    out = portal.render({"id": "d1", "label": "D1"}, data,
                        _entries(*SLUGS), tmp_path, "2026-01-01 00:00 UTC", META)

    assert "Ce qui relie les thèmes" not in out
    assert "Frontières entre voisins" not in out
    assert "Parcours de lecture" in out
