# Evidence merge for the PTCG Pocket radar

The report uses one frozen end timestamp and an inclusive 72-hour window. Collect and validate each source independently before merging. The merge is standard-library Python and not a crawler. It does not infer that an account is a real player; each included record needs first-party editorial review with evidence. Do not fill a failed or unattempted source batch with historical records. A first-party published timestamp is not interchangeable with an edited timestamp or a search result's crawl date.

Prepare one JSON manifest per platform. Example:

```json
{
  "coverage": {"directly_opened": 1, "first_party_timed": 1},
  "records": [{
    "platform": "note",
    "source_id": "stable-original-article-id",
    "canonical_url": "https://note.com/example/n/example-id",
    "created_utc": "2026-01-01T12:00:00+00:00",
    "author": "public-account-handle",
    "parent_thread_id": "stable-original-root-id",
    "time_method": "First-party JSON-LD datePublished and HTML time",
    "evidence": "Paraphrase of the player's firsthand contribution",
    "review_state": "first_party_original_substantive"
  }]
}
```

Run `python3 merge_evidence.py --cutoff <ISO-8601> --batch note note.json --batch youtube youtube.json --batch bluesky bluesky.json --batch pocketmads pocketmads.json --out merged.json`. Submit zero-eligible manifests for attempted paths so they are distinguishable from missing batches. Attribute coverage counters to each independent channel, not the aggregate. Add `proved_same_original_key` only when cross-posting can be independently demonstrated. Structural checks enforce trusted origins, stable source IDs, UTC offsets, window, review status, and deduplication. Count author accounts and discussion roots separately. Site overlap and actual page eligibility remain separate from this merger; even passing coverage is not automatic approval to build.

Tests: `python3 -m unittest -v test_merge` in this directory. The daily task does not need a new workflow, credentials, or a concurrent repository writer.
