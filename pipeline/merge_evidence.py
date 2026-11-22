#!/usr/bin/env python3
"""Join separately reviewed PTCG Pocket source manifests; fail closed."""
import argparse
import json
from collections import Counter
from datetime import datetime as DT, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

PLATFORMS = {
    "note": {"note.com"},
    "bluesky": {"bsky.app"},
    "youtube": {"youtube.com", "www.youtube.com", "youtu.be"},
    "pocketmads": {"app.pocketmads.com"},
}
ALIASES = {"note.com":"note", "bsky":"bluesky"}

def stamp(value):
    d = DT.fromisoformat(str(value).replace("Z", "+00:00"))
    if d.utcoffset() is None: raise ValueError("missing UTC offset")
    return d.astimezone(timezone.utc)

def canonical(platform, link):
    u = urlsplit(link)
    if u.scheme != 'https' or u.hostname not in PLATFORMS[platform] or u.username or u.password:
        raise ValueError("noncanonical origin")
    q = u.query if platform == "youtube" and u.path == "/watch" else ""
    return urlunsplit((u.scheme, u.hostname, u.path.rstrip("/"), q, ""))

def run(end, batches):
    start = end - timedelta(hours=72)
    accepted, rejected, coverage, seen, equivalents, seen_url = [], [], {}, set(), set(), set()
    for platform in PLATFORMS:
        batch=batches.get(platform)
        if not batch:
            coverage[platform]={"state":"not_run_or_no_manifest", "eligible":0}
            continue
        counters=dict(batch.get("coverage", {}))
        raw=batch.get("records", [])
        coverage[platform]={"state":"ran", **counters, "submitted_verified_records":len(raw), "eligible":0}
        for r in raw:
            try:
                if ALIASES.get(r.get("platform"), r.get("platform")) != platform: raise ValueError("wrong batch")
                ts=stamp(r["created_utc"])
                if not start <= ts <= end: raise ValueError("outside window")
                url=canonical(platform, r["canonical_url"])
                for k in ("source_id", "author", "parent_thread_id", "time_method", "evidence"):
                    if not isinstance(r.get(k),str) or not r[k].strip(): raise ValueError("missing "+k)
                if r.get("review_state") != "first_party_original_substantive": raise ValueError("missing reviewer verdict")
                key=(platform, r["source_id"])
                equiv=r.get("proved_same_original_key")
                if key in seen or url in seen_url or (equiv and equiv in equivalents): raise ValueError("duplicate")
            except (KeyError, TypeError, ValueError) as e:
                rejected.append({"platform":platform,"source_id":r.get("source_id"),"reason":str(e)})
                continue
            seen.add(key); seen_url.add(url)
            if equiv: equivalents.add(equiv)
            item={**r,"platform":platform,"canonical_url":url,"created_utc":ts.isoformat()}
            accepted.append(item)
            coverage[platform]["eligible"]+=1
    accepted.sort(key=lambda r:r["created_utc"],reverse=True)
    authors={(r["platform"], r["author"].casefold()) for r in accepted}
    parents={(r["platform"], r["parent_thread_id"]) for r in accepted}
    slices={"0-24h":0, "24-48h":0, "48-72h":0}
    labels=list(slices)
    for r in accepted:
        age=(end-stamp(r["created_utc"])).total_seconds()/3600
        slices[labels[min(2,int(age//24))]]+=1
    return {
        "window":{"start_utc":start.isoformat(),"end_utc":end.isoformat()},
        "reporting":{"strict_eligible_count":len(accepted),"source_goal":100,
                     "shortfall":max(0,100-len(accepted)),"coverage_met":len(accepted)>=100,
                     "quality_gate":"passed_coverage_only" if len(accepted)>=100 and len(parents)>=10 else "failed",
                     "verified_unique_authors":len(authors),"verified_parent_thread_count":len(parents),
                     "per_platform_eligible":dict(Counter({k:v["eligible"] for k,v in coverage.items()})),
                     "slices":slices, "source_diversity_insufficient":len(parents)<10},
        "source_coverage":coverage, "eligible":accepted,"rejected_by_merge":rejected,
        "verification_scope":"Human first-party originality/content review precedes this structural merge; cross-account same-person identity and cross-platform syndication require affirmative evidence."
    }

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cutoff", required=True)
    p.add_argument("--batch",nargs=2,action="append",default=[],metavar=("PLATFORM","FILE"))
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    batches={}
    for platform, file in a.batch:
        if platform not in PLATFORMS or platform in batches: p.error("unknown/duplicate batch "+platform)
        batches[platform]=json.loads(Path(file).read_text())
    a.out.write_text(json.dumps(run(stamp(a.cutoff),batches),indent=2,ensure_ascii=False)+"\n")
