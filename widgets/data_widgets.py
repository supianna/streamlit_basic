import pandas as pd
import streamlit as st


def show_data_widgets():
    st.subheader("📊 데이터 표시 요소 (Data Elements)")
    st.caption("공식 API 레퍼런스를 기반으로 표, 편집기, 메트릭, JSON 등 데이터 표현 요소들을 살펴봅니다.")

    sub_df, sub_metric, sub_json_table = st.tabs([
        "📋 데이터프레임 & 편집기 (dataframe / data_editor)",
        "📈 지표 카드 (st.metric)",
        "🧾 정적 테이블 & JSON (table / json)",
    ])

    # 샘플 데이터 생성
    sample_data = pd.DataFrame({
        "이름": ["김철수", "이영희", "박민수", "정지원"],
        "부서": ["개발팀", "디자인팀", "기획팀", "마케팅팀"],
        "평가점수": [92, 88, 95, 84],
        "재택근무": [True, False, True, True],
    })

    # 1. st.dataframe & st.data_editor
    with sub_df:
        st.write("### 1. 인터랙티브 데이터프레임 (st.dataframe)")
        st.write("정렬, 검색, 열 크기 조절 및 CSV 다운로드 기능을 기본 제공합니다.")
        st.dataframe(sample_data, use_container_width=True)

        st.divider()

        st.write("### 2. 수정 가능한 테이블 (st.data_editor)")
        st.write("사용자가 표의 셀 값을 직접 클릭하여 수정하거나 체크박스를 토글할 수 있습니다.")
        edited_df = st.data_editor(sample_data, num_rows="dynamic", use_container_width=True)
        st.write("👉 현재 편집된 데이터의 행 수:", len(edited_df))

    # 2. st.metric
    with sub_metric:
        st.write("### 지표 및 성과 카드 (st.metric)")
        st.write("KPI 수치와 이전 대비 증감(delta)을 시각적인 화살표 색상으로 표시합니다.")

        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="월간 활성 사용자(MAU)", value="142,500명", delta="12.5%")
        with m_col2:
            st.metric(label="평균 체류 시간", value="4분 32초", delta="-18초", delta_color="inverse")
        with m_col3:
            st.metric(label="오늘의 매출", value="₩3,850,000", delta="₩450,000")

    # 3. st.table & st.json
    with sub_json_table:
        st.write("### 1. 정적 순수 HTML 테이블 (st.table)")
        st.write("상호작용 없이 모든 데이터를 고정된 표 형태로 출력합니다.")
        st.table(sample_data.head(2))

        st.divider()

        st.write("### 2. 계층형 JSON 뷰어 (st.json)")
        st.write("딕셔너리 및 중첩 JSON 데이터를 접고 펼칠 수 있는 트리 형태로 표시합니다.")
        sample_json = {
            "project": "streamlit_basic",
            "version": "1.0.0",
            "settings": {
                "theme": "light",
                "debug": False,
                "allowed_users": ["admin", "guest"],
            },
            "metrics": {"total_views": 15200, "success_rate": 99.8},
        }
        st.json(sample_json, expanded=True)

