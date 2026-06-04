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
  suwon: [
    {
      text: "회사 일 때문에 목과 어깨가 돌덩이처럼 굳었어요. 수원에서 밤 늦게 예약했는데 생각보다 빨리 와주셨어요. 집에서 받는 건데도 전문적인 느낌이었고, 매트 깔고 옷 갈아입고 누우니 정말 편했어요. 손이 뜨겁고 힘이 적당히 들어가는데 아픈 데를 콕콕 찔러주셔서 개운한 정도가 아니라 거의 눈물 날 뻔했어요. 다음 날 몸이 진짜 가벼웠습니다. 비용은 9만원 정도였고 팁은 안 받으시더라고요. 수원에서 출장마사지 처음 받아봤는데 만족해요. 다만 예약 시간을 좀 더 잘 지켜주셨으면 좋겠어요(20분 늦으셨어요).",
      rating: 4,
      name: "수원 직장인 고객",
      course: "60분 · 약 9만원대",
      consent: true
    }
  ],
  dongtan: [],
  yongin:  [],
  bundang: [
    {
      text: "성남 분당에서 받았어요. 회식 다음 날 온몸이 쑤셔서 급하게 전화했는데 한 시간 만에 와주셨어요. 여성 관리사님을 원했는데 그렇게 배정됐고, 조용하셔서 처음엔 살짝 어려웠는데 막상 시작하니 친절하셨어요. 종아리랑 허리 위주로 부탁드렸는데 알아서 뭉친 곳을 잘 찾아주시더라고요. 아프면서도 시원한 느낌이고, 특히 발 마사지가 정말 좋았어요. 방문 전에 샤워하고 대기했더니 바로 시작해서 좋았고요. 90분에 12만원, 약간 비싼가 싶었는데 다음 날 컨디션이 너무 좋아서 또 부를 것 같아요. 단점이라면 관리사님마다 손맛 차이가 있을 것 같다는 점이에요.",
      rating: 4,
      name: "분당 직장인 고객",
      course: "90분 · 12만원",
      consent: true
    }
  ],
  osan:    [],
  giheung: [
    {
      text: "용인 기흥구 아파트에서 받았어요. 임신 6개월 때 허리가 너무 아파서 찾았는데, 임산부 가능한 곳이 많지 않더라고요. 여기는 가능해서 예약했고 경력 많으신 관리사님이 오셨어요. 옆으로 누워서 받는 방식이고 배는 누르지 않고 등이랑 다리를 집중해주셨어요. 살면서 이렇게 시원한 적이 없었어요. 아파트 주차도 미리 알려드려서 헤매지 않으셨고요. 70분에 10만원 조금 넘었는데, 다음 날 아침에 다리랑 발이 날아갈 듯 가벼웠어요. 출산 후에도 또 받을 생각이에요. 다만 카드 결제가 안 되는 경우가 있으니 현금을 챙기시는 게 좋아요.",
      rating: 5,
      name: "기흥 임산부 고객",
      course: "70분 · 10만원대 (임산부 측와위 케어)",
      consent: true
    }
  ],
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
