import streamlit as st


# ------------------------------------------------------------------------------
# 모달 다이얼로그 함수 (@st.dialog)
# ------------------------------------------------------------------------------
@st.dialog("확인 모달 다이얼로그 (st.dialog)")
def open_confirmation_dialog():
    st.write("이것은 모달 팝업 창입니다.")
    name = st.text_input("이름을 입력하세요", placeholder="홍길동")
    if st.button("확인 및 닫기"):
        st.write(f"{name}님 반갑습니다!")
        st.rerun()


def show_layout_widgets():
    st.subheader("📐 레이아웃 & 컨테이너 모음")
    st.caption("아래 하위 탭을 통해 공식 API 레퍼런스의 다양한 레이아웃 요소들을 탐색해보세요.")

    # 레이아웃 하위 서브 탭 구성
    tab_cols, tab_container, tab_expander, tab_pop_modal, tab_side_bottom, tab_empty = st.tabs([
        "🏛️ 컬럼 (st.columns)",
        "📦 컨테이너 (st.container)",
        "📂 익스팬더 (st.expander)",
        "💬 팝오버 & 모달 (st.popover / st.dialog)",
        "📌 사이드바 & 하단 (st.sidebar / st.bottom)",
        "🔄 플레이스홀더 (st.empty)",
    ])

    # 1. 컬럼
    with tab_cols:
        st.write("### 다단 컬럼 레이아웃 (비율 지정, 수직 정렬, 테두리)")
        col1, col2, col3 = st.columns([1, 2, 1], border=True, vertical_alignment="center")
        with col1:
            st.write("**컬럼 1** (비율: 1)")
            st.button("버튼 1")
        with col2:
            st.write("**컬럼 2** (비율: 2, 수직 가운데 정렬)")
            st.info("비율이 2배로 넓은 컬럼 영역입니다.")
        with col3:
            st.write("**컬럼 3** (비율: 1)")
            st.metric(label="온도", value="24°C", delta="1.2°C")

    # 2. 컨테이너
    with tab_container:
        st.write("### 컨테이너 (카드형 테두리 및 스크롤 박스)")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.write("**테두리가 있는 카드형 컨테이너 (border=True)**")
            with st.container(border=True):
                st.write("📦 관련된 위젯들을 시각적으로 묶을 때 사용합니다.")
                st.text_input("컨테이너 내부 입력창", placeholder="내용 입력...")
        with col_c2:
            st.write("**고정 높이 스크롤 컨테이너 (height=130)**")
            with st.container(height=130, border=True):
                st.write("📜 스크롤 가능한 영역입니다.")
                for i in range(1, 10):
                    st.write(f"아이템 #{i}")

    # 3. 익스팬더
    with tab_expander:
        st.write("### 접이식 아코디언 컨테이너")
        with st.expander("자세한 설명 보기 (기본 닫힘 상태)", expanded=False, icon="ℹ️"):
            st.write("사용자가 클릭했을 때만 펼쳐지는 공간입니다.")
            st.code("print('Hello from expander!')", language="python")

        with st.expander("중요 공지사항 (기본 열림: expanded=True)", expanded=True, icon="📢"):
            st.warning("expanded=True 옵션으로 페이지 로드 시 바로 열려있도록 지정할 수 있습니다.")

    # 4. 팝오버 및 모달 다이얼로그
    with tab_pop_modal:
        st.write("### 플로팅 팝오버 및 전체화면 모달 창")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.write("**1. st.popover (클릭 시 펼쳐지는 오버레이 메뉴)**")
            with st.popover("⚙️ 필터 및 설정 열기"):
                st.write("### 팝오버 설정")
                st.slider("감도 설정", 0, 100, 50)
                st.checkbox("알림 수신 동의")
        with col_p2:
            st.write("**2. st.dialog (전체화면 모달 대화상자)**")
            if st.button("모달 팝업 열기"):
                open_confirmation_dialog()

    # 5. 사이드바 및 하단 고정
    with tab_side_bottom:
        st.write("### 사이드바 및 화면 최하단 고정 컨테이너")
        st.info("👈 좌측 사이드바와 👇 화면 최하단 고정 바를 확인해보세요.")

        with st.sidebar:
            st.header("📌 사이드바 설정 (st.sidebar)")
            sidebar_opt = st.selectbox("사이드바 메뉴", ["홈", "대시보드", "환경설정"])
            st.write(f"선택: {sidebar_opt}")
            st.slider("사이드바 슬라이더", 0, 100, 30)

        with st.bottom:
            with st.container(border=True):
                st.write("⚓ **st.bottom 고정 영역**: 화면 맨 아래에 항상 고정됩니다.")

    # 6. 플레이스홀더
    with tab_empty:
        st.write("### 빈 플레이스홀더 (동적 콘텐츠 변경)")
        placeholder = st.empty()
        placeholder.info("이 문구는 아래 버튼을 누르면 다른 내용으로 즉시 교체됩니다.")

        if st.button("플레이스홀더 내용 실시간 교체"):
            placeholder.success("🎉 새로운 내용으로 성공적으로 교체되었습니다!")
