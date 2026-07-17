# Miyakojima Trip Dashboard 2026

2026-07-29부터 2026-08-02까지의 미야코지마 4박 5일 여행을 관리하는 Streamlit 대시보드입니다.

**Live app:** https://miyakojima-trip-dashboard-2026-rrrepfl5rzzfhfbss42rxn.streamlit.app/

현재 버전 `v0.5.0`에는 항공·렌터카 확정 동선과 숙소 주변 식당 20곳 핵심 정보에 더해, 아침 일정을 09:00 시작 기준으로 조정한 동선이 반영되어 있습니다(야비지 투어일인 4일차는 업체 고정 출항 시간 때문에 예외).

## 공개 데이터 원칙

- 상세 숙소 주소와 개인 정보는 저장소 및 앱에서 제외합니다.
- `event_id`는 이후 업데이트에서도 유지합니다.
- 항공편 시각은 7/29 11:00 도착, 8/2 12:00 탑승 기준입니다.
- 해양 활동 여부는 조석뿐 아니라 현장 통제, 파고, 풍속, 투어 업체 판단을 우선합니다.

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit Community Cloud는 `runtime.txt`에 따라 Python 3.12를 사용합니다.

## 업데이트

1. `data/itinerary.csv`, `data/tides.csv`, `data/restaurants.csv` 중 필요한 데이터를 수정합니다.
2. 앱을 로컬에서 확인합니다.
3. 변경 내용을 GitHub에 푸시하면 Streamlit Community Cloud가 자동으로 다시 배포합니다.
