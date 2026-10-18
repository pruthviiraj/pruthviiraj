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
 p=A/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(svg(w,h,title,body))
TOOLS=[('python','Python','https://www.python.org/'),('microsoft-power-bi','Power BI','https://www.microsoft.com/power-platform/products/power-bi'),('excel','Excel','https://www.microsoft.com/microsoft-365/excel'),('sql-server','SQL Server','https://www.microsoft.com/sql-server'),('postgresql','PostgreSQL','https://www.postgresql.org/'),('pandas-icon','pandas','https://pandas.pydata.org/'),('snowflake-icon','Snowflake','https://www.snowflake.com/'),('dbt-icon','dbt','https://www.getdbt.com/'),('microsoft-azure','Azure','https://azure.microsoft.com/'),('looker-icon','Looker Studio','https://lookerstudio.google.com/'),('git-icon','Git','https://git-scm.com/'),('github-icon','GitHub','https://github.com/')]
for name,label,url in TOOLS:
 body=box(1,1,118,110,radius=16)+box(33,12,54,54,fill='#F8FAFC',radius=13,stroke='#F8FAFC')+icon(name,43,22,34,name)+txt(60,92,label,13,'text',600,'middle')
 write(f'tools/{name}.svg',120,112,label,body)

def hero(mobile=False):
 w,h=(720,570) if mobile else (1440,480)
 p='<defs><linearGradient id="accent" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#38BDF8"/><stop offset="1" stop-color="#A78BFA"/></linearGradient><radialGradient id="glow"><stop stop-color="#37306B" stop-opacity=".65"/><stop offset="1" stop-color="#0D1424" stop-opacity="0"/></radialGradient><pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#34445F" opacity=".45"/></pattern></defs>'
 p+=box(1,1,w-2,h-2,fill='bg',radius=20)
 p+=f'<ellipse cx="{w-130}" cy="220" rx="390" ry="260" fill="url(#glow)"/><rect x="{w-500}" y="20" width="470" height="{h-40}" fill="url(#dots)"/>'
 x=44 if mobile else 64
 p+=txt(x,65,'DATA ANALYTICS  /  DATA ENGINEERING',17 if mobile else 18,'cyan',600)
 p+=txt(x,131 if mobile else 153,"Hi, I'm",27,'muted')
 if mobile:
  p+=txt(x-2,222,'Pruthvi',73,'text',700)+txt(x-2,303,'Raj Pudi',73,'text',700)
  p+=txt(x,365,'Reliable pipelines. Clear insights.',25,'muted')
  p+=box(x,415,632,96,fill='panel',radius=14)
  p+=txt(x+24,449,'ANALYZE',16,'cyan',600)+txt(x+24,481,'SQL · Power BI · Excel',21)
  p+=txt(x+337,449,'ENGINEER',16,'violet',600)+txt(x+337,481,'Python · Cloud · dbt',21)
 else:
  p+=txt(x-3,247,'Pruthvi Raj Pudi',76,'text',700)
  p+=txt(x,309,'Reliable pipelines. Clear insights.',29,'muted')
  p+=txt(x,395,'SQL & PYTHON',16,'cyan',600)+txt(x+205,395,'BI & REPORTING',16,'muted',600)+txt(x+440,395,'CLOUD & DBT',16,'violet',600)
  p+=box(900,94,470,290,fill='panel',radius=20)
  p+=txt(928,130,'FROM SOURCE TO INSIGHT',16,'muted',600)
  icons=[('python',930),('microsoft-azure',1038),('snowflake-icon',1146),('dbt-icon',1254)]
  for i,(name,ix) in enumerate(icons):
   p+=box(ix,173,70,70,fill='#F8FAFC',radius=16,stroke='#F8FAFC')+icon(name,ix+14,187,42,'hero'+str(i))
   if i<3:p+=f'<path d="M{ix+77} 208h24m-6-6 6 6-6 6" stroke="#61708C" stroke-width="2" fill="none"/>'
  p+=txt(928,294,'Ingest',17,'muted')+txt(1062,294,'Store',17,'muted')+txt(1189,294,'Model',17,'muted')
  p+=f'<path d="M928 320H1342" stroke="{C["border"]}"/>'
  p+=txt(928,354,'Better data. Better decisions.',20,'text',500)
 p+=f'<path d="M{x} {h-1}H{w-x}" stroke="url(#accent)" stroke-width="3"/>'
 write('hero-mobile.svg' if mobile else 'hero.svg',w,h,'Pruthvi Raj Pudi. Data analytics and data engineering. Reliable pipelines. Clear insights.',p)
