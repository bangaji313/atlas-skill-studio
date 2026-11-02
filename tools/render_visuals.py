"""Regenerate the Atlas README vectors using only Python's standard library."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/assets'
PAPER='#F2EEE4';INK='#132C3A';MUTED='#506473';ACCENT='#166A58'

def start(width,height,title,description):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{description}</desc>
<style>text{{font-family:'Segoe UI',Arial,sans-serif;fill:{INK}}}.serif{{font-family:Georgia,'Times New Roman',serif}}.muted{{fill:{MUTED}}}.eyebrow{{font-size:18px;letter-spacing:3px;font-weight:600}}</style>
<rect width="{width}" height="{height}" fill="{PAPER}"/>'''

def text(x,y,value,size=24,cls='',extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}" {extra}>{value}</text>'

def logo(slug,x,y,size):
    source=(OUT/(slug+'.svg')).read_text(encoding='utf-8')
    viewbox=re.search(r'viewBox="([^"]+)"',source).group(1)
    body=re.sub(r'^.*?<svg[^>]*>','',source,flags=re.S).rsplit('</svg>',1)[0]
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{viewbox}">{body}</svg>'

def hero():
    s=start(1600,720,'Atlas Skill Studio','227 curated agent skills in three focused studios, assembled from pinned sources for Codex, Claude and Antigravity.')
    s+=text(80,92,'ATLAS / SKILL STUDIO',20,'eyebrow')
    s+=text(80,212,'227 skills.',94,'serif')
    s+=text(80,316,'Three focused studios.',94,'serif')
    s+=text(84,388,'Research the opportunity. Shape the story. Build the system.',27,'muted')
    s+='<line x1="80" y1="444" x2="1520" y2="444" stroke="#C9D0CC"/>'
    entries=[('atlas-growth-social','Growth &amp; Social','79 skills',80),('atlas-creative-production','Creative Production','79 skills',588),('atlas-engineering-tools','Engineering Tools','69 skills',1100)]
    for slug,label,count,x in entries:
        s+=logo(slug,x,492,104)+text(x+128,534,label,27,extra='font-weight="600"')+text(x+128,576,count,23,'muted')
    s+=text(84,664,'SOURCE-PINNED BUILDS',17,'eyebrow')+text(1016,664,'Codex  /  Claude  /  Antigravity',23,'muted')
    (OUT/'atlas-hero.svg').write_text(s+'</svg>\n',encoding='utf-8')

def architecture():
    s=start(1600,900,'From upstream expertise to your next deliverable','31 pinned upstream projects are organized into Growth, Creative and Engineering studios. Native packages connect these skills to Codex, Claude and Antigravity Desktop; execution depends on the tools available in each host.')
    s+=text(80,88,'HOW ATLAS FITS TOGETHER',18,'eyebrow')+text(80,160,'One collection. Three ways to get to work.',54,'serif')
    s+=text(80,208,'Choose the studio for the job. Install the format for your host.',25,'muted')
    s+='''<defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#506473"/></marker></defs>
<g fill="none" stroke="#506473" stroke-width="2" marker-end="url(#arrow)">
<path d="M 344,424 H 376 Q 384,424 384,416 V 296 Q 384,288 392,288 H 432"/>
<path d="M 344,464 H 432"/>
<path d="M 344,504 H 376 Q 384,504 384,512 V 632 Q 384,640 392,640 H 432"/>
<path d="M 912,288 H 976 Q 984,288 984,296 V 368 Q 984,376 992,376 H 1056"/>
<path d="M 944,464 H 1008 Q 1016,464 1016,456 V 456 Q 1016,448 1024,448 H 1056"/>
<path d="M 896,640 H 992 Q 1000,640 1000,632 V 528 Q 1000,520 1008,520 H 1056"/>
</g>'''
    s+=f'<rect x="80" y="344" width="264" height="240" rx="8" fill="{PAPER}" stroke="{ACCENT}" stroke-width="2"/>'
    s+=text(104,388,'SOURCE LOCK',16,'eyebrow')+text(104,448,'31 projects',33,extra='font-weight="600"')
    s+=text(104,496,'Pinned commits',23,'muted')+text(104,536,'Verified file hashes',21,'muted')
    for x,y,width,title,subtitle,count in [(432,224,480,'Growth &amp; Social','Research · positioning · content',79),(432,400,512,'Creative Production','Design · video · animation · sound',79),(432,576,464,'Engineering Tools','Code · research · Office · IoT',69)]:
        s+=f'<rect x="{x}" y="{y}" width="{width}" height="128" rx="8" fill="{PAPER}" stroke="#132C3A" stroke-width="1.5"/>'
        s+=text(x+24,y+48,title,28,extra='font-weight="600"')+text(x+24,y+92,subtitle,21,'muted')
        s+=text(x+width-24,y+48,str(count),29,'serif',extra='text-anchor="end"')
    s+=f'<rect x="1056" y="312" width="464" height="296" rx="8" fill="{PAPER}" stroke="#132C3A" stroke-width="1.5"/>'
    s+=text(1080,356,'HOST-NATIVE PACKAGES',16,'eyebrow')+text(1080,412,'Codex',30,extra='font-weight="600"')
    s+=text(1080,460,'Claude',30,extra='font-weight="600"')+text(1080,508,'Antigravity Desktop',30,extra='font-weight="600"')
    s+=text(1080,568,'Tools and runtime setup vary by host.',20,'muted')
    s+='<line x1="80" y1="772" x2="1520" y2="772" stroke="#C9D0CC"/>'
    s+=text(80,824,'FROM A BRIEF TO A DELIVERABLE',16,'eyebrow')+text(704,824,'Content plans · editable media · checked systems',25,'muted')
    (OUT/'atlas-system.svg').write_text(s+'</svg>\n',encoding='utf-8')

if __name__=='__main__':hero();architecture();print('Atlas README vectors regenerated.')
