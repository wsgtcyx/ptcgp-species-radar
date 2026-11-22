#!/usr/bin/env python3
"""PTCG Pocket Reddit public-data research probe and raw-evidence snapshot.
Never declares 100-source success by itself: deck-intent tags are heuristic and
require independent review. Respect 403/429; no credential/anti-bot bypass.
"""
import datetime as dt, json, os, pathlib, re, time, urllib.request, urllib.error
from collections import Counter

UTC=dt.timezone.utc
now=dt.datetime.now(UTC)
cutoff=now-dt.timedelta(hours=72)
subs=("PTCGP","PokemonPocket","PokemonTCGP")
user_agent="PTCGPDeckRadarPublicAudit/0.2 (GitHub: wsgtcyx/ptcgp-species-radar; noncommercial public research)"
headers={"User-Agent":user_agent,"Accept":"application/json"}
kw=re.compile(r"\b(deck|decks|decklist|list|build|building|meta|ranked|matches|winrate|battle|battles|attack|energy|supporter|fossil|evolution|combo|partner|synergy|counter|card|retreat|setup|d[eé]ck)\b|ポケポケ|デッキ|構築|相方", re.I)
high=re.compile(r"\b(deck|decks|decklist|build|building|meta|ranked|winrate|combo|partner|synergy|counter|energy|attack)\b|デッキ|構築",re.I)
failures=[]
queries=[]
raw=[]
seen=set()
def read_json(url):
    time.sleep(0.85)
    try:
        req=urllib.request.Request(url,headers=headers)
        with urllib.request.urlopen(req,timeout=18) as r:
            body=r.read(2000000)
            return json.loads(body)
    except urllib.error.HTTPError as e:
        failures.append({"url":url,"status":e.code,"error":str(e)[:200]})
    except Exception as e:
        failures.append({"url":url,"error":type(e).__name__+":"+str(e)[:200]})
    return None
def add(data,sub,kind,root):
    if not isinstance(data,dict):return
    author=str(data.get("author") or "")
    created=data.get("created_utc")
    if not isinstance(created,(int,float)):return
    when=dt.datetime.fromtimestamp(created,UTC)
    if not (cutoff<=when<=now):return
    if not author or author in ("[deleted]","AutoModerator"):return
    ident=data.get("name") or ("t1_"+data.get("id",""))
    if ident in seen:return
    seen.add(ident)
    body=" ".join(x for x in (data.get("title",""),data.get("selftext",""),data.get("body","")) if isinstance(x,str))
    path=data.get("permalink") or ("/r/"+sub+"/comments/"+root+"/comment/"+str(data.get("id",""))+"/")
    url="https://www.reddit.com"+path if path.startswith("/") else path
    raw.append({"fullname":ident,"kind":kind,"url":url,"subreddit":sub,"author":author,
                "created_utc":created,"published_at_utc":when.isoformat(),
                "parent_thread_id":root,"body_excerpt":body[:1600],
                "pocket_context":True,
                "deck_intent_prefilter":bool(high.search(body)),
                "broad_topic_prefilter":bool(kw.search(body)),
                "verification":"reddit_public_json_data_unreviewed_heuristic"})
def children_from(tree,sub,root):
    if not isinstance(tree,dict):return
    for node in tree.get("data",{}).get("children",[]):
        if node.get("kind")=="t1":
            d=node.get("data",{})
            add(d,sub,"comment",root)
            replies=d.get("replies")
            if isinstance(replies,dict):children_from(replies,sub,root)
# Limit calls for courtesy. Prioritize original deck discussions, then current event threads.
for sub in subs:
    after=None
    for page in range(3):
        url="https://www.reddit.com/r/"+sub+"/new.json?limit=100&raw_json=1"
        if after:url+="&after="+after
        queries.append(url)
        obj=read_json(url)
        if not obj:break
        data=obj.get("data",{})
        nodes=data.get("children",[])
        earliest=None
        for node in nodes:
            if node.get("kind")!="t3":continue
            p=node.get("data",{})
            ts=p.get("created_utc")
            if isinstance(ts,(int,float)):
                earliest=ts if earliest is None else min(earliest,ts)
            add(p,sub,"post",p.get("id",""))
        after=data.get("after")
        if not after or (earliest and earliest<cutoff.timestamp()):break

posts=[r for r in raw if r["kind"]=="post"]
# No other subreddits or non-Pocket TCG data; topics selected from these communities only.
posts.sort(key=lambda r:(not r["broad_topic_prefilter"],-r["created_utc"]))
for p in posts[:110]:
    sub=p["subreddit"]; root=p["parent_thread_id"]
    url=f"https://www.reddit.com/r/{sub}/comments/{root}/.json?limit=500&raw_json=1"
    queries.append(url)
    obj=read_json(url)
    if isinstance(obj,list) and len(obj)>1:
        children_from(obj[1],sub,root)
    if len([x for x in raw if x["deck_intent_prefilter"]])>=250:break

interesting=[r for r in raw if r["deck_intent_prefilter"]]
by_thread=Counter(r["parent_thread_id"] for r in interesting)
out={"schema_version":1,"cutoff_at":now.isoformat(),"window_start":cutoff.isoformat(),
     "source":"Reddit public JSON (not a human-validated deck-intent assessment)",
     "quality_gate":"not_assessed","candidate_prefilter_count":len(interesting),
     "fetched_post_count":len(posts),"fetched_comment_count":len(raw)-len(posts),
     "unique_prefilter_parent_threads":len(by_thread),
     "unique_prefilter_authors":len({r["author"] for r in interesting}),
     "eligible_100_verified":None,
     "queries":queries,"failures":failures,"prefilter_sources":interesting,
     "raw_source_count":len(raw)}
p=pathlib.Path("evidence")
p.mkdir(exist_ok=True)
file=p/("reddit-public-raw-"+now.strftime("%Y-%m-%dT%H%M%SZ")+".json")
file.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"file":str(file),"fetched":len(raw),"prefilter":len(interesting),"parents":len(by_thread),"failures":failures[:8]},ensure_ascii=False))
