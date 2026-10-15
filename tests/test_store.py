from hirewatch.store import Store


def test_mark_and_seen(tmp_path):
    s = Store(tmp_path / "state.json")
    assert s.seen("a") is False
    s.mark("a")
    assert s.seen("a") is True
    assert s.seen("b") is False


def test_persists_across_instances(tmp_path):
    path = tmp_path / "state.json"
    s1 = Store(path)
    s1.mark("a")
    s1.save()

    s2 = Store(path)
    assert s2.seen("a") is True
