import streamlit as st

# 페이지 전역 설정
st.set_page_config(page_title="OpenAI 멀티모달 챗봇", page_icon="💬", layout="wide")

# ------------------------------------------------------------------------------
# Streamlit 공식 멀티페이지 네비게이션 (st.Page & st.navigation)
# ------------------------------------------------------------------------------
chat_page = st.Page(
    "app2_chat.py",
    title="실시간 멀티모달 채팅",
    icon="💬",
    default=True,
)

history_page = st.Page(
    "app2_history.py",
    title="과거 대화 내역 조회",
    icon="📜",
)

# 사이드바에 공식 페이지 이동 네비게이션 메뉴 생성 및 라우팅
pg = st.navigation(
    {
        "네비게이션": [chat_page, history_page],
    },
    position="sidebar",
)

# 현재 선택된 페이지 실행
pg.run()
