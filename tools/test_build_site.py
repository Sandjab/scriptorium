import json, pathlib, pytest
import build_site


def _publish(themes_dir, slug, title="T"):
    """Crée themes_dir/<slug>/dist/<slug>.html avec un <title>."""
    d = pathlib.Path(themes_dir) / slug / "dist"
    d.mkdir(parents=True)
    (d / f"{slug}.html").write_text(f"<title>{title}</title>", encoding="utf-8")


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
    p = tmp_path / "taxonomy.json"
    p.write_text(json.dumps({"version": 1, "domains": domains}), encoding="utf-8")
    return p


def test_load_taxonomy_valid(tmp_path):
    p = _write_taxo(tmp_path, [
        {"id": "d1", "label": "D1", "blurb": "b", "themes": ["alpha"]},
    ])
    assert build_site.load_taxonomy(p)[0]["id"] == "d1"


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


def test_render_domain_headers_in_order():
    secs = [
        {"kind": "domain", "id": "d1", "label": "Premier", "blurb": "b1",
         "themes": [("alpha", "Alpha", [("alpha/alpha.html", "Alpha", "Alpha")])]},
        {"kind": "domain", "id": "d2", "label": "Second", "blurb": "b2",
         "themes": [("beta", "Beta", [("beta/beta.html", "Beta", "Beta")])]},
    ]
    out = build_site.render_index(secs, n_themes=2, n_docs=2)
    assert out.index("Premier") < out.index("Second")
    assert "b1" in out and "b2" in out


def test_render_unclassified_and_legacy_last():
    secs = [
        {"kind": "domain", "id": "d1", "label": "Dom", "blurb": "b",
         "themes": [("alpha", "Alpha", [("alpha/alpha.html", "Alpha", "Alpha")])]},
        {"kind": "unclassified",
         "themes": [("orphan", "Orphan", [("orphan/orphan.html", "Orphan", "Orphan")])]},
        {"kind": "legacy",
         "theme": (LEGACY, "Apo", [(f"{LEGACY}/x.html", "Réf", "Réf")])},
    ]
    out = build_site.render_index(secs, n_themes=3, n_docs=3)
    assert "À classer" in out
    assert out.index("À classer") < out.index("Legacy")  # bucket avant legacy


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
    assert 'href="domaines/d1.html"' in (site / "index.html").read_text(encoding="utf-8")


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
    index = (site / "index.html").read_text(encoding="utf-8")
    assert "domaines/" not in index
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
    index = (site / "index.html").read_text(encoding="utf-8")
    assert "Domaine Un" in index
    assert (site / "alpha" / "alpha.html").is_file()
    assert (site / "beta" / "beta.html").is_file()
