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
