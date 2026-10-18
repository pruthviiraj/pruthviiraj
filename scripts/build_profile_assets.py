"""Build self-contained profile SVGs using the original brand logos in assets/icons/."""
from pathlib import Path
from html import escape
import re
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'
C={'bg':'#0D1424','panel':'#111C30','tile':'#162239','border':'#28354D','text':'#F1F5F9','muted':'#A6B4CB','dim':'#7B8AA5','cyan':'#38BDF8','violet':'#A78BFA'}
FONT='Arial, Helvetica, sans-serif'
def txt(x,y,s,size=20,color='text',weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{C.get(color,color)}">{escape(str(s))}</text>'
def box(x,y,w,h,fill='panel',radius=14,stroke='border'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke)}"/>'
def icon(name,x,y,size,prefix):
 raw=(A/'icons'/f'{name}.svg').read_text()
 raw=raw[raw.index('<svg'):]
 tag=raw[:raw.index('>')+1]
 vb=re.search(r'viewBox="([^"]+)"',tag)
 if vb:view=vb.group(1)
 else:
  root=ET.fromstring(raw);view='0 0 '+re.sub('[^0-9.]','',root.attrib['width'])+' '+re.sub('[^0-9.]','',root.attrib['height'])
 for id_ in re.findall(r'\bid="([^"]+)"',raw):
  raw=raw.replace(f'id="{id_}"',f'id="{prefix}-{id_}"').replace(f'#{id_})',f'#{prefix}-{id_})').replace(f'"#{id_}"',f'"#{prefix}-{id_}"')
 return re.sub(r'<svg[^>]*>',f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{view}" fill="#000" preserveAspectRatio="xMidYMid meet">',raw,count=1)
def svg(w,h,title,body):
 return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>\n'
def write(name,w,h,title,body):
 p=A/name;p.parent.mkdir(parents=True,exist_ok=True)
 source=svg(w,h,title,body);p.write_text(source)
 # Explicit posters also cover readers that do not propagate motion preferences into SVG images.
 poster=re.sub(r'<style>.*?</style>','',source,flags=re.S).replace('class="ambient"','class="ambient" opacity=".4"')
 fallback=A/'still'/name;fallback.parent.mkdir(parents=True,exist_ok=True);fallback.write_text(poster)
TOOLS=[('python','Python','https://www.python.org/'),('microsoft-power-bi','Power BI','https://www.microsoft.com/power-platform/products/power-bi'),('excel','Excel','https://www.microsoft.com/microsoft-365/excel'),('sql-server','SQL Server','https://www.microsoft.com/sql-server'),('postgresql','PostgreSQL','https://www.postgresql.org/'),('pandas-icon','pandas','https://pandas.pydata.org/'),('snowflake-icon','Snowflake','https://www.snowflake.com/'),('dbt-icon','dbt','https://www.getdbt.com/'),('microsoft-azure','Azure','https://azure.microsoft.com/'),('looker-icon','Looker Studio','https://lookerstudio.google.com/'),('git-icon','Git','https://git-scm.com/'),('github-icon','GitHub','https://github.com/')]

EASE = 'cubic-bezier(.4,0,.2,1)'
MOTION = """<style>
@keyframes enter{from{opacity:.25;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes settle{from{opacity:.3;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
@keyframes breathe{0%,100%{opacity:.35;transform:translateY(0)}50%{opacity:.65;transform:translateY(-4px)}}
@keyframes trace{to{stroke-dashoffset:-1250}}
@keyframes pair{from{opacity:.6;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}
@keyframes arrow{0%,75%,87%,100%{transform:translateX(0)}81%,93%{transform:translateX(4px)}}
.enter{animation:enter .5s cubic-bezier(.4,0,.2,1) both}
.secondary{animation:settle .5s cubic-bezier(.4,0,.2,1) .1s both}
.ambient{animation:breathe 7s cubic-bezier(.4,0,.2,1) infinite}
.trace{stroke-dasharray:70 1180;animation:trace 9s linear infinite}
.pair{animation:pair .16s cubic-bezier(.2,0,0,1) both}
.link-arrow{animation:arrow 12s cubic-bezier(.4,0,.2,1) infinite}
@media(prefers-reduced-motion:reduce){
.enter,.secondary,.ambient,.trace,.pair,.link-arrow{animation:none!important;transform:none!important}
.enter,.secondary,.pair{opacity:1!important}.trace{stroke-dasharray:none}.ambient{opacity:.4}
}
</style>"""

def header(mobile=False):
 w,h=(720,210) if mobile else (1200,190)
 x=38 if mobile else 48
 body=MOTION+'<defs><linearGradient id="glow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111C30"/><stop offset="1" stop-color="#191A36"/></linearGradient><radialGradient id="orb"><stop stop-color="#7C83EF" stop-opacity=".5"/><stop offset="1" stop-color="#7C83EF" stop-opacity="0"/></radialGradient><clipPath id="header-clip"><rect x="1" y="1" width="'+str(w-2)+'" height="'+str(h-2)+'" rx="12"/></clipPath></defs>'
 body+=f'<g clip-path="url(#header-clip)"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#glow)" stroke="#28354D"/>'
 body+=f'<g class="ambient"><ellipse cx="{w-120}" cy="80" rx="210" ry="120" fill="url(#orb)"/></g>'
 body+=f'<path d="M{x} 1H{w-x}" stroke="#42517B" stroke-width="2"/><path class="trace" d="M{x} 1H{w-x}" stroke="#9EADFF" stroke-width="3"/>'
 body+='<g class="enter">'+txt(x,88 if mobile else 85,'Pruthvi Raj Pudi',49 if mobile else 52,'text',700)+'</g>'
 body+='<g class="secondary">'+txt(x,138 if mobile else 131,'Data Analytics  ·  Data Engineering',23 if mobile else 24,'muted')+'</g>'
 if not mobile:
  body+=txt(w-x,91,'SQL  /  PYTHON',15,'cyan',500,'end')
  body+=txt(w-x,123,'POWER BI  /  CLOUD',15,'violet',500,'end')
 body+='</g>'
 write('motion-header-mobile.svg' if mobile else 'motion-header.svg',w,h,'Pruthvi Raj Pudi. Data analytics and data engineering.',body)
for mobile in [False,True]:header(mobile)

# Exactly two small logos per labeled category; three columns on desktop, two on mobile.
GROUPS=[
 ('Reporting',[('microsoft-power-bi','Power BI'),('excel','Excel')]),
 ('Python',[('python','Python'),('pandas-icon','pandas')]),
 ('SQL databases',[('sql-server','SQL Server'),('postgresql','PostgreSQL')]),
 ('Cloud data',[('microsoft-azure','Azure'),('snowflake-icon','Snowflake')]),
 ('Analytics platforms',[('dbt-icon','dbt'),('looker-icon','Looker Studio')]),
 ('Version control',[('git-icon','Git'),('github-icon','GitHub')]),
]
for mobile in [False,True]:
 cols=2 if mobile else 3
 cellw,cellh=(360,165) if mobile else (400,148)
 w,h=cols*cellw,((len(GROUPS)+cols-1)//cols)*cellh
 body=MOTION
 for i,(label,tools) in enumerate(GROUPS):
  x=(i%cols)*cellw;y=(i//cols)*cellh
  body+=f'<g class="pair" style="animation-delay:{(i//2)*.16}s">'+box(x+6,y+6,cellw-12,cellh-12,fill='panel',radius=12)
  body+=txt(x+20,y+37,label,24 if mobile else 22,'text',600)
  for j,(name,tool) in enumerate(tools):
   cx=x+cellw*(.26 if j==0 else .74)
   size=50 if mobile else 42
   body+=box(cx-size/2,y+51,size,size,fill='#F8FAFC',radius=10,stroke='#F8FAFC')
   body+=icon(name,cx-size/2+7,y+58,size-14,f'group-{i}-{j}')
   body+=txt(cx,y+(135 if mobile else 122),tool,23 if mobile else 21,'muted',400,'middle')
  body+='</g>'
 write('tech-stack-mobile.svg' if mobile else 'tech-stack.svg',w,h,'Reporting: Power BI and Excel. Python: Python and pandas. SQL databases: SQL Server and PostgreSQL. Cloud data: Azure and Snowflake. Analytics platforms: dbt and Looker Studio. Version control: Git and GitHub.',body)

import textwrap
PROJECTS = [
 ('olist','DATA ENGINEERING · IN PROGRESS','Olist data pipeline','Python and dbt code to load e-commerce data into Snowflake. Includes 10 models. Validation and reports are in progress.','Python · Azure · Snowflake · dbt','View project','snowflake-icon','10 models'),
 ('sales','DATA ANALYSIS','Sales & finance reports','Eight Excel reports on sales and profit. Found a $54.9M gap to the 2021 sales target.','Excel · Power Query · Power Pivot','View reports','excel','8 reports'),
 ('warehouse','DATA ENGINEERING','Sales data warehouse','Combines customer and sales data from two systems in SQL Server. Includes checks for missing and duplicate records.','SQL Server · SQL · Data modeling','View project','sql-server','2 sources'),
 ('hr','DATA ANALYSIS','HR dashboard','Four Power BI pages covering 1,470 employees in a sample dataset, with 16 measures for analysis.','Power BI · DAX · Data modeling','View dashboard','microsoft-power-bi','4 pages'),
]
for index,(slug,category,title,description,stack,link,logo,metric) in enumerate(PROJECTS):
 for mobile in [False,True]:
  w,h=720,460 if mobile else 370
  body=MOTION+'<defs><linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#38BDF8" stop-opacity=".7"/><stop offset="1" stop-color="#A78BFA" stop-opacity=".1"/></linearGradient></defs>'
  body+=box(10,10,w-20,h-20,fill='panel',radius=12)
  body+='<path d="M27 10H693" stroke="url(#edge)" stroke-width="2"/>'
  body+=f'<g class="secondary" style="animation-delay:{index*.07+.08}s">'+box(635,30,44,44,fill='#F8FAFC',radius=10,stroke='#F8FAFC')+icon(logo,643,38,28,slug)+'</g>'
  body+=f'<g class="enter" style="animation-delay:{index*.07}s">'
  body+=txt(32,38,category,18,'cyan',500)
  body+=txt(32,96 if mobile else 91,title,40 if mobile else 36,'text',700)
  lines=textwrap.wrap(description,width=38 if mobile else 44,break_long_words=False)
  for i,line in enumerate(lines):body+=txt(32,(156 if mobile else 145)+i*(42 if mobile else 36),line,32 if mobile else 27,'muted')
  body+=txt(32,h-69,stack,22,'dim')+'</g>'
  body+=txt(32,h-28,link,26,'cyan',500)
  body+=f'<g class="link-arrow" style="animation-delay:-{index*3}s">'+txt(228 if slug=='hr' else 195,h-28,'→',26,'cyan',500)+'</g>'
  body+=txt(676,h-28,metric,22,'muted',500,'end')
  write(f'motion-cards/{slug}{"-mobile" if mobile else ""}.svg',w,h,title+'. '+description,body)
