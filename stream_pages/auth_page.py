# stream_pages/auth_page.py - Streamlit 공식 사용자 인증(Authentication) 쇼케이스

import streamlit as st

st.title("🔐 Streamlit 인증 (Authentication) 쇼케이스")
st.caption(
    "Streamlit 공식 API(st.login, st.logout, st.user)를 활용한 사용자 로그인 기능 예시입니다."
)

# 1. 로그인 여부 확인 (st.user.is_logged_in)
if not st.user.get("is_logged_in", False):
    st.info("현재 로그인되지 않은 상태입니다. 로그인을 진행해주세요.")

    # 로그인 버튼 클릭 시 OIDC 프로바이더(Google) 로그인 흐름 시작
    if st.button("Google 계정으로 로그인", icon=":material/login:", type="primary"):
        st.login("google")

else:
    # 2. 로그인된 사용자 정보 확인 (st.user)
    st.success(f"환영합니다, {st.user.name}님!")

    st.subheader("👤 사용자 정보 (`st.user`)")
    st.write(f"- **이름 (name)**: {st.user.name}")
    st.write(f"- **이메일 (email)**: {st.user.email}")
    st.write(f"- **로그인 여부 (is_logged_in)**: {st.user.is_logged_in}")

    # 전체 사용자 클레임(Claim) 딕셔너리 출력
    with st.expander("전체 사용자 데이터 (to_dict)", expanded=False):
        st.json(st.user.to_dict())

    # 3. 로그아웃 (st.logout)
    if st.button("로그아웃", icon=":material/logout:"):
        st.logout()

