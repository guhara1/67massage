# -*- coding: utf-8 -*-
"""
2-tier 지역 구조 빌더 (구글 도어웨이 정책 대응)
- 독립 7개 권역(수원·동탄·용인·분당·오산·기흥·수지): 8섹션 풀 구조로 재생성
    1 H1·브레드크럼 / 2 도입문 / 3 커버범위(세부동·랜드마크·주차) / 4 이용패턴
    5 가격표(공통) / 6 지역 FAQ(고유) / 7 후기 스캐폴드(빈칸, 가짜 X) / 8 예약 CTA
- 하위 13개 동네: 상위 권역 앵커로 통합 → canonical + 리다이렉트, sitemap 제거
- FAQPage JSON-LD를 화면 FAQ와 동기화해 생성
"""
import json, os, datetime

DOMAIN = "https://67massage.xyz"
TODAY = "2026-06-04"
BASE = os.path.dirname(os.path.abspath(__file__))

# 하위동네 → (상위slug, 앵커, 라벨)  ※ 개별 풀페이지로 전환된 동네는 _build_locals.py가 담당
# 여기 남은 항목만 상위 앵커로 통합되는 noindex 리다이렉트로 유지한다.
CHILD = {
 "guundong":("suwon","guundong","구운동"),
 "pogok":("yongin","pogok","포곡"),
}

# ---- 공통 조각 ----
def header(root):
    return f"""<header class="header">
  <div class="wrap nav">
    <a class="brand" href="{root}index.html" aria-label="67 마사지 홈">
      <img class="brand-logo" src="{root}assets/images/logo-mark.png" alt="67 마사지" width="44" height="35" /><span class="mark">67<b>마사지</b></span><span class="sub">Premium&nbsp;Care</span>
    </a>
    <nav aria-label="주 메뉴"><ul class="menu">
      <li><a href="{root}services.html">서비스 안내 <i class="caret"></i></a>
        <div class="dropdown">
          <a href="{root}services/swedish.html">스웨디시 <span>전신 순환·이완 관리</span></a>
          <a href="{root}services/aroma.html">아로마 테라피 <span>블렌딩 오일 릴렉스</span></a>
          <a href="{root}services/deep.html">딥티슈 <span>뭉친 근육 집중 케어</span></a>
          <a href="{root}services/sports.html">스포츠 회복 <span>운동 후 컨디셔닝</span></a>
          <a href="{root}services/couple.html">커플·2인 <span>동시 출장마사지</span></a>
        </div></li>
      <li><a href="{root}areas.html">출장지역 <i class="caret"></i></a>
        <div class="dropdown mega">
          <a class="mega-all" href="{root}areas.html">전체 지역 보기 →</a>
          <div class="mega-cols">
            <div class="mega-col"><a class="mega-head" href="{root}areas/suwon.html">수원 출장마사지</a><a href="{root}areas/suwon-station.html">수원역</a><a href="{root}areas/ingyedong.html">인계동</a><a href="{root}areas/yeongtong.html">영통</a><a href="{root}areas/suwon.html">권선·장안·팔달·영통</a></div>
            <div class="mega-col"><a class="mega-head" href="{root}areas/yongin.html">용인 출장마사지</a><a href="{root}areas/suji.html">수지</a><a href="{root}areas/giheung.html">기흥</a><a href="{root}areas/singal.html">신갈</a><a href="{root}areas/dongbaek.html">동백</a><a href="{root}areas/cheoingu.html">처인구</a></div>
            <div class="mega-col"><a class="mega-head" href="{root}areas/bundang.html">성남·분당 출장마사지</a><a href="{root}areas/bundang.html">분당</a><a href="{root}areas/jeongja.html">정자역</a><a href="{root}areas/seohyeon.html">서현역</a><a href="{root}areas/sunae.html">수내역</a><a href="{root}areas/migeum.html">미금역</a></div>
            <div class="mega-col"><a class="mega-head" href="{root}areas/dongtan.html">화성·동탄 출장마사지</a><a href="{root}areas/dongtan.html">동탄</a><a href="{root}areas/byeongjeom.html">병점</a><a href="{root}areas/hyangnam.html">향남</a></div>
            <div class="mega-col"><a class="mega-head" href="{root}areas/osan.html">오산 출장마사지</a><a href="{root}areas/osan-station.html">오산역</a><a href="{root}areas/gweoldong.html">궐동</a><a href="{root}areas/segyo.html">세교</a></div>
          </div>
        </div></li>
      <li><a href="{root}magazine/index.html">매거진 <i class="caret"></i></a>
        <div class="dropdown">
          <a href="{root}magazine/index.html#guide">마사지 가이드 <span>기법·선택법 정리</span></a>
          <a href="{root}magazine/index.html#health">효능·건강 <span>근거 기반 회복 정보</span></a>
          <a href="{root}magazine/index.html#local">지역 가이드 <span>동네별 이용 안내</span></a>
          <a href="{root}magazine/index.html#selfcare">셀프케어 <span>집에서 하는 관리</span></a>
          <a href="{root}magazine/index.html#review">이용 후기 <span>실제 방문 경험담</span></a>
        </div></li>
      <li><a href="{root}about.html">회사소개</a></li>
      <li><a href="{root}guide.html">이용안내</a></li>
    </ul></nav>
    <a class="btn btn-gold nav-cta" href="tel:0508-202-4717">예약 0508-202-4717</a>
    <button class="burger" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
  </div>
</header>
<aside class="drawer" id="drawer" aria-label="모바일 메뉴">
  <p class="scrim-label">서비스</p>
  <details><summary>서비스 안내 <i class="caret"></i></summary><div class="sub-links">
    <a href="{root}services/swedish.html">스웨디시</a><a href="{root}services/aroma.html">아로마 테라피</a>
    <a href="{root}services/deep.html">딥티슈</a><a href="{root}services/sports.html">스포츠 회복</a>
    <a href="{root}services/couple.html">커플·2인</a></div></details>
  <details><summary>출장지역 <i class="caret"></i></summary><div class="sub-links">
    <a href="{root}areas.html">전체 지역 보기</a>
    <a class="reg" href="{root}areas/suwon.html">수원 출장마사지</a>
    <a href="{root}areas/suwon-station.html">· 수원역</a><a href="{root}areas/ingyedong.html">· 인계동</a><a href="{root}areas/yeongtong.html">· 영통</a><a href="{root}areas/suwon.html">· 권선·장안·팔달·영통</a>
    <a class="reg" href="{root}areas/yongin.html">용인 출장마사지</a>
    <a href="{root}areas/suji.html">· 수지</a><a href="{root}areas/giheung.html">· 기흥</a><a href="{root}areas/singal.html">· 신갈</a><a href="{root}areas/dongbaek.html">· 동백</a><a href="{root}areas/cheoingu.html">· 처인구</a>
    <a class="reg" href="{root}areas/bundang.html">성남·분당 출장마사지</a>
    <a href="{root}areas/bundang.html">· 분당</a><a href="{root}areas/jeongja.html">· 정자역</a><a href="{root}areas/seohyeon.html">· 서현역</a><a href="{root}areas/sunae.html">· 수내역</a><a href="{root}areas/migeum.html">· 미금역</a>
    <a class="reg" href="{root}areas/dongtan.html">화성·동탄 출장마사지</a>
    <a href="{root}areas/dongtan.html">· 동탄</a><a href="{root}areas/byeongjeom.html">· 병점</a><a href="{root}areas/hyangnam.html">· 향남</a>
    <a class="reg" href="{root}areas/osan.html">오산 출장마사지</a>
    <a href="{root}areas/osan-station.html">· 오산역</a><a href="{root}areas/gweoldong.html">· 궐동</a><a href="{root}areas/segyo.html">· 세교</a></div></details>
  <details><summary>매거진 <i class="caret"></i></summary><div class="sub-links">
    <a href="{root}magazine/index.html#guide">마사지 가이드</a><a href="{root}magazine/index.html#health">효능·건강</a>
    <a href="{root}magazine/index.html#local">지역 가이드</a><a href="{root}magazine/index.html#selfcare">셀프케어</a>
    <a href="{root}magazine/index.html#review">이용 후기</a></div></details>
  <a href="{root}about.html">회사소개</a><a href="{root}guide.html">이용안내</a>
  <a class="btn btn-gold" style="margin-top:26px;justify-content:center;" href="tel:0508-202-4717">전화예약 0508-202-4717</a>
</aside>
<div class="scrim" aria-hidden="true"></div>
"""

