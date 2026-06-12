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
