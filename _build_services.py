# -*- coding: utf-8 -*-
"""
서비스 코스 개별 안내 페이지 빌더 (/services/{slug}.html).
- 코스마다 고유 콘텐츠(코스 설명/적합 대상/진행 방식/추천/주의/FAQ)를 작성, 복붙·도어웨이 회피.
- 타이틀·디스크립션·본문 모두 코스별로 다르게 구성.
- Service/BreadcrumbList/FAQPage JSON-LD, index,follow, self canonical, 정찰 가격표 + 후기 스캐폴드.
실행 순서: _build_tier.py → _build_services.py → _build_locals.py(사이트맵 최종)
"""
import json, os
from _build_tier import header, footer, DOMAIN, TODAY, PRICE

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = "../"
PHONE = "tel:0508-202-4717"

def review_sms(name):
    from urllib.parse import quote
    return "sms:0508-202-4717?body=" + quote(f"[67 마사지 {name} 후기] 코스/시간: , 지역: , 별점(1~5): , 내용: ")

SERVICES = {
"swedish": dict(name="스웨디시", h1="스웨디시 출장마사지",
 title="스웨디시 출장마사지 | 67 마사지 · 전신 순환·이완 코스",
 desc="스웨디시 출장마사지 안내 — 긴 스트로크와 일정한 압으로 전신 긴장을 풀고 순환을 돕는 이완 코스. 처음 받는 분께 맞는 강도·시간·진행 방식과 정찰 가격을 정리했습니다.",
 lead="스웨디시 출장마사지는 긴 스트로크와 일정한 압으로 전신의 긴장을 부드럽게 풀고 혈류·림프 순환을 돕는 가장 기본적인 이완 코스입니다. 강한 자극보다 편안한 흐름을 중시해, 출장마사지를 처음 받아보는 분께 먼저 권해 드립니다.",
 about="스웨디시는 서양식 오일 마사지의 기본으로, 손바닥과 손가락을 이용한 길고 리드미컬한 동작이 특징입니다. 압이 과하지 않아 몸에 무리가 적고, 특정 부위를 강하게 파기보다 전신을 고르게 풀어 하루의 피로를 차분히 가라앉히는 데 적합합니다. 이완과 휴식이 목적인 분께 가장 무난한 선택입니다.",
 who=["출장마사지를 처음 받아보는 분","강한 압이 부담스러운 분","수면·피로 회복이 목적인 분","특정 부위보다 전신을 두루 풀고 싶은 분","잔잔하고 편안한 분위기를 원하는 분"],
 how="방문하면 먼저 컨디션과 불편한 부위, 선호하는 압 세기를 확인한 뒤 오일을 사용해 등·어깨·다리·팔 순서로 전신을 부드럽게 풀어갑니다. 동작이 길고 일정해 자극이 갑작스럽지 않으며, 진행 중에도 압이 강하거나 약하면 언제든 말씀해 주시면 바로 조절합니다. 향에 민감하거나 알레르기가 있으면 무향·저자극 오일로 바꿔 진행합니다.",
 recommend="가볍게 풀고 싶은 날은 60분, 전신을 충분히 받고 싶으면 90·120분이 무난합니다. 잠들기 전 이완이 주된 목적이라면 향까지 더해 휴식감을 높이는 아로마 테라피와 비교해 고르셔도 좋고, 어깨·허리 결림이 오래됐다면 부분 집중이 강한 딥티슈를 함께 고려해 보세요.",
 care="받기 전 가벼운 샤워를 권하며, 식사 직후보다는 약간의 시간을 두고 받는 것이 편안합니다. 받은 뒤에는 수분을 충분히 섭취하시면 좋습니다. 음주가 심하거나 발열·염증·전염성 질환이 있는 경우에는 무리한 관리보다 휴식을 먼저 권합니다. 마사지는 휴식과 피로 회복을 돕는 관리로, 질환 치료나 의료 행위를 대체하지 않습니다.",
 faqs=[("출장마사지가 처음인데 스웨디시가 맞을까요?","네, 스웨디시는 압이 과하지 않고 전신을 고르게 푸는 코스라 처음 받는 분께 가장 무난합니다."),
       ("많이 아프지 않을까요?","긴 스트로크 중심의 부드러운 압이라 자극이 강하지 않습니다. 원하는 세기를 미리 알려주시면 맞춰 진행합니다."),
       ("시간은 어느 정도가 좋나요?","가볍게는 60분, 전신을 충분히 받고 싶으면 90·120분을 권합니다. 컨디션을 알려주시면 함께 정해 드립니다."),
       ("오일 향이 부담스러운데요?","향에 민감하거나 알레르기가 있으면 무향·저자극 오일로 바꿔 진행하니 예약 시 알려주세요."),
       ("받고 난 뒤 주의할 점이 있나요?","수분을 충분히 드시고 무리한 활동은 피하시는 것이 좋습니다.")],
 related=[("aroma","아로마 테라피와 비교"),("deep","딥티슈 코스 보기"),("../services.html","전체 서비스 메뉴"),("../guide.html","이용 안내")]),

"aroma": dict(name="아로마 테라피", h1="아로마 테라피 출장마사지",
 title="아로마 테라피 출장마사지 | 67 마사지 · 블렌딩 오일 릴렉스",
 desc="아로마 테라피 출장마사지 안내 — 목적에 맞춰 블렌딩한 오일로 후각과 촉각을 함께 이완시키는 코스. 향 선택·진행 방식·추천 시간과 정찰 가격을 정리했습니다.",
 lead="아로마 테라피 출장마사지는 라벤더·베르가못 등 목적에 맞춰 블렌딩한 오일을 사용해 후각과 촉각을 함께 이완시키는 코스입니다. 향이 더해지는 만큼 긴장 완화와 기분 전환에 강점이 있어, 스트레스가 쌓였거나 잠들기 전 편안함을 원할 때 잘 맞습니다.",
 about="아로마 테라피는 식물에서 추출한 에센셜 오일의 향과 부드러운 오일 터치를 결합한 코스입니다. 같은 오일 마사지라도 향이 더해지면 심리적 이완감이 커지는 편이라, 강한 압보다는 차분한 분위기와 휴식을 중시하는 분께 적합합니다. 향은 컨디션과 선호에 따라 조절합니다.",
 who=["스트레스·긴장으로 마음이 자주 분주한 분","잠들기 전 편안한 휴식을 원하는 분","강한 압보다 차분한 분위기를 선호하는 분","기분 전환이 필요한 분","향을 통한 이완을 좋아하는 분"],
 how="방문하면 컨디션과 선호하는 향의 방향(상쾌함·진정 등)을 확인한 뒤, 블렌딩한 오일로 전신을 부드럽게 풀어갑니다. 압은 과하지 않게 유지하며 호흡과 함께 천천히 진행해 후각과 촉각이 함께 이완되도록 합니다. 향에 민감하거나 알레르기가 있으면 무향·저자극으로 대체하니 예약 시 알려주세요.",
 recommend="기분 전환과 가벼운 이완은 60분, 충분한 휴식을 원하면 90분이 무난합니다. 향보다 전신 순환·이완 자체가 목적이라면 스웨디시와 비교해 고르시고, 분위기와 휴식감을 함께 중시한다면 무드 오일 케어 구성을 참고하셔도 좋습니다.",
 care="향이 강하게 느껴지지 않도록 환기가 되는 공간이면 더 쾌적합니다. 받기 전 가벼운 샤워를 권하고, 받은 뒤에는 수분을 충분히 드세요. 임신 중이거나 특정 향·성분에 알레르기가 있으면 반드시 예약 시 알려주시기 바랍니다. 마사지는 휴식과 피로 회복을 돕는 관리로, 질환 치료나 의료 행위를 대체하지 않습니다.",
 faqs=[("향은 직접 고를 수 있나요?","상쾌함·진정 등 원하는 방향을 알려주시면 그에 맞춰 블렌딩합니다. 특정 향을 피하고 싶다면 미리 말씀해 주세요."),
       ("향에 민감한데 받아도 되나요?","무향·저자극 오일로 대체해 진행할 수 있으니 예약 시 알려주시면 됩니다."),
       ("스웨디시와 무엇이 다른가요?","두 코스 모두 오일을 쓰지만, 아로마 테라피는 향을 통한 심리적 이완을 더 중시합니다."),
       ("임신 중에도 가능한가요?","향·성분에 민감할 수 있어 사전 안내가 필요합니다. 임신 사실과 주수를 미리 알려주세요."),
       ("잠들기 전에 받아도 되나요?","진정 계열 향으로 차분한 휴식을 돕는 구성이 가능합니다. 야간 예약도 받습니다.")],
 related=[("swedish","스웨디시와 비교"),("deep","딥티슈 코스 보기"),("../services.html","전체 서비스 메뉴"),("../magazine/sleep-recovery.html","수면과 마사지 이야기")]),

"deep": dict(name="딥티슈", h1="딥티슈 출장마사지",
 title="딥티슈 출장마사지 | 67 마사지 · 뭉친 근육 집중 케어",
 desc="딥티슈 출장마사지 안내 — 깊은 근막·근육층을 목표로 오래 뭉친 부위를 집중적으로 풀어내는 강도 높은 코스. 적합 대상·진행 방식·주의사항과 정찰 가격을 정리했습니다.",
 lead="딥티슈 출장마사지는 표층보다 깊은 근막과 근육층을 목표로, 오래 뭉친 부위를 집중적으로 풀어내는 강도 높은 코스입니다. 어깨·등·허리 결림이 누적돼 가벼운 이완으로는 풀리지 않던 분께 적합합니다.",
 about="딥티슈는 느린 동작과 깊은 압으로 근육의 깊은 층을 자극해 만성적으로 뭉친 부위를 풀어가는 방식입니다. 시원함과 함께 다소 묵직한 자극이 동반될 수 있어, 이완 중심의 스웨디시·아로마와는 목적이 다릅니다. 특정 부위의 결림을 집중적으로 다루고 싶을 때 선택합니다.",
 who=["오래 앉아 일해 목·어깨·등이 자주 뭉치는 분","가벼운 마사지로는 잘 안 풀리던 분","특정 부위를 집중적으로 풀고 싶은 분","강한 압을 선호하는 분","장시간 운전·서서 일하는 분"],
 how="방문하면 결림이 심한 부위와 선호 강도를 먼저 확인하고, 해당 부위를 중심으로 깊고 느린 압을 주며 풀어갑니다. 강도가 있는 코스인 만큼 진행 중 통증이 과하면 즉시 말씀해 주시면 압을 조절합니다. 자극이 강한 부위는 무리하지 않고 단계적으로 접근합니다.",
 recommend="부분 집중이 목적이면 60·90분, 전신 균형까지 함께 보고 싶으면 90·120분이 무난합니다. 강도가 부담스럽다면 스웨디시로 시작해 다음에 딥티슈로 넘어가는 방법도 있습니다. 평소 셀프 관리가 궁금하면 폼롤러·스트레칭 글을 참고하셔도 좋습니다.",
 care="강도가 있는 코스라 받은 뒤 부위가 약간 뻐근할 수 있으며, 보통 하루 정도면 가라앉습니다. 수분을 충분히 드시는 것이 좋습니다. 급성 부상·염증·심한 통증이 있거나 디스크 등 질환이 의심되면 딥티슈보다 전문 의료 상담을 먼저 받으시길 권합니다. 마사지는 휴식과 피로 회복을 돕는 관리로, 질환 치료나 의료 행위를 대체하지 않습니다.",
 faqs=[("딥티슈는 많이 아픈가요?","깊은 압이 들어가 시원하면서도 묵직한 자극이 있을 수 있습니다. 통증이 과하면 바로 조절하니 편하게 말씀해 주세요."),
       ("받고 나서 뻐근한데 괜찮은가요?","강도가 있는 코스라 하루 정도 뻐근할 수 있으며 대개 자연히 가라앉습니다. 수분 섭취를 권합니다."),
       ("디스크가 있는데 받아도 되나요?","질환이 의심되거나 진단받은 경우에는 먼저 전문 의료 상담을 권합니다. 무리한 압은 피해야 합니다."),
       ("어느 부위를 집중할 수 있나요?","목·어깨·등·허리 등 결림이 심한 부위를 중심으로 진행합니다. 원하는 부위를 미리 알려주세요."),
       ("처음인데 딥티슈를 바로 받아도 되나요?","강한 압이 부담스러우면 스웨디시로 시작하는 방법도 있습니다. 선호 강도를 알려주시면 맞춰 드립니다.")],
 related=[("swedish","스웨디시와 비교"),("sports","스포츠 회복 코스"),("../magazine/lower-back-deeptissue.html","허리 딥티슈 이야기"),("../magazine/foam-rolling-basics.html","폼롤러 셀프케어")]),

"sports": dict(name="스포츠 회복", h1="스포츠 회복 출장마사지",
 title="스포츠 회복 출장마사지 | 67 마사지 · 운동 후 컨디셔닝",
 desc="스포츠 회복 출장마사지 안내 — 운동 전후 근육 컨디셔닝과 회복을 목표로 가동 범위·피로 부위를 점검하며 관리하는 코스. 적합 대상·진행·주의와 정찰 가격을 정리했습니다.",
 lead="스포츠 회복 출장마사지는 운동 전후의 근육 컨디셔닝과 피로 회복을 목표로 하는 코스입니다. 가동 범위와 피로가 누적된 부위를 점검하며 관리해, 꾸준히 운동하는 분이나 대회·등산 전후 컨디션을 정리하고 싶은 분께 적합합니다.",
 about="스포츠 회복은 운동으로 사용한 근육의 긴장을 풀고 회복을 돕는 데 초점을 둔 구성입니다. 종아리·허벅지·허리·어깨처럼 운동 부하가 집중되는 부위를 점검하며, 이완과 컨디셔닝을 함께 다룹니다. 퍼포먼스 자체보다 ‘회복’에 중심을 둔 관리입니다.",
 who=["꾸준히 운동·운동 후 회복이 필요한 분","대회·등산·라이딩 전후 컨디션을 정리하고 싶은 분","종아리·허벅지 등 하체 피로가 큰 분","같은 동작을 반복해 특정 부위가 자주 뭉치는 분","운동 후 뻐근함을 빨리 가라앉히고 싶은 분"],
 how="방문하면 운동 종류와 부하가 집중된 부위, 컨디션을 확인한 뒤 해당 부위를 중심으로 점검하며 풀어갑니다. 가동 범위와 피로 누적 부위를 함께 살피고, 강도는 부위와 상태에 맞춰 조절합니다. 통증이 있는 부위는 무리하지 않고 회복 관점에서 접근합니다.",
 recommend="운동 후 가벼운 회복은 60·90분, 하체까지 충분히 보고 싶으면 90·120분이 무난합니다. 특정 부위 결림이 심하면 딥티슈를, 전신 이완이 목적이면 스웨디시를 함께 고려해 보세요. 자기 전 셀프 스트레칭 글도 회복에 참고가 됩니다.",
 care="운동 직후 근육에 열감·부기가 심한 상태라면 약간 시간을 두고 받는 것이 좋습니다. 받은 뒤에는 수분 섭취와 충분한 휴식을 권합니다. 부상·통증·염증이 있거나 회복 중이라면 관리보다 전문 의료·재활 상담을 먼저 받으시길 권합니다. 마사지는 휴식과 피로 회복을 돕는 관리로, 치료나 재활을 대체하지 않습니다.",
 faqs=[("운동 직후 바로 받아도 되나요?","열감·부기가 심하면 약간 시간을 두는 편이 좋습니다. 상태를 알려주시면 시점을 함께 정해 드립니다."),
       ("어느 부위를 주로 보나요?","종아리·허벅지·허리·어깨 등 운동 부하가 집중되는 부위를 중심으로 점검하며 풀어갑니다."),
       ("부상이 있는데 받아도 되나요?","부상·통증이 있으면 관리보다 전문 의료·재활 상담을 먼저 권합니다. 무리한 압은 피해야 합니다."),
       ("딥티슈와 어떻게 다른가요?","딥티슈는 결림 부위 집중 이완에, 스포츠 회복은 운동 부위 컨디셔닝과 회복에 중심을 둡니다."),
       ("대회 전에 받아도 되나요?","컨디션 정리 목적의 가벼운 구성이 가능합니다. 일정과 부위를 미리 알려주세요.")],
 related=[("deep","딥티슈와 비교"),("swedish","스웨디시 코스"),("../magazine/night-stretch-5min.html","자기 전 셀프 스트레칭"),("../magazine/foam-rolling-basics.html","폼롤러 근막 이완")]),

"couple": dict(name="커플·2인", h1="커플·2인 출장마사지",
 title="커플·2인 출장마사지 | 67 마사지 · 동시 방문 관리사 2인",
 desc="커플·2인 출장마사지 안내 — 두 분이 같은 공간에서 동시에 받는 구성. 관리사 동시 배정·공간 조건·예약 방법·코스 선택과 정찰 가격을 정리했습니다.",
 lead="커플·2인 출장마사지는 두 분이 같은 공간에서 동시에 관리를 받는 구성입니다. 관리사 2인 동시 배정이 필요해, 기념일이나 함께 쉬고 싶은 날 미리 예약해 두면 편하게 이용할 수 있습니다.",
 about="커플·2인은 같은 방이나 공간에서 두 분이 나란히 동시에 받는 방식으로, 한 분씩 따로 받는 것보다 시간을 함께 보낼 수 있다는 점이 특징입니다. 코스는 두 분이 같게 맞추거나 각각 다르게 선택할 수 있으며, 관리사 동시 배정 일정 조율이 필요합니다.",
 who=["기념일·특별한 날을 함께 보내고 싶은 커플","부부·가족이 함께 받고 싶은 분","친구와 같은 시간에 받고 싶은 분","각자 다른 코스를 같은 시간에 받고 싶은 분","따로 시간 내기 어려워 한 번에 받고 싶은 분"],
 how="예약 시 인원과 각자 원하는 코스·시간을 알려주시면 관리사 2인을 동시 배정해 같은 공간에서 나란히 진행합니다. 두 분의 컨디션과 선호 압을 각각 확인해 개별적으로 맞춰 관리하며, 진행 중 강도 조절도 각자 가능합니다. 동시 배정 특성상 일정 여유를 두고 예약하시면 원활합니다.",
 recommend="두 분 모두 가볍게는 60·90분, 충분히 받고 싶으면 90·120분이 무난합니다. 한 분은 이완 중심 스웨디시·아로마, 다른 한 분은 결림 집중 딥티슈처럼 서로 다른 코스를 선택해도 됩니다. 코스가 고민되면 예약 전화에서 함께 정해 드립니다.",
 care="두 분이 나란히 누울 수 있는 공간이 필요하므로, 예약 시 공간 여건을 함께 알려주시면 안내가 정확합니다. 받기 전 가벼운 샤워를 권하고, 받은 뒤에는 수분을 충분히 드세요. 임신·질환 등 개별 상태가 있으면 각자 미리 알려주시기 바랍니다. 마사지는 휴식과 피로 회복을 돕는 관리로, 의료 행위를 대체하지 않습니다.",
 faqs=[("관리사 두 분이 동시에 오나요?","네, 커플·2인은 관리사 2인을 동시 배정해 같은 공간에서 나란히 진행합니다."),
       ("두 사람이 다른 코스를 받아도 되나요?","가능합니다. 각자 원하는 코스와 시간을 예약 시 알려주시면 개별로 맞춰 진행합니다."),
       ("공간이 좁아도 되나요?","두 분이 나란히 누울 공간이 필요합니다. 공간 여건을 알려주시면 가능 여부를 안내해 드립니다."),
       ("예약은 미리 해야 하나요?","관리사 동시 배정이 필요해 일정 여유를 두고 예약하시면 원활합니다."),
       ("가격은 어떻게 되나요?","코스별 정찰가가 인원수에 따라 적용됩니다. 인원과 코스를 알려주시면 정확히 안내해 드립니다.")],
 related=[("swedish","스웨디시 코스"),("aroma","아로마 테라피 코스"),("../services.html","전체 서비스 메뉴"),("../guide.html","이용 안내")]),
}

