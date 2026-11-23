from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app.js'
s=p.read_text(encoding='utf-8')
s=s.replace("const D=window.EDUATLAS || {updates:[],stakeholders:[],funds:[],timeline:[],policies:[],sources:[],reviewed:'unknown'};", "const D=window.EDUATLAS || {updates:[],stakeholders:[],funds:[],timeline:[],policies:[],sources:[],reviewed:'unknown'};\nconst A=window.EDUATLAS_ACADEMY||{tracks:[],sources:[],glossary:[]};\nconst INITIAL_DAILY=window.EDUATLAS_DAILY||{};")
s=s.replace("['overview','◈','Overview'],['updates','◷','Intelligence feed']", "['overview','◈','Overview'],['daily','◷','Daily 7am brief'],['updates','◷','Intelligence feed']")
s=s.replace("['power','♧','People & power'],['money'", "['power','♧','People & power'],['system','⌘','System map'],['money'")
s=s.replace("['learning','▣','Learning academy'],['sources'", "['learning','▣','Learning academy'],['glossary','≡','Glossary'],['sources'")
s=s.replace("lesson:0,completed:saved.completed||[],following:saved.following||[],notes:saved.notes||'',auto:[],autoNotice:''", "lesson:0,completed:saved.completed||[],following:saved.following||[],notes:saved.notes||'',auto:[],autoNotice:'',daily:INITIAL_DAILY,track:0,studyLesson:'t01-l01',showStudyAnswer:false,studyCompleted:saved.studyCompleted||[],studyNotes:saved.studyNotes||{}")
s=s.replace("completed:S.completed,following:S.following,notes:S.notes", "completed:S.completed,following:S.following,notes:S.notes,studyCompleted:S.studyCompleted,studyNotes:S.studyNotes")
start=s.index('function learning(){')
end=s.index('\nfunction sources(){',start)
frag=(p.parent/'scripts/academy_ui.jsfrag').read_text(encoding='utf-8')
s=s[:start]+frag+s[end:]
s=s.replace("const pages={overview,updates,policies,power,money,history,learning,sources,action};", "const pages={overview,daily,updates,policies,power,system,money,history,learning,glossary,sources,action};")
s=s.replace("const les=ev.target.closest('[data-lesson]');", "const track=ev.target.closest('[data-study-track]');if(track){S.track=Number(track.dataset.studyTrack);S.studyLesson=A.tracks[S.track]?.lessons[0]?.id||S.studyLesson;S.showStudyAnswer=false;render();return}\n  const lessonButton=ev.target.closest('[data-study-lesson]');if(lessonButton){S.studyLesson=lessonButton.dataset.studyLesson;S.showStudyAnswer=false;render();return}\n  const studyAnswer=ev.target.closest('[data-study-answer]');if(studyAnswer){S.showStudyAnswer=!S.showStudyAnswer;render();return}\n  const studyDone=ev.target.closest('[data-study-complete]');if(studyDone){const key=studyDone.dataset.studyComplete;S.studyCompleted=S.studyCompleted.includes(key)?S.studyCompleted.filter(k=>k!==key):[...S.studyCompleted,key];persist();render();return}\n  const studyNext=ev.target.closest('[data-study-next]');if(studyNext){const all=A.tracks.flatMap(t=>t.lessons);let idx=all.findIndex(x=>x.id===S.studyLesson);const next=all[(idx+1)%all.length];S.studyLesson=next.id;S.track=A.tracks.findIndex(t=>t.lessons.some(x=>x.id===next.id));S.showStudyAnswer=false;render();return}\n  const les=ev.target.closest('[data-lesson]');")
s=s.replace("else if(ev.target.id==='notes'){S.notes=ev.target.value;persist();const el=document.getElementById('notesStatus');if(el)el.textContent='✓ Saved locally'}", "else if(ev.target.id==='notes'){S.notes=ev.target.value;persist();const el=document.getElementById('notesStatus');if(el)el.textContent='✓ Saved locally'}else if(ev.target.id==='studyNote'){S.studyNotes[S.studyLesson]=ev.target.value;persist()}")
s=s.replace("<span class=\"safe\">● Curated research edition</span>","<span class=\"safe\">● Research + learning atlas</span>")
s=s.replace("<h1>From education policy<br>to real classroom change.</h1>","<h1>Understand the whole system.<br>Follow what changes each day.</h1>")
s=s.replace("<div class=\"hero-actions\">${nav('learning','Start learning →')}${nav('updates','Explore developments →','btn secondary')}</div>","<div class=\"hero-actions\">${nav('learning','Begin the 65-lesson academy →')}${nav('daily','See the 7am intelligence desk →','btn secondary')}</div>")
s=s.replace("${S.completed.length}/${LESSONS.length}","${S.studyCompleted.length}/${A.tracks.reduce((n,t)=>n+t.lessons.length,0)}")
# Keep the existing source room, expanding it with sources for the academy.
s=s.replace("function sources(){let arr=D.sources.filter(x=>matches(x.name,x.type,x.url));", "function sources(){let all=[...D.sources,...A.sources.map(s=>({name:s.title,type:'Academy research reference',url:s.url}))];let arr=[...new Map(all.map(x=>[x.url,x])).values()].filter(x=>matches(x.name,x.type,x.url));")
# append extra live fetch before IIFE closes; properly display cached fallback even when fetch fails
endtoken='\n})();'
assert s.endswith(endtoken+'\n') or s.endswith(endtoken)
s=s.replace(endtoken,"\nif(location.protocol==='http:'||location.protocol==='https:'){\n fetch('data/daily_brief.json',{cache:'no-store'}).then(r=>r.ok?r.json():null).then(x=>{if(x&&typeof x==='object'){S.daily=x;if(S.route==='daily')render()}}).catch(()=>{});\n}\n})();")
p.write_text(s,encoding='utf-8')
print('Patched app.js',len(s))