for mobile in [False,True]:hero(mobile)

PROJECTS=[('olist','ENGINEERING · IN DEVELOPMENT','Olist marketplace pipeline','Python · Azure · Snowflake · dbt'),('sales','ANALYTICS · SALES & FINANCE','Sales & financial analysis','Excel · Power Query · Power Pivot · DAX'),('warehouse','ENGINEERING · DATA WAREHOUSING','CRM & ERP sales warehouse','SQL Server · T-SQL · ETL · Star schema'),('hr','ANALYTICS · PEOPLE & PERFORMANCE','HR analytics dashboard','Power BI · DAX · Data modeling')]
def art(slug,x,y):
 p=''
 if slug=='olist':
  for i,n in enumerate(['python','microsoft-azure','snowflake-icon','dbt-icon']):
   ix=x+i*81;p+=box(ix,y+25,56,56,fill='#F8FAFC',radius=12,stroke='#F8FAFC')+icon(n,ix+11,y+36,34,slug+str(i))
   if i<3:p+=f'<path d="M{ix+61} {y+53}h14" stroke="#5F7193" stroke-width="2"/>'
  p+=txt(x,y+119,'10 staging models',20,'cyan',600)
 elif slug=='sales':
  p+=icon('excel',x,y+25,65,'sales')
  for i in range(8):
   ix=x+100+(i%4)*43;iy=y+10+(i//4)*47
   p+=box(ix,iy,30,36,fill='tile',radius=5)+f'<path d="M{ix+7} {iy+12}h16m-16 6h11m-11 6h16" stroke="#7DD3FC" stroke-width="2"/>'
  p+=txt(x+100,y+119,'8 published reports',20,'cyan',600)
 elif slug=='warehouse':
  for i,(label,col) in enumerate([('BRONZE','#CD9371'),('SILVER','#C1CEDB'),('GOLD','#F8D47A')]):
   ix=x+i*106;p+=box(ix,y+18,93,65,fill='tile',radius=10)+f'<path d="M{ix+17} {y+41}h59m-59 11h59m-59 11h40" stroke="{col}" stroke-width="3"/>'+txt(ix+46,y+110,label,13,col,600,'middle')
 else:
  p+=f'<circle cx="{x+57}" cy="{y+58}" r="45" stroke="#24324B" stroke-width="12" fill="none"/><circle cx="{x+57}" cy="{y+58}" r="45" stroke="#A78BFA" stroke-width="12" fill="none" stroke-dasharray="45.52 237.22" transform="rotate(-90 {x+57} {y+58})" stroke-linecap="round"/>'
  p+=txt(x+57,y+64,'16.1%',21,'text',600,'middle')+txt(x+130,y+52,'1,470',37,'cyan',700)+txt(x+130,y+85,'employee records',17,'muted')+txt(x+57,y+130,'SAMPLE ATTRITION',12,'muted',500,'middle')
 return p
for slug,role,title,stack in PROJECTS:
 for mobile in [False,True]:
  w,h=(720,375) if mobile else (1200,225)
  p=box(1,1,w-2,h-2,fill='panel',radius=16)+txt(32,43,role,15,'cyan',600)
  p+=txt(32,98,title,32 if mobile else 36,'text',700)+txt(32,137 if mobile else 161,stack,17,'muted')
  p+=f'<path d="M{w-58} 39h19m-7-7 7 7-7 7" stroke="#A78BFA" stroke-width="2" fill="none"/>'
  if mobile:p+=art(slug,48,189)
  else:p+=f'<path d="M797 57v122" stroke="{C["border"]}"/>'+art(slug,835,55)
  write(f'projects/{slug}{"-mobile" if mobile else ""}.svg',w,h,title,p)
