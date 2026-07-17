from pathlib import Path
from html import escape

import altair as alt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).parent
DATA = ROOT / "data"

st.set_page_config(
    page_title="미야코지마 4박 5일",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_data():
    itinerary = pd.read_csv(DATA / "itinerary.csv", dtype=str).fillna("")
    itinerary["date"] = pd.to_datetime(itinerary["date"])
    tides = pd.read_csv(DATA / "tides.csv", dtype=str).fillna("")
    tides["date"] = pd.to_datetime(tides["date"])
    for col in ["high_1_cm", "high_2_cm", "low_1_cm", "low_2_cm"]:
        tides[col] = pd.to_numeric(tides[col])
    restaurants = pd.read_csv(DATA / "restaurants.csv", dtype=str).fillna("")
    restaurants["rank"] = pd.to_numeric(restaurants["rank"])
    return itinerary, tides, restaurants


itinerary, tides, restaurants = load_data()

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.7rem; padding-bottom: 4rem;}
    .hero {background:linear-gradient(120deg,#12304A,#0F766E); padding:1.5rem 1.7rem;
           border-radius:18px; color:white; margin-bottom:1rem;}
    .hero h1 {margin:0; font-size:clamp(1.55rem,5vw,2.15rem);} .hero p {margin:.5rem 0 0; opacity:.92;}
    .event {border-left:5px solid #0F766E; background:white; border-radius:10px;
            padding:.85rem 1rem; margin:.55rem 0; box-shadow:0 2px 12px rgba(15,118,110,.08);}
    .event-time {font-weight:800; color:#0F766E;} .event-place {font-size:1.08rem; font-weight:750;}
    .tag {display:inline-block; background:#E6F7F5; color:#0F5F59; border-radius:999px;
          padding:.15rem .55rem; margin:.25rem .25rem 0 0; font-size:.78rem;}
    .warn {background:#FFF7D6; border:1px solid #F5D26B; border-radius:12px; padding:.8rem 1rem;}
    .metric-grid {display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:.75rem; margin:1rem 0;}
    .metric-card {background:white; border:1px solid #DDEBEA; padding:.85rem 1rem; border-radius:14px;}
    .metric-label {font-size:.82rem; color:#496579;} .metric-value {font-size:1.55rem; color:#17324D; margin-top:.2rem;}
    .restaurant-card {background:white; border:1px solid #DDEBEA; border-radius:14px;
                      padding:1rem 1.1rem; margin:.7rem 0; box-shadow:0 2px 12px rgba(15,48,74,.06);}
    .restaurant-head {display:flex; gap:.55rem; align-items:flex-start; margin-bottom:.45rem;}
    .restaurant-rank {background:#17324D; color:white; border-radius:999px; padding:.18rem .55rem;
                      font-size:.75rem; white-space:nowrap;}
    .restaurant-name {font-weight:800; font-size:1.05rem; color:#17324D;}
    .restaurant-meta {color:#496579; font-size:.88rem; line-height:1.55;}
    .restaurant-booking {margin:.45rem 0; padding:.45rem .65rem; border-radius:9px; background:#FFF7D6; color:#725A00;}
    .restaurant-links {display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.65rem;}
    .restaurant-links a {text-decoration:none; border-radius:9px; padding:.45rem .7rem; font-weight:700;
                         background:#E6F7F5; color:#0F5F59; border:1px solid #B8E2DE;}
    @media (max-width: 768px) {
      .block-container {padding:1rem .8rem 3rem;}
      .hero {padding:1.1rem 1rem; border-radius:14px;}
      .hero p {font-size:.86rem; line-height:1.45;}
      .metric-grid {grid-template-columns:repeat(2,minmax(0,1fr)); gap:.55rem;}
      .metric-card {padding:.7rem .75rem;} .metric-value {font-size:1.2rem;}
      .event {padding:.75rem .8rem;} .event-place {font-size:1rem;}
      .restaurant-card {padding:.85rem .8rem;} .restaurant-name {font-size:1rem;}
      [data-testid="stTabs"] button {padding-left:.55rem; padding-right:.55rem; font-size:.82rem;}
    }
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
    st.markdown("**🚐 PADA X SOU 렌터카**")
    st.caption("7/29 공항 무료 픽업 · 8/2 지정 사무실 반납")
    st.link_button("반납 사무실 지도", "https://maps.app.goo.gl/zkaRcF2k9TVfqGvq7?g_st=ac", use_container_width=True)
    st.divider()
    st.caption("공개용 대시보드에는 숙소 상세 주소와 개인 정보가 포함되지 않습니다.")

day_data = itinerary[itinerary["day_label"].eq(selected_day)].copy()
filtered_day = day_data[day_data["category"].isin(categories)]
selected_date = day_data["date"].iloc[0]
tide = tides[tides["date"].eq(selected_date)].iloc[0]

st.markdown(
    f"""
    <div class="metric-grid">
      <div class="metric-card"><div class="metric-label">오늘 일정</div><div class="metric-value">{len(day_data)}개</div></div>
      <div class="metric-card"><div class="metric-label">식사·카페</div><div class="metric-value">{day_data['category'].isin(['식사','카페']).sum()}곳</div></div>
      <div class="metric-card"><div class="metric-label">첫 만조</div><div class="metric-value">{tide.high_1} · {tide.high_1_cm}cm</div></div>
      <div class="metric-card"><div class="metric-label">일몰</div><div class="metric-value">{tide.sunset}</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_timeline, tab_overview, tab_restaurants, tab_tides, tab_check = st.tabs(
    ["🕒 날짜별 타임라인", "🗓️ 전체 일정", "🍽️ 식당 리스트", "🌊 조석·일몰", "✅ 예약·안전"]
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
        if selected_day == "1일차":
            st.success("11:00 공항 도착 → PADA X SOU 무료 픽업 → 12:40 17END. 간조 13:37을 활용합니다.")
        elif selected_day == "3일차":
            st.warning("11:30까지 시모지시마 공항 도착. 숙소에서 10:30 출발, 11:15 도착 목표로 15분 여유를 둡니다.")
        elif selected_day == "4일차":
            st.warning("야비지 투어 출항 08:00은 업체 고정 시간입니다. 5일 중 이 날만 06:30 이른 시작이 필요합니다.")
            st.error("야비지 투어 종료 약 17:00 → 야키니쿠 나카오 19:00, 6석 예약 필수")
        elif selected_day == "5일차":
            st.warning("PADA X SOU 지정 사무실 반납. 지도에 ‘폐업함’으로 표시되어도 안내받은 위치가 맞습니다.")
            st.info("12:00 항공편 탑승 · 11:00 렌터카 사무실 도착 · 반납 후 즉시 무료 송영으로 공항 이동")
            st.error("반납 사무실 11:00 도착은 탑승까지 여유가 매우 적습니다. 주유·짐 정리를 미리 끝내고 지연 없이 반납해야 합니다.")
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

with tab_restaurants:
    st.subheader("숙소 주변 검토 식당 20곳")
    st.caption("엑셀 검토 목록에서 여행 중 판단에 필요한 정보만 추렸습니다. 거리·이동시간과 예약 가능 여부는 출발 전 다시 확인하세요.")

    search_col, booking_col = st.columns([1.35, 1])
    with search_col:
        restaurant_search = st.text_input("식당·음식 검색", placeholder="예: 미야코규, 카페, 보부리")
    with booking_col:
        booking_filter = st.selectbox(
            "예약 기준",
            ["전체", "온라인 예약 가능/권장", "전화/현장 확인", "예약 불필요/불가"],
        )

    restaurant_view = restaurants.copy()
    restaurant_view["booking_group"] = restaurant_view["reservation"].apply(
        lambda value: (
            "예약 불필요/불가"
            if "불필요" in value or "불가" in value
            else "전화/현장 확인"
            if "전화" in value or "현장" in value
            else "온라인 예약 가능/권장"
        )
    )
    if restaurant_search:
        query = restaurant_search.strip().lower()
        searchable = restaurant_view[["name", "cuisine", "distance", "family_group", "alternative_slot"]].agg(" ".join, axis=1).str.lower()
        restaurant_view = restaurant_view[searchable.str.contains(query, regex=False)]
    if booking_filter != "전체":
        restaurant_view = restaurant_view[restaurant_view["booking_group"].eq(booking_filter)]

    st.caption(f"조건에 맞는 식당 {len(restaurant_view)}곳")
    if restaurant_view.empty:
        st.info("검색 조건에 맞는 식당이 없습니다.")
    for row in restaurant_view.sort_values("rank").itertuples():
        official_link = (
            f'<a href="{escape(row.reservation_url, quote=True)}" target="_blank">예약·공식 정보</a>'
            if row.reservation_url
            else ""
        )
        st.markdown(
            f"""
            <div class="restaurant-card">
              <div class="restaurant-head">
                <span class="restaurant-rank">추천 {row.rank}</span>
                <span class="restaurant-name">{escape(row.name)}</span>
              </div>
              <div class="restaurant-meta"><b>음식</b> {escape(row.cuisine)} · {escape(row.recommended_time)}</div>
              <div class="restaurant-meta"><b>숙소 기준</b> {escape(row.distance)}</div>
              <div class="restaurant-meta"><b>이용</b> {escape(row.family_group)}</div>
              <div class="restaurant-meta"><b>대체 가능 일정</b> {escape(row.alternative_slot)}</div>
              <div class="restaurant-booking"><b>예약</b> {escape(row.reservation)}</div>
              <div class="restaurant-links">
                <a href="{escape(row.map_url, quote=True)}" target="_blank">Google 지도</a>
                {official_link}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.download_button(
        "핵심 식당 리스트 CSV 다운로드",
        restaurants.to_csv(index=False).encode("utf-8-sig"),
        file_name="miyakojima_restaurants_core.csv",
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
        ("항공편", "7/29 11:00 도착, 8/2 12:00 항공편 탑승 확정"),
        ("7/31 공항 픽업", "11:30까지 시모지시마 공항 도착. 숙소에서 10:30 출발하고 도착편·짐 수량 확인"),
        ("렌터카 서류", "7/26까지 운전자 전원의 국제면허 앞면·사진면, 여권 사진면, 한국면허증 앞면 제출"),
        ("공항 픽업", "7/29 출국장 앞 담당자 피켓 확인 후 도착 채팅, 무료 픽업으로 PADA X SOU 사무실 이동"),
        ("차량", "성인 4명+아동 2명과 4박 짐이 들어가는 차급·주니어 시트 확인"),
        ("반납", "8/2 11:00까지 지정 사무실 도착. 지도의 ‘폐업함’ 표시와 무관하게 안내 위치 이용·반납 후 즉시 공항 이동"),
        ("야비지", "8세 2명 참가 가능 연령·집합지·종료·아동용 구명조끼·화장실 확인"),
        ("야키니쿠", "8/1 19:00 나카오 성인 4명+8세 2명, 총 6석 예약"),
        ("식당", "Free Bird·보부리 6석과 아동 동반, Ninufa·Cafe Nuis 당일 영업 확인"),
        ("해양 안전", "출발 48시간 전 풍속·파고·현지 통제 재확인, 어린이 1명당 담당 성인 지정"),
        ("폭염", "45~60분마다 물·그늘 휴식, 아이 컨디션에 따라 일정 단축"),
    ]
    for label, task in checklist:
        st.checkbox(f"**{label}** — {task}", key=f"check-{label}")
    st.link_button("PADA X SOU 반납 사무실 지도", "https://maps.app.goo.gl/zkaRcF2k9TVfqGvq7?g_st=ac")
    st.divider()
    st.markdown("**공식 참고:** [JMA 조석표](https://www.data.jma.go.jp/kaiyou/db/tide/suisan/suisan.php?LV=DL&S_HILO=on&de=03&ds=20&me=08&ms=07&stn=R1&ye=2026&ys=2026) · [야비지](https://miyako-guide.net/spots/spots-1508/) · [시모지시마](https://visitokinawajapan.com/destinations/miyako-islands/shimoji-island/) · [야키니쿠 나카오](https://yakinikunakao.owst.jp/)")

st.divider()
st.caption("v0.5.0 · 아침 시작 09:00 기준으로 일정 조정(야비지 투어일 제외) · 운영시간·예약·날씨·투어 일정은 출발 직전 다시 확인하세요.")
