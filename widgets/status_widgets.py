import time
import streamlit as st


def show_status_widgets():
    st.subheader("🚦 상태 알림 & 피드백 (Status Elements)")
    st.caption("공식 API 레퍼런스의 알림 배너, 진행 상태, 로딩 스피너, 축하 애니메이션 등을 살펴봅니다.")

    tab_alert, tab_progress, tab_fx = st.tabs([
        "📢 알림 메시지 (Alerts)",
        "⏳ 진행률 & 상태 컨테이너 (Progress / Status / Spinner)",
        "🎉 토스트 & 축하 효과 (Toast / Balloons / Snow)",
    ])

    # 1. 알림 메시지 배너
    with tab_alert:
        st.write("### 4가지 기본 알림 메시지 배너")
        st.success("✅ **성공(st.success)**: 작업이 성공적으로 완료되었습니다.", icon="✅")
        st.info("ℹ️ **안내(st.info)**: 참고용 안내 정보입니다.", icon="ℹ️")
        st.warning("⚠️ **경고(st.warning)**: 주의가 필요한 항목입니다.", icon="⚠️")
        st.error("🚨 **오류(st.error)**: 에러가 발생했습니다.", icon="🚨")

    # 2. 진행률 및 상태 컨테이너
    with tab_progress:
        st.write("### 1. 프로그레스 바 (st.progress)")
        prog_val = st.slider("진행률 수동 조절 (%)", 0, 100, 45)
        st.progress(prog_val, text=f"전체 작업의 {prog_val}% 완료")

        st.divider()

        st.write("### 2. 다단계 상태 컨테이너 (st.status)")
        if st.button("단계별 작업 시뮬레이션 시작"):
            with st.status("작업을 진행 중입니다...", expanded=True) as status:
                st.write("1단계: 데이터 다운로드 중...")
                time.sleep(1)
                st.write("2단계: 데이터 변환 및 검증 중...")
                time.sleep(1)
                st.write("3단계: 최종 결과 저장 완료!")
                status.update(label="모든 작업이 완료되었습니다!", state="complete", expanded=False)

    # 3. 토스트 및 축하 효과
    with tab_fx:
        st.write("### 1. 팝업 토스트 알림 (st.toast)")
        if st.button("토스트 알림 띄우기"):
            st.toast("우측 하단에 알림 메시지가 표시됩니다!", icon="🔔")

        st.divider()

        st.write("### 2. 축하 애니메이션 효과")
        col_fx1, col_fx2 = st.columns(2)
        with col_fx1:
            if st.button("🎈 풍선 날리기 (st.balloons)"):
                st.balloons()
        with col_fx2:
            if st.button("❄️ 눈 내리기 (st.snow)"):
                st.snow()

