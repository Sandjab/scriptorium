import json, pathlib, pytest
import build_site


def _publish(themes_dir, slug, title="T"):
    """Crée themes_dir/<slug>/dist/<slug>.html avec un <title>."""
    d = pathlib.Path(themes_dir) / slug / "dist"
    d.mkdir(parents=True)
    (d / f"{slug}.html").write_text(f"<title>{title}</title>", encoding="utf-8")


def _publish_doc(themes_dir, slug, corps):
    """Publie un document dont on maîtrise la structure de fin (</main>, </body>) :
    c'est elle qui porte l'ancre d'injection de la notice."""
    d = pathlib.Path(themes_dir) / slug / "dist"
    d.mkdir(parents=True)
    (d / f"{slug}.html").write_text(corps, encoding="utf-8")


def test_collect_finds_published_theme(tmp_path):
    _publish(tmp_path, "alpha", "Titre Alpha")
    out = build_site.collect(tmp_path)
    assert out == [("alpha", "Alpha", [("alpha/alpha.html", "Titre Alpha", "Titre Alpha")])]


def test_extract_title_unescapes_entities(tmp_path):
    """Le <title> source porte des entités ('&amp;') et tout affichage les ré-échappe :
    sans déséchappement ici, un '&' finit affiché '&amp;' sur la page."""
    _publish(tmp_path, "amp", "Harness &amp; loop engineering")
    out = build_site.collect(tmp_path)
    assert out[0][2][0][2] == "Harness & loop engineering"


def test_collect_skips_dir_without_dist(tmp_path):
    (tmp_path / "nodist").mkdir()
    _publish(tmp_path, "withdist")
    slugs = [slug for slug, _, _ in build_site.collect(tmp_path)]
    assert slugs == ["withdist"]


def _write_taxo(tmp_path, domains):
    """Enveloppe v2 minimale : un seul méta-domaine portant `domains`."""
    return _write_taxo_v2(tmp_path, [
        {"id": "m1", "label": "M1", "blurb": "mb", "domains": domains},
    ])


def _write_taxo_v2(tmp_path, metas):
    p = tmp_path / "taxonomy.json"
    p.write_text(json.dumps({"version": 2, "meta_domains": metas}),
                 encoding="utf-8")
    return p


