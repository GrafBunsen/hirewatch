from textwrap import dedent

from pydantic import HttpUrl

from hirewatch.rss import parse

test_data = dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:job_listing="http://test.com/job_listing">
    <channel>
      <item>
        <title>Test Job</title>
        <link>https://test.com/test</link>
        <pubDate>Tue, 13 Oct 2026 10:51:42 +0000</pubDate>
        <guid isPermaLink="false">test-guid</guid>
        <description>Test Description</description>
        <job_listing:location>Test City</job_listing:location>
        <job_listing:company>Test Company</job_listing:company>
      </item>
    </channel>
    </rss>
""")

test_field_map = {
    "external_id": "guid",
    "title": "title",
    "company": "job_listing:company",
    "location": "job_listing:location",
    "published": "pubDate",
    "description": "description",
    "url": "link",
}

test_namespaces = {"job_listing": "http://test.com/job_listing"}


def test_parse_full_config():
    result = parse(test_data, "Test Source", test_field_map, test_namespaces)
    assert len(result) == 1

    assert result[0].external_id == "test-guid"
    assert result[0].title == "Test Job"
    assert result[0].company == "Test Company"
    assert result[0].location == "Test City"
    assert result[0].published == "Tue, 13 Oct 2026 10:51:42 +0000"
    assert result[0].description == "Test Description"
    assert result[0].url == HttpUrl("https://test.com/test")
    assert result[0].source == "Test Source"


def test_parse_missing_optional():
    data = """<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0">
            <channel><item>
            <title>Test Job</title>
            <link>https://test.com/j</link>
            </item></channel>
            </rss>"""
    field_map = {"title": "title", "url": "link", "company": "company"}
    result = parse(data, "Test Source", field_map, None)
    assert len(result) == 1
    assert result[0].company is None


def test_parse_skips_item_missing_required_field():
    data = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
        <channel>
        <item><link>https://test.com/1</link></item>
        <item><title>Test Job</title><link>https://test.com/2</link></item>
        </channel>
        </rss>"""
    field_map = {"title": "title", "url": "link"}
    result = parse(data, "Test Source", field_map, None)
    assert len(result) == 1
    assert result[0].title == "Test Job"
