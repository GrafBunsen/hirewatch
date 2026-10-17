from textwrap import dedent

from pydantic import HttpUrl

from hirewatch.models import Source
from hirewatch.parse_css import parse_css

test_data = dedent("""\
    <ul>
      <li class="job">
        <a class="link" href="/jobs/1">Test Job</a>
        <span class="company">Test Company</span>
        <span class="location">Test City</span>
      </li>
    </ul>
""")

test_field_map = {
    "title": "a.link",
    "company": "span.company",
    "location": "span.location",
    "url": "a.link@href",
}


def test_parse_full_config():
    test_source = Source(
        title="Test Source",
        url="https://test.com/jobs",
        type="css",
        item_selector="li.job",
        field_map=test_field_map,
    )
    result = parse_css(test_data, test_source)
    assert len(result) == 1

    assert result[0].title == "Test Job"
    assert result[0].company == "Test Company"
    assert result[0].location == "Test City"
    # relative href resolved against the listing url
    assert result[0].url == HttpUrl("https://test.com/jobs/1")
    assert result[0].source == "Test Source"


def test_parse_item_self_attribute():
    # card IS the link: the attribute lives on the item element itself ("@href")
    data = '<a class="job" href="/jobs/1"><h3>Test Job</h3></a>'
    field_map = {"title": "h3", "url": "@href"}
    test_source = Source(
        title="Test Source",
        url="https://test.com/jobs",
        type="css",
        item_selector="a.job",
        field_map=field_map,
    )
    result = parse_css(data, test_source)
    assert len(result) == 1
    assert result[0].title == "Test Job"
    assert result[0].url == HttpUrl("https://test.com/jobs/1")


def test_parse_missing_optional():
    data = '<li class="job"><a class="link" href="/j">Test Job</a></li>'
    field_map = {"title": "a.link", "url": "a.link@href", "company": "span.company"}
    test_source = Source(
        title="Test Source",
        url="https://test.com/jobs",
        type="css",
        item_selector="li.job",
        field_map=field_map,
    )
    result = parse_css(data, test_source)
    assert len(result) == 1
    assert result[0].company is None


def test_parse_skips_item_missing_required_field():
    data = dedent("""\
        <ul>
          <li class="job"><span class="company">Test Company</span></li>
          <li class="job"><a class="link" href="/j">Test Job</a></li>
        </ul>
    """)
    field_map = {"title": "a.link", "url": "a.link@href"}
    test_source = Source(
        title="Test Source",
        url="https://test.com/jobs",
        type="css",
        item_selector="li.job",
        field_map=field_map,
    )
    result = parse_css(data, test_source)
    assert len(result) == 1
    assert result[0].title == "Test Job"
