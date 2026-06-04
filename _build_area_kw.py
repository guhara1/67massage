# -*- coding: utf-8 -*-
"""
지역 페이지 히어로 첫 문단(.lead)에 '지역명+출장마사지' 키워드 문장을 1개 자연스럽게 덧붙인다.
H1/타이틀/설명/JSON-LD에는 이미 키워드가 있으므로, 첫 문단 신호만 보강한다.
멱등: 이미 '출장마사지'가 lead에 있으면 건너뛴다. 과최적화 방지를 위해 문장은 1개만 추가.
"""
import re, glob, os

NAMES = {
 "suwon":"수원","dongtan":"동탄","yongin":"용인","bundang":"분당","yeongtong":"영통",
 "giheung":"기흥","suji":"수지","osan":"오산","suwon-station":"수원역","ingyedong":"인계동",
 "guundong":"구운동","gweoldong":"궐동","cheoingu":"처인구","pogok":"포곡","singal":"신갈",
 "dongbaek":"동백","migeum":"미금역","sunae":"수내역","jeongja":"정자역","seohyeon":"서현역",
}

# 4개 어투를 번갈아 사용해 동일 문장 반복(템플릿화)을 줄인다.
VARIANTS = [
 "{n} 출장마사지를 찾으신다면, 67 마사지가 검증된 관리사를 {n} 전역에 직접 보내 정찰제로 안내합니다.",
 "67 마사지는 {n} 출장마사지를 정찰제와 위생 1회용 원칙으로 운영하며, 24시간 전화 예약을 받습니다.",
 "이동 없이 받는 {n} 출장마사지, 67 마사지가 약속한 시간에 가장 편안한 공간으로 직접 방문해 드립니다.",
 "{n} 출장마사지가 처음이라도 괜찮습니다. 전화로 코스와 시간을 알려주시면 컨디션에 맞춰 안내해 드립니다.",
]

LEAD_RE = re.compile(r'(<h1>[^<]*출장마사지</h1>\s*<p class="lead">)(.*?)(</p>)', re.S)

def main():
    base = os.path.join(os.path.dirname(__file__), "areas")
    changed = 0
    for i, path in enumerate(sorted(glob.glob(os.path.join(base, "*.html")))):
        slug = os.path.splitext(os.path.basename(path))[0]
        name = NAMES.get(slug)
        if not name:
            print("SKIP(no name):", slug); continue
        html = open(path, encoding="utf-8").read()
        m = LEAD_RE.search(html)
        if not m:
            print("WARN(no lead):", slug); continue
        lead_body = m.group(2)
        if "출장마사지" in lead_body:
            print("SKIP(done):", slug); continue
        sent = VARIANTS[i % len(VARIANTS)].format(n=name)
        new_lead = m.group(1) + lead_body.rstrip() + " " + sent + m.group(3)
        html = html[:m.start()] + new_lead + html[m.end():]
        open(path, "w", encoding="utf-8").write(html)
        changed += 1
        print("OK:", slug)
    print("changed:", changed)

if __name__ == "__main__":
    main()
