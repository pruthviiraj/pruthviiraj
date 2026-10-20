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

# Premium motion system: each visual uses a 600ms reveal and low-amplitude
# parallel movement. There are no large container cards or decorative sweeps.
MOTION="""<style>
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes lane{0%,100%{transform:translateX(0)}50%{transform:translateX(28px)}}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes draw{from{stroke-dashoffset:160}to{stroke-dashoffset:0}}
.rise{animation:rise .6s cubic-bezier(.2,0,0,1) both}.d1{animation-delay:.10s}.d2{animation-delay:.20s}.d3{animation-delay:.30s}
.lane{animation:lane 5s cubic-bezier(.4,0,.2,1) infinite}.l2{animation-delay:.55s}.l3{animation-delay:1.1s}.glow{animation:glow 2.8s ease-in-out infinite}.draw{stroke-dasharray:160;animation:draw 1.1s cubic-bezier(.2,0,0,1) both}
@media(prefers-reduced-motion:reduce){.rise,.lane,.glow,.draw{animation:none!important;transform:none;opacity:1;stroke-dashoffset:0}}
</style>"""

def theme_header(theme, ink, muted, grid, blue, violet):
 body=MOTION
 body+=f'<g opacity=".55"><path d="M694 44h410M694 110h410M694 176h410M694 242h410" stroke="{grid}" stroke-width="1"/><path d="M790 18v260M900 18v260M1010 18v260" stroke="{grid}" stroke-width="1"/></g>'
 body+=f'<g class="rise">'+txt(68,82,'PRUTHVI RAJ PUDI',58,ink,700)+f'</g>'
 body+=f'<g class="rise d1">'+txt(70,132,'Data Analytics  ·  Data Engineering',24,muted,500)+f'</g>'
 body+=f'<g class="rise d2">'+txt(70,180,'Building clear paths from operational data to reporting.',20,muted,400)+f'</g>'
 body+=f'<g class="rise d3">'+txt(70,234,'E-commerce  /  Sales  /  Workforce',15,blue,700)+f'</g>'
 for y, color, delay in [(86,blue,''),(156,violet,' l2'),(226,blue,' l3')]:
  body+=f'<path d="M690 {y}h370" stroke="{grid}" stroke-width="2"/><g class="lane{delay}"><circle cx="746" cy="{y}" r="9" fill="{color}"/><path d="M765 {y}h102" stroke="{color}" stroke-width="3" stroke-linecap="round"/><circle class="glow" cx="885" cy="{y}" r="6" fill="{color}"/></g>'
 body+=f'<path class="draw" d="M1034 66v180" stroke="{blue}" stroke-width="4" fill="none"/><path d="M1008 246h52" stroke="{violet}" stroke-width="4"/><circle cx="1034" cy="66" r="8" fill="{ink}" stroke="{blue}" stroke-width="4"/>'
 write(f'motion-header-{theme}.svg',1180,300,'Pruthvi Raj Pudi — Data Analytics and Data Engineering portfolio.',body,animated=True)

theme_header('light','#0F172A','#475569','#D9E2EC','#2563EB','#7C3AED')
theme_header('dark','#F8FAFC','#A6B4CB','#28354D','#60A5FA','#A78BFA')

def pill_icon(kind, color):
 if kind=='resume': return f'<path d="M15 11h14l6 6v20H15zM29 11v7h7M20 25h10m-10 5h10" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
 if kind=='email': return f'<rect x="13" y="15" width="24" height="18" rx="3" fill="none" stroke="{color}" stroke-width="2"/><path d="m15 18 10 8 10-8" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
 if kind=='linkedin': return f'<rect x="14" y="12" width="23" height="23" rx="3" fill="none" stroke="{color}" stroke-width="2"/><circle cx="20" cy="19" r="1.8" fill="{color}"/><path d="M19 24v7m6-7v7m0-4c0-4 7-4 7 0v4" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
 return f'<rect x="13" y="13" width="24" height="20" rx="3" fill="none" stroke="{color}" stroke-width="2"/><path d="m20 19-4 4 4 4m10-8 4 4-4 4" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'

def pill(name,label,width,accent):
 body=f'<rect x="1" y="1" width="{width-2}" height="46" rx="23" fill="#101827" stroke="#334155"/>'
 body+=pill_icon(name,accent)+txt(48,30,label,16,'#F8FAFC',600)
 write(f'pills/{name}.svg',width,48,label+' link',body)

