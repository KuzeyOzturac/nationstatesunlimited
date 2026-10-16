"""Resumable HTTP archive fetch. Eight concurrent workers, cached responses, retries."""
import urllib.request, pathlib, re, time, concurrent.futures, threading, json, sys
ROOT=pathlib.Path(__file__).resolve().parents[1];RAW=ROOT/'data/raw';RAW.mkdir(parents=True,exist_ok=True)
BASE='http://www.mwq.dds.nl/ns/results/'
lock=threading.Lock();last=[0.0]
def fetch(name):
 path=RAW/name
 if path.exists() and path.stat().st_size>500:return True
 for attempt in range(3):
  try:
   with lock:
    delay=max(0,0.25-(time.monotonic()-last[0]));time.sleep(delay);last[0]=time.monotonic()
   req=urllib.request.Request(BASE+name,headers={'User-Agent':'NationStatesUnlimited/1.1 archive importer (KuzeyOzturac/nationstatesunlimited)'})
   with urllib.request.urlopen(req,timeout=30) as r:data=r.read()
   if b'<html' not in data.lower() or len(data)<500:raise ValueError('Invalid HTML response')
   path.write_bytes(data);return True
  except Exception as e:
   if attempt==2:print('FAILED',name,str(e),flush=True);return False
   time.sleep(2*(attempt+1))
for name in ['index.html','issues.html','policies.html']:
 if name=='index.html' and not (RAW/name).exists():
  with urllib.request.urlopen(BASE,timeout=30) as r:(RAW/name).write_bytes(r.read())
 elif name!='index.html':fetch(name)
ids=re.findall(r'href="(\d+\.html)"',(RAW/'index.html').read_text())
if '--limit' in sys.argv:ids=ids[:int(sys.argv[sys.argv.index('--limit')+1])]
fail=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for k,(name,ok) in enumerate(zip(ids,pool.map(fetch,ids)),1):
  if not ok:fail.append(name)
  if k%50==0 or k==len(ids):print(json.dumps({'completed':k,'total':len(ids),'failed':len(fail)}),flush=True)
(RAW/'fetch-report.json').write_text(json.dumps({'total':len(ids),'failed':fail,'fetchedAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},indent=2))

if fail:sys.exit(1)
