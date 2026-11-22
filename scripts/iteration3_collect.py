#!/usr/bin/env python3
"""Iteration 3 public-source exploration: first-party post metadata, not automatic source certification."""
import json, re, time, urllib.request, urllib.error, urllib.parse, html, datetime as dt, pathlib, hashlib
RUN_ID="2026-11-22-160310-iteration3"
END=dt.datetime.fromisoformat("2026-11-22T16:03:10+08:00")
START=END-dt.timedelta(hours=72)
UTC=dt.timezone.utc
now=lambda: dt.datetime.now(UTC).isoformat()
audit=[]
seen=set()
posts=[]
discovery=[]
page_samples=[]
def fetch(url,label,max_bytes=850000):
 m=dict(label=label,url=url,at_utc=now(),status=None,error=None)
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"PTCGPSpeciesRadar/1.0 public-research contact github.com/wsgtcyx/ptcgp-species-radar","Accept":"application/json,text/html;q=0.9"})
  with urllib.request.urlopen(req,timeout=13) as r:
   m["status"]=r.status;m["content_type"]=r.headers.get("Content-Type")
   b=r.read(max_bytes);return b.decode("utf-8","replace"),m
 except urllib.error.HTTPError as e:
  m["status"]=e.code;m["error"]=str(e)[:160]
 except Exception as e:m["error"]=str(e)[:160]
 return None,m
def get(url,label):
 text,meta=fetch(url,label)
 audit.append(meta)
 return text,meta
def parse_time(t):
 try: return dt.datetime.fromisoformat(t.replace("Z","+00:00"))
 except: return None
PAT_GAME=re.compile("ポケポケ|PTCGP|TCGPocket|TCG Pocket|TCGポケット|Pok[eé]mon TCG Pocket|ポケモンカードアプリ|#PokemonTCGPocket|#pokemontcgp",re.I)
PAT_DECK=re.compile("デッキ|構築|対戦|デッキレシピ|ランクマ|組んで|使って|勝率|deck|decklist|ranked|match|combo|partner|synergy|energy|メタ|勝て|勝ち|戦績|限(?:定)?バトル|対人戦|使用率|20枚",re.I)
def collect(feed,origin):
 for x in feed:
  p=x.get("post",x) if isinstance(x,dict) else {}
  if x.get("reason") if isinstance(x,dict) else False:continue
  r=p.get("record") or {};a=p.get("author") or {};uri=p.get("uri") or ""
  if not uri.startswith("at://") or not a.get("did") or uri in seen:continue
  when=parse_time(r.get("createdAt",""))
  if when is None or not START<=when<=END:continue
  seen.add(uri)
  text=r.get("text","")
  if not PAT_GAME.search(text) and not PAT_DECK.search(text):continue
  images=[]
  embed=p.get("embed") or {}
  media=r.get("embed") or {}
  for im in (embed.get("images") or []):
   images.append({"alt":im.get("alt"),"fullsize":im.get("fullsize"),"thumb":im.get("thumb")})
  if not images:
   for im in (media.get("images") or []):
    images.append({"alt":im.get("alt"),"cid":(im.get("image") or {}).get("ref",{}).get("$link")})
  images=images[:5]
  parent=(r.get("reply") or {}).get("root",{}).get("uri",uri)
  posts.append({"platform":"bluesky","source_id":uri,"kind":"reply" if r.get("reply") else "post","parent_thread_id":parent,"canonical_url":"https://bsky.app/profile/"+a.get("handle","")+"/post/"+uri.rsplit("/",1)[-1],"author":a.get("handle"),"author_did":a.get("did"),"created_utc":r.get("createdAt"),"indexed_at":p.get("indexedAt"),"published_at_bjt":when.astimezone(END.tzinfo).isoformat(),"text":text[:2500],"images":images,"like_count":p.get("likeCount"),"reply_count":p.get("replyCount"),"verification_method":"first_party_public_bsky_getAuthorFeed_or_getPostThread","directly_opened":True,"collection_origin":origin,"is_pocket_text":bool(PAT_GAME.search(text)),"is_deck_text":bool(PAT_DECK.search(text)),"source_http_status":200,"eligible":None,"exclusion_reason":"requires_context_and_media_review"})
