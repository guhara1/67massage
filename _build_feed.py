# -*- coding: utf-8 -*-
"""매거진 RSS 2.0 피드 생성 → feed.xml (네이버·구글 빠른 발견용)."""
import re, glob, os
from datetime import datetime

DOMAIN = "https://67massage.netlify.app"
BASE = os.path.dirname(os.path.abspath(__file__))
WD = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
MO = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def rfc822(ymd):
    y,m,d = map(int, ymd.split("-"))
    dt = datetime(y,m,d,9,0,0)
    return f"{WD[dt.weekday()]}, {d:02d} {MO[m-1]} {y} 09:00:00 +0900"

def esc(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def main():
    items=[]
    for f in glob.glob(os.path.join(BASE,"magazine","*.html")):
        if f.endswith("index.html"): continue
        h=open(f,encoding="utf-8").read()
        slug=os.path.basename(f)[:-5]
        title=re.search(r"<title>(.*?)</title>",h,re.S).group(1).strip()
        title=re.split(r"\s*\|\s*", title)[0].strip()
        desc=(re.search(r'name="description"\s+content="(.*?)"',h,re.S) or [None,""])[1].strip()
        tm=re.search(r'<time datetime="([0-9-]+)"',h)
        date=tm.group(1) if tm else "2026-01-01"
        items.append((date, slug, title, desc))
    items.sort(reverse=True)  # 최신 글 먼저
    build = rfc822(items[0][0]) if items else rfc822("2026-06-04")
    rows=[]
    for date,slug,title,desc in items:
        url=f"{DOMAIN}/magazine/{slug}.html"
        rows.append(
            "  <item>\n"
            f"    <title>{esc(title)}</title>\n"
            f"    <link>{url}</link>\n"
            f"    <guid isPermaLink=\"true\">{url}</guid>\n"
            f"    <description>{esc(desc)}</description>\n"
            f"    <pubDate>{rfc822(date)}</pubDate>\n"
            "  </item>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
           '<channel>\n'
           '  <title>67 마사지 매거진</title>\n'
           f'  <link>{DOMAIN}/magazine/index.html</link>\n'
           f'  <atom:link href="{DOMAIN}/feed.xml" rel="self" type="application/rss+xml" />\n'
           '  <description>마사지 선택법·회복 건강 정보·지역 이용 가이드·셀프케어 — 67 마사지 관리사가 현장 경험으로 정리한 매거진</description>\n'
           '  <language>ko</language>\n'
           f'  <lastBuildDate>{build}</lastBuildDate>\n'
           + "\n".join(rows) + "\n"
           '</channel>\n</rss>\n')
    open(os.path.join(BASE,"feed.xml"),"w",encoding="utf-8").write(xml)
    print(f"feed.xml 생성: {len(items)}개 글, 최신 {items[0][0]}")

if __name__=="__main__":
    main()
