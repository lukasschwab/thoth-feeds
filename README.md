# thoth-feeds

JSON feeds for Open Access books on [Thoth](https://github.com/thoth-pub/thoth).

## Notes

It'd be nice to support pagination (JSON Feed's `next_url`), but the Thoth pagination logic seems unstable: it takes an offset rather than a cursor, and creating new records invalidates the offset.