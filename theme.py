"""
파일명: theme.py
목적: 사이버 오로라 네온(Cyber Aurora Neon) 고대비 가독성 보정 및 밝은 네온 버튼 테마 CSS 정의
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
    color: #f8fafc !important;
}

/* 2. 전역 텍스트 가독성 고대비 보정 (어두워서 안 보이는 글씨 완전 해결) */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
}

p, span, div {
    color: #f1f5f9;
}

/* 캡션 및 서브 텍스트 가독성 강화 */
.stCaption, small, [data-testid="stCaptionContainer"] p {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
}

/* 폼 및 위젯 입력 라벨을 선명한 화이트로 고정 */
label, [data-testid="stWidgetLabel"] p, .stWidgetLabel {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* 메트릭 통계 카드 텍스트 */
[data-testid="stMetricValue"] {
    color: #22d3ee !important;
    text-shadow: 0 0 10px rgba(34, 211, 238, 0.4);
}
[data-testid="stMetricLabel"] p {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* 3. 사이드바 스타일 및 스크롤 방지 최적화 */
section[data-testid="stSidebar"] {
    background-color: #080a14 !important;
    border-right: 1px solid rgba(6, 182, 212, 0.25);
}
section[data-testid="stSidebar"] > div {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}
section[data-testid="stSidebar"] div.stVerticalBlock {
    gap: 0.65rem !important;
}
section[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}

/* 4. 밝고 눈에 띄는 네온 버튼 (Bright Neon Button) */
div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #06b6d4 0%, #38bdf8 100%) !important;
    color: #030712 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 0 16px rgba(6, 182, 212, 0.6) !important;
    transition: all 0.25s ease-in-out !important;
}
div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #22d3ee 0%, #a855f7 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 0 24px rgba(34, 211, 238, 0.85) !important;
    transform: translateY(-1px);
}

/* 5. 사용자(User) 채팅 버블: 시안 네온 글로우 */
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

/* 6. 어시스턴트(Assistant) 채팅 버블: 바이올렛 네온 림 */
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

/* 7. 입력창(Chat Input) 네온 림 */
div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 1px solid rgba(6, 182, 212, 0.5) !important;
    box-shadow: 0 0 14px rgba(6, 182, 212, 0.25) !important;
}

/* 8. 카드 및 컨테이너 보더 */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(6, 182, 212, 0.35) !important;
    background: rgba(15, 23, 42, 0.5) !important;
}
</style>
"""


def apply_theme() -> None:
    """사이버 오로라 네온 테마 CSS를 현재 페이지에 주입합니다."""
    st.markdown(CYBER_AURORA_THEME_CSS, unsafe_allow_html=True)
