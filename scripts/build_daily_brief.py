#!/usr/bin/env python3
"""Compile transparent daily discovery status. Never claim unreviewed feeds are verified.
Static artifact only; designed for GitHub Pages after a scheduled workflow run.
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
WAT=ZoneInfo('Africa/Lagos')

def load(name,fallback):
 try: return json.loads((DATA/name).read_text(encoding='utf-8'))
 except (OSError,ValueError): return fallback

def build():
 status=load('feed_status.json',{})
 items=load('auto_updates.json',[])
 now=datetime.now(timezone.utc)
 date_wat=now.astimezone(WAT).date().isoformat()
 latest=[]
 for item in items:
  if not isinstance(item,dict): continue
  date=item.get('date','')
  if date and date >= (now-timedelta(days=7)).date().isoformat():
   latest.append({key:item.get(key) for key in ['id','date','headline','topic','agency','url','status']})
 latest=sorted(latest,key=lambda x:x['date'],reverse=True)[:20]
 attempts=status.get('last_attempt_utc')
 successes=status.get('sources_ok',[])
 failures=status.get('failures',[])
 has_success=bool(successes)
 result={
  'edition':'daily-discovery-v2',
  'generated_utc':now.isoformat(),
  'generated_date_wat':date_wat,
  'target_time':'07:00 Africa/Lagos (WAT, UTC+1)',
  'scheduled_daily':True,
  'last_attempt_utc':attempts,
  'last_successful_check_utc':attempts if has_success else None,
  'feed_health':'partial' if failures and has_success else 'healthy' if has_success else 'unavailable',
  'coverage_note':'Three selected federal agency RSS sources only; not every Nigerian education institution or state. Feed collection is discovery, not editorial verification.',
  'sources_succeeded':successes,
  'sources_failed':failures,
  'recent_unreviewed_discoveries':latest,
  'discovery_count_recent':len(latest),
  'editorial_status':'Automated discovery only. Check original publisher, date, claim, and independent implementation evidence before relying on a record.',
 }
 (DATA/'daily_brief.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (DATA/'daily_brief.js').write_text('window.EDUATLAS_DAILY='+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 print('Brief generated',date_wat,result['feed_health'],len(latest))
if __name__=='__main__': build()
