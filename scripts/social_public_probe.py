#!/usr/bin/env python3
"""Low-volume, authorized/public-channel validation probe; NOT 100-source certification."""
import datetime as dt
import html
from html.parser import HTMLParser
import json, pathlib, re, urllib.request, urllib.error, urllib.parse, time

RUN_ID="2026-11-22-153002-iteration1"
END=dt.datetime.fromisoformat("2026-11-22T15:30:02+08:00")
START=END-dt.timedelta(hours=72)
UTC=dt.timezone.utc
records=[]
requests=[]
class Plain(HTMLParser):
 def __init__(self):
  super().__init__()
  self.text=[]
 def handle_data(self, d):
  if d.strip():self.text.append(d.strip())

def get(url, label):
 item={"label":label,"url":url,"fetched_at_utc":dt.datetime.now(UTC).isoformat(),"status":None,"error":None}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"PTCGPDeckRadarResearch/0.3 (public read audit; wsgtcyx/ptcgp-species-radar)","Accept":"application/json, text/html;q=0.8"})
  with urllib.request.urlopen(req,timeout=13) as res:
   item["status"]=res.status
   body=res.read(900000)
   item["content_type"]=res.headers.get("Content-Type")
   return body.decode("utf-8","replace"),item
 except urllib.error.HTTPError as e:
  item["status"]=e.code;item["error"]=str(e)[:180]
 except Exception as e:item["error"]=str(e)[:180]
 return None,item

for actor in ("rat3ded.bsky.social","sigure0809.bsky.social"):
 url="https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?"+urllib.parse.urlencode({"actor":actor,"limit":100,"filter":"posts_no_replies"})
 raw,meta=get(url,"bluesky_author_feed:"+actor)
 try:
  if raw:
   obj=json.loads(raw)
   posts=obj.get("feed",[])
   meta["returned_posts"]=len(posts);meta["cursor_present"]=bool(obj.get("cursor"))
   for f in posts:
    p=f.get("post",{});author=p.get("author",{});r=p.get("record",{})
    if f.get("reason") or not author.get("did") or not p.get("uri","").startswith("at://"):continue
    try:when=dt.datetime.fromisoformat(r.get("createdAt","").replace("Z","+00:00"))
    except ValueError:continue
    if not START<=when<=END:continue
    uri=p["uri"];rkey=uri.rsplit("/",1)[-1]
    text=r.get("text","")
    records.append({"platform":"bluesky","source_id":uri,"kind":"post","parent_thread_id":uri,
     "canonical_url":"https://bsky.app/profile/"+author.get("handle",actor)+"/post/"+rkey,
     "author":author.get("handle"),"author_did":author.get("did"),"created_at":r.get("createdAt"),
     "record_text":text[:1500],"has_embedded_media":bool(r.get("embed")),"source":"official_public_getAuthorFeed",
     "within_fixed_window":True,"pocket_deck_prefilter":bool(re.search(r"ポケポケ|#PTCGP|TCGPocket|TCG Pocket|ポケモンカードアプリ",text,re.I) and re.search(r"デッキ|構築|対戦|deck|match|energy|メタ|編成",text,re.I)),
     "human_verified_deck_intent":False})
 except Exception as e:meta["parse_error"]=str(e)[:180]
 requests.append(meta);time.sleep(0.7)

urls=[
 ("pocketmads_feed","https://app.pocketmads.com/feed"),
 ("pocketmads_original_deck","https://app.pocketmads.com/feed/c0575dfc-71e3-41bb-89f4-14eefdc0bc7e"),
 ("species_directory_page1","https://pokemontcgpocket.app/en/deck/pokemon"),
 ("species_directory_page2","https://www.pokemontcgpocket.app/en/deck/pokemon?page=2")
]
for label,url in urls:
 raw,meta=get(url,label)
 if raw:
  p=Plain()
  try:p.feed(raw);meta["visible_text_sample"]=" ".join(p.text)[:13500]
  except Exception as e:meta["parser_error"]=str(e)[:140]
  meta["html_time_tags"]=[html.unescape(x)[:350] for x in re.findall(r"<time\\b[^>]*>.*?</time>",raw,re.I|re.S)[:35]]
  meta["datetime_attributes"]=re.findall(r'datetime=["\\\']([^"\\\']+)',raw,re.I)[:35]
  meta["linked_paths"]=list(dict.fromkeys(re.findall(r'href=["\\\'](/(?:en/deck/pokemon|feed/)[^"\\\']*)',raw,re.I)))[:40]
 requests.append(meta);time.sleep(0.6)
result={"run_id":RUN_ID,"fixed_window":{"start":START.isoformat(),"end":END.isoformat()},"generated_at_utc":dt.datetime.now(UTC).isoformat(),"quality_gate":"unassessed_automatic_probe","http_requests":requests,"bluesky_window_posts":records,"automatically_qualified_sources":0,"note":"Requires original content and human review, official getAuthorFeed record timestamps are usable only when source is user-authored substantive Pocket deck content. HTML itself may not expose publication timestamp; reject incomplete rows."}
path=pathlib.Path("evidence")/(RUN_ID+"-live-probe.json")
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"output":str(path),"requests":[{"label":r["label"],"status":r["status"],"error":r["error"]} for r in requests],"window_posts":len(records)},ensure_ascii=False))
