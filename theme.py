"""
파일명: theme.py
목적: 사이버 오로라 네온 테마 CSS(고대비 가독성, 드롭다운/버튼/상단바 전수 보정) 및 버튼 별 팝콘 폭발 인터랙션 효과 주입
"""

import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. 사이버 오로라 네온 CSS 스타일 (전역 가독성 및 UI 요소 완벽 보정)
# ==============================================================================
CYBER_AURORA_THEME_CSS: str = """
<style>
/* 1. 배경 오로라 물결 애니메이션 */
@keyframes auroraMotion {
    0% {
        background-position: 0% 10%, 100% 90%, 50% 50%;
    }
    50% {
        background-position: 40% 30%, 60% 70%, 50% 50%;
    }
    100% {
        background-position: 0% 10%, 100% 90%, 50% 50%;
    }
}

.stApp {
    background-color: #05060b;
    background-image: 
        radial-gradient(ellipse at 15% 25%, rgba(6, 182, 212, 0.28), transparent 50%),
        radial-gradient(ellipse at 85% 75%, rgba(168, 85, 247, 0.30), transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(59, 130, 246, 0.15), transparent 65%);
    background-size: 160% 160%, 160% 160%, 100% 100%;
    animation: auroraMotion 16s ease-in-out infinite alternate;
    color: #f8fafc !important;
}

/* 2. 최상단 헤더 바(stHeader) 가독성 */
header[data-testid="stHeader"] {
    background: transparent !important;
}
header[data-testid="stHeader"] * {
    color: #f8fafc !important;
    fill: #f8fafc !important;
}

/* 3. 탭 바(st.tabs) - 탭 헤더 글씨 선명화 */
div[data-testid="stTabs"] button[role="tab"] {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    background: transparent !important;
}
div[data-testid="stTabs"] button[role="tab"] p {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #22d3ee !important;
    border-bottom-color: #22d3ee !important;
    font-weight: 700 !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p {
    color: #22d3ee !important;
    font-weight: 700 !important;
}

/* 4. 드롭다운(selectbox) 및 팝오버 목록 글씨 선명화 (흰색바탕에 흰색글씨 원천 방지) */
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div,
[data-testid="stSelectbox"] div[data-baseweb="select"],
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #0d1527 !important;
    background: #0d1527 !important;
    border-radius: 10px !important;
    border: 1px solid rgba(6, 182, 212, 0.6) !important;
    color: #ffffff !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] p,
div[data-baseweb="select"] div,
[data-testid="stSelectbox"] div,
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] svg {
    fill: #22d3ee !important;
    color: #22d3ee !important;
}

/* 드롭다운 열렸을 때 팝오버 목록 (BaseWeb Popover) */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] ul {
    background-color: #0b1120 !important;
    background: #0b1120 !important;
    border: 1px solid rgba(6, 182, 212, 0.6) !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8) !important;
}

div[data-baseweb="popover"] li,
div[data-baseweb="popover"] li * {
    background-color: #0b1120 !important;
    color: #ffffff !important;
    font-weight: 500 !important;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li:hover *,
div[data-baseweb="popover"] li[aria-selected="true"],
div[data-baseweb="popover"] li[aria-selected="true"] * {
    background-color: #1e293b !important;
    color: #22d3ee !important;
    font-weight: 700 !important;
}

/* 5. 모든 버튼 전수 스타일링 (흰색 버튼 및 글씨 투명 현상 완전 방지) */
button,
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button,
div[data-testid="stDownloadButton"] > button,
button[kind="secondary"],
button[kind="primary"] {
    background: linear-gradient(135deg, #06b6d4 0%, #38bdf8 100%) !important;
    color: #020617 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 0 16px rgba(6, 182, 212, 0.6) !important;
    transition: all 0.25s ease-in-out !important;
    cursor: pointer !important;
}
button *,
div.stButton > button *,
div[data-testid="stFormSubmitButton"] > button *,
div[data-testid="stDownloadButton"] > button * {
    color: #020617 !important;
    font-weight: 700 !important;
}

button:hover,
div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover,
div[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #22d3ee 0%, #a855f7 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 0 26px rgba(34, 211, 238, 0.9) !important;
    transform: translateY(-1px) scale(1.02);
}
button:hover *,
div.stButton > button:hover *,
div[data-testid="stFormSubmitButton"] > button:hover *,
div[data-testid="stDownloadButton"] > button:hover * {
    color: #ffffff !important;
}

/* 6. 사이드바 스타일 및 네비게이션 링크 */
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

/* 사이드바 네비게이션 링크 (st.Page 링크) */
[data-testid="stSidebarNav"] * {
    color: #ffffff !important;
    font-weight: 600 !important;
}
[data-testid="stSidebarNavLink"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px !important;
    margin-bottom: 4px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background-color: rgba(6, 182, 212, 0.25) !important;
    border-color: rgba(6, 182, 212, 0.6) !important;
}
[data-testid="stSidebarNavLink"][aria-current="page"] {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.35) 0%, rgba(56, 189, 248, 0.2) 100%) !important;
    border: 1px solid #06b6d4 !important;
}

/* 7. 전역 텍스트, 캡션 및 라벨 고대비 보정 */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 700 !important;
    text-shadow: 0 0 12px rgba(6, 182, 212, 0.4);
}

p, span, div {
    color: #f1f5f9;
}

.stCaption, small, [data-testid="stCaptionContainer"] p {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
}

label, [data-testid="stWidgetLabel"] p, .stWidgetLabel {
    color: #ffffff !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #22d3ee !important;
    text-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
}
[data-testid="stMetricLabel"] p {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* 입력 필드 (st.text_input) 배경 및 글자 */
div[data-baseweb="input"] {
    background-color: #0f172a !important;
    border-radius: 10px !important;
    border: 1px solid rgba(6, 182, 212, 0.5) !important;
}
div[data-baseweb="input"] input {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* 사용자(User) 채팅 버블 */
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

/* 어시스턴트(Assistant) 채팅 버블 */
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

/* 입력창(Chat Input) 네온 림 */
div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 1px solid rgba(6, 182, 212, 0.5) !important;
    box-shadow: 0 0 14px rgba(6, 182, 212, 0.25) !important;
}

/* 카드 및 컨테이너 보더 */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(6, 182, 212, 0.35) !important;
    background: rgba(15, 23, 42, 0.5) !important;
}
</style>
"""


