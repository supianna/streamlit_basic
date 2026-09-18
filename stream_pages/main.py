# stream_pages/main.py - 멀티페이지 앱 메인 라우터 엔트리포인트
# 공식 문서: https://docs.streamlit.io/develop/api-reference/navigation

import os
from dotenv import load_dotenv
import streamlit as st

# [1. .env 환경변수 로드 및 secrets 동적 주입]
load_dotenv()

# .env 환경변수가 존재하고 st.secrets에 auth가 없는 경우 programmatic secrets 병합
if "auth" not in st.secrets and os.getenv("GOOGLE_CLIENT_ID"):
    st.secrets.merge_programmatic_secrets(
        {
            "auth": {
                "redirect_uri": os.getenv(
                    "AUTH_REDIRECT_URI", "http://localhost:8501/oauth2callback"
                ),
                "cookie_secret": os.getenv("AUTH_COOKIE_SECRET", ""),
                "google": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
                    "server_metadata_url": os.getenv(
                        "GOOGLE_SERVER_METADATA_URL",
                        "https://accounts.google.com/.well-known/openid-configuration",
                    ),
                },
            }
        }
    )

# [2. 로그인 상태 확인]
is_logged_in = st.user.get("is_logged_in", False)

# [3. 인증 상태에 따른 동적 네비게이션 라우팅 (Dynamic Navigation)]
if not is_logged_in:
    # 비로그인 상태: 다른 모든 페이지의 접근을 차단하고 오직 로그인 페이지만 노출
    login_page = st.Page("auth_page.py", title="로그인", icon="🔐", default=True)
    pg = st.navigation([login_page])
else:
    # 로그인 상태: 모든 기능 페이지(홈, 네비게이션, 데이터, 설정 등) 접근 허용
    home_page = st.Page("home_page.py", title="홈", icon="🏠", default=True)
    nav_page = st.Page("navigation_page.py", title="네비게이션 API", icon="🧭")
    data_page = st.Page("data_page.py", title="데이터 분석", icon="📊")
    settings_page = st.Page("settings_page.py", title="환경설정", icon="⚙️")
    auth_page = st.Page("auth_page.py", title="내 계정 정보", icon="👤")

    pg = st.navigation(
        {
            "메인": [home_page, nav_page],
            "서비스": [data_page],
            "시스템": [settings_page],
            "계정": [auth_page],
        }
    )

# [4. 사이드바 공통 요소]
with st.sidebar:
    if is_logged_in:
        st.caption(f"👤 로그인: **{st.user.name}**")
        if st.button("로그아웃", icon=":material/logout:", key="sidebar_logout"):
            st.logout()
    else:
        st.caption("🔒 로그인 후 전체 기능을 이용할 수 있습니다.")

# [5. 현재 선택된 페이지 실행]
pg.run()