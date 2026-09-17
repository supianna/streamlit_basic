from datetime import date, time, timedelta
import streamlit as st


def show_datetime_widgets():
    st.subheader("1. st.date_input & st.time_input (날짜와 시간)")
    today = date.today()
    col1, col2 = st.columns(2)

    with col1:
        picked_date = st.date_input(
            "생년월일 (단일 날짜, 포맷 지정)",
            value=today,
            min_value=date(1900, 1, 1),
            max_value=today,
            format="YYYY/MM/DD",
        )
        st.write("👉 선택 날짜:", picked_date.strftime("%Y년 %m월 %d일"))

        picked_time = st.time_input(
            "알람 시각 (5분 단위 step=300초)",
            value=time(8, 30),
            step=300,
        )
        st.write("👉 설정 시각:", picked_time.strftime("%H시 %M분"))

    with col2:
        date_range = st.date_input(
            "숙박 기간 (범위 선택 value=(시작, 종료))",
            value=(today, today + timedelta(days=3)),
            min_value=today,
            format="YYYY-MM-DD",
        )
        st.write("👉 선택 기간:", date_range)

