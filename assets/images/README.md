# 이미지 업로드 가이드

## 어디에 올리나
- **블로그(매거진) 본문·썸네일 이미지** → `assets/images/magazine/`
- 공통/브랜드 이미지(대표 OG 등) → `assets/images/` 또는 기존 `assets/og-cover.jpg`

## 파일 이름 (SEO)
- 영문 소문자 + 하이픈, **키워드 포함**. 한글·공백·대문자 금지.
  - 좋음: `suwon-outcall-massage-neck.jpg`, `dongtan-aroma-room.webp`
  - 나쁨: `IMG_1234.JPG`, `수원 마사지.jpg`

## 최적화
- 가로 **1200px 이하**(썸네일은 800px면 충분), 용량 **200KB 이하** 권장
- 형식: 사진 `.jpg`/`.webp`, 그래픽 `.png`
- 업로드 후 `<img>`에 **alt(키워드 자연 포함)**, `loading="lazy"`, `width`/`height` 지정

## 본문에서 부르는 경로
- 매거진 글(`magazine/*.html`)에서: `../assets/images/magazine/파일명.jpg`
- 루트 페이지(`index.html` 등)에서: `assets/images/magazine/파일명.jpg`