def shref(s):
    return f"{s}.html" if s in SERVICES else s

def head(slug, d):
    name = d["name"]; url = f"{DOMAIN}/services/{slug}.html"
    title = d["title"]; desc = d["desc"]
    service = {"@context":"https://schema.org","@type":"Service","serviceType":"출장마사지",
        "name":f"{name} 출장마사지","category":name,
        "provider":{"@type":"HealthAndBeautyBusiness","name":"67 마사지","telephone":"+82-50-8202-4717","url":DOMAIN},
        "areaServed":{"@type":"Place","name":"경기 남부"},"url":url,"description":desc}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"홈","item":f"{DOMAIN}/"},
        {"@type":"ListItem","position":2,"name":"서비스 안내","item":f"{DOMAIN}/services.html"},
        {"@type":"ListItem","position":3,"name":f"{name} 출장마사지","item":url}]}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faqs"]]}
    j = lambda x: json.dumps(x, ensure_ascii=False)
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

H3S = "font-family:var(--font-display);font-size:1.12rem;margin:26px 0 8px;color:var(--paper)"

def li(items):
    return "".join(f"<li>{x}</li>" for x in items)

def build_service(slug, d):
    name = d["name"]; H = head(slug, d)
    links = "".join(f'<a href="{shref(s)}">{txt}</a>' for s,txt in d["related"])
    faqs = "".join(f"<dt>{q}</dt><dd>{a}</dd>" for q,a in d["faqs"])
    rsms = review_sms(name)
    who = li(d["who"])
    body = f"""{header(ROOT)}
<section class="page-hero"><div class="wrap">
  <p class="crumb"><a href="../index.html">홈</a><span>›</span><a href="../services.html">서비스 안내</a><span>›</span>{name} 출장마사지</p>
  <span class="eyebrow" style="margin-top:14px">SERVICE</span>
  <h1>{d['h1']}</h1>
  <p class="lead">{d['lead']}</p>
  <div class="hero-actions" style="margin-top:30px">
    <a class="btn btn-gold" href="{PHONE}">{name} 예약 0508-202-4717</a>
    <a class="btn btn-ghost" href="../services.html">전체 코스 보기</a>
  </div>
</div></section>

<section class="section" style="padding-top:34px;padding-bottom:8px"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">WHAT IS IT</span>
  <h2 class="section-title">{name}란</h2>
  <p class="lead" style="margin-top:18px">{d['about']}</p>
</div></section>

<section class="section" style="padding-top:14px"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">WHO FOR</span>
  <h2 class="section-title">이런 분께 맞습니다</h2>
  <ul class="area-list" style="margin-top:18px;color:var(--paper-dim);line-height:2.1">{who}</ul>
</div></section>

<section class="section" style="padding-top:14px"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">HOW IT GOES</span>
  <h2 class="section-title">{name} 진행 방식</h2>
  <p class="lead" style="margin-top:18px">{d['how']}</p>
  <h3 style="{H3S}">추천 시간·코스 조합</h3>
  <p style="color:var(--paper-dim)">{d['recommend']}</p>
</div></section>

<section class="section" style="padding-top:14px"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">BEFORE · AFTER</span>
  <h2 class="section-title">받기 전·후 주의</h2>
  <p class="lead" style="margin-top:18px">{d['care']}</p>
</div></section>

{PRICE}
<section class="section" style="padding-top:34px"><div class="wrap" style="max-width:780px">
  <span class="eyebrow">FAQ</span>
  <h2 class="section-title">{name} 자주 묻는 질문</h2>
  <dl class="faq" style="margin-top:24px">{faqs}</dl>
</div></section>

<section class="section" style="padding-top:14px"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">NEXT</span>
  <h2 class="section-title">함께 보면 좋은 안내</h2>
  <div class="dropdown grid" style="position:static;opacity:1;visibility:visible;transform:none;margin-top:20px;min-width:0;max-width:520px">{links}</div>
</div></section>

<section class="section areas-band" id="reviews" data-area="svc-{slug}" data-name="67 마사지 · {name}"><div class="wrap" style="max-width:780px">
  <span class="eyebrow">REVIEW</span>
  <h2 class="section-title">{name} 실제 이용 후기</h2>
  <p class="lead" style="margin-top:16px">{name} 코스를 받은 <strong style="color:var(--gold-hi)">실제 이용 후기</strong>만 게재합니다. 모든 후기는 게재 동의를 받아 과장·왜곡 없이 그대로 싣습니다.</p>
  <div data-review-list class="review-list"></div>
  <div data-review-empty class="review-empty">아직 등록된 후기가 없습니다. {name} 관리를 받으신 뒤 후기를 남겨주시면 다음 이용자에게 가장 정확한 정보가 됩니다. (게재 동의하신 후기만 노출됩니다.)</div>
  <div class="review-actions">
    <a class="btn btn-gold" href="{rsms}">{name} 후기 남기기</a>
    <a class="btn btn-ghost" href="{PHONE}">{name} 예약 0508-202-4717</a>
  </div>
</div></section>

{footer(ROOT)}
</body></html>
"""
    return H + body, body

def main():
    import re
    sdir = os.path.join(BASE, "services")
    os.makedirs(sdir, exist_ok=True)
    for slug, d in SERVICES.items():
        full, body = build_service(slug, d)
        open(os.path.join(sdir, f"{slug}.html"), "w", encoding="utf-8").write(full)
        text = re.sub(r"\s+"," ", re.sub(r"<[^>]+>"," ", re.sub(r"<(header|footer|aside|script|style).*?</\1>","",body,flags=re.S))).strip()
        print(f"SERVICE: {slug:8s} 본문 약 {len(text)}자")

if __name__ == "__main__":
    main()
