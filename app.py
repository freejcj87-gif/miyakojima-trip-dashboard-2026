from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).parent
DATA = ROOT / "data"

st.set_page_config(
    page_title="미야코지마 4박 5일",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    itinerary = pd.read_csv(DATA / "itinerary.csv", dtype=str).fillna("")
    itinerary["date"] = pd.to_datetime(itinerary["date"])
    tides = pd.read_csv(DATA / "tides.csv", dtype=str).fillna("")
    tides["date"] = pd.to_datetime(tides["date"])
    for col in ["high_1_cm", "high_2_cm", "low_1_cm", "low_2_cm"]:
        tides[col] = pd.to_numeric(tides[col])
    return itinerary, tides


itinerary, tides = load_data()

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.7rem; padding-bottom: 4rem;}
    .hero {background:linear-gradient(120deg,#12304A,#0F766E); padding:1.5rem 1.7rem;
           border-radius:18px; color:white; margin-bottom:1rem;}
    .hero h1 {margin:0; font-size:2.15rem;} .hero p {margin:.5rem 0 0; opacity:.92;}
    .event {border-left:5px solid #0F766E; background:white; border-radius:10px;
            padding:.85rem 1rem; margin:.55rem 0; box-shadow:0 2px 12px rgba(15,118,110,.08);}
    .event-time {font-weight:800; color:#0F766E;} .event-place {font-size:1.08rem; font-weight:750;}
    .tag {display:inline-block; background:#E6F7F5; color:#0F5F59; border-radius:999px;
          padding:.15rem .55rem; margin:.25rem .25rem 0 0; font-size:.78rem;}
    .warn {background:#FFF7D6; border:1px solid #F5D26B; border-radius:12px; padding:.8rem 1rem;}
    [data-testid="stMetric"] {background:white; border:1px solid #DDEBEA; padding:.8rem;
                              border-radius:14px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🏝️ MIYAKOJIMA 4박 5일</h1>
      <p>2026.07.29–08.02 · 성인 4명 + 8세 2명 · 렌터카 · 조석 기반 해변 동선</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("여행 설정")
    selected_day = st.radio(
        "날짜",
        options=itinerary["day_label"].drop_duplicates().tolist(),
        format_func=lambda x: f"{x} · {itinerary.loc[itinerary.day_label.eq(x), 'date'].iloc[0]:%m/%d}",
    )
    all_categories = sorted(itinerary["category"].unique().tolist())
    categories = st.multiselect("일정 유형", all_categories, default=all_categories)
    st.divider()
    st.caption("공개용 대시보드에는 숙소 상세 주소와 개인 정보가 포함되지 않습니다.")

day_data = itinerary[itinerary["day_label"].eq(selected_day)].copy()
filtered_day = day_data[day_data["category"].isin(categories)]
selected_date = day_data["date"].iloc[0]
tide = tides[tides["date"].eq(selected_date)].iloc[0]

m1, m2, m3, m4 = st.columns(4)
m1.metric("오늘 일정", f"{len(day_data)}개")
m2.metric("식사·카페", f"{day_data['category'].isin(['식사','카페']).sum()}곳")
m3.metric("첫 만조", f"{tide.high_1} · {tide.high_1_cm}cm")
m4.metric("일몰", tide.sunset)

tab_timeline, tab_overview, tab_tides, tab_check = st.tabs(
    ["🕒 날짜별 타임라인", "🗓️ 전체 일정", "🌊 조석·일몰", "✅ 예약·안전"]
)

with tab_timeline:
    left, right = st.columns([2.15, 1])
    with left:
        st.subheader(f"{selected_day} · {selected_date:%Y년 %m월 %d일}")
        if filtered_day.empty:
            st.info("선택한 유형에 해당하는 일정이 없습니다.")
        for row in filtered_day.itertuples():
            map_link = f' · <a href="{row.maps_url}" target="_blank">Google 지도</a>' if row.maps_url else ""
            meal = f'<span class="tag">{row.meal}</span>' if row.meal else ""
            tide_tag = f'<span class="tag">🌊 {row.tide_note}</span>' if row.tide_note and row.tide_note != "없음" else ""
            st.markdown(
                f"""
                <div class="event">
                  <span class="event-time">{row.start}–{row.end}</span>
                  <div class="event-place">{row.place}</div>
                  <div>{row.activity}{map_link}</div>
                  <span class="tag">{row.area}</span><span class="tag">{row.category}</span>
                  <span class="tag">{row.status}</span>{meal}{tide_tag}
                </div>
                """,
                unsafe_allow_html=True,
            )
    with right:
        st.subheader("오늘의 조석")
        st.markdown(
            f"""
            <div class="warn">
            <b>만조</b> {tide.high_1} ({tide.high_1_cm}cm) · {tide.high_2} ({tide.high_2_cm}cm)<br>
            <b>간조</b> {tide.low_1} ({tide.low_1_cm}cm) · {tide.low_2} ({tide.low_2_cm}cm)<br>
            <b>해 뜸/짐</b> {tide.sunrise} / {tide.sunset}<br><br>
            {tide.recommendation}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.subheader("핵심 운영")
        if selected_day == "4일차":
            st.error("야비지 투어 종료 약 17:00 → 야키니쿠 나카오 19:00, 6석 예약 필수")
        elif selected_day == "5일차":
            st.warning("출발 15:30 가정. 늦은 항공편이면 17END를 13:30 이후로 이동")
        else:
            st.info("아이 컨디션과 현장 파도·바람이 일정표보다 우선입니다.")

with tab_overview:
    st.subheader("전체 5일 일정")
    display = itinerary[["date", "day_label", "start", "end", "place", "category", "activity", "status"]].copy()
    display["date"] = display["date"].dt.strftime("%m/%d")
    display.columns = ["날짜", "일차", "시작", "종료", "장소", "유형", "활동", "상태"]
    st.dataframe(display, hide_index=True, use_container_width=True, height=610)
    st.download_button(
        "공개용 일정 CSV 다운로드",
        itinerary.to_csv(index=False).encode("utf-8-sig"),
        file_name="miyakojima_public_itinerary.csv",
        mime="text/csv",
    )

with tab_tides:
    st.subheader("2026년 조석 높이")
    chart_data = tides.melt(
        id_vars=["date"],
        value_vars=["high_1_cm", "high_2_cm", "low_1_cm", "low_2_cm"],
        var_name="type",
        value_name="height_cm",
    )
    labels = {"high_1_cm":"첫 만조", "high_2_cm":"둘째 만조", "low_1_cm":"첫 간조", "low_2_cm":"둘째 간조"}
    chart_data["type"] = chart_data["type"].map(labels)
    chart = (
        alt.Chart(chart_data)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("date:T", title="날짜", axis=alt.Axis(format="%m/%d")),
            y=alt.Y("height_cm:Q", title="예측 조위(cm)"),
            color=alt.Color("type:N", title="조석"),
            tooltip=[alt.Tooltip("date:T", format="%Y-%m-%d"), "type:N", "height_cm:Q"],
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)
    tide_table = tides.copy()
    tide_table["date"] = tide_table["date"].dt.strftime("%m/%d")
    tide_table.columns = ["날짜","요일","만조1","cm","만조2","cm ","간조1","cm  ","간조2","cm   ","일출","일몰","추천"]
    st.dataframe(tide_table, hide_index=True, use_container_width=True)
    st.caption("조석: 일본 기상청(JMA) 히라라 지점 예측값. 조석만으로 입수 안전을 판단하지 마세요.")

with tab_check:
    st.subheader("출발 전 필수 확인")
    checklist = [
        ("항공편", "7/29 도착·8/2 출발 시각 확정 후 1·5일차 조정"),
        ("렌터카", "성인 4명+아동 2명과 4박 짐이 들어가는 미니밴급·주니어 시트 확인"),
        ("야비지", "8세 2명 참가 가능 연령·집합지·종료·아동용 구명조끼·화장실 확인"),
        ("야키니쿠", "8/1 19:00 나카오 성인 4명+8세 2명, 총 6석 예약"),
        ("식당", "Free Bird·보부리 6석과 아동 동반, Ninufa·Cafe Nuis 당일 영업 확인"),
        ("해양 안전", "출발 48시간 전 풍속·파고·현지 통제 재확인, 어린이 1명당 담당 성인 지정"),
        ("폭염", "45~60분마다 물·그늘 휴식, 아이 컨디션에 따라 일정 단축"),
    ]
    for label, task in checklist:
        st.checkbox(f"**{label}** — {task}", key=f"check-{label}")
    st.divider()
    st.markdown("**공식 참고:** [JMA 조석표](https://www.data.jma.go.jp/kaiyou/db/tide/suisan/suisan.php?LV=DL&S_HILO=on&de=03&ds=20&me=08&ms=07&stn=R1&ye=2026&ys=2026) · [야비지](https://miyako-guide.net/spots/spots-1508/) · [시모지시마](https://visitokinawajapan.com/destinations/miyako-islands/shimoji-island/) · [야키니쿠 나카오](https://yakinikunakao.owst.jp/)")

st.divider()
st.caption("v0.1.0 · 마지막 정리 2026-07-17 · 운영시간·날씨·투어 일정은 출발 직전 다시 확인하세요.")

