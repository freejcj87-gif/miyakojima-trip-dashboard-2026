import base64
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
           border-radius:18px; color:white; margin-bottom:1rem;
           display:flex; align-items:center; gap:1.25rem;}
    .hero h1 {margin:0; font-size:clamp(1.55rem,5vw,2.15rem);} .hero p {margin:.5rem 0 0; opacity:.92;}
    .hero-img {width:138px; height:138px; object-fit:cover; object-position:center 62%;
               border-radius:18px; border:3px solid rgba(255,255,255,.6); flex:none;
               box-shadow:0 4px 16px rgba(0,0,0,.28);}
    .badge-need {display:inline-block; background:#D93636; color:#fff; border-radius:999px;
                 padding:.16rem .6rem; margin:.25rem .25rem 0 0; font-size:.76rem; font-weight:800;
                 box-shadow:0 1px 6px rgba(217,54,54,.35); vertical-align:middle;}
    .badge-done {display:inline-block; background:#1E9E4B; color:#fff; border-radius:999px;
                 padding:.16rem .6rem; margin:.25rem .25rem 0 0; font-size:.76rem; font-weight:800;
                 box-shadow:0 1px 6px rgba(30,158,75,.35); vertical-align:middle;}
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
      .hero {padding:1.1rem 1rem; border-radius:14px; gap:.8rem;}
      .hero p {font-size:.86rem; line-height:1.45;}
      .hero-img {width:92px; height:92px; border-radius:14px;}
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

hero_img_path = ROOT / "assets" / "hero.jpg"
hero_img_html = ""
if hero_img_path.exists():
    hero_b64 = base64.b64encode(hero_img_path.read_bytes()).decode()
    hero_img_html = f'<img class="hero-img" src="data:image/jpeg;base64,{hero_b64}" alt="규나와 연우"/>'

