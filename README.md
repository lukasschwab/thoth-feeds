# thoth-feeds

JSON feeds for Open Access books on [Thoth](https://github.com/thoth-pub/thoth).

## Usage

`thoth-feeds` is hosted at https://us-central1-arxiv-feeds.cloudfunctions.net/thoth-feeds.

You can filter the feed by adding a `filter` URL parameter:

```
https://us-central1-arxiv-feeds.cloudfunctions.net/thoth-feeds?filter=Object
```


## Notes

It'd be nice to support pagination (JSON Feed's `next_url`), but the Thoth pagination logic seems unstable: it takes an offset rather than a cursor, and creating new records invalidates the offset.