def footer(root):
    return f"""<footer class="footer"><div class="wrap">
  <div class="footer-top">
    <div class="foot-brand"><a class="brand" href="{root}index.html"><img class="brand-logo" src="{root}assets/images/logo-mark.png" alt="67 마사지" width="44" height="35" /><span class="mark">67<b>마사지</b></span></a>
      <p class="desc">검증된 관리사가 직접 방문하는 경기 남부 프리미엄 출장 관리 서비스. 정찰제와 위생 1회용 원칙을 지킵니다.</p>
      <p class="foot-contact"><a class="foot-tel" href="tel:0508-202-4717">0508-202-4717</a><span>24시간 연중무휴 전화예약</span></p></div>
    <div><h5>서비스 코스</h5><ul class="fl">
      <li><a href="{root}services/swedish.html">스웨디시</a></li><li><a href="{root}services/aroma.html">아로마 테라피</a></li>
      <li><a href="{root}services/deep.html">딥티슈</a></li><li><a href="{root}services/sports.html">스포츠 회복</a></li>
      <li><a href="{root}services/couple.html">커플·2인</a></li></ul></div>
    <div><h5>출장지역</h5><ul class="fl">
      <li><a href="{root}areas.html">전체 지역 보기</a></li><li><a href="{root}areas/suwon.html">수원 출장마사지</a></li>
      <li><a href="{root}areas/yongin.html">용인 출장마사지</a></li><li><a href="{root}areas/bundang.html">성남·분당 출장마사지</a></li>
      <li><a href="{root}areas/dongtan.html">화성·동탄 출장마사지</a></li><li><a href="{root}areas/osan.html">오산 출장마사지</a></li></ul></div>
    <div><h5>고객지원</h5><ul class="fl">
      <li><a href="{root}guide.html">이용안내</a></li><li><a href="{root}about.html">회사소개</a></li>
      <li><a href="{root}magazine/index.html">매거진</a></li>
      <li><a href="{root}privacy.html">개인정보처리방침</a></li><li><a href="{root}terms.html">이용약관</a></li></ul></div>
  </div>
  <div class="biz">
    <b>상호</b> 67 마사지 &nbsp;|&nbsp; <b>회사</b> YH LAB &nbsp;|&nbsp; <b>대표</b> 김유환 &nbsp;|&nbsp; <b>사업자등록번호</b> 815-26-00585<br>
    <b>주소</b> 경기도 파주시 청석로 268 &nbsp;|&nbsp; <b>대표전화</b> <a href="tel:0508-202-4717" style="color:var(--gold-hi)">0508-202-4717</a> &nbsp;|&nbsp; <b>운영시간</b> 24시간 연중무휴<br>
    © <span data-year>2026</span> 67 마사지 (YH LAB). All rights reserved.
  </div>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"HealthAndBeautyBusiness","name":"67 마사지","legalName":"YH LAB","url":"https://67massage.xyz/","logo":"https://67massage.xyz/assets/images/logo-mark.png","image":"https://67massage.xyz/assets/og-cover.jpg","telephone":"+82-50-8202-4717","taxID":"815-26-00585","founder":{{"@type":"Person","name":"김유환"}},"address":{{"@type":"PostalAddress","addressCountry":"KR","addressRegion":"경기도","streetAddress":"파주시 청석로 268"}},"areaServed":[{{"@type":"City","name":"수원"}},{{"@type":"City","name":"용인"}},{{"@type":"City","name":"성남"}},{{"@type":"City","name":"화성"}},{{"@type":"City","name":"오산"}},{{"@type":"City","name":"기흥"}}],"openingHoursSpecification":{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}},"priceRange":"₩₩"}}</script>
</div></footer>
<span class="fab-label" aria-hidden="true">전화예약</span>
<a class="fab-call" href="tel:0508-202-4717" aria-label="전화로 예약하기 0508-202-4717">
  <svg viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>
</a>
<script src="{root}assets/js/reviews.js"></script>
<script src="{root}assets/js/main.js"></script>
"""

