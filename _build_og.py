# -*- coding: utf-8 -*-
"""지역·서비스 페이지별 OG 이미지(1200x630) 생성 → assets/og/{slug}.jpg
브랜드 다크 배경 + 골드 글로우 + 엠블럼 + '{이름} 출장마사지' + 연락처."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from _build_tier import PARENTS
from _build_locals import LOCALS
from _build_services import SERVICES

BASE = os.path.dirname(os.path.abspath(__file__))
OGDIR = os.path.join(BASE, "assets", "og")
os.makedirs(OGDIR, exist_ok=True)
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
W, H = 1200, 630
INK=(22,18,14); GOLD_HI=(230,207,156); GOLD=(201,168,106); PAPER=(246,241,232); DIM=(176,168,150)

def font(sz): return ImageFont.truetype(FONT, sz)

def make_bg():
    bg = Image.new("RGB",(W,H),INK)
    # 골드 글로우 2개(우상단·좌하단)
    g = ImageOps.invert(Image.radial_gradient("L")).resize((900,900))
    for (cx,cy,scale,op) in [(W-120,-120,900,70),(-160,H-120,820,55)]:
        layer=Image.new("RGB",(W,H),GOLD)
        mask=Image.new("L",(W,H),0)
        gg=g.resize((scale,scale)); mask.paste(gg,(cx-scale//2,cy-scale//2))
        mask=mask.point(lambda v: int(v*op/255))
        bg=Image.composite(layer,bg,mask)
    d=ImageDraw.Draw(bg)
    # 인셋 골드 보더
    d.rectangle([28,28,W-28,H-28], outline=(120,98,55), width=2)
    # 엠블럼
    try:
        em=Image.open(os.path.join(BASE,"assets","images","logo-mark.png")).convert("RGBA")
        eh=120; ew=round(em.width*eh/em.height); em=em.resize((ew,eh))
        bg.paste(em,(70,66),em)
    except Exception: pass
    return bg

BG = make_bg()

def wrap(draw, text, fnt, maxw):
    words=text.split(" "); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=fnt)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def render(slug, title, tagline):
    im=BG.copy(); d=ImageDraw.Draw(im)
    # 상단 eyebrow
    d.text((72,210),"67 MASSAGE · 경기 남부 출장마사지",font=font(26),fill=GOLD)
    # 타이틀(필요시 줄바꿈)
    tf=font(96); lines=wrap(d,title,tf,W-150)
    if len(lines)>2:  # 너무 길면 폰트 축소
        tf=font(72); lines=wrap(d,title,tf,W-150)
    y=258
    for ln in lines:
        d.text((70,y),ln,font=tf,fill=GOLD_HI); y+=tf.size+10
    # 골드 악센트 라인
    d.rectangle([74,y+8,74+90,y+12],fill=GOLD)
    # 태그라인
    d.text((72,y+34),tagline,font=font(34),fill=DIM)
    # 하단 연락처
    d.text((72,H-92),"24시간 예약 · 정찰제",font=font(28),fill=PAPER)
    d.text((72,H-54),"0508-202-4717",font=font(40),fill=GOLD_HI)
    out=os.path.join(OGDIR,f"{slug}.jpg")
    im.convert("RGB").save(out,"JPEG",quality=86,optimize=True,progressive=True)
    return out

def main():
    n=0
    AREA_TAG="검증된 관리사 · 정찰제 · 24시간 방문"
    for slug,d in PARENTS.items():
        render(slug, f"{d['name']} 출장마사지", AREA_TAG); n+=1
    for slug,d in LOCALS.items():
        pname=PARENTS[d['parent']]['name']
        render(slug, f"{d['name']} 출장마사지", f"{pname} 권역 · 정찰제 · 24시간 방문"); n+=1
    SVC_TAG={"swedish":"전신 순환·이완 코스","aroma":"블렌딩 오일 릴렉스 코스",
             "deep":"뭉친 근육 집중 케어","sports":"운동 후 컨디셔닝","couple":"동시 방문 2인 코스"}
    for slug,d in SERVICES.items():
        render(slug, f"{d['name']} 출장마사지", SVC_TAG.get(slug,"프리미엄 출장 코스")); n+=1
    print(f"OG 이미지 {n}개 생성 → assets/og/")

if __name__=="__main__":
    main()
