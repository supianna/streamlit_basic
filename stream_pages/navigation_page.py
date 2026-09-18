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
    st.subheader("내부 페이지 이동 링크")
    st.page_link(
        r"stream_pages\home_page.py",
        label="🏠 홈 페이지로 이동",
        icon="🏠",
        use_container_width=True,
    )
    st.page_link(
        r"stream_pages\auth_page.py",
        label="🔐 Google 로그인 쇼케이스로 이동",
        icon="🔐",
        use_container_width=True,
    )
    st.page_link(
        r"stream_pages\data_page.py",
        label="📊 데이터 분석 페이지로 이동",
        icon="📊",
        use_container_width=True,
    )
    st.page_link(
        r"stream_pages\settings_page.py",
        label="⚙️ 환경설정 페이지로 이동",
        icon="⚙️",
        use_container_width=True,
    )

with col2:
    st.subheader("외부 링크 및 옵션 예시")
    st.page_link(
        "https://docs.streamlit.io/develop/api-reference/navigation",
        label="🌐 Streamlit Navigation 공식 문서",
        icon="📖",
        help="공식 API 레퍼런스 페이지를 새 브라우저 탭에서 엽니다.",
        use_container_width=True,
    )
    st.page_link(
        r"stream_pages\home_page.py",
        label="⛔ 비활성화 링크 (disabled=True)",
        icon="🔒",
        disabled=True,
        use_container_width=True,
    )

st.divider()

# =====================================================================
# 2. st.switch_page: 프로그래밍 방식 페이지 전환
# =====================================================================
st.header("2. `st.switch_page` (코드 기반 즉시 페이지 전환)")
st.write(
    "버튼 클릭이나 특정 로직/조건에 따라 파이썬 코드 상에서 즉시 대상 페이지로 화면을 전환합니다."
)

col_switch1, col_switch2 = st.columns(2)

with col_switch1:
    st.subheader("버튼 클릭 즉시 이동")
    if st.button("🚀 데이터 분석 페이지로 바로 가기", type="primary", use_container_width=True):
        st.switch_page(r"stream_pages\data_page.py")

    if st.button("🔐 로그인 페이지로 바로 가기", use_container_width=True):
        st.switch_page(r"stream_pages\auth_page.py")

with col_switch2:
    st.subheader("조건부 이동 시뮬레이션")
    dest_page = st.selectbox(
        "이동할 대상 페이지 선택",
        [
            ("홈 페이지", r"stream_pages\home_page.py"),
            ("데이터 분석", r"stream_pages\data_page.py"),
            ("환경설정", r"stream_pages\settings_page.py"),
            ("Google 인증", r"stream_pages\auth_page.py"),
        ],
        format_func=lambda x: x[0],
    )
    if st.button("선택한 페이지로 전환", use_container_width=True):
        st.toast(f"'{dest_page[0]}' 페이지로 이동합니다...")
        st.switch_page(dest_page[1])

st.divider()

# =====================================================================
# 3. st.navigation & st.Page: 앱 라우팅 및 멀티페이지 구성
# =====================================================================
st.header("3. `st.navigation` & `st.Page` (멀티페이지 라우터 구성)")
st.write(
    "메인 엔트리포인트 파일(`main.py`)에서 `st.Page`로 각 페이지를 등록하고 `st.navigation`으로 "
    "전체 앱의 카테고리별 사이드바 메뉴 및 라우팅을 관리합니다."
)

# 현재 실제 적용된 라우터 코드 표시
st.code("""# stream_pages/main.py (현재 적용된 멀티페이지 라우터 코드)
import streamlit as st

# [1. 개별 페이지 정의]
home_page = st.Page(r"stream_pages\\home_page.py", title="홈", icon="🏠", default=True)
nav_page = st.Page(r"stream_pages\\navigation_page.py", title="네비게이션 API", icon="🧭")
auth_page = st.Page(r"stream_pages\\auth_page.py", title="Google 인증", icon="🔐")
data_page = st.Page(r"stream_pages\\data_page.py", title="데이터 분석", icon="📊")
settings_page = st.Page(r"stream_pages\\settings_page.py", title="환경설정", icon="⚙️")

# [2. 섹션별 그룹화 네비게이션 라우터 정의]
pg = st.navigation(
    {
        "메인": [home_page, nav_page],
        "서비스": [auth_page, data_page],
        "시스템": [settings_page],
    }
)

# [3. 현재 선택된 페이지 실행]
pg.run()
""", language="python")
