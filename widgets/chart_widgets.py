import numpy as np
import pandas as pd
import streamlit as st


def show_chart_widgets():
    st.subheader("📈 차트 및 지도 시각화 (Chart Elements)")
    st.caption("Streamlit에 내장된 간결하고 강력한 차트 및 지도 시각화 컴포넌트들을 살펴봅니다.")

    tab_trend, tab_dist, tab_map = st.tabs([
        "📉 추세 차트 (라인 / 영역)",
        "📊 비교 & 산점도 (막대 / 산점도)",
        "🗺️ 인터랙티브 지도 (st.map)",
    ])

    # 1. 라인 및 에어리어 차트
    with tab_trend:
        st.write("### 라인 차트 (st.line_chart) & 영역 차트 (st.area_chart)")
        chart_data = pd.DataFrame(
            np.random.randn(20, 3) + [10, 15, 20],
            columns=["제품 A", "제품 B", "제품 C"],
        )

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.write("**선 그래프 (Line Chart)**")
            st.line_chart(chart_data)
        with col_c2:
            st.write("**영역 그래프 (Area Chart)**")
            st.area_chart(chart_data)

    # 2. 바 차트 및 스캐터 차트
    with tab_dist:
        st.write("### 막대 차트 (st.bar_chart) & 산점도 (st.scatter_chart)")
        bar_data = pd.DataFrame({
            "요일": ["월", "화", "수", "목", "금", "토", "일"],
            "방문자수": [120, 150, 180, 220, 310, 450, 390],
        })

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.write("**막대 그래프 (Bar Chart)**")
            st.bar_chart(bar_data, x="요일", y="방문자수")

        with col_b2:
            st.write("**산점도 (Scatter Chart)**")
            scatter_data = pd.DataFrame({
                "공부시간": [1, 2, 3, 4, 5, 6, 7, 8],
                "시험점수": [55, 60, 68, 72, 80, 85, 93, 98],
            })
            st.scatter_chart(scatter_data, x="공부시간", y="시험점수")

    # 3. 지도 시각화
    with tab_map:
        st.write("### 인터랙티브 지도 (st.map)")
        st.write("위도(lat)와 경도(lon) 컬럼을 가진 데이터를 전달하면 지도 위에 마커를 시각화합니다.")

        # 서울 주요 랜드마크 샘플 좌표 (서울시청, 남산타워, 강남역 등)
        seoul_locations = pd.DataFrame({
            "latitude": [37.5665, 37.5512, 37.4979, 37.5113],
            "longitude": [126.9780, 126.9882, 127.0276, 127.0980],
            "장소": ["서울시청", "N서울타워", "강남역", "잠실 롯데월드"],
        })
        st.map(seoul_locations, zoom=11)

