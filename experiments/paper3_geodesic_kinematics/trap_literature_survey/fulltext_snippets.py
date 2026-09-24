import sys
import re
import urllib.request
import os
D='/tmp/claude-0/-home-user-ACADEMIC-JVP-WORK-/45846392-2c30-55c7-ba68-e8fc861add6f/scratchpad/ft'
KW={'data':r'dataset|recorded|recording|session|run\b|runs\b|trials?\b|subjects?\b|participants?|BCI Competition|PhysioNet|eyes',
    'cv':r'cross-validat|\bfolds?\b|\b\d+-fold|leave-one|shuffl|train(ing)? and test|test set|split|permutation|held-out|hold-out|chronolog|session-to-session|cross-session|cross-subject',
    'ocular':r'\bEOG\b|ocular|blink|eye movement|\bICA\b|independent component|artifact|artefact|Fp1|Fp2|frontal',
    'window':r'window|epoch|segment|overlap|onset|localiz|change.point'}
def get(pmc):
    f=os.path.join(D,pmc+'.txt')
    if os.path.exists(f): return open(f).read()
    try:
        x=urllib.request.urlopen(f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML',timeout=60).read().decode('utf8','replace')
    except Exception:
        return ''
    t=re.sub(r'<ref-list.*?</ref-list>','',x,flags=re.S)
    t=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'\s+',' ',t)
    open(f,'w').write(t); return t
for pmc in sys.argv[1:]:
    t=get(pmc); print('#####',pmc,len(t))
    if not t: continue
    sents=re.split(r'(?<=[.!?])\s+',t)
    for k,p in KW.items():
        hits=[s for s in sents if re.search(p,s,re.I) and len(s)<600]
        print(f'  [{k}] {len(hits)} hits')
        for s in hits[:int(os.environ.get("N","6"))]: print('   -',s[:330])
