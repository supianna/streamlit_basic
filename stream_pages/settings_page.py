# stream_pages/settings_page.py - 환경설정 및 사용자 옵션 페이지

import streamlit as st

st.title("⚙️ 환경설정 (Settings)")
st.caption("앱 설정 및 사용자 개인화 옵션을 조작할 수 있는 페이지입니다.")

# [1. 일반 설정]
st.subheader("🛠️ 일반 설정")
app_theme = st.selectbox("기본 테마 선택", ["시스템 기본값", "라이트 모드", "다크 모드"])
enable_notifications = st.toggle("이메일 알림 받기", value=True)
auto_refresh = st.checkbox("데이터 자동 새로고침 (5분 주기)", value=False)

# [2. 계정 환경설정]
st.subheader("👤 프로필 및 표시 옵션")
display_name = st.text_input("표시 이름(닉네임)", value=st.user.get("name", "홍길동"))
language = st.radio("언어 설정", ["한국어 (Korean)", "English"], horizontal=True)

st.divider()

# [3. 설정 저장 버튼]
if st.button("설정 저장", type="primary"):
    st.success(f"설정이 저장되었습니다! (테마: {app_theme}, 언어: {language})")
    st.toast("성공적으로 저장되었습니다.")
