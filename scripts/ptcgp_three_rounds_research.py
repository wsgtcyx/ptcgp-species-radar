#!/usr/bin/env python3
"""Independent bounded first-party evidence probes for three sequential study loops.
Never asserts a strict-eligible source on keyword matching; a human audit must adjudicate originals.
"""
import datetime as dt, json, re, time, urllib.parse, urllib.request, urllib.error, html, pathlib, xml.etree.ElementTree as ET
from html.parser import HTMLParser
UTC=dt.timezone.utc
BJT=dt.timezone(dt.timedelta(hours=8))
ROOT=pathlib.Path("evidence")
ROOT.mkdir(exist_ok=True)
SEEDS={"fictionlife06.bsky.social","rat3ded.bsky.social","sigure0809.bsky.social","yusrikhairi765.bsky.social","snli.bsky.social"}
def now():return dt.datetime.now(UTC)
def bjt(t):return t.astimezone(BJT).isoformat()
def parse(t):
 try:return dt.datetime.fromisoformat(t.replace("Z","+00:00"))
 except:return None
def get(url,tag,out,cap=500000):
 record={"url":url,"tag":tag,"at":now().isoformat(),"status":None,"size":None,"error":None}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; PTCGP-Species-Radar/1.1; original-research)","Accept":"application/json,text/html,application/xml,*/*"})
  with urllib.request.urlopen(req,timeout=14) as resp:
   record.update({"status":resp.status,"size":int(resp.headers.get("Content-Length") or 0),"final_url":resp.geturl(),"content_type":resp.headers.get("Content-Type")})
   raw=resp.read(cap).decode("utf-8","replace")
 except urllib.error.HTTPError as e:record["status"]=e.code;record["error"]=str(e)[:120];raw=""
 except Exception as e:record["error"]=str(e)[:120];raw=""
 out["http_attempts"].append(record)
 return raw
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.text=[];self.links=[];self.times=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=="a" and d.get("href"):self.links.append(d["href"])
  if tag=="time" and d.get("datetime"):self.times.append(d["datetime"])
 def handle_data(self,data):
  data=data.strip()
  if data:self.text.append(data)
def unique(records):
 ans=[];seen=set()
 for x in records:
  id=x.get("source_id") or x.get("url")
  if id and id not in seen:seen.add(id);ans.append(x)
 return ans
def init(round_num):
 cutoff=now().astimezone(BJT);start=cutoff-dt.timedelta(hours=72)
 rid=cutoff.strftime("%Y-%m-%d-%H%M%S")+f"-iteration{round_num}"
 return {"run_id":rid,"iteration":round_num,"window":{"start":start.isoformat(),"end":cutoff.isoformat(),"hours":72},"created_at":now().isoformat(),"raw_posts":[],"http_attempts":[],"site":[],"rss":[],"pocketmads":[],"discovery":[],"notes":["PROBE ONLY; no keyword hit auto-counted as original verified deck building","Prior records used as discovery seeds only; re-read all originals inside this run","RSS title only not sufficient; original video description requires substantive content and human review"]}
def seeds_from_previous():
 seeds=set(SEEDS)
 p=pathlib.Path("evidence/2026-11-22-160310-iteration3.json")
 if p.exists():
  try:
   d=json.loads(p.read_text())
   for r in d.get("records",[]):
    a=r.get("author")
    if a and isinstance(a,str) and "." in a and ("bsky" in a or r.get("platform")=="bluesky"):seeds.add(a)
  except:pass
 return seeds
def discover_bluenews(out):
 handles=set()
 for url in ["https://www.bluenews.app/hashtag/ptcgp?tab=latest","https://www.bluenews.app/hashtag/%E3%83%9D%E3%82%B1%E3%83%9D%E3%82%B1?tab=latest","https://www.bluenews.app/hashtag/pokemontcgpocket?tab=latest"]:
  raw=get(url,"discovery_bluenews",out,280000)
  matches=re.findall(r'([a-zA-Z0-9][a-zA-Z0-9.-]{2,80}\.bsky\.social)',raw)
  handles.update(matches)
  out["discovery"].append({"url":url,"found_handles":len(set(matches)),"not_qualified_source":True})
 return handles
def collect_bsky(out,handles,limit=55,reply_depth=1):
 start=parse(out["window"]["start"]);end=parse(out["window"]["end"])
 candidate_threads=[]
 for a in sorted(handles)[:limit]:
  raw=get("https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?"+urllib.parse.urlencode({"actor":a,"limit":80}),"bsky_author_feed:"+a,out,420000)
  try:items=json.loads(raw).get("feed",[])
  except:continue
  for it in items:
   p=it.get("post") or {};rec=p.get("record") or {};date=parse(rec.get("createdAt",""))
   author=(p.get("author") or {}).get("handle")
   if not date or not(start<=date<=end) or author!=a:continue
   if it.get("reason"):continue
   txt=str(rec.get("text",""))
   if not re.search(r'ポケポケ|pokemon.?tcg.?pocket|#ptcgp|#tcgpocket|TCGPocket|Pocket.*(?:deck|battle)|デッキ|構築|対戦|ランクマ|(?:ranked|decklist|deck)[^a-z]',txt,re.I):continue
   uri=p.get("uri","");rkey=uri.rsplit("/",1)[-1]
   x={"platform":"bluesky","source_id":uri,"url":f"https://bsky.app/profile/{a}/post/{rkey}","kind":"comment" if rec.get("reply") else "post","author":a,"author_did":(p.get("author") or {}).get("did"),"published_utc":rec.get("createdAt"),"published_bjt":bjt(date),"root_uri":(((rec.get("reply") or {}).get("root") or {}).get("uri") or uri),"text":txt[:3500],"embed_alt":[im.get("alt","")[:700] for im in ((p.get("embed") or {}).get("images") or [])][:3],"original_author_feed":True,"origin_verified":False,"eligible":False,"exclusion_reason":"pending_human_substantive_deck_and_originality_review"}
   out["raw_posts"].append(x)
   if re.search(r'デッキ|構築|対戦|ランクマ|deck|ranked|勝率|戦績|勝ち|energy|match|win',txt,re.I):candidate_threads.append(uri)
  time.sleep(.13)
 # Individually open likely top-level posts and limited reply threads; original URI and author verified again
 for uri in list(dict.fromkeys(candidate_threads))[:65]:
  raw=get("https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?"+urllib.parse.urlencode({"uri":uri,"depth":reply_depth}),"bsky_getPostThread",out,450000)
  try:th=json.loads(raw).get("thread") or {}
  except:continue
  def walk(node,level=0):
   p=node.get("post") or {};rec=p.get("record") or {};posturi=p.get("uri");t=parse(rec.get("createdAt",""))
   if posturi and t and start<=t<=end and isinstance(rec.get("text"),str):
    x={"platform":"bluesky","source_id":posturi,"url":"https://bsky.app/profile/"+(p.get("author",{}).get("handle") or p.get("author",{}).get("did") or "unknown")+"/post/"+posturi.rsplit("/",1)[-1],
    "kind":"comment" if rec.get("reply") else "post","author":p.get("author",{}).get("handle"),"author_did":p.get("author",{}).get("did"),
    "published_utc":rec.get("createdAt"),"published_bjt":bjt(t),"root_uri":(((rec.get("reply") or {}).get("root") or {}).get("uri") or posturi),
    "text":rec.get("text","")[:4500],"embed_alt":[im.get("alt","")[:700] for im in ((p.get("embed") or {}).get("images") or [])][:3],
    "direct_original_http":True,"origin_verified":True,"eligible":False,"exclusion_reason":"pending_human_substantive_deck_and_originality_review"}
    out["raw_posts"].append(x)
   if level<reply_depth:
    for q in node.get("replies",[])[:30]:
     if isinstance(q,dict):walk(q,level+1)
  if th:walk(th)
  time.sleep(.14)
 out["raw_posts"]=unique(sorted(out["raw_posts"],key=lambda x: (not x.get("origin_verified",False),x["source_id"])))
def collect_pocket(out):
 raw=get("https://app.pocketmads.com/feed","pocketmads_feed",out,350000)
 ids=list(dict.fromkeys(re.findall(r'/feed/([a-f0-9]{8}-(?:[a-f0-9]{4}-){3}[a-f0-9]{12})',raw,re.I)))
 ids=["c0575dfc-71e3-41bb-89f4-14eefdc0bc7e"]+[i for i in ids if i!="c0575dfc-71e3-41bb-89f4-14eefdc0bc7e"]
 for id in ids[:15]:
  url="https://app.pocketmads.com/feed/"+id
  page=get(url,"pocketmads_original:"+id,out,200000)
  p=Parser()
  if page:p.feed(page)
  date=parse(p.times[0]) if p.times else None
  out["pocketmads"].append({"source_id":"pocketmads:"+id,"url":url,"original_published_utc":p.times[0] if p.times else None,"within_window":bool(date and parse(out["window"]["start"])<=date<=parse(out["window"]["end"])),"html_datetime_present":bool(p.times),"original_text":" ".join(p.text)[:4500] if p.times else None,"original_read":bool(page and p.times),"eligible":False,"reason":"pending_human_deck_review"})
  time.sleep(.12)
def collect_rss(out):
 ids=["UC_SI1j1d8vJo_rYMV5o_dRg","UCsf22ppLrgqdNoek8wc3y5A","UCq0VWPCoiu3ynVRQCgyhF6g","UCg-0sgAgnDDvEZIjL6qOvcA","UC8G8act2Xl_8bcRghswIY5A"]
 ns={"a":"http://www.w3.org/2005/Atom","yt":"http://www.youtube.com/xml/schemas/2015","m":"http://search.yahoo.com/mrss/"}
 for ch in ids:
  raw=get("https://www.youtube.com/feeds/videos.xml?channel_id="+ch,"youtube_official_creator_rss",out,160000)
  try:root=ET.fromstring(raw)
  except:continue
  channel=root.findtext("a:title",default=None,namespaces=ns)
  for entry in root.findall("a:entry",ns):
   s=entry.findtext("a:published",default="",namespaces=ns);date=parse(s)
   if not date or not parse(out["window"]["start"])<=date<=parse(out["window"]["end"]):continue
   vid=entry.findtext("yt:videoId",namespaces=ns)
   title=entry.findtext("a:title",default="",namespaces=ns)
   desc=entry.findtext(".//m:description",default="",namespaces=ns)
   out["rss"].append({"platform":"youtube","source_id":vid,"url":"https://www.youtube.com/watch?v="+str(vid),"author":channel,"channel_id":ch,"original_published_utc":s,"published_at_bjt":bjt(date),"title":title,"first_party_author_description":desc[:5500],"description_text_readable":bool(desc),"eligible":False,"reason":"requires_original_deck_content_review; RSS title alone never sufficient"})
  time.sleep(.15)
def collect_site(out):
 for name,url in [("popular_1","https://www.pokemontcgpocket.app/en/deck/pokemon"),("popular_2","https://www.pokemontcgpocket.app/en/deck/pokemon?page=2"),("name_1","https://www.pokemontcgpocket.app/en/deck/pokemon?sort=name"),("name_2","https://www.pokemontcgpocket.app/en/deck/pokemon?page=2&sort=name")]:
  raw=get(url,"species_directory:"+name,out,320000)
  p=Parser()
  if raw:p.feed(raw)
  out["site"].append({"name":name,"url":url,"html_present":bool(raw),"page_markers":re.findall(r'Page\s+\d+\s+of\s+\d+',raw)[:3],"unique_species_link_urls":sorted(set(x for x in p.links if "/en/deck/pokemon/" in x))[:75],"visible_count":len(set(x for x in p.links if "/en/deck/pokemon/" in x))})
  time.sleep(.1)
def collect_reddit_once(out):
 for sub in ["PTCGP","PokemonPocket","PokemonTCGP"]:
  get("https://www.reddit.com/r/"+sub+"/new/","reddit_public_new:"+sub,out,120000)
def run(num):
 out=init(num)
 handles=seeds_from_previous()
 handles.update(discover_bluenews(out))
 # 4: baseline; 5: more authors; 6: deeper replies + broader author coverage
 collect_bsky(out,handles,limit={4:35,5:55,6:75}[num],reply_depth=2 if num==6 else 1)
 collect_pocket(out)
 collect_rss(out)
 collect_site(out)
 collect_reddit_once(out)
 out["completed_at"]=now().isoformat()
 out["funnel"]={"seed_handles":len(handles),"bluesky_originals_review_queue":len(out["raw_posts"]),"bluesky_direct_originals":sum(bool(x.get("origin_verified")) for x in out["raw_posts"]),"pocketmads_originals_opened":sum(bool(x.get("original_read")) for x in out["pocketmads"]),"rss_video_descriptions":sum(bool(x.get("description_text_readable")) for x in out["rss"]),"strict_eligible_count":None,"note":"All preliminary; strict eligibility requires original-content assessment and evidence metadata verification."}
 path=ROOT/(out["run_id"]+"-probe.json")
 path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("PROBE_SUMMARY",json.dumps({"run_id":out["run_id"],"iteration":num,"path":str(path),"funnel":out["funnel"],"requests":len(out["http_attempts"]),"failed_http":sum(x["status"]!=200 for x in out["http_attempts"])},ensure_ascii=False),flush=True)
 return path
if __name__=="__main__":
 for r in [4,5,6]:
  run(r)
  time.sleep(.5)
