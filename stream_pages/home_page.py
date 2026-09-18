# stream_pages/home_page.py - 홈 및 대시보드 개요 페이지

import streamlit as st

st.title("🏠 홈 (Home)")
st.caption("Streamlit 멀티페이지 앱에 오신 것을 환영합니다.")

# [1. 주요 지표 메트릭]
st.subheader("📌 앱 개요 및 지표")
col1, col2, col3 = st.columns(3)
col1.metric("총 등록 페이지", "5개", delta="신규 추가")
col2.metric("라우터 방식", "st.navigation", delta="Modern API")
col3.metric("인증 상태", "로그인 연동됨" if st.user.get("is_logged_in", False) else "비로그인")

st.divider()

# [2. 빠른 페이지 바로가기 (st.page_link)]
st.subheader("🚀 주요 기능 바로가기")
col_a, col_b = st.columns(2)

with col_a:
    st.page_link(r"stream_pages\navigation_page.py", label="🧭 네비게이션 API 실습 페이지", help="네비게이션 기능 상세 실습")
    st.page_link(r"stream_pages\auth_page.py", label="🔐 Google 로그인 쇼케이스", help="사용자 인증 기능 확인")

with col_b:
    st.page_link(r"stream_pages\data_page.py", label="📊 데이터 분석 & 차트", help="데이터프레임 및 차트 시각화")
    st.page_link(r"stream_pages\settings_page.py", label="⚙️ 환경설정 페이지", help="앱 환경설정 조작")