def actor_feed(actor,limit=65):
 url="https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?"+urllib.parse.urlencode({"actor":actor,"limit":limit,"filter":"posts_with_replies"})
 raw,meta=get(url,"bluesky_author_feed:"+actor)
 if raw:
  try:
   j=json.loads(raw)
   meta["raw_items"]=len(j.get("feed",[]));meta["cursor_present"]=bool(j.get("cursor"))
   collect(j.get("feed",[]),"getAuthorFeed:"+actor)
  except Exception as e:meta["parse_error"]=str(e)[:160]
 time.sleep(0.30)
def post_thread(uri):
 url="https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?"+urllib.parse.urlencode({"uri":uri,"depth":2,"parentHeight":0})
 raw,meta=get(url,"bluesky_thread:"+uri.rsplit("/",1)[-1])
 if raw:
  try:
   j=json.loads(raw)
   def rec(v,depth=0):
    if not isinstance(v,dict) or depth>3:return
    p=v.get("post") or {}
    if p:collect([p],"getPostThread:"+uri.rsplit("/",1)[-1])
    for y in (v.get("replies") or [])[:55]:rec(y,depth+1)
   rec(j.get("thread") or {})
  except Exception as e:meta["parse_error"]=str(e)[:160]
 time.sleep(0.30)
# Open discovery aggregator only to find handles; aggregator never counts as evidence.
for slug in ["ptcgp","%E3%83%9D%E3%82%B1%E3%83%9D%E3%82%B1","PokemonTCGPocket","TCGPocket"]:
 url="https://www.bluenews.app/hashtag/"+slug+"?tab=latest"
 raw,meta=get(url,"bluenews_discovery:"+slug)
 if raw:
  handles=list(dict.fromkeys(re.findall(r"@([a-z0-9_.-]+(?:\.bsky\.social|\.social\.ap\.brid\.gy))",raw,re.I)))
  meta["handles_found"]=handles[:65]
  discovery+=handles
 time.sleep(.30)
# New seed authors from discovery + previously found participants, not counted without fresh original.
seeds=["rat3ded.bsky.social","sigure0809.bsky.social","fictionlife06.bsky.social","azukey-game.bsky.social",
 "mrahmedgaming.bsky.social","tornado9797.bsky.social","yusrikhairi765.bsky.social","skybluesodapop.bsky.social",
 "jdogtoocool.bsky.social","arcsdad.bsky.social","vegestache.bsky.social","lanzervyn.bsky.social",
 "damagedqueen.satan.social","dexdrifter.bsky.social","doaroa570.bsky.social","nyahgust.bsky.social",
 "skylerpfury.bsky.social","tomjanacek.bsky.social","mikaiah.sakurajima.social.ap.brid.gy"]
actors=list(dict.fromkeys(discovery+seeds))[:36]
for a in actors:actor_feed(a)
# Direct first-party thread reads on potential original deck posts, including image-first originals.
thread_seeds=["at://did:plc:7ni2hyn3xwijwj4nnfedkkhn/app.bsky.feed.post/3n2tc5t6hps2o"]
for p in posts:
 if p["is_pocket_text"] and (p["is_deck_text"] or p.get("images")) and len(thread_seeds)<8:
  thread_seeds.append(p["source_id"])
