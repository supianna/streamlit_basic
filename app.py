import streamlit as st

from widgets.chart_widgets import show_chart_widgets
from widgets.data_widgets import show_data_widgets
from widgets.input_widgets import show_input_widgets
from widgets.layout_widgets import show_layout_widgets
from widgets.status_widgets import show_status_widgets
from widgets.text_media_widgets import show_text_media_widgets

# 페이지 기본 설정
st.set_page_config(page_title="Streamlit 종합 컴포넌트 탐색", layout="wide")

st.title("🚀 Streamlit 올인원(All-in-One) 기능 종합 탐색")
st.caption("공식 API 레퍼런스를 기반으로 핵심 카테고리별 대분류 탭과 세부 기능별 소분류 탭으로 구성된 탐색기입니다.")

# 최상위 탭 그룹 (6대 메인 카테고리)
(
    main_tab_inputs,
    main_tab_layouts,
    main_tab_data,
    main_tab_charts,
    main_tab_text_media,
    main_tab_status,
) = st.tabs([
    "🎛️ 인풋 위젯 (Inputs)",
    "📐 레이아웃 & 컨테이너 (Layouts)",
    "📊 데이터 요소 (Data)",
    "📈 차트 & 지도 (Charts & Map)",
    "📝 텍스트 & 미디어 (Text & Media)",
    "🚦 상태 & 피드백 (Status)",
])

# 1. 인풋 위젯
with main_tab_inputs:
    show_input_widgets()

# 2. 레이아웃 & 컨테이너
with main_tab_layouts:
    show_layout_widgets()

# 3. 데이터 요소
with main_tab_data:
    show_data_widgets()

# 4. 차트 & 지도 시각화
with main_tab_charts:
    show_chart_widgets()

# 5. 텍스트 & 미디어
with main_tab_text_media:
    show_text_media_widgets()

# 6. 상태 & 피드백
with main_tab_status:
    show_status_widgets()