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
 body=box(1,1,30,30,fill='#F8FAFC',radius=7,stroke='#E2E8F0')+icon(name,5,5,22,name)
 write(f'tools-small/{name}.svg',32,32,label,body)

def header(mobile=False):
 w,h=(720,210) if mobile else (1200,190)
 x=38 if mobile else 48
 body='<defs><linearGradient id="glow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111C30"/><stop offset="1" stop-color="#15172E"/></linearGradient></defs>'
 body+=f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#glow)" stroke="#28354D"/>'
 body+=f'<path d="M{x} 1H{w-x}" stroke="#7C9BF5" stroke-width="2"/>'
 body+=txt(x,88 if mobile else 85,'Pruthvi Raj Pudi',49 if mobile else 52,'text',700)
 body+=txt(x,138 if mobile else 131,'Data Analytics  ·  Data Engineering',23 if mobile else 24,'muted')
 if not mobile:
  body+=txt(w-x,91,'SQL  /  PYTHON',15,'cyan',500,'end')
  body+=txt(w-x,123,'POWER BI  /  CLOUD',15,'violet',500,'end')
 write('profile-header-mobile.svg' if mobile else 'profile-header.svg',w,h,'Pruthvi Raj Pudi. Data analytics and data engineering.',body)

for mobile in [False,True]:header(mobile)

# Fixed-width cards sit side by side on desktop and wrap on narrow screens.
import textwrap
PROJECTS = [
 ('olist','DATA ENGINEERING · IN PROGRESS','Olist data pipeline','Python and dbt code to load e-commerce data into Snowflake. Includes 10 models. Validation and reports are in progress.','Python · Azure · Snowflake · dbt','View project'),
 ('sales','DATA ANALYSIS','Sales & finance reports','Eight Excel reports on sales and profit. Found a $54.9M gap to the 2021 sales target.','Excel · Power Query · Power Pivot','View reports'),
 ('warehouse','DATA ENGINEERING','Sales data warehouse','Combines customer and sales data from two systems in SQL Server. Includes checks for missing and duplicate records.','SQL Server · SQL · Data modeling','View project'),
 ('hr','DATA ANALYSIS','HR dashboard','Four Power BI pages covering 1,470 employees in a sample dataset, with 16 measures for analysis.','Power BI · DAX · Data modeling','View dashboard'),
]
for slug,category,title,description,stack,link in PROJECTS:
 for mobile in [False,True]:
  w,h=720,460 if mobile else 370
  body=box(10,10,w-20,h-20,fill='panel',radius=12)
  body+=txt(32,38,category,18,'cyan',500)
  body+=txt(32,96 if mobile else 91,title,40 if mobile else 36,'text',700)
  lines=textwrap.wrap(description,width=38 if mobile else 44,break_long_words=False)
  for i,line in enumerate(lines):body+=txt(32,(156 if mobile else 145)+i*(42 if mobile else 36),line,32 if mobile else 27,'muted')
  body+=txt(32,h-69,stack,22,'dim')
  body+=txt(32,h-28,link+' →',26,'cyan',500)
  write(f'cards/{slug}{"-mobile" if mobile else ""}.svg',w,h,title+'. '+description,body)
