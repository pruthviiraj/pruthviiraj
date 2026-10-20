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

# A quiet visual anchor for the profile. The README keeps all portfolio copy as
# native Markdown so it remains accessible and scales with GitHub's interface.
for theme, background, line, accent, muted in [
 ('light', '#F8FAFC', '#D9E2EC', '#2563EB', '#64748B'),
 ('dark', '#0D1424', '#28354D', '#60A5FA', '#A6B4CB'),
]:
 body=f'<rect width="1180" height="250" rx="16" fill="{background}"/>'
 body+=f'<path d="M148 125H1032" stroke="{line}" stroke-width="2"/>'
 body+=f'<path d="M319 125H469M711 125H861" stroke="{accent}" stroke-width="2"/>'
 for x, radius, fill in [(148,38,accent),(498,50,background),(741,50,background),(1032,38,accent)]:
  body+=f'<circle cx="{x}" cy="125" r="{radius}" fill="{fill}" stroke="{accent}" stroke-width="2"/>'
 body+=f'<circle cx="148" cy="125" r="11" fill="{background}"/><circle cx="1032" cy="125" r="11" fill="{background}"/>'
 body+=f'<path d="M476 106h44v38h-44zM719 106h44v38h-44z" fill="none" stroke="{accent}" stroke-width="2"/>'
 body+=f'<path d="M490 118h16m-16 12h16m227-12h16m-16 12h16" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>'
 for x, height in [(949,26),(967,48),(985,34)]:
  body+=f'<path d="M{x} {151-height}v{height}" stroke="{accent}" stroke-width="7" stroke-linecap="round"/>'
 body+=f'<path d="M182 85h73M925 165h73" stroke="{line}" stroke-width="2"/>'
 body+=txt(218,80,'SOURCE',16,muted,600,'middle')+txt(620,80,'MODELS',16,muted,600,'middle')+txt(962,187,'REPORTING',16,muted,600,'middle')
 write(f'profile-visual-{theme}.svg',1180,250,'Abstract data workflow from sources to models and reporting.',body)

# Motion system: a controlled 600ms header reveal and one continuous skill
# ribbon. Text outside these visuals remains native Markdown for accessibility.
PREMIUM_MOTION="""<style>
@keyframes rise{0%{opacity:0;transform:translateY(18px)}100%{opacity:1;transform:translateY(0)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes blink{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes marquee{from{transform:translateX(0)}to{transform:translateX(-2016px)}}
.rise{animation:rise .6s cubic-bezier(.2,0,0,1) both}.d1{animation-delay:.10s}.d2{animation-delay:.20s}.d3{animation-delay:.30s}
.float{animation:float 4s cubic-bezier(.4,0,.2,1) infinite}.pulse{animation:blink 2.4s ease-in-out infinite}
.marquee{animation:marquee 24s linear infinite}
@media(prefers-reduced-motion:reduce){.rise,.float,.pulse,.marquee{animation:none!important;transform:none;opacity:1}}
</style>"""

body=PREMIUM_MOTION+'<rect width="1180" height="430" rx="22" fill="#101827"/><path d="M0 350C220 280 350 460 580 370S940 270 1180 350V430H0Z" fill="#15223A"/>'
body+='<g opacity=".55"><path d="M650 70h430M650 150h430M650 230h430M650 310h430" stroke="#263651" stroke-width="1"/><path d="M760 40v300M870 40v300M980 40v300" stroke="#263651" stroke-width="1"/></g>'
body+=txt(70,74,'DATA PORTFOLIO',15,'#93C5FD',700)+f'<g class="rise">'+txt(70,166,'Pruthvi Raj Pudi',58,'#F8FAFC',700)+f'</g>'
body+=f'<g class="rise d1">'+txt(70,218,'Data Analytics  ·  Data Engineering',24,'#CBD5E1',500)+f'</g>'
body+=f'<g class="rise d2">'+txt(70,270,'From operational data to clear reporting.',22,'#A6B4CB',400)+f'</g>'
body+=f'<g class="rise d3">'+txt(70,332,'E-commerce  /  Sales  /  Workforce',16,'#93C5FD',600)+f'</g>'
body+='<g class="float"><rect x="706" y="107" width="138" height="98" rx="16" fill="#15223A" stroke="#60A5FA" stroke-width="2"/><circle cx="744" cy="143" r="12" fill="#60A5FA"/><path d="M768 137h46m-46 16h31" stroke="#CBD5E1" stroke-width="5" stroke-linecap="round"/></g>'
body+='<g class="float" style="animation-delay:.5s"><rect x="895" y="175" width="150" height="108" rx="16" fill="#15223A" stroke="#A78BFA" stroke-width="2"/><path d="M926 247v-26m24 26v-47m24 47v-33m24 33v-67" stroke="#A78BFA" stroke-width="9" stroke-linecap="round"/></g>'
body+='<path d="M844 156h52m-9-8 9 8-9 8" stroke="#60A5FA" stroke-width="2" fill="none"/><circle class="pulse" cx="870" cy="156" r="5" fill="#93C5FD"/>'
write('motion-header.svg',1180,430,'Pruthvi Raj Pudi — Data Analytics and Data Engineering portfolio.',body,animated=True)

def pill(name,label,width,accent):
 body=f'<rect x="1" y="1" width="{width-2}" height="46" rx="23" fill="#101827" stroke="#334155"/>'
 body+=f'<circle cx="24" cy="24" r="6" fill="{accent}"/>'+txt(40,30,label,16,'#F8FAFC',600)+txt(width-20,30,'↗',17,'#CBD5E1',600,'middle')
 write(f'pills/{name}.svg',width,48,label+' link',body)

pill('resume','Resume',150,'#38BDF8')
pill('email','Email',136,'#A78BFA')
pill('linkedin','LinkedIn',158,'#60A5FA')
pill('portfolio','Portfolio',170,'#F8FAFC')

SKILLS=[('python','Python'),('microsoft-azure','Azure'),('snowflake-icon','Snowflake'),('dbt-icon','dbt'),('sql-server','SQL Server'),('postgresql','PostgreSQL'),('microsoft-power-bi','Power BI'),('excel','Excel'),('pandas-icon','pandas'),('looker-icon','Looker Studio'),('git-icon','Git'),('github-icon','GitHub')]
def skill_chips(offset):
 body=''
 for i,(name,label) in enumerate(SKILLS):
  x=offset+i*168
  body+=f'<g><rect x="{x}" y="20" width="150" height="62" rx="13" fill="#162239" stroke="#2A3A55"/>'
  body+=icon(name,x+16,37,28,'ribbon'+str(offset)+'-'+str(i))+txt(x+54,58,label,16,'#E2E8F0',600)+'</g>'
 return body

body=PREMIUM_MOTION+'<clipPath id="ribbon-clip"><rect width="1180" height="102" rx="14"/></clipPath><rect width="1180" height="102" rx="14" fill="#101827"/>'
body+='<g clip-path="url(#ribbon-clip)"><g class="marquee">'+skill_chips(0)+skill_chips(2016)+'</g></g>'
write('motion-skills.svg',1180,102,'Scrolling toolkit: Python, Azure, Snowflake, dbt, SQL Server, PostgreSQL, Power BI, Excel, pandas, Looker Studio, Git, and GitHub.',body,animated=True)
