"""
파일명: app2.py
목적: Streamlit 채팅 애플리케이션의 메인 진입점 및 세션 기반 인증/페이지 라우팅 관리
"""

import logging
import streamlit as st

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# 기본 사용자 인증 정보 (학습 및 데모용)
AUTH_CREDENTIALS: dict[str, str] = {
    "admin": "admin1234",
    "user": "user1234",
}

# 페이지 전역 설정
st.set_page_config(
    page_title="AI 챗봇 서비스",
    page_icon="💬",
    layout="wide",
)

# 사이버 오로라 네온 테마 적용
from theme import apply_theme
apply_theme()


# ==============================================================================
# [단계 1] 로그인 인증 및 보안 안내 뷰
# ==============================================================================
def render_login_page() -> None:
    """로그인 폼 및 보안 취약점 안내 메시지를 렌더링합니다."""
    st.title("🔒 챗봇 서비스 로그인")

    # 보안 취약점 주의 안내 메시지
    st.warning(
        "⚠️ **보안 취약점 주의 안내**\n\n"
        "- 본 페이지는 데모 및 실습을 위한 **기본 세션 상태(Session State) 기반 인증**을 사용합니다.\n"
        "- HTTPS 암호화 통신이나 데이터베이스 기반의 전용 보안 인증 모듈이 적용되어 있지 않습니다.\n"
        "- 따라서 공용 네트워크 환경에서 패킷 감청 위험이 있으므로, **실제 포털, 금융, 개인 이메일 등에서 사용하는 중요 비밀번호를 절대 입력하지 마십시오.**"
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form", clear_on_submit=False):
            st.subheader("계정 로그인")
            user_id = st.text_input("아이디 (ID)", placeholder="예: admin")
            user_pw = st.text_input("비밀번호 (Password)", type="password", placeholder="비밀번호 입력")
            submitted = st.form_submit_button("로그인", use_container_width=True)

            if submitted:
                cleaned_id = user_id.strip()
                if cleaned_id in AUTH_CREDENTIALS and AUTH_CREDENTIALS[cleaned_id] == user_pw:
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = cleaned_id
                    logger.info("로그인 성공: 사용자 %s", cleaned_id)
                    st.success("로그인 성공! 페이지를 불러옵니다...")
                    st.rerun()
                else:
                    logger.warning("로그인 실패 시도: 아이디 %s", cleaned_id)
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

        st.caption("💡 테스트용 기본 계정: `admin` / `admin1234` 또는 `user` / `user1234`")


# ==============================================================================
# [단계 2] 세션 인증 상태 검증 및 메인 라우팅
# ==============================================================================
if not st.session_state.get("logged_in", False):
    render_login_page()
else:
    # 로그인 완료 시 사이드바 상단에 사용자 정보 및 로그아웃 버튼 표시
    with st.sidebar:
        st.markdown(f"👤 **접속 계정:** `{st.session_state.get('user_id', '사용자')}`")
        if st.button("🚪 로그아웃", use_container_width=True):
            logger.info("로그아웃 실행: %s", st.session_state.get("user_id"))
            st.session_state["logged_in"] = False
            # API 키 및 세션 정보 초기화
            if "user_api_key" in st.session_state:
                del st.session_state["user_api_key"]
            st.rerun()
        st.divider()

    # 공식 멀티페이지 네비게이션 정의
    chat_page = st.Page(
        "app2_chat.py",
        title="실시간 텍스트 채팅",
        icon="💬",
        default=True,
    )

    history_page = st.Page(
        "app2_history.py",
        title="과거 대화 내역 조회",
        icon="📜",
    )

    pg = st.navigation(
        {
            "서비스 메뉴": [chat_page, history_page],
        },
        position="sidebar",
    )

    pg.run()