def test_load_taxonomy_valid(tmp_path):
    p = _write_taxo(tmp_path, [
        {"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]},
    ])
    metas = build_site.load_taxonomy(p)
    assert metas[0]["id"] == "m1"
    assert metas[0]["domains"][0]["id"] == "d1"


def test_load_taxonomy_v1_fails(tmp_path):
    """Un taxonomy.json v1 résiduel doit casser, pas être interprété en silence."""
    p = tmp_path / "taxonomy.json"
    p.write_text(json.dumps({"version": 1, "domains": [
        {"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]},
    ]}), encoding="utf-8")
    with pytest.raises(SystemExit):
        build_site.load_taxonomy(p)


def test_load_taxonomy_duplicate_meta_id_fails(tmp_path):
    p = _write_taxo_v2(tmp_path, [
        {"id": "m1", "label": "A", "blurb": "b",
         "domains": [{"id": "d1", "label": "D", "blurb": "b", "themes": ["x"]}]},
        {"id": "m1", "label": "B", "blurb": "b",
         "domains": [{"id": "d2", "label": "D", "blurb": "b", "themes": ["y"]}]},
    ])
    with pytest.raises(SystemExit):
        build_site.load_taxonomy(p)


def test_load_taxonomy_duplicate_domain_id_across_metas_fails(tmp_path):
    p = _write_taxo_v2(tmp_path, [
        {"id": "m1", "label": "A", "blurb": "b",
         "domains": [{"id": "d1", "label": "D", "blurb": "b", "themes": ["x"]}]},
        {"id": "m2", "label": "B", "blurb": "b",
         "domains": [{"id": "d1", "label": "D", "blurb": "b", "themes": ["y"]}]},
    ])
    with pytest.raises(SystemExit):
        build_site.load_taxonomy(p)


def test_load_taxonomy_empty_meta_fails(tmp_path):
    p = _write_taxo_v2(tmp_path, [
        {"id": "m1", "label": "A", "blurb": "b", "domains": []},
    ])
    with pytest.raises(SystemExit):
        build_site.load_taxonomy(p)


@pytest.mark.parametrize("notice", ["", "   ", 42, None])
def test_load_taxonomy_invalid_notice_fails(tmp_path, notice):
    """La 'notice' porte le bandeau de non-conseil médical des pages santé.
    Vide ou non textuelle, elle produirait un bandeau muet — ou pas de bandeau du
    tout — sur des pages d'efficacité et de sécurité : à refuser au chargement.
    Le `match` garantit que c'est bien la notice qui fait échouer : sans lui, une
    future validation obligatoire ferait passer ce test sans qu'il teste rien."""
    p = _write_taxo_v2(tmp_path, [
        {"id": "m1", "label": "A", "blurb": "b", "notice": notice,
         "domains": [{"id": "d1", "label": "D", "blurb": "b", "themes": ["x"]}]},
    ])
    with pytest.raises(SystemExit, match="notice"):
        build_site.load_taxonomy(p)


@pytest.mark.parametrize("bad_id", ["index", "", "../evade", "Majuscule", "avec espace"])
def test_load_taxonomy_invalid_meta_id_fails(tmp_path, bad_id):
    """L'id d'un méta-domaine devient un nom de fichier à la racine du site.
    'index' écraserait le hub et ferait disparaître le méta-domaine, '' écrirait
    _site/.html, '../evade' écrirait hors de _site/ — chacun produisant un site
    faux avec un build en succès, le pire des cas pour ce projet."""
    p = _write_taxo_v2(tmp_path, [
        {"id": bad_id, "label": "A", "blurb": "b",
         "domains": [{"id": "d1", "label": "D", "blurb": "b", "themes": ["x"]}]},
    ])
    with pytest.raises(SystemExit, match="id de méta-domaine"):
        build_site.load_taxonomy(p)


def test_load_taxonomy_missing_file_fails(tmp_path):
    with pytest.raises(SystemExit):
        build_site.load_taxonomy(tmp_path / "absent.json")


def test_load_taxonomy_duplicate_id_fails(tmp_path):
    p = _write_taxo(tmp_path, [
        {"id": "d1", "label": "A", "blurb": "b", "themes": ["x"]},
        {"id": "d1", "label": "B", "blurb": "b", "themes": ["y"]},
    ])
    with pytest.raises(SystemExit):
        build_site.load_taxonomy(p)


def test_load_taxonomy_missing_key_fails(tmp_path):
    p = _write_taxo(tmp_path, [{"id": "d1", "label": "A", "themes": ["x"]}])  # pas de blurb
    with pytest.raises(SystemExit):
        build_site.load_taxonomy(p)


LEGACY = "automatic-prompt-optimization"


def _collected(*slugs):
    """Imite la sortie de collect() : (slug, label, docs)."""
    return [(s, s.title(), [(f"{s}/{s}.html", s, s)]) for s in slugs]


def test_group_orders_and_alpha_sorts(tmp_path):
    domains = [
        {"id": "d2", "label": "D2", "blurb": "b", "themes": ["gamma", "alpha"]},
        {"id": "d1", "label": "D1", "blurb": "b", "themes": ["beta"]},
    ]
    secs = build_site.group_by_domain(_collected("alpha", "beta", "gamma"), domains, LEGACY)
    assert [s["kind"] for s in secs] == ["domain", "domain"]
    assert secs[0]["id"] == "d2"
    assert [t[0] for t in secs[0]["themes"]] == ["alpha", "gamma"]  # tri alpha intra-domaine


def test_group_slug_without_dist_fails():
    domains = [{"id": "d1", "label": "D1", "blurb": "b", "themes": ["ghost"]}]
    with pytest.raises(SystemExit):
        build_site.group_by_domain(_collected("alpha"), domains, LEGACY)


def test_group_slug_in_two_domains_fails():
    domains = [
        {"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]},
        {"id": "d2", "label": "D2", "blurb": "b", "themes": ["alpha"]},
    ]
    with pytest.raises(SystemExit):
        build_site.group_by_domain(_collected("alpha"), domains, LEGACY)


def test_group_empty_domain_fails():
    domains = [{"id": "d1", "label": "D1", "blurb": "b", "themes": []}]
    with pytest.raises(SystemExit):
        build_site.group_by_domain(_collected("alpha"), domains, LEGACY)


def test_group_unclassified_bucket():
    domains = [{"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]}]
    secs = build_site.group_by_domain(_collected("alpha", "orphan"), domains, LEGACY)
    assert secs[-1]["kind"] == "unclassified"
    assert [t[0] for t in secs[-1]["themes"]] == ["orphan"]


def test_group_legacy_last():
    domains = [{"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]}]
    secs = build_site.group_by_domain(_collected("alpha", LEGACY), domains, LEGACY)
    assert secs[-1]["kind"] == "legacy"
    assert secs[-1]["theme"][0] == LEGACY


META = {"id": "m1", "label": "Méta Un", "blurb": "Blurb méta."}


def test_render_meta_page_headers_in_order():
    secs = [
        {"kind": "domain", "id": "d1", "label": "Premier", "blurb": "b1",
         "themes": [("alpha", "Alpha", [("alpha/alpha.html", "Alpha", "Alpha")])]},
        {"kind": "domain", "id": "d2", "label": "Second", "blurb": "b2",
         "themes": [("beta", "Beta", [("beta/beta.html", "Beta", "Beta")])]},
    ]
    out = build_site.render_meta_page(META, secs, portals=())
    assert out.index("Premier") < out.index("Second")
    assert "b1" in out and "b2" in out
    assert "Méta Un" in out
    assert 'href="index.html"' in out  # retour au hub


def test_render_meta_page_notice_banner():
    meta = dict(META, notice="Information, pas un avis médical.")
    secs = [{"kind": "domain", "id": "d1", "label": "Dom", "blurb": "b",
             "themes": [("alpha", "Alpha", [("alpha/alpha.html", "Alpha", "Alpha")])]}]
    out = build_site.render_meta_page(meta, secs, portals=())
    assert "Information, pas un avis médical." in out


def test_render_hub_cards_and_tail_sections():
    metas = [
        {"id": "m1", "label": "Méta Un", "blurb": "b1", "n_domains": 2, "n_themes": 5},
        {"id": "m2", "label": "Méta Deux", "blurb": "b2", "n_domains": 1, "n_themes": 3},
    ]
    tail = [
        {"kind": "unclassified",
         "themes": [("orphan", "Orphan", [("orphan/orphan.html", "Orphan", "Orphan")])]},
        {"kind": "legacy",
         "theme": (LEGACY, "Apo", [(f"{LEGACY}/x.html", "Réf", "Réf")])},
    ]
    out = build_site.render_hub(metas, tail, n_themes=8, n_docs=9)
    assert 'href="m1.html"' in out and 'href="m2.html"' in out
    assert out.index("Méta Un") < out.index("Méta Deux")
    assert "À classer" in out and out.index("À classer") < out.index("Legacy")


def _write_portal_file(portals_dir, domain_id, slugs):
    portals_dir.mkdir(parents=True, exist_ok=True)
    (portals_dir / f"{domain_id}.json").write_text(json.dumps({
        "domain": domain_id,
        "intro": "Intro du domaine.",
        "parcours": [{"slug": s, "pourquoi": f"étape {s}"} for s in slugs],
        "aretes": [], "delimitations": [],
    }), encoding="utf-8")


def _write_tldr(themes_dir, slug):
    (themes_dir / slug).mkdir(parents=True, exist_ok=True)
    (themes_dir / slug / "tldr.json").write_text(
        json.dumps({"these": f"Thèse de {slug}."}), encoding="utf-8")


def test_main_writes_portal_and_links_it_from_home(tmp_path):
    """Un portail présent doit être rendu ET atteignable : une page publiée mais
    orpheline de lien serait invisible."""
    themes = tmp_path / "themes"
    for s in ("alpha", "beta"):
        _publish(themes, s, s.title())
        _write_tldr(themes, s)
    taxo = _write_taxo(tmp_path, [
        {"id": "d1", "label": "Domaine Un", "blurb": "b", "themes": ["alpha", "beta"]},
    ])
    portals = tmp_path / "portals"
    _write_portal_file(portals, "d1", ["alpha", "beta"])
    site = tmp_path / "_site"

    assert build_site.main(themes_dir=themes, taxonomy_path=taxo, site_dir=site,
                           portals_dir=portals) == 0
    page = site / "domaines" / "d1.html"
    assert page.is_file()
    assert "Thèse de alpha." in page.read_text(encoding="utf-8")
    meta_page = (site / "m1.html").read_text(encoding="utf-8")
    assert 'href="domaines/d1.html"' in meta_page
    hub = (site / "index.html").read_text(encoding="utf-8")
    assert 'href="m1.html"' in hub          # le hub mène à la page méta
    assert "domaines/d1.html" not in hub    # ... qui seule porte le lien portail


def test_main_without_portal_has_no_link(tmp_path):
    """Les petits domaines n'ont pas de portail : la home ne doit pas proposer de lien mort."""
    themes = tmp_path / "themes"
    _publish(themes, "alpha", "Alpha")
    taxo = _write_taxo(tmp_path, [
        {"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]},
    ])
    site = tmp_path / "_site"
    build_site.main(themes_dir=themes, taxonomy_path=taxo, site_dir=site,
                    portals_dir=tmp_path / "portals-absent")
    assert "domaines/" not in (site / "m1.html").read_text(encoding="utf-8")
    assert not (site / "domaines").exists()


def test_orphan_portal_file_fails(tmp_path):
    """Un portail dont le domaine a été renommé ou supprimé doit casser le build
    plutôt que rester ignoré en silence."""
    themes = tmp_path / "themes"
    _publish(themes, "alpha", "Alpha")
    _write_tldr(themes, "alpha")
    taxo = _write_taxo(tmp_path, [
        {"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]},
    ])
    portals = tmp_path / "portals"
    _write_portal_file(portals, "ancien-nom", ["alpha"])
    with pytest.raises(SystemExit):
        build_site.main(themes_dir=themes, taxonomy_path=taxo,
                        site_dir=tmp_path / "_site", portals_dir=portals)


def test_main_end_to_end(tmp_path):
    themes = tmp_path / "themes"
    _publish(themes, "alpha", "Alpha")
    _publish(themes, "beta", "Beta")
    taxo = _write_taxo(tmp_path, [
        {"id": "d1", "label": "Domaine Un", "blurb": "b", "themes": ["alpha", "beta"]},
    ])
    site = tmp_path / "_site"
    rc = build_site.main(themes_dir=themes, taxonomy_path=taxo, site_dir=site,
                         portals_dir=tmp_path / "portals-absent")
    assert rc == 0
    hub = (site / "index.html").read_text(encoding="utf-8")
    assert 'href="m1.html"' in hub
    meta_page = (site / "m1.html").read_text(encoding="utf-8")
    assert "Domaine Un" in meta_page
    assert (site / "alpha" / "alpha.html").is_file()
    assert (site / "beta" / "beta.html").is_file()


def test_main_two_metas_two_pages(tmp_path):
    """Chaque méta-domaine a sa page, et les compteurs annoncés sont ceux de SON
    périmètre : un décompte faux (celui du site entier, ou domaines et thèmes
    intervertis) ferait mentir la seule vue d'ensemble qu'a le lecteur.
    Toutes les valeurs sont volontairement distinctes — 1 domaine mais 2 thèmes
    pour `ia`, 3 thèmes mais 4 documents sur le site — pour qu'aucune inversion
    de compteurs ne puisse passer inaperçue."""
    themes = tmp_path / "themes"
    for s in ("alpha", "beta", "gamma"):
        _publish(themes, s, s.title())
    # un thème à deux documents : sépare le compte des thèmes de celui des documents
    (themes / "alpha" / "dist" / "alpha-pedagogique.html").write_text(
        "<title>Alpha — édition pédagogique</title>", encoding="utf-8")
    taxo = _write_taxo_v2(tmp_path, [
        {"id": "ia", "label": "IA", "blurb": "b1",
         "domains": [{"id": "d1", "label": "D1", "blurb": "b",
                      "themes": ["alpha", "gamma"]}]},
        {"id": "sante", "label": "Santé", "blurb": "b2",
         "domains": [{"id": "d2", "label": "D2", "blurb": "b", "themes": ["beta"]}]},
    ])
    site = tmp_path / "_site"
    build_site.main(themes_dir=themes, taxonomy_path=taxo, site_dir=site,
                    portals_dir=tmp_path / "portals-absent")
    assert (site / "ia.html").is_file()
    assert (site / "sante.html").is_file()
    hub = (site / "index.html").read_text(encoding="utf-8")
    assert 'href="ia.html"' in hub and 'href="sante.html"' in hub
    assert "D1" not in hub  # les domaines vivent sur les pages méta, pas au hub
    # cartes du hub : le périmètre de chaque méta, pas celui du site
    assert "1 domaines · 2 thèmes" in hub      # ia
    assert "1 domaines · 1 thèmes" in hub      # sante
    # en-tête du hub : le site entier, thèmes et documents distincts
    assert "<span>3 thèmes</span>" in hub
    assert "<span>4 documents</span>" in hub
    # en-tête de chaque page méta, recalculé depuis ses propres sections
    ia_page = (site / "ia.html").read_text(encoding="utf-8")
    sante_page = (site / "sante.html").read_text(encoding="utf-8")
    assert "<span>1 domaines</span>" in ia_page
    assert "<span>2 thèmes</span>" in ia_page
    assert "<span>1 thèmes</span>" in sante_page   # pas « toujours le premier méta »


def test_main_notice_injected_into_theme_copies(tmp_path):
    """La notice d'un méta-domaine doit atteindre les copies publiées de SES
    monographies (et seulement les siennes) : c'est le bandeau non-conseil médical."""
    themes = tmp_path / "themes"
    _publish(themes, "alpha", "Alpha")   # méta sans notice
    _publish_doc(themes, "creatine",
                 "<title>Créatine</title><body><main>corps</main>"
                 "<footer>colophon</footer></body>")
    taxo = _write_taxo_v2(tmp_path, [
        {"id": "ia", "label": "IA", "blurb": "b",
         "domains": [{"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]}]},
        {"id": "sante", "label": "Santé", "blurb": "b",
         "notice": "Information documentaire, pas un avis médical.",
         "domains": [{"id": "d2", "label": "D2", "blurb": "b", "themes": ["creatine"]}]},
    ])
    site = tmp_path / "_site"
    build_site.main(themes_dir=themes, taxonomy_path=taxo, site_dir=site,
                    portals_dir=tmp_path / "portals-absent")
    copied = (site / "creatine" / "creatine.html").read_text(encoding="utf-8")
    assert "pas un avis médical" in copied
    # dans la colonne de prose, avant le colophon — pas relégué en fin de <body>
    assert copied.index("notice-sante-doc") < copied.index("</main>")
    assert copied.index("notice-sante-doc") < copied.index("colophon")
    # apparence portée par la charte inlinée, pas par du style dupliqué ici
    assert 'class="notice-sante-doc callout"' in copied
    assert "#7A1C2A" not in copied
    untouched = (site / "alpha" / "alpha.html").read_text(encoding="utf-8")
    assert "avis médical" not in untouched
    # la source dist/ n'est JAMAIS modifiée
    src = (themes / "creatine" / "dist" / "creatine.html").read_text(encoding="utf-8")
    assert "avis médical" not in src


@pytest.mark.parametrize("corps", [
    "<title>Créatine</title><body>sans ancre</body>",          # zéro </main>
    "<title>C</title><body><main>a</main><main>b</main></body>",  # deux </main>
])
def test_main_notice_needs_exactly_one_anchor(tmp_path, corps):
    """L'ancre d'injection doit être unique. Zéro : la notice serait perdue sans
    bruit et on publierait une monographie santé DÉPOURVUE de son non-conseil
    médical. Deux : le document recevrait DEUX bandeaux, dont un planté au milieu
    du corps. Dans les deux cas casser le build est le seul comportement tenable."""
    themes = tmp_path / "themes"
    _publish_doc(themes, "creatine", corps)
    taxo = _write_taxo_v2(tmp_path, [
        {"id": "sante", "label": "Santé", "blurb": "b",
         "notice": "Information documentaire, pas un avis médical.",
         "domains": [{"id": "d2", "label": "D2", "blurb": "b", "themes": ["creatine"]}]},
    ])
    with pytest.raises(SystemExit, match="</main>"):
        build_site.main(themes_dir=themes, taxonomy_path=taxo,
                        site_dir=tmp_path / "_site",
                        portals_dir=tmp_path / "portals-absent")
