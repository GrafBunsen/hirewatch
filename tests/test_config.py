from hirewatch.config import load_source, load_sources


def test_load_source_reads_yaml(tmp_path):
    yaml_file = tmp_path / "test_source.yaml"
    yaml_file.write_text(
        "title: Test Source\n"
        'url: "https://test.com/feed"\n'
        "field_map:\n"
        "  title: title\n"
        "  url: link\n"
    )

    src = load_source(yaml_file)

    assert src.title == "Test Source"
    assert str(src.url) == "https://test.com/feed"
    assert src.field_map["url"] == "link"


def test_load_sources_skips_broken(tmp_path):
    (tmp_path / "good.yaml").write_text(
        'title: Good\nurl: "https://test.com"\nfield_map:\n  title: title\n  url: link\n'
    )
    (tmp_path / "broken.yaml").write_text("title: Broken\n")
    sources = load_sources(tmp_path)

    assert len(sources) == 1
    assert sources[0].title == "Good"
