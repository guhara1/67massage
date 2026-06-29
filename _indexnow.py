# -*- coding: utf-8 -*-
"""
IndexNow 제출기 — 새 글/수정 글을 Bing·Naver·Yandex·Seznam 등에 즉시 색인 통보.

준비물(이미 완료):
  - 루트에 키 파일: f0ceaaa66503df1016e69e607b75fbfd.txt  (내용=키)
  - 배포된 사이트에서 https://67massage.netlify.app/f0ceaaa66503df1016e69e607b75fbfd.txt 가 200으로 열려야 함

사용법:
  python3 _indexnow.py --changed     # 직전 커밋에서 바뀐 .html만 통보 (글 올릴 때마다 권장)
  python3 _indexnow.py --all         # sitemap.xml 전체 통보 (최초 1회/대규모 변경 시)
  python3 _indexnow.py /areas/segyo.html https://67massage.netlify.app/magazine/sleep-recovery.html
                                     # 특정 URL/경로만 통보
  python3 _indexnow.py --all --dry   # 전송 없이 대상 URL만 출력
"""
import sys, json, subprocess, urllib.request, urllib.error, re, os

HOST = "67massage.netlify.app"
KEY = "f0ceaaa66503df1016e69e607b75fbfd"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/IndexNow"  # 공유 엔드포인트(참여 검색엔진에 전파)
BASE = os.path.dirname(os.path.abspath(__file__))
# noindex 리다이렉트 페이지는 통보 제외
SKIP = {"areas/guundong.html", "areas/pogok.html"}

def to_url(p):
    p = p.strip()
    if p.startswith("http"):
        return p
    p = p.lstrip("/")
    if p in SKIP:
        return None
    if p in ("", "index.html"):
        return f"https://{HOST}/"
    return f"https://{HOST}/{p}"

def from_sitemap():
    path = os.path.join(BASE, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 빌드 스크립트를 실행하세요.")
    xml = open(path, encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", xml)

def from_git_changed():
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD", "--", "*.html"],
            cwd=BASE, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        sys.exit("git diff 실패 — 커밋이 1개뿐이거나 git 저장소가 아닙니다.")
    files = [l for l in out.splitlines() if l.strip()]
    urls = [to_url(f) for f in files]
    return [u for u in urls if u]

def collect(args):
    flags = [a for a in args if a.startswith("--")]
    rest = [a for a in args if not a.startswith("--")]
    if "--all" in flags:
        urls = from_sitemap()
    elif "--changed" in flags:
        urls = from_git_changed()
    elif rest:
        urls = [to_url(a) for a in rest]
    else:
        print(__doc__); sys.exit(0)
    # 정리: None 제거, 중복 제거, 호스트 일치
    seen, out = set(), []
    for u in urls:
        if not u or u in seen: continue
        if HOST not in u: continue
        seen.add(u); out.append(u)
    return out, ("--dry" in flags)

def submit(urls):
    payload = {"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"✅ IndexNow 응답: {r.status} {r.reason}  ({len(urls)}개 URL 통보)")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        print(f"⚠️ HTTP {e.code} {e.reason}\n{body}")
        if e.code == 403:
            print("  → 키 파일이 라이브 사이트 루트에 배포됐는지 확인하세요:", KEY_LOCATION)
        return False
    except Exception as e:
        print("⚠️ 전송 실패(네트워크/방화벽 가능):", e)
        return False

def wait_live(urls, tries=24, gap=10):
    """배포(GitHub Pages) 반영 대기 — 각 URL이 200으로 뜰 때까지 폴링."""
    import time
    pending = list(urls)
    for i in range(tries):
        still = []
        for u in pending:
            try:
                req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "indexnow-wait"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    if r.status >= 400: still.append(u)
            except Exception:
                still.append(u)
        pending = still
        if not pending:
            print(f"✅ 모든 URL 라이브 확인 ({i*gap}s)"); return
        print(f"⏳ 배포 대기… 미반영 {len(pending)}개 ({(i+1)*gap}s 경과)")
        time.sleep(gap)
    print(f"⚠️ 일부 URL이 아직 미반영({len(pending)}개)이지만 통보를 진행합니다.")

def main():
    args = sys.argv[1:]
    urls, dry = collect(args)
    if not urls:
        print("통보할 URL이 없습니다."); return
    print(f"대상 {len(urls)}개 URL:")
    for u in urls: print("  -", u)
    if dry:
        print("\n[--dry] 전송하지 않았습니다."); return
    if "--wait" in args:
        wait_live(urls)
    submit(urls)

if __name__ == "__main__":
    main()
