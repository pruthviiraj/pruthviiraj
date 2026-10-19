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
def write(name,w,h,title,body,animated=False):
 p=A/name;p.parent.mkdir(parents=True,exist_ok=True)
 value=svg(w,h,title,body);p.write_text(value)
 if animated:
  p=A/'previews/static'/Path(name).name;p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text(re.sub(r'<style>.*?</style>','',value,flags=re.S))

MOTION="""<style>
@keyframes assemble{from{opacity:.5;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.assemble{animation:assemble .45s cubic-bezier(.2,0,0,1) both}
@media(prefers-reduced-motion:reduce){.assemble{animation:none!important;transform:none;opacity:1}}
</style>"""
# Schematic of the implemented Olist toolchain; body copy remains native Markdown.
body=MOTION+box(1,1,718,403,fill='#F8FAFC',radius=10,stroke='#E2E8F0')
for i,(name,label) in enumerate([('python','Python'),('microsoft-azure','Azure'),('snowflake-icon','Snowflake'),('dbt-icon','dbt')]):
 x=57+i*169
 body+=f'<g class="assemble" style="animation-delay:{i*.08}s">'
 body+=box(x,130,98,98,fill='#FFFFFF',radius=18,stroke='#DBE3EE')+icon(name,x+23,153,52,'flow'+str(i))
 body+=txt(x+49,266,label,26,'#334155',500,'middle')+'</g>'
 if i<3:body+=f'<path d="M{x+114} 179h34m-8-7 8 7-8 7" stroke="#94A3B8" stroke-width="2" fill="none"/>'
write('previews/olist-flow.svg',720,405,'Olist code workflow: Python, Azure Blob Storage, Snowflake, and dbt.',body,animated=True)
# Simplified view of the warehouse layers documented in the project.
body=MOTION+box(1,1,718,403,fill='#F8FAFC',radius=10,stroke='#E2E8F0')
for i,(label,color,description) in enumerate([('Bronze','#C48A56','Raw data'),('Silver','#9AAABD','Clean data'),('Gold','#C8AB59','Sales tables')]):
 x=48+i*228
 body+=f'<g class="assemble" style="animation-delay:{i*.1}s">'
 body+=f'<path d="M{x+30} 118c0-23 116-23 116 0v87c0 23-116 23-116 0Z" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-width="3"/><ellipse cx="{x+88}" cy="118" rx="58" ry="18" fill="#F8FAFC" stroke="{color}" stroke-width="3"/><path d="M{x+30} 160c0 23 116 23 116 0" fill="none" stroke="{color}" stroke-width="3"/>'
 body+=txt(x+88,274,label,28,'#334155',600,'middle')+txt(x+88,310,description,23,'#64748B',400,'middle')+'</g>'
 if i<2:body+=f'<path d="M{x+174} 165h33m-8-7 8 7-8 7" stroke="#94A3B8" stroke-width="2" fill="none"/>'
write('previews/warehouse-layers.svg',720,405,'Warehouse structure: raw data in Bronze, cleaned data in Silver, and sales tables in Gold.',body,animated=True)

# The stack uses labels sized to match the 16px native README body text.
GROUPS=[
 ('Reporting',[('microsoft-power-bi','Power BI'),('excel','Excel')]),
 ('Programming',[('python','Python'),('pandas-icon','pandas')]),
 ('Databases',[('sql-server','SQL Server'),('postgresql','PostgreSQL')]),
 ('Cloud & warehouse',[('microsoft-azure','Azure'),('snowflake-icon','Snowflake')]),
 ('Analytics tools',[('dbt-icon','dbt'),('looker-icon','Looker Studio')]),
 ('Version control',[('git-icon','Git'),('github-icon','GitHub')]),
]
for mobile in [False,True]:
 cols=2 if mobile else 3
 cw,ch=(360,184) if mobile else (400,175)
 w,h=cols*cw,((len(GROUPS)+cols-1)//cols)*ch
 body=''
 for i,(label,tools) in enumerate(GROUPS):
  x=(i%cols)*cw;y=(i//cols)*ch
  body+=box(x+7,y+7,cw-14,ch-14,fill='panel',radius=10)
  body+=txt(x+22,y+43,label,32 if mobile else 26,'text',600)
  for j,(name,tool) in enumerate(tools):
   cx=x+cw*(.26 if j==0 else .74)
   size=50 if mobile else 44
   body+=box(cx-size/2,y+64,size,size,fill='#F8FAFC',radius=9,stroke='#F8FAFC')
   body+=icon(name,cx-size/2+7,y+71,size-14,'stack-'+str(i)+'-'+str(j))
   body+=txt(cx,y+153,tool,30 if mobile else 26,'muted',400,'middle')
 write('previews/stack-mobile.svg' if mobile else 'previews/stack.svg',w,h,'Reporting: Power BI and Excel. Programming: Python and pandas. Databases: SQL Server and PostgreSQL. Cloud and warehouse: Azure and Snowflake. Analytics tools: dbt and Looker Studio. Version control: Git and GitHub.',body)
