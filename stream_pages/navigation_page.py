# stream_pages/navigation_page.py - Streamlit 공식 네비게이션 및 페이지 관리 실습 페이지
# 공식 문서: https://docs.streamlit.io/develop/api-reference/navigation

import streamlit as st

# [페이지 타이틀 및 소개]
st.title("🧭 네비게이션 & 페이지 관리 (Navigation & Pages)")
st.caption("공식 API: `st.navigation`, `st.Page`, `st.page_link`, `st.switch_page`")
st.write(
    "Streamlit의 최신 네비게이션 기능을 통해 멀티페이지 앱을 손쉽게 구성하고, "
    "사용자 상호작용 또는 코드 조건에 따라 페이지 간 이동을 제어할 수 있습니다."
)

st.divider()

# =====================================================================
# 1. st.page_link: 선언적 페이지 링크 위젯
# =====================================================================
st.header("1. `st.page_link` (페이지 링크 위젯)")
st.write(
    "사용자가 클릭하여 다른 내부 페이지로 이동하거나, 외부 웹사이트를 새 탭으로 열 수 있는 링크 위젯입니다."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("내부 페이지 링크")
    # 메인 페이지(main.py)로 이동하는 내부 링크
    st.page_link(
        r"stream_pages\main.py",
        label="메인 로그인 페이지로 이동",
        icon="🔐",
        help="stream_pages/main.py 페이지로 이동합니다.",
        use_container_width=True,
    )

    # 비활성화(disabled) 상태 예시
    st.page_link(
        r"stream_pages\main.py",
        label="비활성화된 링크 (disabled=True)",
        icon="⛔",
        disabled=True,
        use_container_width=True,
    )

with col2:
    st.subheader("외부 웹사이트 링크")
    # 외부 공식 문서 링크
    st.page_link(
        "https://docs.streamlit.io/develop/api-reference/navigation",
        label="Streamlit Navigation 공식 문서 열기",
        icon="🌐",
        help="공식 API 레퍼런스 페이지를 새 브라우저 탭에서 엽니다.",
        use_container_width=True,
    )

    st.page_link(
        "https://streamlit.io",
        label="Streamlit 공식 웹사이트",
        icon="🎈",
        use_container_width=True,
    )

st.divider()

# =====================================================================
# 2. st.switch_page: 프로그래밍 방식 페이지 전환
# =====================================================================
st.header("2. `st.switch_page` (코드 기반 페이지 전환)")
st.write(
    "버튼 클릭이나 특정 조건 충족 시, 파이썬 코드 상에서 즉시 다른 페이지로 화면을 전환합니다."
)

col_switch1, col_switch2 = st.columns(2)

with col_switch1:
    if st.button("🚀 메인 페이지로 즉시 전환 (st.switch_page)", type="primary", use_container_width=True):
        st.switch_page(r"stream_pages\main.py")

with col_switch2:
    target_role = st.selectbox("사용자 역할 선택 시뮬레이션", ["일반 사용자", "관리자"])
    if st.button("역할 확인 후 메인 페이지 이동", use_container_width=True):
        st.toast(f"'{target_role}' 권한으로 메인 페이지로 전환합니다...")
        st.switch_page(r"stream_pages\main.py")

st.divider()

# =====================================================================
# 3. st.navigation & st.Page: 앱 라우팅 및 멀티페이지 구성
# =====================================================================
st.header("3. `st.navigation` & `st.Page` (멀티페이지 라우터 구성)")
st.write(
    "진입점(Entrypoint) 파일에서 `st.Page` 객체를 선언하고 `st.navigation`으로 "
    "전체 앱의 페이지 구성, 사이드바 메뉴, 메뉴 위치를 일괄 제어합니다."
)

# 주요 파라미터 실습 탐색기
nav_position = st.radio(
    "네비게이션 위치 (`position` 파라미터)",
    options=["sidebar", "top", "hidden"],
    format_func=lambda x: f"`{x}`: {'사이드바에 메뉴 표시' if x == 'sidebar' else '상단 네비게이션 바로 표시' if x == 'top' else '메뉴 숨김 (링크나 코드로만 이동)'}",
    horizontal=True,
)

group_mode = st.toggle("섹션별 그룹화 (Dictionary 구조 사용)", value=True)

# 선택된 설정에 따른 샘플 코드 동적 출력
sample_code = f"""import streamlit as st

# [1. 개별 페이지 정의 (st.Page)]
main_page = st.Page(
    r"stream_pages\\main.py",
    title="로그인 쇼케이스",
    icon="🔐",
    default=True
)
nav_page = st.Page(
    r"stream_pages\\navigation_page.py",
    title="네비게이션 실습",
    icon="🧭"
)

# [2. 네비게이션 라우터 정의 (st.navigation)]
"""

if group_mode:
    sample_code += f"""pg = st.navigation(
    {{
        "인증": [main_page],
        "페이지 탐색": [nav_page],
    }},
    position="{nav_position}"
)
"""
else:
    sample_code += f"""pg = st.navigation(
    [main_page, nav_page],
    position="{nav_position}"
)
"""

sample_code += """
# [3. 선택된 현재 페이지 실행]
pg.run()
"""

st.code(sample_code, language="python")
