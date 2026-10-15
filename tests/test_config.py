from hirewatch.config import load_source


def test_load_source_reads_yaml(tmp_path):
    yaml_file = tmp_path / "test_source.yaml"
    yaml_file.write_text(
        'title: Testsource\nurl: "https://test.com/feed"\nfield_map:\n  title: title\n  url: link\n'
    )

    src = load_source(yaml_file)

    assert src.title == "Testsource"
    assert str(src.url) == "https://test.com/feed"
    assert src.field_map["url"] == "link"
