import streamlit as st


def show_text_media_widgets():
    st.subheader("📝 텍스트 서식 & 미디어 요소 (Text & Media Elements)")
    st.caption("공식 API 레퍼런스의 마크다운, 코드 블록, 수식(LaTeX), 이미지, 오디오, 비디오 요소를 살펴봅니다.")

    tab_text_format, tab_media = st.tabs([
        "🖋️ 텍스트 서식 & 코드 (Markdown / Code / LaTeX)",
        "🎬 미디어 재생 (Image / Audio / Video)",
    ])

    # 1. 텍스트 서식
    with tab_text_format:
        st.write("### 1. 마크다운 스타일링 (st.markdown)")
        st.markdown("""
        - **굵은 글씨 (Bold)** 및 *기울임 (Italic)*
        - 색상 텍스트: :red[빨간색], :blue[파란색], :green[초록색]
        - 이모지와 인라인 코드: `:rocket:` -> 🚀, `st.write()`
        """)

        st.divider()

        st.write("### 2. 코드 블록 표시 (st.code)")
        sample_python_code = """def greet(name: str) -> str:
    return f"안녕하세요, {name}님!"

message = greet("김누리")
print(message)"""
        st.code(sample_python_code, language="python", line_numbers=True)

        st.divider()

        st.write("### 3. 수학 수식 표현 (st.latex)")
        st.latex(r"E = mc^2")
        st.latex(r"f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi)\,e^{2 \pi i \xi x}\,d\xi")

    # 2. 미디어 재생
    with tab_media:
        st.write("### 1. 이미지 표시 (st.image)")
        st.image(
            "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600",
            caption="Unsplash 무료 샘플 아트워크 이미지",
            use_container_width=True,
        )

        st.divider()

        st.write("### 2. 비디오 및 오디오 플레이어")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.write("**동영상 플레이어 (st.video)**")
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

        with col_v2:
            st.write("**오디오 플레이어 (st.audio)**")
            st.audio("https://www.w3schools.com/html/horse.mp3")

