#!/usr/bin/env python3
import json,io,datetime as dt,base64,urllib.request,urllib.parse,hashlib,pathlib
from PIL import Image
b=json.loads(pathlib.Path("evidence/2026-11-22-160310-iteration3-live-probe.json").read_text(encoding="utf8"))
targets=[]
p=next((p for p in b["bsky_records"] if p["canonical_url"]=="https://bsky.app/profile/fictionlife06.bsky.social/post/3n2tt2z6glc2f"),None)
if p:targets.append({"post":p,"url":p["images"][0]["fullsize"],"note":"Alolan Exeggutor Mega Venusaur match results"})
sig="at://did:plc:7a2f4k4fzgl7es36p5izwos5/app.bsky.feed.post/3n2s6uzoyck27"
# Get the post by public handle, not by speculative DID.
url="https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=sigure0809.bsky.social&limit=100&filter=posts_with_replies"
req=urllib.request.Request(url,headers={"User-Agent":"PTCGPSpeciesRadar/1.0"})
with urllib.request.urlopen(req,timeout=14) as res:j=json.load(res)
for row in j.get("feed",[]):
 q=row.get("post") or {}
 if q.get("uri","").endswith("/3n2s6uzoyck27"):
  im=(q.get("embed") or {}).get("images") or []
  if im:
   targets.append({"post":{"canonical_url":"https://bsky.app/profile/sigure0809.bsky.social/post/3n2s6uzoyck27","created_utc":(q.get("record") or {}).get("createdAt"),"author":(q.get("author") or {}).get("handle")},"url":im[0]["fullsize"],"note":"Sigure original match screenshot"})
  break
out=[]
for t in targets:
 z={k:v for k,v in t.items() if k!="post"}
 z.update({"post_url":t["post"]["canonical_url"],"created_utc":t["post"]["created_utc"],"author":t["post"]["author"]})
 try:
  with urllib.request.urlopen(urllib.request.Request(t["url"],headers={"User-Agent":"PTCGPSpeciesRadar/1.0"}),timeout=13) as res:
   z["http_status"]=res.status;raw=res.read(2300000)
  im=Image.open(io.BytesIO(raw)).convert("RGB")
  z["original_size"]=list(im.size);im.thumbnail((1150,1150),Image.Resampling.LANCZOS)
  buffer=io.BytesIO();im.save(buffer,format="JPEG",quality=79,optimize=True)
  z["preview_size"]=list(im.size);z["sha256"]=hashlib.sha256(buffer.getvalue()).hexdigest();z["b64_jpeg"]=base64.b64encode(buffer.getvalue()).decode()
 except Exception as e:z["error"]=str(e)[:180]
 out.append(z)
path=pathlib.Path("evidence/2026-11-22-160310-iteration3-extra-images.json")
path.write_text(json.dumps({"run_id":b["run_id"],"iteration":3,"images":out,"note":"First-party fullsize images resized for manual inspection; not automatic eligibility."},ensure_ascii=False,indent=2)+"\n")
print(json.dumps([{"post":x["post_url"],"http":x.get("http_status"),"bytes":len(x.get("b64_jpeg","")),"error":x.get("error")} for x in out]))
