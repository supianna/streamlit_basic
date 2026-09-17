import json
import sqlite3
import streamlit as st

DB_FILE = "chat_history.db"

st.title("📜 과거 채팅 내역 뷰어 (SQLite)")
st.caption("로컬 SQLite 데이터베이스(chat_history.db)에 저장된 이전 대화 기록들을 조회하고 검색 및 다운로드합니다.")


# ==============================================================================
# SQLite 데이터베이스 조회 헬퍼 함수
# ==============================================================================
def get_db_stats():
    """전체 세션 수와 메시지 수 통계를 반환합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sessions")
    session_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM messages")
    message_count = cursor.fetchone()[0]
    conn.close()
    return session_count, message_count


def get_all_sessions():
    """저장된 모든 대화 세션 목록을 반환합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, title, created_at FROM sessions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_messages_by_session(session_id: str):
    """특정 세션의 모든 메시지 내역을 반환합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, role, content, files, created_at FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_messages(keyword: str):
    """키워드가 포함된 메시지를 검색합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT m.id, m.session_id, s.title, m.role, m.content, m.files, m.created_at
        FROM messages m
        LEFT JOIN sessions s ON m.session_id = s.session_id
        WHERE m.content LIKE ?
        ORDER BY m.created_at DESC
        """,
        (f"%{keyword}%",),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_session(session_id: str):
    """지정된 세션과 해당 메시지들을 삭제합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()


# ==============================================================================
# 상단 대시보드 통계 카드
# ==============================================================================
try:
    total_sessions, total_messages = get_db_stats()
except Exception:
    total_sessions, total_messages = 0, 0

stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric(label="총 대화 세션 수", value=f"{total_sessions}개")
with stat_col2:
    st.metric(label="총 누적 메시지 수", value=f"{total_messages}개")
with stat_col3:
    st.metric(label="데이터베이스 파일", value="chat_history.db")

st.divider()

# ==============================================================================
# 메인 탭: 세션별 대화 상세 보기 vs 전체 메시지 키워드 검색
# ==============================================================================
tab_by_session, tab_search = st.tabs(["💬 대화 세션별 상세 조회", "🔍 키워드 검색"])

# ------------------------------------------------------------------------------
# 1. 세션별 상세 조회
# ------------------------------------------------------------------------------
with tab_by_session:
    sessions = get_all_sessions()

    if not sessions:
        st.info("현재 저장된 과거 대화 내역이 없습니다. app2.py에서 대화를 나눠보세요!")
    else:
        # 사이드바 또는 상단 선택창에서 세션 선택
        session_options = {f"[{s[2][:16]}] {s[1]} (ID: {s[0]})": s[0] for s in sessions}
        selected_label = st.selectbox(
            "조회할 대화 세션을 선택하세요",
            options=list(session_options.keys()),
        )
        selected_sid = session_options[selected_label]

        # 세션 컨트롤 (다운로드 및 삭제)
        col_info, col_actions = st.columns([3, 1])

        # 선택된 세션의 메시지 가져오기
        msg_rows = get_messages_by_session(selected_sid)

        with col_actions:
            # 텍스트 형식 다운로드 생성
            download_text = f"=== 대화 세션: {selected_label} ===\n\n"
            for m in msg_rows:
                download_text += f"[{m[4]}] {m[1].upper()}:\n{m[2]}\n"
                if m[3]:
                    download_text += f"첨부: {m[3]}\n"
                download_text += "-" * 40 + "\n"

            st.download_button(
                label="📥 대화 내역 텍스트 다운로드",
                data=download_text,
                file_name=f"{selected_sid}.txt",
                mime="text/plain",
                use_container_width=True,
            )

            if st.button("🗑️ 이 세션 삭제하기", use_container_width=True):
                delete_session(selected_sid)
                st.success("세션이 삭제되었습니다.")
                st.rerun()

        st.subheader(f"대화 내용 (총 {len(msg_rows)}개 메시지)")

        # 대화 메시지 렌더링
        for m in msg_rows:
            # m = (id, role, content, files, created_at)
            with st.chat_message(m[1]):
                st.caption(f"🕒 {m[4]}")
                if m[3]:
                    st.caption(f"📎 첨부파일: {m[3]}")
                st.write(m[2])

# ------------------------------------------------------------------------------
# 2. 전체 메시지 키워드 검색
# ------------------------------------------------------------------------------
with tab_search:
    st.write("### 🔍 전체 대화 메시지 키워드 검색")
    search_query = st.text_input("검색어를 입력하세요", placeholder="검색할 단어 입력 후 Enter...")

    if search_query:
        search_results = search_messages(search_query)
        st.write(f"👉 **'{search_query}'** 검색 결과: 총 **{len(search_results)}**건")

        for res in search_results:
            # res = (id, session_id, session_title, role, content, files, created_at)
            with st.container(border=True):
                col_r1, col_r2 = st.columns([3, 1])
                with col_r1:
                    st.markdown(f"**대화방:** {res[2] or res[1]} | **작성자:** `{res[3]}`")
                with col_r2:
                    st.caption(f"🕒 {res[6]}")

                if res[5]:
                    st.caption(f"📎 첨부: {res[5]}")

                # 검색어 하이라이트 느낌으로 표시
                st.write(res[4])

