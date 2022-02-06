# thoth-feeds

JSON feeds for Open Access books on [Thoth](https://thoth.pub/).

## Usage

`thoth-feeds` is hosted at https://us-central1-arxiv-feeds.cloudfunctions.net/thoth-feeds.

Filter the feed by adding a `filter` URL parameter:

```
https://us-central1-arxiv-feeds.cloudfunctions.net/thoth-feeds?filter=Object
```

From Thoth's GraphQL API documentation for the `filter` argument:

> A query string to search. This argument is a test, do not rely on it. At present it simply searches for case insensitive literals on full_title, doi, reference, short_abstract, long_abstract, and landing_page.

## Notes

It'd be nice to support pagination (JSON Feed's `next_url`), but the Thoth pagination logic seems unstable: it takes an offset rather than a cursor, and creating new records invalidates the offset.