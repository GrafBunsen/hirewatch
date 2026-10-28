# Defining sources

A source tells hirewatch where to look and how to read the jobs it finds. Each
source is a single YAML file in your sources directory (`data/sources/` under
Docker, `sources/` otherwise). Every `*.yaml` file there is loaded on each run; a
broken file is skipped with a log message and does not stop the others.

Ready-to-edit templates for all three types live in
[examples/](examples/).

## Common fields

| Field | Required | Applies to | Meaning |
|---|---|---|---|
| `title` | yes | all | A short name for the source. Also shown per job in the email. |
| `url` | yes | all | The page or feed to fetch. |
| `type` | yes | all | One of `rss`, `css`, `ai`. |
| `field_map` | rss, css | rss, css | Maps job fields to feed tags / CSS selectors (see below). |
| `item_selector` | css | css | CSS selector matching one job card. |
| `namespaces` | no | rss | XML namespace prefixes used in `field_map`. |
| `criterion` | no | all | A plain-language rule; an LLM keeps only matching jobs. |

The job fields hirewatch understands are `title`, `url` (both required in a
`field_map`), and the optional `external_id`, `company`, `location`,
`published`, `description`.

`external_id` is the provider's own identifier (an RSS `guid`, a URL fragment).
When present it is used to recognise a job across runs; otherwise hirewatch falls
back to `source + title`. Mapping it when the feed offers one makes de-duplication
more robust.

## `rss` — a feed

For sites that publish a job feed. `field_map` maps job fields to the feed's XML
tags.

```yaml
title: example-feed
type: rss
url: "https://example.com/jobs/feed/"
field_map:
  external_id: guid
  title: title
  published: pubDate
  url: link
```

Some feeds put extra fields in a custom XML namespace. Declare the prefix under
`namespaces` and use `prefix:tag` in the map:

```yaml
namespaces:
  job_listing: "https://example.com"
field_map:
  company: job_listing:company
  location: job_listing:location
```

## `css` — a static HTML page

For pages that render jobs server-side in stable markup. `item_selector` matches
each job card; the selectors in `field_map` are evaluated **within** each card.

```yaml
title: example-html
type: css
url: "https://example.com/jobs"
item_selector: "li.job"
field_map:
  title: ".job-title"
  company: ".employer"
  location: ".location"
  url: "a@href"
```

Notes:

- Use `@attr` to read an attribute instead of text, e.g. `a@href` for a link's
  target, or `@href` when the card element *is* the link.
- Relative URLs are resolved against the source `url`.
- Only the fetched page is read — there is no pagination following. For a daily
  watcher that is usually fine, since new jobs appear on the first page.
- Field text is taken verbatim. If a site prefixes labels ("Location: Berlin"),
  the text keeps them; a `criterion` (below) copes with messy text well.

## `ai` — let an LLM read the page

For pages with no usable structure, or that change layout often. hirewatch sends
the page to your configured LLM and asks it to extract jobs. No `field_map` or
`item_selector` is needed.

```yaml
title: example-ai
type: ai
url: "https://example.com/careers"
criterion: >
  Only real job openings. No apprenticeships, internships, or volunteer roles.
```

`ai` sources require an LLM endpoint — see
[configuration.md](configuration.md#llm) and make sure the backend has enough
context length for a full page.

## `criterion` — filter in plain language

Any source type can add a `criterion`: a sentence (or a few) describing which
jobs to keep. After the jobs are read, the LLM drops the ones that do not match.
This is the part a non-technical user can actually write — no selectors, no
syntax.

```yaml
criterion: >
  Only jobs based in Berlin, Brandenburg, or remote. Topics: arts, culture,
  media, communication. No titles containing "internship" or "working student".
```

Like `ai` sources, a `criterion` needs the LLM endpoint configured. A source can
combine any fetch type with a `criterion` — e.g. a `css` page narrowed by a rule,
or an `rss` feed trimmed to the roles you care about.