PRICE = """<section class="section areas-band" id="price"><div class="wrap">
  <span class="eyebrow">PRICE</span>
  <h2 class="section-title">투명한 정찰 가격표</h2>
  <p class="lead">모든 코스는 아래 금액 그대로 안내되며, 방문 현장에서 추가 요금을 요구하지 않습니다. 코스 선택이 고민되시면 전화로 컨디션을 알려주세요.</p>
  <div class="price-grid">
    <article class="price-card"><span class="tier">BASIC · 타이</span><h3>타이 베이직</h3>
      <p class="desc">오일 없이 압과 스트레칭 중심으로 진행합니다. 짧은 시간 안에 몸의 긴장을 가볍게 풀고 싶을 때 안내합니다.</p>
      <div class="price-rows"><div class="price-row"><span class="t">60분</span><span class="v">80,000원</span></div><div class="price-row"><span class="t">90분</span><span class="v">100,000원</span></div><div class="price-row"><span class="t">120분</span><span class="v">120,000원</span></div></div></article>
    <article class="price-card"><span class="tier">AROMA · 오일</span><h3>아로마 릴랙스</h3>
      <p class="desc">부드러운 오일 터치로 편안한 휴식을 돕는 코스입니다. 강한 압보다 차분한 컨디션 관리를 원할 때 적합합니다.</p>
      <div class="price-rows"><div class="price-row"><span class="t">60분</span><span class="v">90,000원</span></div><div class="price-row"><span class="t">90분</span><span class="v">110,000원</span></div><div class="price-row"><span class="t">120분</span><span class="v">130,000원</span></div></div></article>
    <article class="price-card"><span class="tier">MOOD · 감성</span><h3>무드 오일 케어</h3>
      <p class="desc">조용한 흐름과 섬세한 압 조절을 중심으로 구성합니다. 휴식감과 분위기를 함께 고려하는 오일 코스입니다.</p>
      <div class="price-rows"><div class="price-row"><span class="t">60분</span><span class="v">100,000원</span></div><div class="price-row"><span class="t">90분</span><span class="v">120,000원</span></div><div class="price-row"><span class="t">120분</span><span class="v">140,000원</span></div></div></article>
    <article class="price-card"><span class="best">BEST</span><span class="tier">PREMIUM · 전신</span><h3>프리미엄 전신</h3>
      <p class="desc">건식과 오일 흐름을 함께 조율하는 긴 코스입니다. 여유 있는 시간으로 전신 관리를 받고 싶을 때 추천합니다.</p>
      <div class="price-rows"><div class="price-row"><span class="t">60분</span><span class="v">110,000원</span></div><div class="price-row"><span class="t">90분</span><span class="v">130,000원</span></div><div class="price-row"><span class="t">120분</span><span class="v">150,000원</span></div><div class="price-row"><span class="t">150분</span><span class="v">180,000원</span></div></div></article>
    <article class="price-card"><span class="tier">K-CARE · 지정</span><h3>한국인 스페셜</h3>
      <p class="desc">한국인 매니저 상담 매칭 코스입니다. 사전 통화로 선호 강도와 진행 방식을 더 정확히 조율합니다.</p>
      <div class="price-rows"><div class="price-row"><span class="t">60분</span><span class="v">150,000원</span></div><div class="price-row"><span class="t">90분</span><span class="v">190,000원</span></div></div></article>
    <article class="price-card"><span class="tier">MEN'S · 전용</span><h3>맨즈 밸런스</h3>
      <p class="desc">남성 고객 상담에 맞춘 전용 코스입니다. 컨디션, 선호 압, 이용 시간을 확인한 뒤 가능 일정을 안내합니다.</p>
      <div class="price-rows"><div class="price-row"><span class="t">60분</span><span class="v">100,000원</span></div><div class="price-row"><span class="t">90분</span><span class="v">130,000원</span></div><div class="price-row"><span class="t">120분</span><span class="v">160,000원</span></div></div></article>
  </div>
  <p class="price-note">표시 금액은 운영 권역 내 정찰가 기준입니다. 심야·예약 상황에 따라 가능 시간이 달라질 수 있어, 최종 안내는 통화로 확정해 드립니다.</p>
</div></section>
"""

