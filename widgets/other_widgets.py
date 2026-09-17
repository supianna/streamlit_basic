import streamlit as st


def show_other_widgets():
    st.subheader("1. 색상 선택 및 버튼형 태그")
    col1, col2 = st.columns(2)

    with col1:
        color = st.color_picker("테마 색상 선택 (st.color_picker)", value="#FF4B4B")
        st.write("👉 색상 코드:", color)
        st.markdown(
            f'<div style="width:100%; height:40px; background-color:{color}; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">색상 미리보기</div>',
            unsafe_allow_html=True,
        )

    with col2:
        pill = st.pills("관심 분야 (st.pills 알약 버튼)", ["AI/머신러닝", "웹 개발", "데이터 분석", "클라우드"], default="AI/머신러닝")
        st.write("👉 선택한 분야:", pill)

    st.divider()

    st.subheader("2. st.chat_input (채팅 스타일 입력)")
    st.info("화면 최하단에 항상 떠 있는 고정 챗 입력창입니다.")
    chat_msg = st.chat_input("메시지를 입력해보세요 (Enter로 전송)...")
    if chat_msg:
        st.success(f"💬 전송된 메시지: {chat_msg}")

