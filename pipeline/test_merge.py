import unittest
from merge_evidence import run, stamp

END=stamp("2026-11-22T09:21:00Z")
def record(src="a",date="2026-11-20T12:00:00Z",**changes):
    return {"platform":"note","source_id":src, "created_utc":date,
    "canonical_url":"https://note.com/test/n/"+src, "author":"same", "parent_thread_id":"root",
    "time_method":"datePublished", "evidence":"First-hand deck change after matches",
    "review_state":"first_party_original_substantive", **changes}
class MergeTests(unittest.TestCase):
    def evaluate(self,*r): return run(END,{"note":{"records":r}})
    def test_limit(self):
        a=self.evaluate(record("start","2026-11-19T09:21:00Z"),
                        record("before","2026-11-19T09:20:59Z"),
                        record("end","2026-11-22T09:21:00Z"),
                        record("after","2026-11-22T09:21:01Z"))
        self.assertEqual(a["reporting"]["strict_eligible_count"],2)
        self.assertEqual(a["reporting"]["slices"],{"0-24h":1,"24-48h":0,"48-72h":1})
    def test_dedupe(self):
        a=self.evaluate(record(),record(),record("b"))
        self.assertEqual((a["reporting"]["strict_eligible_count"],a["reporting"]["verified_unique_authors"],a["reporting"]["verified_parent_thread_count"]),(2,1,1))
        self.assertEqual(a["source_coverage"]["pocketmads"]["state"],"not_run_or_no_manifest")
    def test_fail_closed(self):
        a=self.evaluate(record(date="2026-11-20T12:00:00"),record(review_state="pending"),record(canonical_url="https://example.com/a"))
        self.assertEqual(a["reporting"]["strict_eligible_count"],0)
        self.assertEqual(len(a["rejected_by_merge"]),3)
    def test_proved_cross_platform_duplicate(self):
        a=record(proved_same_original_key="same")
        b={**record(), "platform":"bluesky","canonical_url":"https://bsky.app/profile/author/post/id","proved_same_original_key":"same"}
        out=run(END,{"note":{"records":[a]},"bluesky":{"records":[b]}})
        self.assertEqual(out["reporting"]["strict_eligible_count"],1)
if __name__=="__main__": unittest.main()
