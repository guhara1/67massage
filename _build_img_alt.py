# -*- coding: utf-8 -*-
"""
대표 이미지(og-cover.jpg)에 접근성·SEO용 대체 텍스트를 부여한다.
- og:image 다음 줄에 og:image:alt 추가
- twitter:image 다음 줄에 twitter:image:alt 추가
alt 문구는 해당 페이지의 og:title(없으면 <title>)에서 가져와 이미지가 무엇을 나타내는지 설명한다.
멱등: 이미 alt가 있으면 건너뛴다.
"""
import re, glob, os

def get_alt(html):
    m = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    if not m:
        m = re.search(r'<title>([^<]+)</title>', html)
    alt = m.group(1) if m else "67 마사지 출장마사지"
    # 구분 기호 뒤 군더더기(예: ' · 24시간 예약') 정리해 이미지 설명답게 다듬기
    alt = re.split(r'\s*[·|]\s*24시간', alt)[0].strip()
    return alt

def main():
    changed = 0
    for path in sorted(glob.glob("**/*.html", recursive=True)):
        if os.path.basename(path).startswith("_"):
            continue
        html = open(path, encoding="utf-8").read()
        if 'og:image:alt' in html:
            print("SKIP(done):", path); continue
        alt = get_alt(html).replace('"', '')
        new = html
        # og:image 뒤에 og:image:alt 삽입 (width/height 줄이 뒤따라도 og:image 라인 바로 뒤)
        new, n1 = re.subn(
            r'(<meta property="og:image" content="[^"]+" />)',
            r'\1\n<meta property="og:image:alt" content="%s" />' % alt,
            new, count=1)
        # twitter:image 뒤에 twitter:image:alt 삽입
        new, n2 = re.subn(
            r'(<meta name="twitter:image" content="[^"]+" />)',
            r'\1\n<meta name="twitter:image:alt" content="%s" />' % alt,
            new, count=1)
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
            print(f"OK: {path}  (og:{n1}, tw:{n2})  alt='{alt}'")
        else:
            print("WARN(no og:image):", path)
    print("changed:", changed)

if __name__ == "__main__":
    main()
