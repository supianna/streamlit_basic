# stream_pages/data_page.py - 데이터 및 차트 시각화 페이지

import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 데이터 분석 (Data & Charts)")
st.caption("Streamlit의 데이터프레임 및 다양한 차트 컴포넌트 실습 예시입니다.")

# [1. 샘플 데이터 생성]
@st.cache_data
def get_sample_data() -> pd.DataFrame:
    data = {
        "월별": ["1월", "2월", "3월", "4월", "5월", "6월"],
        "방문자수": [1200, 1900, 3000, 5000, 4200, 6100],
        "매출액(만원)": [350, 420, 680, 890, 750, 1100],
        "만족도(점)": [4.2, 4.5, 4.1, 4.8, 4.6, 4.9],
    }
    return pd.DataFrame(data)

df = get_sample_data()

# [2. 데이터프레임 출력]
st.subheader("📋 월별 통계 데이터")
st.dataframe(df, use_container_width=True)

# [3. 차트 시각화]
st.subheader("📈 트렌드 차트")
chart_col = st.selectbox("시각화할 컬럼 선택", ["방문자수", "매출액(만원)", "만족도(점)"])

tab1, tab2 = st.tabs(["꺾은선 차트 (Line Chart)", "막대 차트 (Bar Chart)"])

with tab1:
    st.line_chart(df.set_index("월별")[chart_col])

with tab2:
    st.bar_chart(df.set_index("월별")[chart_col])