st.markdown(
    f"""
    <div class="hero">
      {hero_img_html}
      <div>
        <h1>🏝️ 규나 &amp; 연우 Summer IN 미야코지마</h1>
        <p>'26.07.29~'26.08.02</p>
      </div>
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

tab_grid, tab_timeline, tab_overview, tab_restaurants, tab_tides, tab_check = st.tabs(
    ["📅 시간표", "🕒 날짜별 타임라인", "🗓️ 전체 일정", "🍽️ 식당 리스트", "🌊 조석·일몰", "✅ 예약·안전"]
)

with tab_grid:
    st.subheader("5일 전체 시간표")
    st.caption("대학교 시간표처럼 한눈에 보는 전체 동선입니다. 블록에 마우스를 올리면 상세 활동이 표시됩니다.")

    CAT_STYLE = {
        "이동": ("#EDF1F5", "#49607A"),
        "해변": ("#DBEFFB", "#0B6AA8"),
        "투어": ("#D7EEF0", "#0F766E"),
        "식사": ("#FFE8D1", "#A85B00"),
        "카페": ("#FFF3C4", "#8A6D00"),
        "관광": ("#E3F4E3", "#2F7D32"),
        "휴식": ("#EFE9F7", "#6B4FA1"),
        "쇼핑": ("#FBE3EE", "#A83E6E"),
    }
    PX_PER_HOUR = 52
    GRID_START, GRID_END = 6 * 60, 21 * 60 + 30
    col_height = (GRID_END - GRID_START) / 60 * PX_PER_HOUR

    def _to_min(hhmm):
        h, m = hhmm.split(":")
        return int(h) * 60 + int(m)

    weekday_ko = ["월", "화", "수", "목", "금", "토", "일"]
    axis_html = "".join(
        f'<div class="tt-hour" style="top:{(h * 60 - GRID_START) / 60 * PX_PER_HOUR}px">{h:02d}</div>'
        for h in range(6, 22)
    )
    cols_html = ""
    for day in itinerary["day_label"].drop_duplicates():
        sub = itinerary[itinerary["day_label"].eq(day)]
        day_date = sub["date"].iloc[0]
        blocks = ""
        for row in sub.itertuples():
            top = (_to_min(row.start) - GRID_START) / 60 * PX_PER_HOUR
            height = max((_to_min(row.end) - _to_min(row.start)) / 60 * PX_PER_HOUR - 2, 14)
            bg, fg = CAT_STYLE.get(row.category, ("#EEF2F5", "#3D5468"))
            book_mark, book_style = "", ""
            if row.booking == "예약필":
                book_mark = "❗"
                book_style = "box-shadow:inset 0 0 0 2px #D93636;"
            elif row.booking == "예약완료":
                book_mark = "✅"
                book_style = "box-shadow:inset 0 0 0 2px #1E9E4B;"
            tip = escape(
                f"{row.start}–{row.end} {row.place} · {row.activity}"
                + (f" · {row.booking}" if row.booking else "")
                + (f" · 🐢거북이 {row.turtle}" if row.turtle else ""),
                quote=True,
            )
            blocks += (
                f'<div class="tt-ev" title="{tip}" style="top:{top}px;height:{height}px;'
                f'background:{bg};color:{fg};{book_style}">'
                f'<span class="tt-ev-t">{row.start}</span> {book_mark}{escape(row.place)}</div>'
            )
        cols_html += (
            f'<div class="tt-col"><div class="tt-head">{day}<br>'
            f'<span>{day_date:%m/%d}({weekday_ko[day_date.weekday()]})</span></div>'
            f'<div class="tt-body" style="height:{col_height}px">{blocks}</div></div>'
        )
    legend_html = "".join(
        f'<span class="tag" style="background:{bg};color:{fg}">{cat}</span>'
        for cat, (bg, fg) in CAT_STYLE.items()
    ) + (
        '<span class="badge-need">❗ 예약필</span>'
        '<span class="badge-done">✅ 예약완료</span>'
    )
    st.markdown(
        f"""
        <style>
        .tt-wrap {{overflow-x:auto; padding-bottom:.6rem;}}
        .tt {{display:flex; gap:5px; min-width:660px;}}
        .tt-axis {{width:34px; flex:none;}}
        .tt-axis-body {{position:relative;}}
        .tt-hour {{position:absolute; right:4px; transform:translateY(-50%); font-size:.66rem; color:#7A93A5;}}
        .tt-col {{flex:1; min-width:112px;}}
        .tt-head {{text-align:center; font-weight:800; color:#17324D; font-size:.85rem; height:42px; line-height:1.3;}}
        .tt-head span {{font-weight:600; color:#496579; font-size:.72rem;}}
        .tt-body {{position:relative; background:white; border:1px solid #DDEBEA; border-radius:10px;
                   background-image:repeating-linear-gradient(to bottom, #EFF4F3 0 1px, transparent 1px {PX_PER_HOUR}px);}}
        .tt-ev {{position:absolute; left:3px; right:3px; border-radius:6px; padding:1px 5px;
                 font-size:.63rem; line-height:1.25; overflow:hidden; font-weight:600;}}
        .tt-ev-t {{font-weight:800; opacity:.75;}}
        </style>
        <div style="margin-bottom:.5rem">{legend_html}</div>
        <div class="tt-wrap"><div class="tt">
          <div class="tt-axis"><div class="tt-head"></div><div class="tt-axis-body" style="height:{col_height}px">{axis_html}</div></div>
          {cols_html}
        </div></div>
        """,
        unsafe_allow_html=True,
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
            turtle_tag = f'<span class="tag">🐢 거북이 {row.turtle}</span>' if row.turtle else ""
            if row.booking == "예약필":
                booking_badge = '<span class="badge-need">❗ 예약필</span>'
            elif row.booking == "예약완료":
                booking_badge = '<span class="badge-done">✅ 예약완료</span>'
            else:
                booking_badge = ""
            st.markdown(
                f"""
                <div class="event">
                  <span class="event-time">{row.start}–{row.end}</span> {booking_badge}
                  <div class="event-place">{row.place}</div>
                  <div>{row.activity}{map_link}</div>
                  <span class="tag">{row.area}</span><span class="tag">{row.category}</span>
                  <span class="tag">{row.status}</span>{meal}{tide_tag}{turtle_tag}
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
            st.success("11:00 공항 도착 → PADA X SOU 무료 픽업 → 12:45 Blue Turtle 점심 → 이라부대교 경유 15:00 체크인")
            st.info("Blue Turtle: 점심 11:00~17:00 연속 영업·일요일 휴무·점심 예약 불가(워크인). 대안: 이라부소바 카메(15시 전 품절 주의)")
        elif selected_day == "3일차":
            st.warning("11:30까지 시모지시마 공항 도착. 숙소에서 10:30 출발, 11:15 도착 목표로 15분 여유를 둡니다.")
        elif selected_day == "4일차":
            st.warning("야비지 투어 출항 08:00은 업체 고정 시간입니다. 5일 중 이 날만 06:30 이른 시작이 필요합니다.")
            st.success("야비지 투어 종료 약 17:00 → 야키니쿠 나카오 19:00 저녁, 6석 예약 완료 ✅")
        elif selected_day == "5일차":
            st.warning("PADA X SOU 지정 사무실 반납. 지도에 ‘폐업함’으로 표시되어도 안내받은 위치가 맞습니다.")
            st.info("12:00 항공편 탑승 · 11:00 렌터카 사무실 도착 · 반납 후 즉시 무료 송영으로 공항 이동")
            st.error("반납 사무실 11:00 도착은 탑승까지 여유가 매우 적습니다. 주유·짐 정리를 미리 끝내고 지연 없이 반납해야 합니다.")
        else:
            st.info("아이 컨디션과 현장 파도·바람이 일정표보다 우선입니다.")

with tab_overview:
    st.subheader("전체 5일 일정")
    display = itinerary[["date", "day_label", "start", "end", "place", "category", "activity", "status", "booking", "turtle"]].copy()
    display["date"] = display["date"].dt.strftime("%m/%d")
    display["booking"] = display["booking"].map(
        lambda v: "❗ 예약필" if v == "예약필" else ("✅ 예약완료" if v == "예약완료" else "")
    )
    display["turtle"] = display["turtle"].map(lambda v: f"🐢 {v}" if v else "")
    display.columns = ["날짜", "일차", "시작", "종료", "장소", "유형", "활동", "상태", "예약", "거북이"]
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
        ("야키니쿠", "✅ 예약 완료 — 8/1 19:00 나카오 성인 4명+8세 2명, 총 6석"),
        ("식당", "✅ 카메스시 7/31 18:00 6석 예약 완료(김규나 명의) · Free Bird 6석 예약 필요, Ninufa·돈카라야 당일 영업 확인"),
        ("해양 안전", "출발 48시간 전 풍속·파고·현지 통제 재확인, 어린이 1명당 담당 성인 지정"),
        ("폭염", "45~60분마다 물·그늘 휴식, 아이 컨디션에 따라 일정 단축"),
    ]
    for label, task in checklist:
        st.checkbox(f"**{label}** — {task}", key=f"check-{label}")
    st.link_button("PADA X SOU 반납 사무실 지도", "https://maps.app.goo.gl/zkaRcF2k9TVfqGvq7?g_st=ac")
    st.divider()
    st.markdown("**공식 참고:** [JMA 조석표](https://www.data.jma.go.jp/kaiyou/db/tide/suisan/suisan.php?LV=DL&S_HILO=on&de=03&ds=20&me=08&ms=07&stn=R1&ye=2026&ys=2026) · [야비지](https://miyako-guide.net/spots/spots-1508/) · [시모지시마](https://visitokinawajapan.com/destinations/miyako-islands/shimoji-island/) · [야키니쿠 나카오](https://yakinikunakao.owst.jp/)")

st.divider()
st.caption("v0.7.0 · 타이틀 리뉴얼·식당 예약필/예약완료 배지 추가 · 아침 시작 09:00 기준(야비지 투어일 제외) · 운영시간·예약·날씨·투어 일정은 출발 직전 다시 확인하세요.")
