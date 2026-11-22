#!/usr/bin/env python3
import json, pathlib, urllib.request, urllib.parse, urllib.error, datetime as dt, re, io, base64, hashlib, time
from PIL import Image
base="evidence/2026-11-22-160310-iteration3-live-probe.json"
existing=json.loads(pathlib.Path(base).read_text(encoding="utf-8"))
bsky=existing["bsky_records"]
targets=["rat3ded.bsky.social","fictionlife06.bsky.social","grayhair-wolf.bsky.social"]
selected=[]
for name in targets:
 arr=[p for p in bsky if p["author"]==name and (p.get("images") or []) and (p.get("is_deck_text") or name=="rat3ded.bsky.social")]
 selected+=arr[:2]
images=[];requests=[]
for p in selected:
 im=p["images"][0];url=im.get("fullsize")
 if not url:continue
 item=dict(post_url=p["canonical_url"],image_url=url,post_created_at=p["created_utc"],label=p["author"],image_alt=im.get("alt"),status=None,error=None)
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"PTCGPSpeciesRadar/1.0"})
  with urllib.request.urlopen(req,timeout=13) as r:
   item["status"]=r.status
   by=r.read(2200000)
  pic=Image.open(io.BytesIO(by)).convert("RGB");item["original_size"]=list(pic.size)
  pic.thumbnail((1150,1150),Image.Resampling.LANCZOS)
  out=io.BytesIO();pic.save(out,format="JPEG",quality=77,optimize=True)
  enc=out.getvalue()
  item["resized_size"]=list(pic.size);item["bytes"]=len(enc)
  item["sha256"]=hashlib.sha256(enc).hexdigest()
  item["b64_jpeg"]=base64.b64encode(enc).decode()
 except Exception as e:item["error"]=str(e)[:180]
 images.append(item)
 time.sleep(.4)
# Separate missing 1st-party actor feeds not contained in prior run.
more=[]
end=dt.datetime.fromisoformat("2026-11-22T16:03:10+08:00");start=end-dt.timedelta(hours=72)
actors=["sigure0809.bsky.social","azukey-game.bsky.social","lanzervyn.bsky.social","tornado9797.bsky.social","arcsdad.bsky.social","skylerpfury.bsky.social","the-pale-gurl.bsky.social","kaqpu.bsky.social","maruboshi-game.bsky.social"]
for actor in actors:
 u="https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?"+urllib.parse.urlencode({"actor":actor,"limit":65,"filter":"posts_with_replies"})
 rec={"actor":actor,"http":None,"error":None,"items":None}
 try:
  req=urllib.request.Request(u,headers={"User-Agent":"PTCGPSpeciesRadar/1.0"})
  with urllib.request.urlopen(req,timeout=13) as r:rec["http"]=r.status;j=json.load(r)
  rec["items"]=len(j.get("feed",[]))
  for x in j.get("feed",[]):
   p=x.get("post") or {};v=p.get("record") or {};a=p.get("author") or {}
   if x.get("reason") or not a.get("did") or not p.get("uri","").startswith("at://"):continue
   when=dt.datetime.fromisoformat(v["createdAt"].replace("Z","+00:00"))
   if not start<=when<=end:continue
   text=v.get("text","")
   if not re.search(r"ポケポケ|PTCGP|TCGPocket|PokemonTCGPocket|デッキ|構築|対戦",text,re.I):continue
   uri=p["uri"]
   more.append({"platform":"bluesky","source_id":uri,"parent_thread_id":(v.get("reply") or {}).get("root",{}).get("uri",uri),
     "kind":"reply" if v.get("reply") else "post","author":a.get("handle"),"author_did":a.get("did"),"created_utc":v["createdAt"],
     "published_at_bjt":when.astimezone(end.tzinfo).isoformat(),"text":text[:2000],
     "canonical_url":"https://bsky.app/profile/"+a.get("handle","")+"/post/"+uri.rsplit("/",1)[-1],
     "images":[{"alt":q.get("alt"),"fullsize":q.get("fullsize")} for q in (p.get("embed") or {}).get("images",[])][:4],
     "verification_method":"official_public_getAuthorFeed","directly_opened":True})
 except Exception as e:rec["error"]=str(e)[:180]
 requests.append(rec);time.sleep(.45)
path=pathlib.Path("evidence/2026-11-22-160310-iteration3-media-probe.json")
path.write_text(json.dumps({"run_id":existing["run_id"],"iteration":3,"generated_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
"image_original_first_party":images,"additional_actor_scans":requests,"additional_originals":more,
"note":"Original images included resized for manual human inspection. No automatic deck eligibility claims."},ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"path":str(path),"image_count":len(images),"images_http":[x.get("status") for x in images],"image_bytes":[x.get("bytes") for x in images],"additional_sources":len(more),"actors":len(requests)},ensure_ascii=False))