def head(slug, name, faqs):
    url = f"{DOMAIN}/areas/{slug}.html"
    title = f"{name} 출장마사지 | 67 마사지 · 24시간 방문 예약"
    desc = f"{name} 출장마사지 - 검증된 관리사가 {name} 전역에 직접 방문합니다. 정찰제·위생 1회용. 세부 동네·이용 안내·자주 묻는 질문까지. 24시간 예약 0508-202-4717."
    service = {"@context":"https://schema.org","@type":"Service","serviceType":"출장마사지","name":f"{name} 출장마사지",
        "areaServed":{"@type":"Place","name":name},
        "provider":{"@type":"HealthAndBeautyBusiness","name":"67 마사지","telephone":"+82-50-8202-4717","url":DOMAIN},
        "url":url,"description":desc}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"홈","item":f"{DOMAIN}/"},
        {"@type":"ListItem","position":2,"name":"출장지역","item":f"{DOMAIN}/areas.html"},
        {"@type":"ListItem","position":3,"name":name,"item":url}]}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    j = lambda d: json.dumps(d, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LT3JPBSCEB"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-LT3JPBSCEB');</script>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="theme-color" content="#16120e" />
<link rel="icon" href="../assets/favicon.ico" sizes="any" />
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg" />
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="../assets/favicon-16.png" />
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{url}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="author" content="67 마사지 (YH LAB)" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="67 마사지" />
<meta property="og:locale" content="ko_KR" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{DOMAIN}/assets/og/{slug}.jpg" />
<meta property="og:image:alt" content="{name} 출장마사지 | 67 마사지" />
<meta property="og:image:width" content="1200" /><meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="{DOMAIN}/assets/og/{slug}.jpg" />
<meta name="twitter:image:alt" content="{name} 출장마사지 | 67 마사지" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
<link rel="stylesheet" href="../assets/css/style.css" />
<script type="application/ld+json">{j(service)}</script>
<script type="application/ld+json">{j(crumb)}</script>
<script type="application/ld+json">{j(faq)}</script>
</head>
<body>
"""

def coverage_block(cov):
    # cov: list of (anchor, label, paragraph). anchor='' -> 앵커 없는 일반 동네
    out=[]
    for anchor,label,para in cov:
        aid = f' id="{anchor}"' if anchor else ''
        out.append(f'  <div class="cov-item"><h3{aid} style="font-family:var(--font-display);font-size:1.18rem;margin:0 0 6px;color:var(--gold-hi)">{label}</h3><p style="color:var(--paper-dim)">{para}</p></div>')
    return "\n".join(out)

def faq_block(faqs):
    items="".join(f"<dt>{q}</dt><dd>{a}</dd>" for q,a in faqs)
    return f'<dl class="faq" style="margin-top:24px">{items}</dl>'

def build_parent(slug, d):
    root="../"
    name=d["name"]
    from urllib.parse import quote
    sms = "?body=" + quote(f"[67 마사지 {name} 후기] 지역/동네: , 코스(예 60분 아로마): , 별점(1~5): , 내용: ")
    H = head(slug, name, d["faqs"])
    body = f"""{header(root)}
<section class="page-hero"><div class="wrap">
  <p class="crumb"><a href="../index.html">홈</a><span>›</span><a href="../areas.html">출장지역</a><span>›</span>{name}</p>
  <span class="eyebrow" style="margin-top:14px">SERVICE AREA</span>
  <h1>{name} 출장마사지</h1>
  <p class="lead">{d['lead']}</p>
  <div class="hero-actions" style="margin-top:30px">
    <a class="btn btn-gold" href="tel:0508-202-4717">{name} 전화예약 0508-202-4717</a>
    <a class="btn btn-ghost" href="../services.html">서비스 메뉴 보기</a>
  </div>
</div></section>

<section class="section" style="padding-top:34px;padding-bottom:8px"><div class="wrap" style="max-width:880px">
  <span class="eyebrow">WHY HERE</span>
  <h2 class="section-title">{name}에 방문 수요가 많은 이유</h2>
  <p class="lead" style="margin-top:18px">{d['intro1']}</p>
  <p style="margin-top:18px;color:var(--paper-dim)">{d['intro2']}</p>
</div></section>

<section class="section" style="padding-top:18px"><div class="wrap" style="max-width:880px">
  <span class="eyebrow">COVERAGE</span>
  <h2 class="section-title">{name} 커버 범위 · 세부 권역</h2>
  <p class="lead" style="margin-top:18px">{d['cov_intro']}</p>
  <div class="cov-grid" style="margin-top:26px;display:grid;gap:20px">
{coverage_block(d['coverage'])}
  </div>
  <div class="callout" style="margin-top:28px;background:var(--ink-2);border:1px solid var(--line);border-radius:14px;padding:22px 24px">
    <strong style="color:var(--gold-hi)">도착·주차 안내</strong><br>{d['parking']}
  </div>
</div></section>

<section class="section" style="padding-top:18px"><div class="wrap" style="max-width:880px">
  <span class="eyebrow">HOW PEOPLE USE</span>
  <h2 class="section-title">{name} 이용 패턴과 추천 코스</h2>
  <p class="lead" style="margin-top:18px">{d['usage']}</p>
  <p style="margin-top:18px;color:var(--paper-dim)">{d['peak']}</p>
</div></section>

{PRICE}
<section class="section" style="padding-top:34px"><div class="wrap" style="max-width:780px">
  <span class="eyebrow">FAQ</span>
  <h2 class="section-title">{name} 자주 묻는 질문</h2>
  {faq_block(d['faqs'])}
</div></section>

<section class="section areas-band" id="reviews" data-area="{slug}" data-name="67 마사지 · {name} 출장마사지"><div class="wrap" style="max-width:780px">
  <span class="eyebrow">REVIEW</span>
  <h2 class="section-title">{name} 실제 이용 후기</h2>
  <p class="lead" style="margin-top:16px">{name}에서 받은 <strong style="color:var(--gold-hi)">실제 이용 후기</strong>만 게재합니다. 모든 후기는 이용 고객의 게재 동의를 받아 과장·왜곡 없이 그대로 싣습니다.</p>
  <div data-review-list class="review-list"></div>
  <div data-review-empty class="review-empty">
    아직 등록된 후기가 없습니다. {name}에서 관리를 받으신 뒤 후기를 남겨주시면, 다음 이용자에게 가장 정확한 정보가 됩니다. (게재 동의하신 후기만 노출됩니다.)
  </div>
  <div class="review-actions">
    <a class="btn btn-gold" href="sms:0508-202-4717{sms}">{name} 후기 남기기</a>
    <a class="btn btn-ghost" href="tel:0508-202-4717">{name} 예약 0508-202-4717</a>
  </div>
</div></section>

{footer(root)}
</body></html>
"""
    return H + body

def build_redirect(slug):
    parent, anchor, label = CHILD[slug]
    parent_name = PARENTS[parent]["name"]
    target = f"{parent}.html#{anchor}"
    canonical = f"{DOMAIN}/areas/{parent}.html"
    title = f"{label} 출장마사지 | 67 마사지"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<link rel="icon" href="../assets/favicon.ico" sizes="any" />
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg" />
<link rel="canonical" href="{canonical}" />
<meta http-equiv="refresh" content="0; url={target}" />
<meta name="robots" content="noindex, follow" />
<script>location.replace("{target}");</script>
<link rel="stylesheet" href="../assets/css/style.css" />
</head>
<body>
<div class="wrap" style="padding:80px 0;text-align:center">
<p style="color:var(--paper-dim)">{label} 출장마사지 안내는 <a href="{target}" style="color:var(--gold-hi)">{parent_name} 출장마사지 · {label} 세부 안내</a>로 통합되었습니다.</p>
<p style="margin-top:20px"><a class="btn btn-gold" href="tel:0508-202-4717">전화예약 0508-202-4717</a></p>
</div>
</body></html>
"""

# ---- 부모 7개 데이터 ----
PARENTS = {
"suwon": dict(name="수원",
  lead="수원 출장마사지를 찾으신다면, 67 마사지가 검증된 관리사를 수원 전역에 직접 보내 정찰제로 안내합니다. 인계동·수원역·영통·구운동까지 동일 정찰가로 방문합니다.",
  intro1="수원은 인구 120만이 넘는 경기도 최대 도시로, 인계동 번화가와 수원역 상권, 영통·광교 업무지구, 권선·매탄·구운동 주거지가 한 도시 안에 공존합니다. 생활 반경이 넓고 약속·회식이 잦아, 일과를 마친 뒤 이동 없이 자택이나 숙소에서 받는 출장마사지 수요가 특히 높습니다.",
  intro2="67 마사지는 수원 전역을 단일 정찰 권역으로 운영합니다. 권역 안에서는 별도 출장비가 없고, 예약 시 안내된 코스 금액 그대로 결제하시면 됩니다. 아래는 수원 안에서도 이용 성격이 뚜렷이 다른 세부 권역별 안내입니다.",
  cov_intro="수원은 동네마다 방문 동선과 이용 시간대가 다릅니다. 아래 세부 권역 안내를 참고하시면 본인 동네에 맞는 이용 그림이 그려집니다.",
  coverage=[
    ("yeongtong","영통","삼성디지털시티와 광교테크노밸리가 가까워 연구·개발 직군이 밀집한 주거·업무지입니다. 종일 앉아 일한 뒤 목·어깨를 푸는 야간 예약이 많고, 신축 아파트 단지가 많아 진입이 수월합니다."),
    ("suwon-station","수원역","AK플라자·롯데몰과 호텔이 모인 교통·상권 허브입니다. 출장·여행객의 숙소 방문과 심야 체크인 예약이 잦아, 객실 호수와 체크인 상태를 미리 주시면 도착 후 곧바로 진행됩니다."),
    ("ingyedong","인계동","나혜석거리 번화가와 시청 인근입니다. 모임·회식 뒤 자택이나 인근 숙소에서 받는 심야 예약이 많아, 밤 시간대 도심 진입 동선에 익숙합니다."),
    ("guundong","구운동","권선구 서남부의 조용한 주거 밀집지입니다. 번잡함 없이 퇴근 후 집에서 편히 받는 이용이 고르고, 늦은 밤에는 조용한 방문을 원칙으로 합니다."),
  ],
  parking="인계동·수원역 도심은 시간대별 정체와 주차 제약이 있어, 출발 시 도착 예정 시간을 먼저 안내드립니다. 광교·영통 신축 단지는 방문자 동선이 비교적 수월하며, 단지·동·출입구를 함께 주시면 도착이 정확합니다.",
  usage="처음이거나 가벼운 피로 회복이 목적이면 타이 베이직·아로마 릴랙스 60·90분이 무난합니다. 종일 앉아 일하는 영통·광교 직장인은 목·어깨·등을 깊게 푸는 프리미엄 전신 90·120분 만족도가 높습니다. 코스가 고민되면 한국인 스페셜 상담으로 선호 압을 맞춰 진행합니다.",
  peak="수원은 도심 회식·약속이 늦게까지 이어져 평일 저녁부터 자정 무렵 예약이 집중됩니다. 광교·영통은 퇴근 직후, 인계동·수원역은 모임 이후 시간대 문의가 많습니다. 67 마사지는 예약한 관리사가 그대로 방문하며, 직접 닿는 소모품은 1인 1회용으로 교체합니다.",
  faqs=[("수원 어느 동까지 방문하나요?","인계동·수원역·영통·구운동·권선·매탄·광교 등 수원 전역을 운영 권역으로 둡니다."),
        ("수원 도심은 차가 막히는데 도착 시간을 믿을 수 있나요?","출발 시 도착 예정 시간을 안내드리고, 정체가 예상되면 미리 연락드립니다."),
        ("출장비가 따로 있나요?","수원 권역 내에서는 별도 출장비 없이 정찰가 그대로 이용하실 수 있습니다."),
        ("심야에도 예약되나요?","연중무휴 24시간 예약을 받으며, 수원역 인근 심야 체크인 방문도 가능합니다.")]),

"dongtan": dict(name="동탄",
  lead="동탄 출장마사지가 처음이라도 괜찮습니다. 67 마사지가 동탄1·2신도시 전역에 검증된 관리사를 직접 보내 정찰제로 안내합니다.",
  intro1="동탄은 화성시에 조성된 1·2신도시로, 동탄역과 메타폴리스를 중심으로 신축 아파트·오피스텔이 밀집한 대표 신도시입니다. 신혼 가구와 젊은 직장인 비중이 높고 단지 구조가 잘 정비돼 있어, 관리사가 동을 찾고 진입하기 수월합니다.",
  intro2="67 마사지는 동탄1신도시와 동탄2신도시를 모두 단일 정찰 권역으로 운영합니다. 맞벌이·교대 근무 가구가 많아 늦은 밤과 새벽 예약 비중이 높고, 그에 맞춘 심야 응대 경험이 충분합니다.",
  cov_intro="동탄은 권역이 넓어 단지 위치에 따라 도착 시간이 달라집니다. 아래 세부 구역 안내를 참고해 주세요.",
  coverage=[
    ("","동탄역·메타폴리스","SRT 동탄역과 메타폴리스 상업지구 일대입니다. 역세권 오피스텔과 출장객 숙소 방문이 잦고, 야간 도착 예약이 많습니다."),
    ("","동탄1신도시","반석산·센트럴파크 인근의 초기 조성 주거지입니다. 가족 단위 거주가 많아 저녁 시간대 예약이 고르게 분포합니다."),
    ("","동탄2신도시·호수공원","동탄호수공원을 중심으로 계속 확장 중인 신축 단지 지역입니다. 단지명과 동 번호 체계가 복잡한 곳이 있어 위치를 함께 주시면 좋습니다."),
    ("byeongjeom","병점","동탄과 맞닿은 화성·수원 경계의 역세권 주거지입니다. 병점역 인근 아파트·빌라가 밀집해 퇴근 후 자택에서 받는 저녁 예약이 고르며, 동탄 권역과 같은 정찰가로 방문합니다."),
    ("hyangnam","향남","화성 남부 향남읍의 택지지구와 제약·산업단지가 함께 있는 지역입니다. 교대 근무자의 야간 예약과 신축 단지 가족 단위 이용이 많아, 단지명·동과 출입 방법을 함께 주시면 도착이 정확합니다."),
  ],
  parking="동탄2신도시는 단지가 넓고 동 번호 체계가 복잡한 곳이 있어, 예약 시 단지명과 동·출입구를 함께 알려주시면 도착이 더 정확합니다. 동탄역 SRT 이용 출장객의 인근 숙소 방문도 가능합니다.",
  usage="맞벌이·교대 근무로 수면이 부족한 분이 많아 수면·피로 회복용 아로마 릴랙스·무드 오일 케어 90분이 인기입니다. 운동 인구가 많아 컨디셔닝을 겸한 프리미엄 전신 120분도 자주 선택됩니다. 부부가 함께 받고 싶으면 예약 시 인원을 미리 알려주시면 동시 배정으로 안내합니다.",
  peak="잠들기 전 받는 야간·새벽 예약 비중이 다른 신도시보다 높습니다. 67 마사지는 배정 관리사 정보를 사전에 안내드리고, 소모품은 1인 1회용으로 관리합니다. 신도시 특성상 야간에는 조용한 방문을 원칙으로 합니다.",
  faqs=[("동탄1·2신도시 모두 방문하나요?","네, 두 신도시 전역을 동일 정찰가로 방문합니다."),
        ("단지가 많아 위치 찾기가 어렵습니다.","단지명과 동·출입구를 알려주시면 정확히 도착하며, 출발 시 예정 시간을 문자로 안내드립니다."),
        ("부부가 함께 받을 수 있나요?","예약 시 인원을 알려주시면 관리사 동시 배정으로 안내해 드립니다."),
        ("늦은 밤에도 가능한가요?","맞벌이·교대 근무가 많은 지역이라 야간·심야 예약을 상시 받습니다.")]),

"yongin": dict(name="용인",
  lead="이동 없이 받는 용인 출장마사지, 67 마사지가 수지·기흥·처인 전역에 약속한 시간에 직접 방문해 드립니다.",
  intro1="용인은 처인구·기흥구·수지구 세 개 구로 이루어진 면적이 넓은 도시입니다. 수지의 주거 밀집지, 기흥의 삼성전자·역세권, 처인의 구도심과 전원 지역까지 구마다 생활 모습이 크게 달라, 방문 동선을 구 단위로 나눠 운영합니다.",
  intro2="67 마사지는 용인 전역을 단일 정찰 권역으로 두되, 면적이 넓은 만큼 도착 시간을 정확히 약속드리는 것을 가장 중요하게 봅니다. 아래는 용인 안에서 이용 성격이 다른 세부 권역 안내입니다.",
  cov_intro="용인은 같은 시라도 구 사이 이동 거리가 길어, 동네를 구체적으로 알려주실수록 도착이 빨라집니다.",
  coverage=[
    ("","수지구(죽전·풍덕천·동천)","신분당선으로 강남까지 닿는 주거 밀집지입니다. 강남 출퇴근 직장인의 야간 예약이 많습니다. (수지 전용 안내 페이지를 따로 운영합니다.)"),
    ("","기흥구(기흥역·동백·신갈)","삼성전자 기흥캠퍼스와 역세권, 신도시 주거가 어우러진 지역입니다. (기흥 전용 안내 페이지를 따로 운영합니다.)"),
    ("cheoingu","처인구","용인시청이 있는 행정 중심이자 면적이 가장 넓은 구입니다. 김량장동 구도심과 외곽 단독·전원주택까지 이동 거리가 다양해, 동을 구체적으로 주시면 가장 가까운 관리사를 배정합니다."),
    ("pogok","포곡","처인구 포곡읍, 에버랜드 인근의 전원·펜션 지역입니다. 시간을 넉넉히 잡는 120·150분 장코스 선호가 뚜렷하며, 진입로·주차 위치를 함께 주시면 도착이 정확합니다."),
  ],
  parking="구 사이 이동 거리가 길어, 예약 시 동(죽전·기흥역·김량장동·포곡 등)을 구체적으로 알려주시면 가장 가까운 관리사를 배정해 도착을 앞당깁니다. 외곽 단독·전원주택은 진입로 안내를 함께 주시면 좋습니다.",
  usage="강남 출퇴근이 많은 수지는 누적된 목·허리 피로를 푸는 프리미엄 전신이, 연구·생산직이 많은 기흥은 어깨 긴장을 다스리는 아로마 릴랙스가 잘 맞습니다. 처인·포곡 전원 주택에서는 여유 있게 받는 120·150분 장코스 선호가 뚜렷합니다.",
  peak="수지·기흥은 저녁 예약이 몰리고, 처인·포곡 외곽은 주말 장코스 비중이 큽니다. 67 마사지는 가장 가까운 관리사를 배정해 이동 시간을 줄이고, 출발 시 예정 시간을 다시 안내드립니다. 소모품은 1인 1회용으로 관리합니다.",
  faqs=[("용인 어느 구까지 가나요?","수지·기흥·처인 전역을 운영 권역으로 둡니다. 수지·기흥은 전용 안내 페이지를 따로 운영합니다."),
        ("처인구 외곽도 방문하나요?","김량장동·포곡 등 외곽도 방문하며, 이동 거리에 따른 도착 시간을 미리 안내드립니다."),
        ("출장비가 붙나요?","용인 권역 내에서는 별도 출장비 없이 정찰가 그대로입니다."),
        ("도착 시간을 정확히 알 수 있나요?","동을 구체적으로 주시면 가장 가까운 관리사를 배정해 시간을 앞당깁니다.")]),

"bundang": dict(name="분당",
  lead="67 마사지는 분당 출장마사지를 정찰제와 위생 1회용 원칙으로 운영하며, 정자·서현·수내·미금 전역에서 24시간 전화 예약을 받습니다.",
  intro1="분당은 성남시에 계획적으로 조성된 1기 신도시로, 정자·서현·수내·미금·이매 등 안정적인 역세권 주거지가 분당선과 신분당선을 따라 이어집니다. 판교 테크노밸리와 가까워 IT·전문직 직장인이 많고, 정주 환경과 상권이 성숙해 방문 수요가 꾸준합니다.",
  intro2="67 마사지는 분당 전역을 단일 정찰 권역으로 운영합니다. 야근이 잦은 직장인 비중이 높아 늦은 밤 예약이 많고, 심야 응대를 상시 운영합니다. 아래는 분당 안에서 이용 성격이 다른 역세권별 안내입니다.",
  cov_intro="분당은 역을 중심으로 생활권이 나뉩니다. 본인 생활권 역세권 안내를 참고해 주세요.",
  coverage=[
    ("migeum","미금역","분당선·신분당선이 만나는 환승 거점입니다. 강남·판교 출퇴근 직장인의 늦은 밤 예약이 많은 역세권으로, 오피스텔 공동현관 출입 방법을 주시면 도착이 빠릅니다."),
    ("sunae","수내역","중앙공원과 학원가(정평)를 낀 주거 중심 생활권입니다. 가사·업무로 지친 어깨를 푸는 저녁 예약이 고르게 분포합니다."),
    ("jeongja","정자역","카페거리와 주상복합이 모인 상권 역세권입니다. 모임 후 인근에서 받는 심야 예약이 잦아, 주상복합 엘리베이터 출입 방법을 미리 주시면 좋습니다."),
    ("seohyeon","서현역","AK플라자를 낀 분당 최대 번화가입니다. 약속이 늦게 끝나는 밤 시간대 예약이 몰리며, 정확한 건물·출입구를 주시면 도착 시간을 줄일 수 있습니다."),
  ],
  parking="역세권 주상복합·오피스텔은 공동현관·엘리베이터 출입 방법을 미리 주시면 지체가 없습니다. 중앙공원 인근 단지는 방문자 주차 안내를 함께 드리며, 번화가는 밤 시간대 정체를 감안해 예정 시간을 먼저 안내드립니다.",
  usage="장시간 모니터 앞에 앉아 일하는 분이 많아 목·어깨·등을 집중적으로 푸는 프리미엄 전신 90·120분이 가장 선호됩니다. 스트레스·수면 문제를 함께 다루고 싶으면 무드 오일 케어가 적합합니다. 강한 압을 원하면 사전 상담에서 알려주시면 딥티슈 강도로 조절합니다.",
  peak="판교·강남 출퇴근 직장인이 많아 평일 밤 9시 이후 예약이 가장 많습니다. 67 마사지는 예약한 관리사가 그대로 방문하며, 타월·시트는 1인 1회용으로 교체합니다.",
  faqs=[("분당 어느 역세권까지 가나요?","정자·서현·수내·미금 등 분당 전역을 방문합니다."),
        ("주상복합은 출입이 까다로운데요?","공동현관·엘리베이터 출입 방법을 주시면 지체 없이 도착합니다."),
        ("판교 인근도 가능한가요?","판교 인접 숙소 방문도 가능합니다."),
        ("야근 후 늦은 시간 예약되나요?","직장인 비중이 높아 심야 예약을 상시 운영합니다.")]),

"osan": dict(name="오산",
  lead="오산 출장마사지를 찾으신다면, 67 마사지가 세교신도시·운암지구·궐동·산업단지 일대에 검증된 관리사를 직접 보내 정찰제로 안내합니다.",
  intro1="오산은 수원·동탄과 맞닿은 도시로, 세교신도시의 신축 단지와 운암지구 주거지, 여러 산업단지, 그리고 오산대 인근 대학가가 함께 자리합니다. 제조·물류 종사자와 신도시 가구, 1인 가구가 섞여 있어 합리적인 정찰가로 받는 방문 수요가 꾸준합니다.",
  intro2="67 마사지는 오산 전역을 단일 정찰 권역으로 운영합니다. 교대·야간 근무자가 많은 산업단지 특성상 늦은 시간 예약 응대에 익숙합니다.",
  cov_intro="오산은 신도시·산업단지·대학가가 섞여 동네별 이용 성격이 다릅니다.",
  coverage=[
    ("segyo","세교신도시","계속 확장 중인 신축 주거지입니다. 가족 단위 거주가 많아 저녁 예약이 고르며, 단지명과 동을 함께 주시면 도착이 정확합니다."),
    ("osan-station","운암지구·오산역","오산역 인근 주거·상권 지역입니다. 역세권 숙소 방문과 직장인 이용이 많습니다."),
    ("gweoldong","궐동","오산대 인근 대학가·원룸 밀집지입니다. 1인 가구의 간편한 60분 코스 예약이 많고, 비슷한 원룸 건물이 많아 건물명·호수와 공동현관 출입 방법을 함께 주시면 도착이 빠릅니다."),
  ],
  parking="세교신도시 신축 단지는 단지명과 동을, 산업단지·기숙사는 출입 절차를 함께 주시면 도착이 정확합니다. 궐동 원룸가는 야간 유동인구가 많아 출발 시 예정 시간을 안내드립니다.",
  usage="현장·생산직처럼 몸을 많이 쓰는 분께는 종아리·허리·어깨를 함께 푸는 프리미엄 전신이, 가볍게 피로만 덜고 싶은 날은 타이 베이직 60분이 잘 맞습니다. 궐동 대학가는 부담 없는 60분 코스 선호가 뚜렷합니다.",
  peak="산업단지 교대 근무에 맞춰 심야·새벽 예약 비중이 높습니다. 67 마사지는 예약한 관리사가 그대로 방문하며, 직접 닿는 소모품은 1인 1회용으로 교체합니다.",
  faqs=[("오산 어디까지 방문하나요?","세교신도시·운암지구·오산역·궐동·산업단지 일대를 방문합니다."),
        ("산업단지 기숙사도 가능한가요?","출입 절차를 주시면 기숙사·숙소 방문도 가능합니다."),
        ("출장비가 있나요?","오산 권역 내에서는 별도 출장비 없이 정찰가입니다."),
        ("교대 근무라 새벽에 받고 싶어요.","심야·새벽 예약을 상시 받습니다.")]),

"giheung": dict(name="기흥",
  lead="67 마사지는 기흥 출장마사지를 정찰제와 위생 1회용 원칙으로 운영하며, 기흥역·동백·신갈 전역에서 24시간 전화 예약을 받습니다.",
  intro1="기흥은 용인 기흥구의 중심으로, 삼성전자 기흥캠퍼스와 기흥역세권, 동백·신갈·구갈·보정의 주거지가 함께 자리합니다. 생산·연구 교대 근무 인구가 많아 낮과 밤의 생활 리듬이 다양하고, 시간대를 가리지 않는 방문 수요가 꾸준합니다.",
  intro2="67 마사지는 기흥구 전역을 단일 정찰 권역으로 운영합니다. 교대 근무자의 새벽 예약 사례가 많아 심야·새벽 응대가 안정적입니다. 아래는 기흥 안에서 이용 성격이 다른 세부 권역 안내입니다.",
  cov_intro="기흥은 캠퍼스 역세권과 신도시 주거지가 섞여 동네별 이용 시간대가 다릅니다.",
  coverage=[
    ("","기흥역·구갈·보정","삼성전자 캠퍼스와 기흥역 환승 인구가 많은 지역입니다. 캠퍼스 주변 오피스텔·원룸 방문과 교대 근무 새벽 예약이 많습니다."),
    ("singal","신갈","신갈오거리와 신갈분기점을 낀 교통 요지입니다. 경부·영동고속도로가 만나 인근에서의 진입이 빠르고, 장거리 운전 뒤 허리·어깨를 푸는 저녁 예약이 많습니다."),
    ("dongbaek","동백","동백호수공원을 중심으로 한 계획 주거지구입니다. 가족 단위 거주 비중이 높아 늦은 저녁 예약이 고르고, 비슷한 단지명이 많아 정확한 단지·동을 주시면 좋습니다."),
  ],
  parking="기흥역 역세권은 환승 인구가 많아 인근 숙소 방문이 잦고, 동백·신갈 단지는 동·출입구를 주시면 도착이 빠릅니다. 캠퍼스 주변 원룸·오피스텔도 방문 가능합니다.",
  usage="장시간 서서 일하거나 같은 자세를 반복하는 직군이 많아 종아리·허리·어깨를 함께 푸는 프리미엄 전신 만족도가 높습니다. 야간 근무 후 빠른 회복에는 아로마 릴랙스·무드 오일 케어 90분이 잘 맞습니다.",
  peak="교대 근무 인구가 많아 새벽 예약 사례가 꾸준합니다. 67 마사지는 예약한 관리사가 그대로 방문하며, 소모품은 1인 1회용으로 교체합니다. 새벽 시간대에도 도착 예정 시간을 미리 안내드립니다.",
  faqs=[("기흥구 어디까지 가나요?","기흥역·동백·신갈·구갈·보정 등 기흥구 전역입니다."),
        ("삼성 캠퍼스 인근 원룸도 가능한가요?","캠퍼스 주변 오피스텔·원룸 방문도 가능합니다."),
        ("새벽 근무 후 예약되나요?","교대 근무가 많아 새벽 예약을 상시 받습니다."),
        ("출장비가 붙나요?","기흥구 권역 내에서는 별도 출장비 없이 정찰가입니다.")]),

"suji": dict(name="수지",
  lead="이동 없이 받는 수지 출장마사지, 67 마사지가 죽전·풍덕천·동천 전역에 약속한 시간에 직접 방문해 드립니다.",
  intro1="수지는 용인 수지구의 주거 밀집지로, 죽전·풍덕천·동천·상현 일대에 아파트 단지가 촘촘히 들어서 있습니다. 신분당선으로 강남까지 빠르게 닿아 서울로 출퇴근하는 직장인이 많고, 학원가가 발달해 가족 단위 정주 인구가 두텁습니다.",
  intro2="67 마사지는 수지구 전역을 단일 정찰 권역으로 운영합니다. 강남 출퇴근으로 귀가가 늦은 직장인이 많아 야간 예약 비중이 높고, 단지가 조밀해 관리사 진입과 동선이 수월합니다.",
  cov_intro="수지는 단지가 조밀해 동·출입구만 정확히 주시면 도착이 빠릅니다. 주요 생활권 안내입니다.",
  coverage=[
    ("","죽전·보정","죽전역과 카페거리 인근 주거지입니다. 가족 단위와 직장인 이용이 고르고, 단지 진입이 수월합니다."),
    ("","풍덕천·신봉","수지구청 인근 중심 주거지입니다. 학원가가 발달해 저녁 시간대 가족 단위 이용이 많습니다."),
    ("","동천·상현","신분당선 역세권 주거지입니다. 강남 출퇴근 직장인의 늦은 밤 예약이 특히 많습니다."),
  ],
  parking="죽전·풍덕천·동천은 단지가 밀집해 동·출입구만 정확히 주시면 도착이 빠릅니다. 신분당선 역세권 오피스텔은 공동현관 출입 방법을 함께 주시면 좋습니다.",
  usage="장거리 출퇴근으로 허리·골반과 어깨에 피로가 누적되는 분이 많아 깊게 풀어내는 프리미엄 전신 90·120분이 가장 선호됩니다. 잠들기 전 긴장을 가라앉히는 무드 오일 케어, 가벼운 관리에는 타이 베이직·아로마 릴랙스 60분도 충분합니다.",
  peak="강남 출퇴근으로 귀가가 늦어 평일 밤 시간대 예약이 가장 많습니다. 출근이 이른 가구를 위해 이른 아침 예약도 받습니다. 67 마사지는 배정 관리사 정보를 사전에 안내드리고, 타월·시트는 1인 1회용으로 관리합니다.",
  faqs=[("수지구 어디까지 방문하나요?","죽전·풍덕천·동천·상현 등 수지구 전역입니다."),
        ("강남 출퇴근이라 늦게 끝나요. 가능한가요?","귀가가 늦은 직장인이 많은 지역이라 야간 예약을 상시 받습니다."),
        ("출장비가 있나요?","수지구 권역 내에서는 별도 출장비 없이 정찰가입니다."),
        ("이른 아침도 가능한가요?","출근이 이른 가구를 위해 이른 아침 예약도 받습니다.")]),
}

def write_sitemap():
    pages = [("/","daily","1.0"),("/services.html","monthly","0.9"),("/areas.html","weekly","0.9"),
             ("/about.html","monthly","0.7"),("/guide.html","monthly","0.7"),
             ("/magazine/index.html","weekly","0.8")]
    mag = ["desk-neck-care","dongtan-guide","first-time-outcall","flat-rate-policy","foam-rolling-basics",
           "hygiene-checklist","lower-back-deeptissue","massage-duration","night-stretch-5min","sleep-recovery",
           "suwon-guide","swedish-vs-aroma","yongin-guide"]
    for m in mag: pages.append((f"/magazine/{m}.html","monthly","0.6"))
    for p in PARENTS: pages.append((f"/areas/{p}.html","monthly","0.8"))
    rows=[]
    for loc,cf,pr in pages:
        rows.append(f"  <url>\n    <loc>{DOMAIN}{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"
    open(os.path.join(BASE,"sitemap.xml"),"w",encoding="utf-8").write(xml)
    return len(pages)

def main():
    adir=os.path.join(BASE,"areas")
    for slug,d in PARENTS.items():
        open(os.path.join(adir,f"{slug}.html"),"w",encoding="utf-8").write(build_parent(slug,d))
        print("PARENT:",slug)
    for slug in CHILD:
        open(os.path.join(adir,f"{slug}.html"),"w",encoding="utf-8").write(build_redirect(slug))
        print("REDIRECT:",slug,"->",CHILD[slug][0],"#"+CHILD[slug][1])
    n=write_sitemap()
    print("sitemap urls:",n)

if __name__=="__main__":
    main()
