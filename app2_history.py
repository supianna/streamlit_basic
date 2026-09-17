import sqlite3
import streamlit as st

DB_FILE = "chat_history.db"

st.title("📜 과거 채팅 내역 뷰어 (SQLite)")
st.caption("SQLite 데이터베이스(chat_history.db)에 연속 저장된 모든 대화 기록을 조회하고 검색 및 다운로드합니다.")


# ==============================================================================
# SQLite 데이터베이스 조회 헬퍼 함수
# ==============================================================================
def get_all_messages():
    """DB에 저장된 모든 대화 메시지를 시간순으로 반환합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, role, content, files, created_at FROM messages ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_messages(keyword: str):
    """키워드가 포함된 메시지를 검색합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, role, content, files, created_at FROM messages WHERE content LIKE ? ORDER BY id DESC",
        (f"%{keyword}%",),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def clear_all_messages():
    """모든 대화 내역을 삭제합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()


# 데이터 로드
try:
    all_msgs = get_all_messages()
except Exception:
    all_msgs = []

user_count = sum(1 for m in all_msgs if m[1] == "user")
ai_count = sum(1 for m in all_msgs if m[1] == "assistant")

# ==============================================================================
# 상단 대시보드 통계 카드
# ==============================================================================
stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric(label="총 누적 대화 수", value=f"{len(all_msgs)}개")
with stat_col2:
    st.metric(label="사용자 질문 / AI 답변", value=f"{user_count} / {ai_count}")
with stat_col3:
    st.metric(label="데이터베이스 파일", value="chat_history.db")

st.divider()

# ==============================================================================
# 상단 액션 바 (다운로드 및 대화 비우기)
# ==============================================================================
if all_msgs:
    col_down, col_clear = st.columns([3, 1])

    with col_down:
        # 텍스트 형식 다운로드 데이터 생성
        download_text = "=== OpenAI 대화 기록 전체 내역 ===\n\n"
        for m in all_msgs:
            download_text += f"[{m[4]}] {m[1].upper()}:\n{m[2]}\n"
            if m[3]:
                download_text += f"첨부: {m[3]}\n"
            download_text += "-" * 50 + "\n"

        st.download_button(
            label="📥 전체 대화 내역 텍스트 다운로드 (.txt)",
            data=download_text,
            file_name="chat_history_backup.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col_clear:
        if st.button("🗑️ 대화 내역 전체 삭제", use_container_width=True):
            clear_all_messages()
            st.success("대화 내역이 모두 삭제되었습니다.")
            st.rerun()

# ==============================================================================
# 메인 탭: 전체 대화 타임라인 vs 키워드 검색
# ==============================================================================
tab_all, tab_search = st.tabs(["💬 전체 대화 내역", "🔍 대화 내용 검색"])

# 1. 전체 대화 내역
with tab_all:
    if not all_msgs:
        st.info("현재 저장된 대화 내역이 없습니다. 채팅 페이지에서 대화를 나눠보세요!")
    else:
        st.subheader(f"대화 타임라인 (총 {len(all_msgs)}개)")
        for m in all_msgs:
            # m = (id, role, content, files, created_at)
            with st.chat_message(m[1]):
                st.caption(f"🕒 {m[4]}")
                if m[3]:
                    st.caption(f"📎 첨부: {m[3]}")
                st.write(m[2])

# 2. 키워드 검색
with tab_search:
    st.write("### 🔍 대화 키워드 검색")
    query = st.text_input("검색할 단어를 입력하세요", placeholder="검색어 입력 후 Enter...")

    if query:
        search_results = search_messages(query)
        st.write(f"👉 **'{query}'** 검색 결과: 총 **{len(search_results)}**건")

        for res in search_results:
            # res = (id, role, content, files, created_at)
            with st.container(border=True):
                col_r1, col_r2 = st.columns([3, 1])
                with col_r1:
                    st.markdown(f"**작성자:** `{res[1]}`")
                with col_r2:
                    st.caption(f"🕒 {res[4]}")

                if res[3]:
                    st.caption(f"📎 첨부: {res[3]}")

                st.write(res[2])
