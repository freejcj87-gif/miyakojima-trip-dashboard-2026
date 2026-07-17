# Miyakojima Trip Dashboard 2026

2026-07-29부터 2026-08-02까지의 미야코지마 4박 5일 여행을 관리하는 Streamlit 대시보드입니다.

**Live app:** https://miyakojima-trip-dashboard-2026-rrrepfl5rzzfhfbss42rxn.streamlit.app/

현재 버전 `v0.3.1`에는 7/29 11시 도착, 7/31 11시 30분 공항 도착, 8/2 11시 렌터카 사무실 도착 및 12시 항공편 탑승 동선이 반영되어 있습니다.

## 공개 데이터 원칙

- 상세 숙소 주소와 개인 정보는 저장소 및 앱에서 제외합니다.
- `event_id`는 이후 업데이트에서도 유지합니다.
- 항공편 시각은 현재 도착 15:30, 출발 15:30 가정값입니다.
- 해양 활동 여부는 조석뿐 아니라 현장 통제, 파고, 풍속, 투어 업체 판단을 우선합니다.

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit Community Cloud는 `runtime.txt`에 따라 Python 3.12를 사용합니다.

## 업데이트

1. `data/itinerary.csv` 또는 `data/tides.csv`를 수정합니다.
2. 앱을 로컬에서 확인합니다.
3. 변경 내용을 GitHub에 푸시하면 Streamlit Community Cloud가 자동으로 다시 배포합니다.
