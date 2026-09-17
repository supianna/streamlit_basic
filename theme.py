"""
파일명: theme.py
목적: 사이버 오로라 네온(Cyber Aurora Neon) 테마 CSS 스타일 정의 및 페이지 주입 함수
"""

import streamlit as st

CYBER_AURORA_THEME_CSS: str = """
<style>
/* 1. 메인 배경: 딥 블랙 + 시안/퍼플 오로라 광채 */
.stApp {
    background-color: #05060b;
    background-image: 
        radial-gradient(ellipse at 10% 20%, rgba(6, 182, 212, 0.22), transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(168, 85, 247, 0.24), transparent 50%);
    color: #e0e7ff;
}

/* 2. 사이드바 스타일 */
section[data-testid="stSidebar"] {
    background-color: #080a14 !important;
    border-right: 1px solid rgba(6, 182, 212, 0.25);
}
section[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

/* 3. 사용자(User) 채팅 버블: 시안 네온 글로우 */
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, #0891b2 0%, #0284c7 100%) !important;
    color: #ffffff !important;
    border-radius: 18px 18px 4px 18px !important;
    box-shadow: 0 0 18px rgba(6, 182, 212, 0.35) !important;
    border: 1px solid rgba(103, 232, 249, 0.3) !important;
    padding: 12px 18px !important;
    margin-bottom: 12px !important;
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) * {
    color: #ffffff !important;
}

/* 4. 어시스턴트(Assistant) 채팅 버블: 바이올렛 네온 림 */
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    background: rgba(15, 17, 30, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    border-radius: 18px 18px 18px 4px !important;
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.25) !important;
    color: #f1f5f9 !important;
    padding: 14px 18px !important;
    margin-bottom: 12px !important;
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) * {
    color: #f1f5f9 !important;
}

/* 5. 입력창(Chat Input) 네온 림 */
div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 1px solid rgba(6, 182, 212, 0.4) !important;
    box-shadow: 0 0 12px rgba(6, 182, 212, 0.2) !important;
}

/* 6. 버튼 및 컨테이너 네온 감성 보정 */
div.stButton > button {
    border: 1px solid rgba(6, 182, 212, 0.4) !important;
    background: rgba(15, 23, 42, 0.8) !important;
    color: #e0e7ff !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}
div.stButton > button:hover {
    border-color: rgba(168, 85, 247, 0.8) !important;
    box-shadow: 0 0 15px rgba(168, 85, 247, 0.4) !important;
    color: #ffffff !important;
}

/* 7. 카드 및 컨테이너 보더 */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(6, 182, 212, 0.25) !important;
    background: rgba(15, 23, 42, 0.4) !important;
}
</style>
"""


def apply_theme() -> None:
    """사이버 오로라 네온 테마 CSS를 현재 페이지에 주입합니다."""
    st.markdown(CYBER_AURORA_THEME_CSS, unsafe_allow_html=True)
