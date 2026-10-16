"""Parse actual archive HTML into provenance-bearing records. No invented issue prose."""
from html.parser import HTMLParser
from pathlib import Path
import re,json,hashlib,datetime,copy
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'data/raw';OUT=ROOT/'src/data';OUT.mkdir(parents=True,exist_ok=True)
BASE='http://www.mwq.dds.nl/ns/results/'
class Node:
 def __init__(self,tag='',attrs=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=[]
 def text(self):return ''.join(c if isinstance(c,str) else c.text() for c in self.children)
 def all(self,tag):
  result=[]
  for c in self.children:
   if isinstance(c,Node):
    if c.tag==tag:result.append(c)
    result+=c.all(tag)
  return result
class DOM(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root];self.feed(s)
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in ['meta','br','img','link','hr','input']:self.stack.append(n)
 def handle_endtag(self,t):
  for k in range(len(self.stack)-1,0,-1):
   if self.stack[k].tag==t:self.stack=self.stack[:k];break
 def handle_data(self,s):self.stack[-1].children.append(s)
def clean(s):return re.sub(r'\s+',' ',s).strip()
def parse_effects(source):
 root=DOM(source).root;options=[]
 for row in root.all('tr'):
  cells=[n for n in row.children if isinstance(n,Node) and n.tag=='td']
  if len(cells)!=3:continue
  match=re.match(r'([\d/]+)\.\s*(.*)',clean(cells[0].text()))
  if not match:continue
  records=[];transitions=[];notes=[]
  lines=cells[1].all('div');data=cells[2].all('div')
  for k,line in enumerate(lines):
   text=clean(line.text());m=re.fullmatch(r'([+-]?[\d.]+) to ([+-]?[\d.]+) (.*?) \(mean ([+-]?[\d.]+)\)',text)
   count=clean(data[k].text()) if k<len(data) else ''
   if m:records.append({'stat':m[3],'min':float(m[1]),'max':float(m[2]),'mean':float(m[4]),'samples':int(count) if count.isdigit() else None})
   else:
    fixed=re.fullmatch(r'([+-]?[\d.]+) ([A-Za-z].*)',text)
    if fixed:
     value=float(fixed[1]);records.append({'stat':fixed[2],'min':value,'max':value,'mean':value,'samples':int(count) if count.isdigit() else None,'fixed':True});continue
    p=re.match(r'(sometimes )?(adds|removes) policy:\s*(.*)',text)
    if p:transitions.append({'policy':p[3],'action':'add' if p[2]=='adds' else 'remove','conditional':bool(p[1])})
    else:notes.append(text)
  dates=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',cells[2].text())
  for number in match[1].split('/'):
   options.append({'number':int(number),'text':match[2],'observations':copy.deepcopy(records),'policyChanges':copy.deepcopy(transitions),'notes':notes[:],'lastConfirmed':max(dates) if dates else None})
 return options
def main():
 # All issue IDs/options from the site's combined list.
 root=DOM((RAW/'issues.html').read_text()).root
 catalogue=[];current=None
 for child in root.all('a'):
  href=child.attrs.get('href','')
  if re.fullmatch(r'\d+\.html',href):
   number=int(href[:-5]);title=re.sub(r'^#\d+\s*','',clean(child.text()))
   catalogue.append({'id':str(number),'number':number,'title':title,'source':BASE+href,'provenance':'mwq-observed','eligibilityStatus':'unknown','options':[]})
 # Capture text between links, using parser event stream rather than DOM siblings.
 class Combined(HTMLParser):
  def __init__(self,s):super().__init__(convert_charrefs=True);self.current=None;self.inlink=False;self.lines={};self.feed(s)
  def handle_starttag(self,t,a):
   d=dict(a)
   if t=='a' and re.fullmatch(r'\d+\.html',d.get('href','')):self.current=d['href'][:-5];self.lines[self.current]=[];self.inlink=True
  def handle_endtag(self,t):
   if t=='a':self.inlink=False
  def handle_data(self,s):
   if self.current and not self.inlink:
    for line in s.splitlines():
     m=re.match(r'\s*(\d+)\.\s*(.+)',line)
     if m:self.lines[self.current].append({'number':int(m[1]),'text':clean(m[2])})
 combined=Combined((RAW/'issues.html').read_text())
 # Policy reference catalogue and complete option-to-policy relationships.
 policy_root=DOM((RAW/'policies.html').read_text()).root
 policies=[];category=''
 for item in policy_root.children:
  if not isinstance(item,Node):continue
  # document body is nested; handled below by ordered walk
 
 def ordered(n):
  for c in n.children:
   if isinstance(c,Node):yield c;yield from ordered(c)
 for node in ordered(policy_root):
  if node.tag=='h1':category=clean(node.text())
  if node.tag!='table':continue
  headings=node.all('h2')
  if not headings:continue
  name=clean(headings[0].text());description=clean(node.all('i')[0].text()) if node.all('i') else ''
  policy={'name':name,'category':category,'description':description,'source':BASE+'policies.html#'+headings[0].attrs.get('id',name.replace(' ','_')),'relations':[]}
  for cell in node.all('td'):
   mode=None;issue_id=None
   for child in cell.children:
    if not isinstance(child,Node):continue
    if child.tag=='h4':mode=clean(child.text())
    elif child.tag=='div':
     links=child.all('a')
     if links and re.fullmatch(r'\d+\.html',links[0].attrs.get('href','')):issue_id=links[0].attrs['href'][:-5]
     else:
      m=re.match(r'([\d/]+)\.\s*(.*)',clean(child.text()))
      if m and mode and issue_id:
       for number in m[1].split('/'):
        policy['relations'].append({'issue':issue_id,'option':int(number),'action':'remove' if 'Removed' in mode or 'removed' in mode else 'add','conditional':'Sometimes' in mode or 'sometimes' in mode})
  policies.append(policy)
 relations={}
 for p in policies:
  for r in p['relations']:relations.setdefault((r['issue'],r['option']),[]).append({'policy':p['name'],'action':r['action'],'conditional':r['conditional']})
 files=[];detailed=0
 for issue in catalogue:
  path=RAW/(issue['id']+'.html')
  if path.exists():
   opts=parse_effects(path.read_text());files.append({'path':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
   if opts:issue['options']=opts;issue['effectsStatus']='observed';detailed+=1
  if not issue['options']:
   issue['options']=[{**o,'observations':[],'policyChanges':relations.get((issue['id'],o['number']),[]),'notes':[],'lastConfirmed':None} for o in combined.lines.get(issue['id'],[])];issue['effectsStatus']='unavailable'
  for o in issue['options']:
   # The policy page is a second view of the same source. Preserve missing mappings.
   existing={(p['policy'],p['action']) for p in o['policyChanges']}
   o['policyChanges'] += [p for p in relations.get((issue['id'],o['number']),[]) if (p['policy'],p['action']) not in existing]
  # Archive has no full validity code; conservative curated rules are separate.
  if not issue['options']:issue['unplayableReason']='No outcome options published in archive'
 # Emit chunks to keep GitHub API writes and diffs manageable.
 for old in OUT.glob('issues-*.json'):old.unlink()
 for start in range(0,len(catalogue),100):(OUT/f'issues-{start//100:02}.json').write_text(json.dumps(catalogue[start:start+100],ensure_ascii=False,separators=(',',':')))
 (OUT/'policies.json').write_text(json.dumps(policies,ensure_ascii=False,separators=(',',':')))
 manifest={'source':BASE,'fetchedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'issues':len(catalogue),'options':sum(len(i['options']) for i in catalogue),'detailedIssues':detailed,'unplayableIds':[i['id'] for i in catalogue if not i['options']],'missingDetailIds':[i['id'] for i in catalogue if i['effectsStatus']!='observed' and i['options']],'policies':len(policies),'policyRelations':sum(len(p['relations']) for p in policies),'files':files,'indexSha256':hashlib.sha256((RAW/'index.html').read_bytes()).hexdigest()}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({k:(len(v) if k=='missingDetailIds' else v) for k,v in manifest.items() if k!='files'},indent=2))
 # Compact playable catalogue: retain every archive option number, local indicator means,
 # exact policy mappings and missing-data status. Detailed observations remain in chunks.
 stat_map={'Civil Rights':'civil','Political Freedom':'political','Economic Freedom':'economic','Economy':'economy','Income Equality':'equality','Health':'health','Public Education':'education','Eco-Friendliness':'environment','Safety':'security'}
 compact=[]
 for i,issue in enumerate(catalogue):
  if not issue['options']:continue
  compact.append({**{k:v for k,v in issue.items() if k!='options'},'chunk':f'issues-{i//100:02}.json','options':[{**{k:v for k,v in o.items() if k not in ['observations','notes']},'effects':{stat_map[r['stat']]:r['mean'] for r in o['observations'] if r['stat'] in stat_map},'observationCount':len(o['observations'])} for o in issue['options']]})
 stat_labels={'civil':'Civil rights','political':'Political freedom','economic':'Economic freedom','economy':'Economy','equality':'Equality','health':'Public health','education':'Education','environment':'Environment','security':'Security'}
 (ROOT/'src/catalogue.js').write_text('// Generated from MWQ. Run scripts/import-archive.py; do not hand edit.\nexport const stats='+json.dumps(stat_labels)+';\nexport const issues='+json.dumps(compact,ensure_ascii=False,separators=(',',':'))+';\nexport const policyCatalogue='+json.dumps([{k:v for k,v in p.items() if k!='relations'} for p in policies],ensure_ascii=False,separators=(',',':'))+';\nexport const coverage='+json.dumps({k:v for k,v in manifest.items() if k!='files'})+';\n')

if __name__=="__main__":main()
