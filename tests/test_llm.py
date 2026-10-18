from hirewatch.llm import to_text


def test_to_text_inlines_links_and_strips_chrome():
    html = """<html><body>
      <nav>MENU</nav>
      <script>var x=1;</script>
      <a href="/job/5?a=1&amp;b=2">Kurator</a>
      <p>Berlin</p>
    </body></html>"""
    out = to_text(html)
    assert "Kurator </job/5?a=1&b=2>" in out
    assert "MENU" not in out
    assert "var x" not in out
    assert "Berlin" in out
