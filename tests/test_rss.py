from pydantic import HttpUrl

from hirewatch.rss import parse

test_data = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:job_listing="http://testlink.com/job_listing">

<channel>
	<title>Test Jobs</title>
	<item>
		<title>Testjob</title>
		<link>https://testlink.com/test</link>
		<comments>Test Comment</comments>
		<pubDate>Tue, 13 Oct 2026 10:51:42 +0000</pubDate>
		<guid isPermaLink="false">test-guid</guid>
        <description>Test Description</description>
        <job_listing:location>Test City</job_listing:location>
        <job_listing:job_type>Test Job Type</job_listing:job_type>
        <job_listing:company>Test Company</job_listing:company>
	</item>
    <item>
		<title>Testjob 2</title>
		<link>https://testlink.com/test2</link>
		<comments>Test Comment 2</comments>
		<pubDate>Tue, 14 Oct 2026 10:51:42 +0000</pubDate>
		<guid isPermaLink="false">test-guid2</guid>
        <description>Test Description 2</description>
        <job_listing:location>Test City 2</job_listing:location>
        <job_listing:job_type>Test Job Type 2</job_listing:job_type>
        <job_listing:company>Test Company 2</job_listing:company>
	</item>
	</channel>
</rss>
"""

test_field_map = {
    "external_id": "guid",
    "title": "title",
    "company": "job_listing:company",
    "location": "job_listing:location",
    "published": "pubDate",
    "description": "description",
    "url": "link",
}

test_namespaces = {"job_listing": "http://testlink.com/job_listing"}


def test_parse():
    result = parse(test_data, "test_source", test_field_map, test_namespaces)
    assert len(result) == 2

    assert result[0].external_id == "test-guid"
    assert result[0].title == "Testjob"
    assert result[0].company == "Test Company"
    assert result[0].location == "Test City"
    assert result[0].published == "Tue, 13 Oct 2026 10:51:42 +0000"
    assert result[0].description == "Test Description"
    assert result[0].url == HttpUrl("https://testlink.com/test")
    assert result[0].source == "test_source"