for uri in list(dict.fromkeys(thread_seeds))[:8]:post_thread(uri)
# PocketMads public page only; explicitly do not access /api/
raw,meta=get("https://app.pocketmads.com/feed","pocketmads_feed")
if raw:
 import html.parser
 class P(html.parser.HTMLParser):
  def __init__(self):super().__init__();self.text=[];self.times=[];self.links=[]
  def handle_data(self,v):
   if v.strip():self.text.append(v.strip())
  def handle_starttag(self,tag,attrs):
   d=dict(attrs)
   if tag=="time":self.times.append(d.get("datetime"))
   if tag=="a" and d.get("href","").startswith("/feed/"):self.links.append(d["href"])
 p=P();p.feed(raw)
 meta["time_datetime"]=p.times[:30];meta["original_post_paths"]=list(dict.fromkeys(p.links))[:25]
 meta["visible_excerpt"]=" ".join(p.text)[:12000]
 for path in list(dict.fromkeys(p.links))[:5]:
  raw2,m=get("https://app.pocketmads.com"+path,"pocketmads_original:"+path.rsplit("/",1)[-1])
  if raw2:
   z=P();z.feed(raw2)
   m["time_datetime"]=z.times[:3];m["visible_text"]=" ".join(z.text)[:5500]
  time.sleep(.3)
# Site all+name exact paginated pages.
for url,label in [
 ("https://pokemontcgpocket.app/en/deck/pokemon","species_default_page1"),
 ("https://www.pokemontcgpocket.app/en/deck/pokemon?sort=name","species_name_page1"),
 ("https://www.pokemontcgpocket.app/en/deck/pokemon?sort=name&page=2","species_name_page2"),
 ("https://www.pokemontcgpocket.app/en/deck/pokemon?page=2","species_default_page2"),
 ("https://pokemontcgpocket.app/sitemap.xml","site_sitemap")]:
 raw,m=get(url,label)
 if raw:
  class P(__import__("html.parser",fromlist=["HTMLParser"]).HTMLParser):
   def __init__(self):super().__init__();self.text=[];self.links=[]
   def handle_data(self,v):
    if v.strip():self.text.append(v.strip())
   def handle_starttag(self,tag,attrs):
    d=dict(attrs)
    if tag=="a" and d.get("href"):self.links.append(d["href"])
  p=P();p.feed(raw)
  m["visible_text"]=(" ".join(p.text))[:18000]
  m["links"]=list(dict.fromkeys(p.links))[:120]
  m["returned_bytes"]=len(raw)
 time.sleep(.35)
# Reddit test only once per endpoint category; 403 -> no bypass
for url,label in [
 ("https://www.reddit.com/r/PTCGP/new.json?limit=25","reddit_public_new"),
 ("https://www.reddit.com/r/PokemonPocket/new.json?limit=25","reddit_public_new_2"),
 ("https://www.reddit.com/r/PokemonTCGP/new.json?limit=25","reddit_public_new_3")]:
 raw,m=get(url,label)
 if raw and m["status"]==200:
  try:
   j=json.loads(raw);m["raw_items"]=len(j.get("data",{}).get("children",[]))
  except:m["invalid_json"]=True
 time.sleep(.4)
post_count=len(posts)
result={"run_id":RUN_ID,"iteration":3,"fixed_window":{"start":START.isoformat(),"end":END.isoformat()},"generated_at_utc":now(),
"quality_gate":"unassessed_probe","http_requests":audit,
"scanned_unique_bluesky_actors":len(actors),"actors":actors,"bsky_posts_within_72h_matching_game_or_deck_text":post_count,
"bsky_records":posts,"declared_strict_eligible":0,
"note":"All bsky_records are first-party originals returned by getAuthorFeed/getPostThread, but require manual content and image validation; bluenews discovery is excluded. Media links are not viewed by this script, and images must not be claimed verified."}
path=pathlib.Path("evidence")/(RUN_ID+"-live-probe.json")
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"path":str(path),"actors":len(actors),"bsky_game_or_deck_text":post_count,
"by_label":[{"label":r["label"],"http":r["status"],"items":r.get("raw_items")} for r in audit],
"output_sha256":hashlib.sha256(path.read_bytes()).hexdigest()},ensure_ascii=False))