pill('resume','Resume',150,'#38BDF8')
pill('email','Email',136,'#A78BFA')
pill('linkedin','LinkedIn',158,'#60A5FA')
pill('portfolio','Portfolio',170,'#F8FAFC')

SKILLS=[('python','Python'),('microsoft-azure','Azure'),('snowflake-icon','Snowflake'),('dbt-icon','dbt'),('sql-server','SQL Server'),('postgresql','PostgreSQL'),('microsoft-power-bi','Power BI'),('excel','Excel'),('pandas-icon','pandas'),('looker-icon','Looker Studio'),('git-icon','Git'),('github-icon','GitHub')]
def parallel_skills(theme, ink, muted, grid, chip):
 body=MOTION+f'<g opacity=".8"><path d="M18 47h1144M18 107h1144M18 167h1144" stroke="{grid}" stroke-width="2"/></g>'
 for lane in range(3):
  body+=f'<g class="lane l{lane+1}">'
  for slot,(name,label) in enumerate(SKILLS[lane*4:(lane+1)*4]):
   x=75+slot*260;y=lane*60+20
   body+=f'<circle cx="{x}" cy="{y+27}" r="20" fill="{chip}" stroke="{grid}"/>'
   body+=icon(name,x-11,y+16,22,'parallel-'+theme+'-'+str(lane)+'-'+str(slot))
   body+=txt(x+31,y+33,label,17,ink,600)
  body+='</g>'
 write(f'motion-skills-{theme}.svg',1180,214,'Parallel toolkit lanes with Python, Azure, Snowflake, dbt, SQL Server, PostgreSQL, Power BI, Excel, pandas, Looker Studio, Git, and GitHub.',body,animated=True)

parallel_skills('light','#1E293B','#64748B','#D9E2EC','#F8FAFC')
parallel_skills('dark','#E2E8F0','#A6B4CB','#28354D','#162239')

def project_tracks(theme, ink, muted, grid, colors):
 body=MOTION
 names=[('Olist pipeline','Python · Azure · Snowflake · dbt'),('Sales analysis','Excel · targets · profit'),('Sales warehouse','SQL Server · quality checks'),('HR dashboard','Power BI · sample workforce data')]
 for i,((label,detail),color) in enumerate(zip(names,colors)):
  y=34+i*66
  body+=f'<path d="M240 {y}h860" stroke="{grid}" stroke-width="2"/><g class="lane l{(i%3)+1}"><circle cx="280" cy="{y}" r="8" fill="{color}"/><path d="M304 {y}h96" stroke="{color}" stroke-width="3" stroke-linecap="round"/><circle class="glow" cx="418" cy="{y}" r="5" fill="{color}"/></g>'
  body+=txt(24,y+5,label,19,ink,700)+txt(470,y+5,detail,16,muted,500)
 write(f'projects-parallel-{theme}.svg',1180,266,'Four equal project tracks: Olist pipeline, sales analysis, sales warehouse, and HR dashboard.',body,animated=True)

project_tracks('light','#1E293B','#64748B','#D9E2EC',['#2563EB','#C0841A','#A16207','#0F9D58'])
project_tracks('dark','#F1F5F9','#A6B4CB','#28354D',['#60A5FA','#FACC15','#F59E0B','#34D399'])

def activity_motion(theme, ink, muted, grid, blue, violet):
 body=MOTION+f'<path d="M20 152h1140M20 98h1140M20 44h1140" stroke="{grid}" stroke-width="1"/>'
 heights=[35,72,51,99,64,118,82,138,104,154]
 for i,height in enumerate(heights):
  x=72+i*104
  color=blue if i%2==0 else violet
  body+=f'<path class="draw" style="animation-delay:{i*.05}s" d="M{x} 166v-{height}" stroke="{color}" stroke-width="18" stroke-linecap="round"/>'
 body+=txt(22,196,'ACTIVITY MOTION',15,muted,700)+txt(1158,196,'Live GitHub metrics below',15,muted,500,'end')
 write(f'activity-motion-{theme}.svg',1180,214,'Animated activity bars that introduce the live GitHub account metrics below.',body,animated=True)

activity_motion('light','#1E293B','#64748B','#D9E2EC','#2563EB','#7C3AED')
activity_motion('dark','#F1F5F9','#A6B4CB','#28354D','#60A5FA','#A78BFA')
