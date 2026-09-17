"""
파일명: theme_preview.py
목적: 3가지 채팅 배경 및 UI 테마(모던 딥테크, 미니멀 클린, 사이버 오로라)를 직접 전환하며 눈으로 확인할 수 있는 체험용 독립 뷰어
"""

import logging
import streamlit as st

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="채팅 테마 갤러리 미리보기",
    page_icon="🎨",
    layout="wide",
)


# ==============================================================================
# [단계 1] 테마별 CSS 스타일 정의
# ==============================================================================
THEME_CSS: dict[str, str] = {
    # 1. 모던 딥 테크 & 글래스모피즘
    "theme1": """
    <style>
    /* 메인 배경: 딥 네이비 & 인디고 광원 그라데이션 */
    .stApp {
        background-color: #0b0f19;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.18), transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.15), transparent 45%),
            linear-gradient(135deg, #0b0f19 0%, #111827 50%, #030712 100%);
        color: #f3f4f6;
    }

    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #0d1322 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    section[data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    /* 사용자(User) 채팅 버블 */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        border-radius: 18px 18px 4px 18px !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
        border: none !important;
        padding: 12px 18px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) * {
        color: #ffffff !important;
    }

    /* 어시스턴트(Assistant) 채팅 버블: 반투명 글래스모피즘 */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background: rgba(26, 34, 53, 0.65) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 18px 18px 18px 4px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
        color: #f3f4f6 !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) * {
        color: #f3f4f6 !important;
    }

    /* 입력창 디자인 */
    div[data-testid="stChatInput"] {
        border-radius: 24px !important;
    }
    </style>
    """,

    # 2. 미니멀 클린 웜 & 마이크로 도트
    "theme2": """
    <style>
    /* 메인 배경: 눈이 편안한 오프화이트 + 은은한 도트 격자 */
    .stApp {
        background-color: #f8fafc;
        background-image: radial-gradient(#cbd5e1 1.2px, transparent 1.2px);
        background-size: 22px 22px;
        color: #0f172a;
    }

    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] * {
        color: #1e293b !important;
    }

    /* 사용자(User) 채팅 버블: 세련된 다크 차콜 */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 18px 18px 4px 18px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
        border: none !important;
        padding: 12px 18px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) * {
        color: #ffffff !important;
    }

    /* 어시스턴트(Assistant) 채팅 버블: 순백색 카드 & 소프트 섀도우 */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 18px 18px 18px 4px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
        color: #1e293b !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) * {
        color: #1e293b !important;
    }
    </style>
    """,

    # 3. 사이버 오로라 네온
    "theme3": """
    <style>
    /* 메인 배경: 딥 블랙 + 시안/퍼플 오로라 광채 */
    .stApp {
        background-color: #05060b;
        background-image: 
            radial-gradient(ellipse at 10% 20%, rgba(6, 182, 212, 0.22), transparent 50%),
            radial-gradient(ellipse at 90% 80%, rgba(168, 85, 247, 0.24), transparent 50%);
        color: #e0e7ff;
    }

    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #080a14 !important;
        border-right: 1px solid rgba(6, 182, 212, 0.2);
    }
    section[data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }

    /* 사용자(User) 채팅 버블: 시안 네온 글로우 */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #0891b2 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border-radius: 18px 18px 4px 18px !important;
        box-shadow: 0 0 18px rgba(6, 182, 212, 0.4) !important;
        border: 1px solid rgba(103, 232, 249, 0.3) !important;
        padding: 12px 18px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) * {
        color: #ffffff !important;
    }

    /* 어시스턴트(Assistant) 채팅 버블: 바이올렛 네온 림 */
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
    </style>
    """,
}


# ==============================================================================
# [단계 2] 테마 선택 컨트롤 (사이드바)
# ==============================================================================
with st.sidebar:
    st.title("🎨 테마 선택기")
    st.caption("3가지 디자인 테마를 즉시 전환해보며 마음에 드는 스타일을 비교해 보세요.")

    theme_choice = st.radio(
        "확인할 테마를 고르세요:",
        options=[
            "1. 모던 딥 테크 & 글래스모피즘 (추천 1순위)",
            "2. 미니멀 클린 웜 & 마이크로 도트 (라이트 테마)",
            "3. 사이버 오로라 네온 (트렌디 테크)",
        ],
        index=0,
    )

    theme_key = "theme1"
    if "1." in theme_choice:
        theme_key = "theme1"
        st.info("💎 **모던 딥 테크**: 어두운 네이비 배경에 은은한 글래스모피즘이 적용되어 눈이 편안하고 고급스럽습니다.")
    elif "2." in theme_choice:
        theme_key = "theme2"
        st.info("📄 **미니멀 클린**: 도트 격자가 은은한 화이트/오프화이트 배경으로 정갈하고 산뜻한 업무용 느낌을 줍니다.")
    else:
        theme_key = "theme3"
        st.info("🌌 **사이버 오로라**: 딥 블랙에 네온 빛 조명이 퍼지는 미래지향적 분위기를 연출합니다.")

    st.divider()
    st.markdown("💡 **안내**: 이 화면은 기존 메인 챗봇 코드(`app2.py`, `app2_chat.py`)에 영향을 주지 않는 **독립형 체험 페이지**입니다.")


# ==============================================================================
# [단계 3] 선택된 테마 CSS 주입
# ==============================================================================
st.markdown(THEME_CSS[theme_key], unsafe_allow_html=True)


# ==============================================================================
# [단계 4] 샘플 채팅 대화 렌더링
# ==============================================================================
st.title("💬 실시간 채팅 테마 실물 미리보기")
st.caption("현재 선택된 테마: " + theme_choice)

# 샘플 대화 데이터
sample_dialogues = [
    {
        "role": "user",
        "content": "안녕하세요! 이번에 적용될 채팅 화면의 배경과 말풍선 디자인을 테스트 중입니다.",
    },
    {
        "role": "assistant",
        "content": "반갑습니다! 현재 보시는 화면이 선택하신 테마가 실제 적용되었을 때의 디자인입니다. 배경의 깊이감과 말풍선의 입체감, 그리고 텍스트 가독성을 확인해 보세요.",
    },
    {
        "role": "user",
        "content": "코드 블록이나 글머리 기호는 어떻게 보이나요?",
    },
    {
        "role": "assistant",
        "content": """다음과 같이 코드 및 마크다운 요소도 테마에 맞춰 조화롭게 표현됩니다:

```python
# 스트림릿 테마 데모 코드
def greet(user_name: str) -> str:
    return f"반갑습니다, {user_name}님! 테마가 멋지네요."
```

- ✨ **특징 1**: 사용자 말풍선과 어시스턴트 말풍선의 명확한 시각적 대비
- 🎯 **특징 2**: 눈의 피로를 덜어주는 균형 잡힌 색상 배색
- 📱 **특징 3**: 모바일 및 와이드스크린 모두에 어울리는 레이아웃""",
    },
]

for msg in sample_dialogues:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 인터랙티브 입력창 체험 (실제 텍스트 입력 가능)
interactive_prompt = st.chat_input("메시지를 직접 입력해보며 반응을 확인해 보세요...")
if interactive_prompt:
    with st.chat_message("user"):
        st.markdown(interactive_prompt)
    with st.chat_message("assistant"):
        st.markdown(f"입력하신 메시지: **'{interactive_prompt}'**\n\n이 테마가 마음에 드시면 채팅창에 번호를 알려주세요!")

