#!/usr/bin/env python3
"""Discover Nigerian education agency RSS headlines for EduAtlas.

Discovers ONLY. The UI labels all discovered entries unreviewed. No item here
becomes a verified policy, budget result, stakeholder, or learning outcome.
Run in a network-enabled environment (GitHub Actions); Python 3.11+ stdlib.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'auto_updates.json'
STATUS = ROOT / 'data' / 'feed_status.json'
FEEDS = [
    ('FME', 'https://education.gov.ng/feed/', {'education.gov.ng'}),
    ('UBEC', 'https://ubec.gov.ng/feed/', {'ubec.gov.ng'}),
    ('NUC', 'https://www.nuc.edu.ng/feed/', {'nuc.edu.ng'}),
]
USER_AGENT = 'EduAtlas Nigeria Research Discovery/0.1 (+human-review-required)'
KEYWORDS = [
    ('Public finance', 'budget grant funding disbursement appropriation fiscal procurement expenditure'),
    ('Foundational learning', 'reading literacy numeracy basic education foundational'),
    ('Teachers', 'teacher teaching training professional'),
    ('Curriculum', 'curriculum syllabus textbook subjects'),
    ('Education data', 'school census nemis nedi data statistics'),
    ('Digital learning', 'digital ai technology edtech chatbot online'),
    ('Tertiary education', 'university tertiary academic research accreditation'),
]

def clean(raw: str, limit=360) -> str:
    x = html.unescape(re.sub('<[^>]+>', ' ', raw or ''))
    x = re.sub(r'\s+', ' ', x).strip()
    return x[:limit].rsplit(' ', 1)[0] + '…' if len(x) > limit else x

def classify(title: str, summary: str) -> str:
    text = (title + ' ' + summary).lower()
    return next((topic for topic, keys in KEYWORDS if any(k in text for k in keys.split())), 'Governance')

def valid_url(u: str, allowed: set[str]) -> bool:
    p = urlparse(u)
    host = (p.hostname or '').lower()
    return p.scheme == 'https' and any(host == x or host.endswith('.' + x) for x in allowed)

def get_text(el: ET.Element, q: str) -> str:
    x = el.find(q)
    return (x.text or '').strip() if x is not None else ''

def parse_date(text: str) -> str | None:
    if not text: return None
    try:
        x = parsedate_to_datetime(text)
        if x.tzinfo is None: x = x.replace(tzinfo=timezone.utc)
        return x.astimezone(timezone.utc).date().isoformat()
    except (ValueError, TypeError, IndexError):
        try: return datetime.fromisoformat(text.replace('Z', '+00:00')).date().isoformat()
        except ValueError: return None

def fetch(name: str, url: str, allowed: set[str]) -> list[dict]:
    req = Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/rss+xml,application/xml,text/xml'})
    with urlopen(req, timeout=25) as resp:
        content = resp.read(1_500_000)
    root = ET.fromstring(content)
    items = root.findall('./channel/item')
    if not items:
        ns = {'a': 'http://www.w3.org/2005/Atom'}
        items = root.findall('./a:entry', ns)
    out = []
    for it in items[:40]:
        title = clean(get_text(it, 'title') or get_text(it, '{http://www.w3.org/2005/Atom}title'), 170)
        link = get_text(it, 'link')
        if not link:
            a = it.find('{http://www.w3.org/2005/Atom}link')
            if a is not None: link = a.get('href', '')
        date = parse_date(get_text(it, 'pubDate') or get_text(it, '{http://www.w3.org/2005/Atom}updated') or get_text(it,'{http://www.w3.org/2005/Atom}published'))
        summary = clean(get_text(it, 'description') or get_text(it, '{http://www.w3.org/2005/Atom}summary'), 300)
        if not title or not date or not valid_url(link, allowed):
            continue
        if date > (datetime.now(timezone.utc)+timedelta(days=1)).date().isoformat():
            continue
        out.append({'id': 'auto-'+re.sub('[^a-z0-9]', '', (name+date+title).lower())[:55],
                    'date': date,'topic': classify(title,summary),'agency': name,
                    'headline': title,'summary': summary or 'Automatically discovered agency headline. Read the original before citing it.',
                    'url': link,'status': 'Unreviewed discovery',
                    'impact': 'Open the source, check the claim and date, and seek separate implementation evidence.'})
    return out

def main():
    prior = []
    if OUT.exists():
        try: prior=json.loads(OUT.read_text(encoding='utf-8'))
        except (ValueError,OSError): pass
    result = {x['url']: x for x in prior if isinstance(x,dict) and isinstance(x.get('url'),str)}
    successes=[]; failures=[]
    for name,url,allowed in FEEDS:
        try:
            items=fetch(name,url,allowed)
            for x in items: result[x['url']]=x
            successes.append({'source':name,'entries':len(items)})
        except Exception as exc:
            failures.append({'source':name,'error':str(exc)[:190]})
            print(f'Warning: {name}: {exc}', file=sys.stderr)
    cutoff=(datetime.now(timezone.utc)-timedelta(days=180)).date().isoformat()
    final=sorted((x for x in result.values() if x.get('date','')>=cutoff),key=lambda x:x['date'],reverse=True)[:90]
    OUT.write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    STATUS.write_text(json.dumps({'last_attempt_utc':datetime.now(timezone.utc).isoformat(),'sources_ok':successes,'failures':failures,'number_of_discoveries':len(final)},indent=2)+'\n',encoding='utf-8')
    print(f'Discoveries: {len(final)} | feeds successful: {len(successes)} | failures: {len(failures)}')
    # Fail only if all feeds fail; previous data remains usable.
    return 1 if not successes else 0

if __name__ == '__main__': raise SystemExit(main())
