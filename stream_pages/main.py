# stream_pages/main.py - 멀티페이지 앱 메인 라우터 엔트리포인트
# 공식 문서: https://docs.streamlit.io/develop/api-reference/navigation

import streamlit as st

# [1. 개별 페이지 정의 (st.Page)]
# 메인 엔트리포인트(main.py)와 같은 폴더에 있으므로 상대 경로로 파일명 직접 지정
home_page = st.Page("home_page.py", title="홈", icon="🏠", default=True)
nav_page = st.Page("navigation_page.py", title="네비게이션 API", icon="🧭")
auth_page = st.Page("auth_page.py", title="Google 인증", icon="🔐")
data_page = st.Page("data_page.py", title="데이터 분석", icon="📊")
settings_page = st.Page("settings_page.py", title="환경설정", icon="⚙️")

# [2. 섹션별 그룹화 네비게이션 라우터 구성 (st.navigation)]
pg = st.navigation(
    {
        "메인": [home_page, nav_page],
        "서비스": [auth_page, data_page],
        "시스템": [settings_page],
    }
)

# [3. 사이드바 공통 요소 (옵션)]
with st.sidebar:
    if st.user.get("is_logged_in", False):
        st.caption(f"👤 로그인: **{st.user.name}**")
        if st.button("로그아웃", icon=":material/logout:", key="sidebar_logout"):
            st.logout()
    else:
        st.caption("🔒 비로그인 상태")

# [4. 현재 선택된 페이지 실행]
pg.run()