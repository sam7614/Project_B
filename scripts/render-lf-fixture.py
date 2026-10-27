"""Render a labelled development-fixture LF chart with ReportLab (no survey claims)."""
from pathlib import Path
import argparse,json,math,xml.etree.ElementTree as ET
from reportlab.graphics.shapes import Drawing,Line,String,Circle,Rect
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor

def drawing_for(summary):
    if summary.get('real_participants')!=0 or 'synthetic calculation fixture only'not in summary.get('purpose',''):raise ValueError('Only explicitly labelled development fixtures may be plotted')
    items=summary['items'];xcut=summary['lf_thresholds']['mean_importance'];ycut=summary['lf_thresholds']['mean_gap']
    if not items or not all(math.isfinite(float(i[k]))for i in items for k in ('mean_importance','mean_gap')):raise ValueError('Non-finite or missing plot values')
    if not 1<=xcut<=5 or not -4<=ycut<=4:raise ValueError('Invalid axis thresholds')
    W,H=760,540;left,bottom,width,height=90,100,585,335
    X=lambda v:left+(v-1)/4*width;Y=lambda v:bottom+(v+4)/8*height
    d=Drawing(W,H);d.add(Rect(0,0,W,H,fillColor=HexColor('#ffffff'),strokeColor=None))
    def label(x,y,text,size=10,color='#334155',anchor='start'):
        d.add(String(x,y,text,fontName='Helvetica',fontSize=size,fillColor=HexColor(color),textAnchor=anchor))
    label(40,H-30,'Locus for Focus - calculation fixture',19,'#0f172a');label(40,H-52,f"DEVELOPMENT ONLY | {int(summary['synthetic_case_ids'])} synthetic case IDs | {len(items)} dummy items | real respondents: 0",10,'#9a3412')
    for x in range(1,6):d.add(Line(X(x),bottom,X(x),bottom+height,strokeColor=HexColor('#e2e8f0'),strokeWidth=.6));label(X(x),bottom-20,str(x),10,anchor='middle')
    for y in range(-4,5):d.add(Line(left,Y(y),left+width,Y(y),strokeColor=HexColor('#e2e8f0'),strokeWidth=.6));label(left-15,Y(y)-3,str(y),10,anchor='end')
    d.add(Rect(left,bottom,width,height,fillColor=None,strokeColor=HexColor('#334155'),strokeWidth=1))
    d.add(Line(X(xcut),bottom,X(xcut),bottom+height,strokeColor=HexColor('#64748b'),strokeWidth=1.2,strokeDashArray=[5,4]))
    d.add(Line(left,Y(ycut),left+width,Y(ycut),strokeColor=HexColor('#64748b'),strokeWidth=1.2,strokeDashArray=[5,4]))
    for tx,ty,t in [(left+12,bottom+height-18,'LH'),(left+width-35,bottom+height-18,'HH'),(left+12,bottom+12,'LL'),(left+width-35,bottom+12,'HL')]:label(tx,ty,t,12,'#64748b')
    for i in items:
        x,y=float(i['mean_importance']),float(i['mean_gap'])
        if not 1<=x<=5 or not -4<=y<=4:raise ValueError('Point outside1..5/-4..4 axes')
        color='#b45309'if i.get('lf_boundary')else'#2563eb';d.add(Circle(X(x),Y(y),5,fillColor=HexColor(color),strokeColor=None));label(X(x)+10,Y(y)+7,f"{i['item_id']} ({x:.2f}, {y:.2f})",10)
    label(left+width/2,48,'Mean importance (1-5)',11,anchor='middle');label(left, bottom+height+12,'Mean discrepancy = importance - current (-4 to 4)',10)
    label(40,26,f'Equal-item-weight cuts: importance={xcut:.6f}; discrepancy={ycut:.6f}. Strict >; boundary flagged.',9)
    label(40,10,'Not an empirical needs result, a feature ranking, or evidence of educational effect.',9,'#9a3412')
    return d

def main():
    p=argparse.ArgumentParser();p.add_argument('summary');p.add_argument('--out',default='research/figures/lf-development-fixture.svg');a=p.parse_args();s=json.loads(Path(a.summary).read_text(encoding='utf-8'));out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);renderSVG.drawToFile(drawing_for(s),str(out));ET.parse(out);print(f'Rendered labelled fixture: {out}')
if __name__=='__main__':main()
