import streamlit as st


def show_text_widgets():
    st.subheader("1. st.text_input (한 줄 텍스트 입력)")
    col1, col2 = st.columns(2)

    with col1:
        basic_val = st.text_input("기본 텍스트", value="홍길동")
        st.write("👉 결과:", basic_val)

        help_val = st.text_input(
            "이메일 (placeholder, help)",
            placeholder="user@example.com",
            help="물음표에 마우스를 올리면 툴팁이 표시됩니다.",
        )
        st.write("👉 결과:", help_val)

        pw_val = st.text_input("비밀번호 (type='password')", type="password")
        st.write("👉 입력 글자 수:", len(pw_val))

    with col2:
        char_limit_val = st.text_input(
            "인증코드 (max_chars=6)",
            max_chars=6,
            placeholder="6자리 제한",
        )
        st.write("👉 결과:", char_limit_val)

        disabled_val = st.text_input(
            "비활성화 필드 (disabled=True)",
            value="수정 불가 텍스트",
            disabled=True,
        )
        st.write("👉 결과:", disabled_val)

        visibility_mode = st.radio(
            "라벨 표시 옵션 (label_visibility)",
            ["visible", "hidden", "collapsed"],
            horizontal=True,
        )
        label_val = st.text_input(
            "라벨 테스트",
            placeholder=f"현재 모드: {visibility_mode}",
            label_visibility=visibility_mode,
        )
        st.write("👉 결과:", label_val)

    st.divider()

    st.subheader("2. st.text_area (여러 줄 장문 입력)")
    col3, col4 = st.columns(2)

    with col3:
        area_h = st.text_area(
            "높이 조절 메모장 (height=130)",
            value="첫 번째 줄\n두 번째 줄\n세 번째 줄",
            height=130,
        )
        st.write(f"👉 줄 수: {len(area_h.splitlines())}줄, 글자 수: {len(area_h)}자")

    with col4:
        area_limit = st.text_area(
            "글자 수 제한 메모장 (max_chars=100)",
            placeholder="100자 이내로 입력하세요.",
            max_chars=100,
            height=130,
        )
        st.write(f"👉 입력 글자 수: {len(area_limit)} / 100자")

