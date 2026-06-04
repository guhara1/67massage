/* =========================================================================
   67 마사지 — 지역별 "실제" 이용 후기 데이터 + 렌더러
   -------------------------------------------------------------------------
   ⚠️ 반드시 실제로 받은 후기만 입력하세요. 가짜·조작 후기는 한국 표시광고법 위반이며
      구글 스팸 정책으로 별점 리치결과 박탈·사이트 신뢰도 하락을 부릅니다.

   후기 추가 방법 (이 파일만 수정하면 카드 + 별점 + 구조화 데이터가 자동 생성됩니다):
     해당 지역 배열에 객체 한 줄을 추가하세요.
     {
       text:   "후기 내용 (고객이 남긴 실제 문장, 과장·왜곡 없이)",
       rating: 5,                 // 1~5
       name:   "권선동 김**",      // 표시명 (개인정보 최소화)
       course: "60분 아로마 릴랙스",
       date:   "2026-06-01",      // YYYY-MM-DD
       consent: true              // 게재 동의를 받았다는 표시 (없으면 게재 금지)
     }
   ========================================================================= */
window.REVIEWS = {
  suwon:   [],
  dongtan: [],
  yongin:  [],
  bundang: [],
  osan:    [],
  giheung: [],
  suji:    []
};

(function () {
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function starStr(n) {
    n = Math.max(1, Math.min(5, Math.round(Number(n) || 5)));
    return "★".repeat(n) + "☆".repeat(5 - n);
  }

  function render() {
    var sec = document.getElementById("reviews");
    if (!sec) return;
    var area = sec.getAttribute("data-area");
    var name = sec.getAttribute("data-name") || "67 마사지";
    var all = (window.REVIEWS && window.REVIEWS[area]) || [];
    // 게재 동의(consent)가 명시된 후기만 노출 — 법적 안전장치
    var list = all.filter(function (r) { return r && r.consent === true && r.text; });

    var holder = sec.querySelector("[data-review-list]");
    var empty = sec.querySelector("[data-review-empty]");
    if (!list.length) return;            // 후기 없으면 빈 상태(empty) 그대로 유지
    if (empty) empty.style.display = "none";

    holder.innerHTML = list.map(function (r) {
      var n = Math.max(1, Math.min(5, Math.round(Number(r.rating) || 5)));
      var foot = ["— " + esc(r.name || "익명")];
      if (r.course) foot.push(esc(r.course));
      if (r.date) foot.push(esc(r.date));
      return '<figure class="review-card">' +
        '<div class="stars" aria-label="별점 ' + n + '점 만점에 5점">' + starStr(n) + "</div>" +
        "<blockquote>" + esc(r.text) + "</blockquote>" +
        '<figcaption class="meta">' + foot.join(" · ") + "</figcaption></figure>";
    }).join("");

    // 구조화 데이터(Review + AggregateRating) 자동 주입 — 실제 후기가 있을 때만
    var sum = list.reduce(function (a, r) { return a + (Number(r.rating) || 5); }, 0);
    var avg = (sum / list.length);
    var schema = {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": name,
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": avg.toFixed(1),
        "reviewCount": list.length,
        "bestRating": 5, "worstRating": 1
      },
      "review": list.map(function (r) {
        var o = {
          "@type": "Review",
          "reviewRating": { "@type": "Rating", "ratingValue": Number(r.rating) || 5, "bestRating": 5 },
          "author": { "@type": "Person", "name": r.name || "익명" },
          "reviewBody": r.text
        };
        if (r.date) o.datePublished = r.date;
        return o;
      })
    };
    var sc = document.createElement("script");
    sc.type = "application/ld+json";
    sc.textContent = JSON.stringify(schema);
    document.head.appendChild(sc);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();
