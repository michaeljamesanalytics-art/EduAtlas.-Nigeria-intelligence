#!/usr/bin/env python3
"""Offline, self-contained demonstration. Scheduled feed data only works when deployed."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'EduAtlas-Nigeria-Expanded-Demo.html'
css=(ROOT/'styles.css').read_text(encoding='utf-8')
scripts=[(ROOT/'data'/n).read_text(encoding='utf-8') for n in ('curated.js','academy.js','daily_brief.js')]
scripts.append((ROOT/'app.js').read_text(encoding='utf-8'))
script='\n'.join(scripts).replace('</script','<\\/script')
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" /><meta name="description" content="EduAtlas Nigeria — 65 lessons, glossary and education intelligence demo" /><title>EduAtlas Nigeria — Systematic Learning & Intelligence</title><style>{css}</style></head><body><div id="app"></div><script>{script}</script></body></html>'''
DEST.write_text(html,encoding='utf-8')
print(DEST,len(html),'bytes')
