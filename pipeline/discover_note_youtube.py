#!/usr/bin/env python3
"""Read-only PTCGP discovery (not a player-original classifier).
Usage:
  python ptcgp_public_jp_discovery.py --cutoff ISO8601 --note-tag ポケポケ --note-tag ポケポケデッキ --note-user HANDLE --youtube-channel-id UC... > discovery.json
Uses publicly supported creator RSS and public note.com tag/article paths only.
No login, API, retries, or automatic video-watch fallback. Feed article summaries are
not a substitute for reading the original; no entry is marked eligible automatically.
"""
import argparse
import datetime as dt
import email.utils
import html
import json
import re
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen
import xml.etree.ElementTree as ET

UTC=dt.timezone.utc
ATOM='{http://www.w3.org/2005/Atom}'
YT='{http://www.youtube.com/xml/schemas/2015}'
MRSS='{http://search.yahoo.com/mrss/}'
NOTE_LINK=re.compile(r'https://note\.com/[A-Za-z0-9_]+/n/n[a-z0-9]{8,15}$')
NOTE_PATH=re.compile(r'(/[A-Za-z0-9_]+/n/n[a-z0-9]{8,15})')
LD_JSON=re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',re.S|re.I)
args=None
blocked=set()

def datetime_offset(value):
    if not value:
        return None
    try:
        value=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:
        value=email.utils.parsedate_to_datetime(value)
    if value.utcoffset() is None:
        raise ValueError('Timestamp has no explicit UTC offset')
    return value.astimezone(UTC)

def get_public(url):
    host=url.split('/')[2]
    if host in blocked:
        raise RuntimeError('Skipped after origin HTTP 403 or 429; no retry in this scan')
    time.sleep(args.delay)
    try:
        with urlopen(url,timeout=args.timeout) as resp:
            return resp.read()
    except HTTPError as exc:
        if exc.code in (403,429):
            blocked.add(host)
        raise

def note_tag(tag):
    url=f'https://note.com/tag/{quote(tag)}?mode=new'
    s=get_public(url).decode('utf-8')
    return ['https://note.com'+p for p in dict.fromkeys(NOTE_PATH.findall(s))]

def note_rss(handle):
    url=f'https://note.com/{handle}/rss'
    doc=ET.fromstring(get_public(url))
    result=[]
    for item in doc.findall('./channel/item'):
        canonical=item.findtext('link')
        native=item.findtext('pubDate')
        if canonical and NOTE_LINK.fullmatch(canonical):
            result.append({'canonical_url':canonical,'title':item.findtext('title'),
                           'first_party_content_url':url,'native_timestamp':native,
                           'time_method':'official note.com RSS item pubDate'})
    return result

def note_original(url):
    s=get_public(url).decode('utf-8')
    for raw in LD_JSON.findall(s):
        try:
            doc=json.loads(raw)
        except ValueError:
            continue
        if not isinstance(doc,dict) or not doc.get('datePublished'):
            continue
        return {'platform':'note.com','source_id':url.rsplit('/',1)[-1],
                'author':url.split('/')[3],'canonical_url':url,
                'native_timestamp':doc['datePublished'],'time_method':'original JSON-LD datePublished',
                'title':doc.get('headline'),'article_is_free':doc.get('isAccessibleForFree'),
                'directly_opened_first_party':True}
    return {'platform':'note.com','canonical_url':url,'directly_opened_first_party':True,
            'reason':'No explicit article-level datePublished in public JSON-LD'}

def youtube_rss(channel):
    url=f'https://www.youtube.com/feeds/videos.xml?channel_id={channel}'
    doc=ET.fromstring(get_public(url))
    result=[]
    for item in doc.findall(ATOM+'entry'):
        video=item.findtext(YT+'videoId')
        if not video:
            continue
        result.append({'platform':'youtube','source_id':video,'canonical_url':f'https://www.youtube.com/watch?v={video}',
                       'author':item.findtext(ATOM+'author/'+ATOM+'name'),
                       'author_channel_id':item.findtext(YT+'channelId'),
                       'title':item.findtext(ATOM+'title'),
                       'native_timestamp':item.findtext(ATOM+'published'),
                       'description':item.findtext(MRSS+'group/'+MRSS+'description'),
                       'first_party_content_url':url,'directly_opened_first_party':True,
                       'time_method':'official YouTube creator Atom published and yt:videoId'})
    return result

def add_time(item,start,cutoff):
    try:
        t=datetime_offset(item.get('native_timestamp'))
    except (ValueError, TypeError):
        t=None
    item['created_utc']=t.isoformat().replace('+00:00','Z') if t else None
    item['within_window']=start<=t<=cutoff if t else None
    item['eligible']=None
    return item

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cutoff',required=True,help='Frozen ISO timestamp with explicit offset')
    p.add_argument('--note-tag',action='append',default=[])
    p.add_argument('--note-user',action='append',default=[])
    p.add_argument('--youtube-channel-id',action='append',default=[])
    p.add_argument('--limit-note-articles',type=int,default=20)
    p.add_argument('--delay',type=float,default=.6,help='Seconds before each public request; minimum 0.5')
    p.add_argument('--timeout',type=float,default=8)
    args=p.parse_args()
    args.delay=max(.5,args.delay)
    if args.limit_note_articles<0 or args.limit_note_articles>60:
        p.error('Limit must be between 0 and 60; keep public requests bounded.')
    if any(not re.fullmatch(r'[A-Za-z0-9_]+',h) for h in args.note_user):
        p.error('Invalid note.com creator handle')
    if any(not re.fullmatch(r'UC[A-Za-z0-9_-]{22}',h) for h in args.youtube_channel_id):
        p.error('Invalid YouTube channel id')
    cutoff=datetime_offset(args.cutoff)
    start=cutoff-dt.timedelta(hours=72)
    errors=[]
    def safe(kind,key,fn):
        try:
            return fn(key)
        except (HTTPError,OSError,etree_errors,RuntimeError,ValueError) as exc:
            errors.append({'route':kind,'selector':key,'reason':str(exc)})
            return None
    etree_errors=ET.ParseError
    discovered={}
    for user in args.note_user:
        for it in (safe('note RSS',user,note_rss) or []):
            add_time(it,start,cutoff)
            discovered[it['canonical_url']]=it
    for tag in args.note_tag:
        for url in (safe('note recent tag',tag,note_tag) or []):
            discovered.setdefault(url,{'canonical_url':url,'discovered_via':'public newest tag'})
    # Known stale RSS URLs need no origin read. Newest tag URLs are emitted in order.
    note=[]
    for url in [u for u,i in discovered.items() if i.get('within_window') is not False][:args.limit_note_articles]:
        row=safe('public note article',url,note_original)
        if row:
            note.append(add_time(row,start,cutoff))
    youtube=[]
    for channel in dict.fromkeys(args.youtube_channel_id):
        youtube.extend(add_time(i,start,cutoff) for i in (safe('official YouTube creator Atom',channel,youtube_rss) or []))
    print(json.dumps({'window_start_utc':start.isoformat(),'cutoff_utc':cutoff.isoformat(),
                      'note_discovered':list(discovered.values()),'note_articles':note,'youtube_entries':youtube,
                      'errors':errors,'eligibility':'Requires independent review of attributable first-person play, build decisions, or matchup evidence.'},ensure_ascii=False,indent=2))