# ==============================================================================
# 2. 버튼 별 팝콘 폭발 인터랙션 스크립트 (Star Popcorn Burst Effect)
# ==============================================================================
STAR_POPCORN_SCRIPT: str = """
<script>
(function() {
    const parentDoc = window.parent.document;
    if (parentDoc.getElementById('star-popcorn-script-active')) return;

    // 중복 주입 방지 마커
    const marker = parentDoc.createElement('div');
    marker.id = 'star-popcorn-script-active';
    marker.style.display = 'none';
    parentDoc.body.appendChild(marker);

    // 파티클 키프레임 애니메이션 스타일 등록
    const styleEl = parentDoc.createElement('style');
    styleEl.innerHTML = `
        @keyframes starPopcorn {
            0% {
                transform: translate(0, 0) scale(0.3) rotate(0deg);
                opacity: 1;
            }
            45% {
                transform: translate(var(--pop-x), calc(var(--pop-y) - 30px)) scale(1.45) rotate(var(--pop-rot));
                opacity: 1;
            }
            100% {
                transform: translate(calc(var(--pop-x) * 1.35), calc(var(--pop-y) + 32px)) scale(0) rotate(calc(var(--pop-rot) * 2));
                opacity: 0;
            }
        }
        .star-popcorn-item {
            position: fixed;
            pointer-events: none;
            z-index: 9999999;
            will-change: transform, opacity;
            user-select: none;
            animation: starPopcorn 0.75s cubic-bezier(0.18, 0.89, 0.32, 1.28) forwards;
            filter: drop-shadow(0 0 6px rgba(253, 224, 71, 0.8));
        }
    `;
    parentDoc.head.appendChild(styleEl);

    const STARS = ['✨', '⭐', '🌟', '💫', '✦', '✧', '💛'];
    let lastHoverTime = 0;

    // 팝콘 별 파티클 생성 함수
    function explodeStarPopcorn(x, y, count = 12) {
        for (let i = 0; i < count; i++) {
            const star = parentDoc.createElement('div');
            star.className = 'star-popcorn-item';
            star.innerText = STARS[Math.floor(Math.random() * STARS.length)];

            // 팝콘처럼 위로 솟구쳤다가 사방으로 튀어오르는 물리 궤적
            const angle = Math.random() * Math.PI * 2;
            const distance = 45 + Math.random() * 70;
            const popX = (Math.cos(angle) * distance) + 'px';
            const popY = (Math.sin(angle) * distance - (20 + Math.random() * 35)) + 'px';
            const popRot = (Math.random() * 360 - 180) + 'deg';
            const size = (16 + Math.random() * 14) + 'px';

            star.style.left = (x - 10) + 'px';
            star.style.top = (y - 10) + 'px';
            star.style.fontSize = size;
            star.style.setProperty('--pop-x', popX);
            star.style.setProperty('--pop-y', popY);
            star.style.setProperty('--pop-rot', popRot);

            parentDoc.body.appendChild(star);

            setTimeout(() => {
                if (star.parentNode) star.parentNode.removeChild(star);
            }, 800);
        }
    }

    // 버튼 호버 시 (마우스 커서 올릴 때): 팝콘 터짐
    parentDoc.addEventListener('mouseover', function(e) {
        const btn = e.target.closest('button');
        if (btn) {
            const now = Date.now();
            if (now - lastHoverTime > 300) {
                lastHoverTime = now;
                const rect = btn.getBoundingClientRect();
                const x = e.clientX || (rect.left + rect.width / 2);
                const y = e.clientY || (rect.top + rect.height / 2);
                explodeStarPopcorn(x, y, 10);
            }
        }
    }, true);

    // 버튼 클릭 시 (누를 때): 대형 팝콘 별 폭발!
    parentDoc.addEventListener('click', function(e) {
        const btn = e.target.closest('button');
        if (btn) {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX || (rect.left + rect.width / 2);
            const y = e.clientY || (rect.top + rect.height / 2);
            explodeStarPopcorn(x, y, 18);
        }
    }, true);
})();
</script>
"""


def apply_theme() -> None:
    """사이버 오로라 네온 테마 CSS 및 버튼 별 팝콘 인터랙션 효과를 현재 페이지에 주입합니다."""
    st.markdown(CYBER_AURORA_THEME_CSS, unsafe_allow_html=True)
    components.html(STAR_POPCORN_SCRIPT, height=0, width=0)
