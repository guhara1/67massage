# -*- coding: utf-8 -*-
"""
GA4 일일 리포트 → 텔레그램 발송.
GitHub Actions(예약)에서 실행. 다음 환경변수(=GitHub Secrets) 필요:
  GA4_PROPERTY_ID            GA4 속성 ID(숫자, 측정ID G-… 아님)
  TELEGRAM_BOT_TOKEN         텔레그램 봇 토큰(123456:ABC…)
  TELEGRAM_CHAT_ID           받을 채팅 ID(개인/그룹/채널)
  GOOGLE_APPLICATION_CREDENTIALS  서비스계정 JSON 파일 경로(워크플로가 생성)
"""
import os, json, urllib.request, urllib.parse
from datetime import datetime, timedelta, timezone

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, OrderBy)

PROP = os.environ["GA4_PROPERTY_ID"]
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]
client = BetaAnalyticsDataClient()
KST = timezone(timedelta(hours=9))

def totals(start, end):
    r = client.run_report(RunReportRequest(
        property=f"properties/{PROP}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        metrics=[Metric(name="activeUsers"), Metric(name="sessions"),
                 Metric(name="screenPageViews")]))
    if not r.rows: return (0,0,0)
    v = r.rows[0].metric_values
    return (int(v[0].value), int(v[1].value), int(v[2].value))

def top_pages(start, end, n=5):
    r = client.run_report(RunReportRequest(
        property=f"properties/{PROP}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimensions=[Dimension(name="pageTitle")],
        metrics=[Metric(name="screenPageViews")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
        limit=n))
    return [(row.dimension_values[0].value, int(row.metric_values[0].value)) for row in r.rows]

def events(start, end):
    r = client.run_report(RunReportRequest(
        property=f"properties/{PROP}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")]))
    d = {row.dimension_values[0].value: int(row.metric_values[0].value) for row in r.rows}
    return d

def top_sources(start, end, n=4):
    r = client.run_report(RunReportRequest(
        property=f"properties/{PROP}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimensions=[Dimension(name="sessionDefaultChannelGroup")],
        metrics=[Metric(name="sessions")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=n))
    return [(row.dimension_values[0].value, int(row.metric_values[0].value)) for row in r.rows]

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build_message():
    y_u, y_s, y_v = totals("yesterday", "yesterday")
    w_u, w_s, w_v = totals("7daysAgo", "yesterday")
    ev = events("yesterday", "yesterday")
    evw = events("7daysAgo", "yesterday")
    calls = ev.get("phone_call", 0); sms = ev.get("sms_click", 0)
    calls_w = evw.get("phone_call", 0); sms_w = evw.get("sms_click", 0)
    pages = top_pages("yesterday", "yesterday")
    srcs = top_sources("7daysAgo", "yesterday")
    ymd = (datetime.now(KST) - timedelta(days=1)).strftime("%Y-%m-%d")

    lines = []
    lines.append(f"<b>📊 67 마사지 · GA4 리포트</b>")
    lines.append(f"<i>{ymd} (어제 기준)</i>\n")
    lines.append("<b>어제</b>")
    lines.append(f"· 방문자 {y_u} · 세션 {y_s} · 페이지뷰 {y_v}")
    lines.append(f"· 📞 전화클릭 {calls} · ✉️ 문자클릭 {sms}\n")
    lines.append("<b>최근 7일</b>")
    lines.append(f"· 방문자 {w_u} · 세션 {w_s} · 페이지뷰 {w_v}")
    lines.append(f"· 📞 전화클릭 {calls_w} · ✉️ 문자클릭 {sms_w}")
    if srcs:
        lines.append("\n<b>유입 경로(7일)</b>")
        for name, s in srcs: lines.append(f"· {esc(name)} — {s}")
    if pages:
        lines.append("\n<b>어제 인기 페이지</b>")
        for t, v in pages: lines.append(f"· {esc(t)[:40]} — {v}")
    return "\n".join(lines)

def send(text):
    data = urllib.parse.urlencode({
        "chat_id": CHAT, "text": text,
        "parse_mode": "HTML", "disable_web_page_preview": "true"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data)
    with urllib.request.urlopen(req, timeout=20) as r:
        print("Telegram:", r.status)

if __name__ == "__main__":
    try:
        msg = build_message()
    except Exception as e:
        msg = f"⚠️ GA4 리포트 생성 실패: {type(e).__name__}: {e}"
    print(msg)
    send(msg)
