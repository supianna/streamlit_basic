from datetime import time
import streamlit as st


def show_numeric_widgets():
    st.subheader("1. st.number_input (숫자 입력)")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("나이 (정수 min/max/step)", min_value=0, max_value=120, value=25, step=1)
        st.write("👉 나이:", age)

        temp = st.number_input("체온 (실수 float 포맷)", min_value=30.0, max_value=45.0, value=36.5, step=0.1, format="%.1f")
        st.write("👉 체온:", temp)

    with col2:
        score = st.number_input("점수 (step=10 단위)", min_value=0, max_value=100, value=50, step=10)
        st.write("👉 점수:", score)

        empty_num = st.number_input("초기값 없음 (value=None)", value=None, placeholder="숫자를 입력하세요")
        st.write("👉 입력값:", empty_num)

    st.divider()

    st.subheader("2. st.slider & st.select_slider (슬라이더 조작)")
    col3, col4 = st.columns(2)

    with col3:
        slider_int = st.slider("볼륨 조절 (정수)", min_value=0, max_value=100, value=50)
        st.write("👉 볼륨:", slider_int)

        slider_float = st.slider("비율 설정 (실수 step=0.05)", min_value=0.0, max_value=1.0, value=0.25, step=0.05, format="%.2f")
        st.write("👉 비율:", slider_float)

        satisfaction = st.select_slider("만족도 (카테고리 select_slider)", options=["매우 불만족", "불만족", "보통", "만족", "매우 만족"], value="보통")
        st.write("👉 선택한 만족도:", satisfaction)

    with col4:
        price_range = st.slider("가격 범위 (양방향 Range Slider)", min_value=0, max_value=1000, value=(200, 700), step=50)
        st.write(f"👉 선택 범위: {price_range[0]}만원 ~ {price_range[1]}만원")

        meeting_time = st.slider("시간 선택 슬라이더", min_value=time(9, 0), max_value=time(18, 0), value=time(11, 30), format="HH:mm")
        st.write("👉 선택 시간:", meeting_time.strftime("%H시 %M분"))

        size_range = st.select_slider("사이즈 범위 선택 (select_slider)", options=["XS", "S", "M", "L", "XL", "2XL"], value=("S", "L"))
        st.write(f"👉 선택 사이즈: {size_range[0]} ~ {size_range[1]}")

