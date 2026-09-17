import streamlit as st

from widgets.datetime_widgets import show_datetime_widgets
from widgets.numeric_widgets import show_numeric_widgets
from widgets.other_widgets import show_other_widgets
from widgets.selection_widgets import show_selection_widgets
from widgets.text_widgets import show_text_widgets


def show_input_widgets():
    st.subheader("🎛️ 입력 위젯 모음")
    st.caption("아래 하위 탭을 통해 다양한 사용자 입력 위젯을 탐색해보세요.")

    # 하위 서브 탭 구성
    sub_text, sub_numeric, sub_select, sub_date, sub_other = st.tabs([
        "📝 텍스트 입력",
        "🔢 숫자 & 슬라이더",
        "🔘 선택 위젯 (라디오/셀렉트/체크/토글)",
        "📅 날짜 & 시간",
        "🎨 기타 위젯 (색상/알약/채팅)",
    ])

    with sub_text:
        show_text_widgets()

    with sub_numeric:
        show_numeric_widgets()

    with sub_select:
        show_selection_widgets()

    with sub_date:
        show_datetime_widgets()

    with sub_other:
        show_other_widgets()

