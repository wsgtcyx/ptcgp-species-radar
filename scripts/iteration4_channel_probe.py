#!/usr/bin/env python3
"""Iteration 4: bounded first-party creator/channel verification, no synthetic eligibility."""
import datetime as dt, hashlib, html, json, pathlib, re, time, urllib.parse, urllib.request, urllib.error, xml.etree.ElementTree as ET
END=dt.datetime.fromisoformat("2026-11-22T16:15:36+08:00")
START=END-dt.timedelta(hours=72)
RUN="2026-11-22-161536-iteration4"
UTC=dt.timezone.utc
AUDIT={"run_id":RUN,"iteration":4,"cutoff":END.isoformat(),"start":START.isoformat(),"probe_started_utc":dt.datetime.now(UTC).isoformat(),"attempts":[],"youtube":[],"site":[],"pocketmads":[],"bluesky":[],"method":"GitHub Actions first-party public HTTP only; no auth, no redirects to alternative hosts, no bypass"}
def pull(url,tag,limit=500000):
 log={"tag":tag,"url":url,"at_utc":dt.datetime.now(UTC).isoformat(),"http_status":None,"error":None,"content_type":None,"bytes":None}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; PTCGPSpeciesRadar/1.0; github.com/wsgtcyx/ptcgp-species-radar)","Accept":"text/html,application/atom+xml,application/json,*/*;q=0.5"})
  with urllib.request.urlopen(req,timeout=13) as res:
   log["http_status"]=res.status
   log["content_type"]=res.headers.get("Content-Type")
   b=res.read(limit)
   log["bytes"]=len(b)
   log["final_url"]=res.geturl()
   out=b.decode("utf-8","replace")
 except urllib.error.HTTPError as e:
  log["http_status"]=e.code;log["error"]="HTTPError:"+str(e)[:150];out=""
 except Exception as e:
  log["error"]=str(e)[:180];out=""
 AUDIT["attempts"].append(log)
 return out,log
def parse_datetime(s):
 try:return dt.datetime.fromisoformat(s.replace("Z","+00:00"))
 except:return None
# Discovery videos are different creator channels. Third-party index text is discovery, never a qualified original.
videos=[
 ("ポメ生徒会長","oLmPhWeEsrk","Blastoise deck"),
 ("Sifu","9fuDpFi8Vlw","Dual Fusion meta decks"),
 ("unknown","DpVJOft6VnM","previous seed"),
 ("unknown","5nSJ5UN37kA","previous seed"),
 ("unknown","r-ynWsRXZuQ","previous seed"),
 ("unknown","8cBRc6u4-gs","previous seed"),
 ("unknown","IBI1cXo_C14","previous seed"),
 ("unknown","F9eaA1ff4iM","previous seed")
]
channels=set()
for label,vid,context in videos:
 url="https://www.youtube.com/watch?v="+vid
 raw,log=pull(url,"youtube_watch:"+vid,350000)
 channel_candidates=re.findall(r'"(?:channelId|externalId|browseId|externalChannelId)"\s*:\s*"(UC[\w-]{22})"',raw)
 title=re.search(r'<title>(.*?)</title>',raw,re.S)
 description=re.search(r'<meta\s+name="description"\s+content="([^"]+)',raw,re.I)
 first_desc=description.group(1) if description else None
 video={"video_id":vid,"creator_label_from_discovery":label,"context_from_discovery":context,
 "watch_status":log["http_status"],"watch_bytes":log["bytes"],"watch_title":html.unescape(title.group(1))[:240] if title else None,
 "first_party_description":html.unescape(first_desc)[:1500] if first_desc else None,
 "channel_id_found_in_watch":channel_candidates[0] if channel_candidates else None,
 "watch_has_video_identifiers":bool(re.search(r'ytInitialPlayerResponse|ytInitialData|videoDetails|og:video',raw)),
 "youtube_first_party_content_verified":False,
 "reason":"Title or generic watch shell alone does not verify gameplay or a deck"}
 if channel_candidates:channels.add(channel_candidates[0])
 if not channel_candidates:
  oembed,ol=pull("https://www.youtube.com/oembed?"+urllib.parse.urlencode({"url":url,"format":"json"}),"youtube_oembed:"+vid,50000)
  if oembed:
   try:
    o=json.loads(oembed)
    video["first_party_oembed_author_name"]=o.get("author_name")
    video["first_party_oembed_author_url"]=o.get("author_url")
    author_url=o.get("author_url","")
    if re.search(r'/channel/(UC[\w-]{22})',author_url):
     ch=re.search(r'/channel/(UC[\w-]{22})',author_url).group(1)
     video["channel_id_from_oembed"]=ch;channels.add(ch)
   except Exception as e:video["oembed_parse_error"]=str(e)[:120]
 AUDIT["youtube"].append(video)
 time.sleep(0.30)
# Known official channel validates whether RSS is transport-readable but is NOT a deck source.
channels.add("UC_SI1j1d8vJo_rYMV5o_dRg")
rss=[]
for ch in sorted(channels)[:12]:
 url="https://www.youtube.com/feeds/videos.xml?channel_id="+ch
 raw,m=pull(url,"youtube_official_rss:"+ch,300000)
 item={"channel_id":ch,"http_status":m["http_status"],"content_type":m["content_type"],"readable_xml":False,"entries":[]}
 if raw:
  try:
   root=ET.fromstring(raw)
   item["readable_xml"]=True
   NS={"a":"http://www.w3.org/2005/Atom","yt":"http://www.youtube.com/xml/schemas/2015","media":"http://search.yahoo.com/mrss/"}
   item["channel_name"]=root.findtext("a:title",default=None,namespaces=NS)
   for ent in root.findall("a:entry",NS)[:15]:
    desc=ent.findtext(".//media:description",default="",namespaces=NS)
    published=ent.findtext("a:published",default=None,namespaces=NS)
    channel=ent.findtext("yt:channelId",default=None,namespaces=NS)
    id=ent.findtext("yt:videoId",default=None,namespaces=NS)
    item["entries"].append({"video_id":id,"channel_id":channel,"published":published,"within_window":bool(parse_datetime(published) and START<=parse_datetime(published)<=END),"title":ent.findtext("a:title",default=None,namespaces=NS),"media_description":desc[:2700] if desc else None,"description_explicit_author_deck_explanation":False,"eligible":False})
  except Exception as e:item["parse_error"]=str(e)[:150]
 rss.append(item)
 time.sleep(0.3)
AUDIT["youtube_rss"]=rss
# First party site: both filters, both actual pages; record status / last page and exact names in source text.
from html.parser import HTMLParser
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.times=[];self.text=[];self.in_time=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=="a":self.links.append((d.get("href"),""))
  if tag=="time":self.times.append(d.get("datetime"))
 def handle_data(self,v):
  v=v.strip()
  if v:self.text.append(v)
for sort,url in [
 ("popular_page1","https://www.pokemontcgpocket.app/en/deck/pokemon"),
 ("popular_page2","https://www.pokemontcgpocket.app/en/deck/pokemon?page=2"),
 ("name_page1","https://www.pokemontcgpocket.app/en/deck/pokemon?sort=name"),
 ("name_page2","https://www.pokemontcgpocket.app/en/deck/pokemon?sort=name&page=2")]:
 raw,m=pull(url,"site_directory:"+sort,280000)
 p=Page()
 if raw:p.feed(raw)
 AUDIT["site"].append({"sort":sort,"url":url,"status":m["http_status"],"final_url":m.get("final_url"),"page_indicator":re.findall(r'Page\s+\d+\s+of\s+\d+',raw)[:4],"pokemon_links":list(dict.fromkeys([href for href,_ in p.links if href and re.search(r'/en/deck/pokemon/',href)]))[:65],"visible_labels":p.text[50:160] if raw else []})
 time.sleep(0.2)
# Exact site strategy URLs, excluding generic hubs. Capture source identity and card labels, not visibility in browse directory.
for species,variant in [
 ("Chandelure","chandelure-b2-oricorio-b4"),
 ("Paldean Clodsire","paldean-clodsire-c1"),
 ("Malamar","malamar-b3-mega-sableye-ex-b3b"),
 ("Blastoise","blastoise-c1-araquanid-b4"),
 ("Alolan Exeggutor","alolan-exeggutor-ex-c1")]:
 url="https://www.pokemontcgpocket.app/en/deck/"+variant
 raw,m=pull(url,"site_strategy:"+species,270000)
 title=re.search(r'<title>(.*?)</title>',raw,re.S)
 AUDIT.setdefault("existing_strategies",[]).append({"species":species,"variant_slug":variant,"url":url,"http_status":m["http_status"],"title":html.unescape(title.group(1))[:150] if title else None,"card_number_mentions":list(dict.fromkeys(re.findall(r"\b[A-C]\d+[a-z]?(?:-[0-9]{3})\b",raw,re.I)))[:40]})
 time.sleep(0.2)
# Community player-created public immutable posts, never /api.
for slug in ["c0575dfc-71e3-41bb-89f4-14eefdc0bc7e","e7d762fe-fd5e-4c5d-862a-d155ea32275b"]:
 url="https://app.pocketmads.com/feed/"+slug
 raw,m=pull(url,"pocketmads_original:"+slug,250000)
 p=Page()
 if raw:p.feed(raw)
 AUDIT["pocketmads"].append({"source_id":slug,"url":url,"http_status":m["http_status"],"time_datetime":p.times[:5],"body_text":" ".join(p.text)[:4500],"first_party_readable":bool(raw and p.times)})
 time.sleep(.2)
# Reread four original Bluesky seeds, not automatic requalification. Check record.createdAt and content.
for handle,rkey in [("fictionlife06.bsky.social","3n2tt2z6glc2f"),("fictionlife06.bsky.social","3n2tt3bdmy22f"),("fictionlife06.bsky.social","3n2tsrz7jms2f"),("rat3ded.bsky.social","3n2tc5t6hps2o")]:
 resolve_url="https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?"+urllib.parse.urlencode({"handle":handle})
 raw,rm=pull(resolve_url,"bsky_resolve:"+handle,50000)
 did=None
 try:did=json.loads(raw).get("did")
 except:pass
 if not did:continue
 uri=f"at://{did}/app.bsky.feed.post/{rkey}"
 url="https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?"+urllib.parse.urlencode({"uri":uri,"depth":0})
 raw,m=pull(url,"bsky_original:"+rkey,250000)
 if raw:
  try:
   p=json.loads(raw).get("thread",{}).get("post",{})
   record=p.get("record",{}) or {}
   AUDIT["bluesky"].append({"uri":uri,"url":f"https://bsky.app/profile/{handle}/post/{rkey}","http_status":m["http_status"],"author":p.get("author",{}).get("handle"),"did":p.get("author",{}).get("did"),"created_at":record.get("createdAt"),"indexed_at":p.get("indexedAt"),"root_uri":record.get("reply",{}).get("root",{}).get("uri",uri),"body":record.get("text"),"images":p.get("embed",{}).get("images",[])[:2],"within_window":bool(parse_datetime(record.get("createdAt")) and START<=parse_datetime(record.get("createdAt"))<=END)})
  except Exception as e:AUDIT["bluesky"].append({"uri":uri,"error":str(e)[:100]})
 time.sleep(.2)
AUDIT["completed_at_utc"]=dt.datetime.now(UTC).isoformat()
out=pathlib.Path("evidence/2026-11-22-161536-iteration4-channel-probe.json")
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("PROBE_SUMMARY",json.dumps({"youtube_videos":len(AUDIT["youtube"]),"youtube_channels":len(channels),"rss_readable":sum(x["readable_xml"] for x in rss),"site_http":[(x["sort"],x["status"]) for x in AUDIT["site"]],"bsky_originals":len(AUDIT["bluesky"]),"pocketmads":len(AUDIT["pocketmads"]),"output":str(out)},ensure_ascii=False))
