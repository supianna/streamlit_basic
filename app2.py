"""
파일명: app2.py
목적: 방명록 스타일 닉네임 및 삭제 비밀번호 기반 입장, 페이지 라우팅 관리
"""

import logging
import streamlit as st
from theme import apply_theme

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# 페이지 전역 설정
st.set_page_config(
    page_title="AI 챗봇 서비스",
    page_icon="💬",
    layout="wide",
)

# 사이버 오로라 네온 테마 적용
apply_theme()


# ==============================================================================
# [단계 1] 방명록 스타일 입장 및 보안 안내 뷰
# ==============================================================================
def render_guestbook_login_page() -> None:
    """닉네임과 삭제 비밀번호를 입력받는 방명록 형태의 입장 페이지를 렌더링합니다."""
    st.title("📝 챗봇 서비스 입장 (방명록)")

    # 보안 취약점 주의 안내 메시지
    st.warning(
        "⚠️ **보안 취약점 주의 안내**\n\n"
        "- 본 서비스는 방명록 방식으로 누구나 닉네임과 삭제 비밀번호를 등록하고 입장할 수 있습니다.\n"
        "- 입력하신 **'삭제 비밀번호'**는 본인이 작성한 대화 기록을 삭제할 때 확인용으로 사용됩니다.\n"
        "- 전용 암호화 백엔드가 없는 실습 환경이므로, **실제 포털, 금융, 개인 이메일 등에서 사용하는 중요 비밀번호를 절대 입력하지 마십시오.**"
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("guestbook_entry_form", clear_on_submit=False):
            st.subheader("방명록 작성 및 입장")
            nickname = st.text_input("🏷️ 닉네임 (대화명)", placeholder="예: 코딩토끼 (대화 저장 시 사용)")
            delete_pw = st.text_input(
                "🔑 삭제 비밀번호",
                type="password",
                placeholder="대화를 삭제할 때 필요한 비밀번호 입력",
                help="나중에 대화 기록을 삭제할 때 본인 확인용으로 사용됩니다.",
            )
            submitted = st.form_submit_button("🚀 채팅방 입장하기", use_container_width=True)

            if submitted:
                cleaned_nickname = nickname.strip()
                cleaned_pw = delete_pw.strip()

                if not cleaned_nickname:
                    st.error("닉네임을 1자 이상 입력해 주세요.")
                elif not cleaned_pw:
                    st.error("대화 삭제 시 사용할 비밀번호를 입력해 주세요.")
                else:
                    st.session_state["logged_in"] = True
                    st.session_state["nickname"] = cleaned_nickname
                    st.session_state["delete_pw"] = cleaned_pw
                    st.session_state["user_id"] = cleaned_nickname
                    logger.info("방명록 입장 완료: 닉네임 '%s'", cleaned_nickname)
                    st.success(f"'{cleaned_nickname}'님 환영합니다! 채팅방으로 이동합니다...")
                    st.rerun()

        st.caption("💡 원하는 닉네임과 기억하기 쉬운 간단한 삭제 비밀번호를 입력하시면 바로 입장하실 수 있습니다.")


# ==============================================================================
# [단계 2] 세션 인증 상태 검증 및 메인 라우팅
# ==============================================================================
if not st.session_state.get("logged_in", False):
    render_guestbook_login_page()
else:
    # 로그인 완료 시 사이드바 상단에 닉네임 및 퇴장(로그아웃) 버튼을 1줄로 컴팩트하게 표시
    with st.sidebar:
        col_u1, col_u2 = st.columns([1.6, 1], vertical_alignment="center")
        with col_u1:
            st.caption(f"🏷️ `{st.session_state.get('nickname', '익명')}`")
        with col_u2:
            if st.button("퇴장", use_container_width=True):
                logger.info("퇴장 실행: %s", st.session_state.get("nickname"))
                st.session_state["logged_in"] = False
                if "user_api_key" in st.session_state:
                    del st.session_state["user_api_key"]
                if "nickname" in st.session_state:
                    del st.session_state["nickname"]
                if "delete_pw" in st.session_state:
                    del st.session_state["delete_pw"]
                st.rerun()

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