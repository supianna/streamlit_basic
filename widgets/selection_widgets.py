import streamlit as st


def show_selection_widgets():
    st.subheader("1. st.radio (라디오 버튼)")
    col1, col2 = st.columns(2)

    with col1:
        genre = st.radio("영화 장르 (세로형)", ["액션", "코미디", "SF", "로맨스", "스릴러"], index=0)
        st.write("👉 선택 장르:", genre)

    with col2:
        payment = st.radio(
            "결제 방식 (가로형 horizontal & captions)",
            ["신용카드", "계좌이체", "간편결제"],
            captions=["무이자 할부", "수수료 무료", "네이버/카카오페이"],
            horizontal=True,
        )
        st.write("👉 선택 결제:", payment)

    st.divider()

    st.subheader("2. st.selectbox & st.multiselect (드롭다운)")
    col3, col4 = st.columns(2)

    with col3:
        city = st.selectbox("지역 선택 (기본)", ["서울특별시", "부산광역시", "인천광역시", "대구광역시", "대전광역시"])
        st.write("👉 선택 지역:", city)

        job = st.selectbox("직무 선택 (초기선택 없음 index=None)", ["기획자", "개발자", "디자이너", "데이터분석가"], index=None, placeholder="직무를 골라주세요")
        st.write("👉 선택 직무:", job)

    with col4:
        skills = st.multiselect(
            "보유 기술 (다중 선택, max_selections=3)",
            ["Python", "Streamlit", "SQL", "Docker", "AWS", "FastAPI"],
            default=["Python", "Streamlit"],
            max_selections=3,
        )
        st.write(f"👉 선택 기술 ({len(skills)}개):", ", ".join(skills))

    st.divider()

    st.subheader("3. st.checkbox & st.toggle (체크 및 스위치)")
    col5, col6 = st.columns(2)

    with col5:
        agree1 = st.checkbox("서비스 이용약관 동의", value=True)
        agree2 = st.checkbox("마케팅 알림 동의")
        st.write(f"👉 이용약관: {agree1}, 마케팅: {agree2}")

    with col6:
        dark_mode = st.toggle("다크 모드 켜기", value=False)
        sound_alert = st.toggle("소리 알림 켜기", value=True)
        st.write(f"👉 다크모드: {dark_mode}, 소리알림: {sound_alert}")

