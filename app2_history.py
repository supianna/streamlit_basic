"""
파일명: app2_history.py
목적: SQLite 데이터베이스(chat_history.db)에 저장된 세션별 대화 내역 조회, 검색 및 텍스트 백업 뷰어
"""

import logging
import sqlite3
import streamlit as st
from theme import apply_theme

# 사이버 오로라 네온 테마 적용
apply_theme()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

DB_FILE: str = "chat_history.db"

st.title("📜 과거 채팅 내역 뷰어 (세션별 조회)")
st.caption("최대 10개의 세션과 세션당 최대 100개 대화(내채팅+AI답변)가 관리되는 SQLite 기록을 확인합니다.")


# ==============================================================================
# [단계 1] SQLite 데이터베이스 조회 헬퍼 함수
# ==============================================================================
def get_all_sessions() -> list[dict[str, str]]:
    """대화 메시지가 존재하는 유효 세션 목록을 최신순으로 반환합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.session_id, s.title, s.created_at
        FROM sessions s
        WHERE EXISTS (SELECT 1 FROM messages m WHERE m.session_id = s.session_id)
        ORDER BY s.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{"session_id": r[0], "title": r[1], "created_at": r[2]} for r in rows]


def get_messages_by_session(session_id: str | None = None) -> list[tuple]:
    """특정 세션 또는 전체 세션의 대화 메시지들을 시간순으로 반환합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if session_id and session_id != "all":
        cursor.execute(
            "SELECT id, role, content, created_at, session_id FROM messages WHERE session_id = ? ORDER BY id ASC",
            (session_id,),
        )
    else:
        cursor.execute(
            "SELECT id, role, content, created_at, session_id FROM messages ORDER BY id ASC"
        )
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_messages(keyword: str, session_id: str | None = None) -> list[tuple]:
    """키워드가 포함된 메시지를 검색합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if session_id and session_id != "all":
        cursor.execute(
            "SELECT id, role, content, created_at, session_id FROM messages WHERE session_id = ? AND content LIKE ? ORDER BY id DESC",
            (session_id, f"%{keyword}%"),
        )
    else:
        cursor.execute(
            "SELECT id, role, content, created_at, session_id FROM messages WHERE content LIKE ? ORDER BY id DESC",
            (f"%{keyword}%",),
        )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_session(session_id: str) -> None:
    """특정 세션과 해당 세션의 메시지를 삭제합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
    logger.info("세션 삭제 완료: %s", session_id)


# ==============================================================================
# [단계 2] 세션 선택 및 통계 대시보드
# ==============================================================================
sessions = get_all_sessions()

if not sessions:
    st.info("현재 저장된 채팅 세션이 없습니다. 채팅 페이지에서 대화를 시작해보세요!")
    st.stop()

col_select, col_del = st.columns([4, 1])

with col_select:
    session_options = ["all"] + [s["session_id"] for s in sessions]
    session_labels = {"all": "🌐 전체 세션 통합 조회"}
    for s in sessions:
        session_labels[s["session_id"]] = f"📁 {s['title']} ({s['created_at'][:16]})"

    selected_session = st.selectbox(
        "조회할 세션을 선택하세요",
        options=session_options,
        format_func=lambda x: session_labels.get(x, x),
    )

with col_del:
    st.write("")  # 간격 맞춤
    st.write("")
    if selected_session != "all":
        if st.button("🗑️ 세션 삭제", use_container_width=True):
            delete_session(selected_session)
            st.success("세션이 삭제되었습니다.")
            st.rerun()

# 선택된 세션의 메시지 로드
all_msgs = get_messages_by_session(selected_session)
user_count = sum(1 for m in all_msgs if m[1] == "user")
ai_count = sum(1 for m in all_msgs if m[1] == "assistant")
conversation_pairs = user_count  # 1개 대화 = 내채팅+AI답변

stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric(label="총 세션 수 (최대 10개)", value=f"{len(sessions)} / 10개")
with stat_col2:
    st.metric(label="선택 세션 대화 수 (최대 100쌍)", value=f"{conversation_pairs} / 100 쌍")
with stat_col3:
    st.metric(label="총 메시지 수 (질문 / 답변)", value=f"{user_count} / {ai_count}")

st.divider()


# ==============================================================================
# [단계 3] 텍스트 다운로드 백업
# ==============================================================================
if all_msgs:
    download_text = f"=== 대화 기록 내역 ({selected_session}) ===\n\n"
    for m in all_msgs:
        # m = (id, role, content, created_at, session_id)
        download_text += f"[{m[3]}] [{m[4]}] {m[1].upper()}:\n{m[2]}\n"
        download_text += "-" * 50 + "\n"

    st.download_button(
        label="📥 대화 내역 텍스트 다운로드 (.txt)",
        data=download_text,
        file_name=f"chat_history_{selected_session}.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ==============================================================================
# [단계 4] 메인 탭: 대화 타임라인 vs 키워드 검색
# ==============================================================================
tab_timeline, tab_search = st.tabs(["💬 대화 타임라인", "🔍 대화 내용 검색"])

# 1. 대화 타임라인
with tab_timeline:
    if not all_msgs:
        st.info("해당 세션에 저장된 대화 내용이 없습니다.")
    else:
        st.subheader(f"대화 목록 (총 {len(all_msgs)}개 메시지)")
        for m in all_msgs:
            # m = (id, role, content, created_at, session_id)
            with st.chat_message(m[1]):
                st.caption(f"🕒 {m[3]}")
                st.write(m[2])

# 2. 키워드 검색
with tab_search:
    st.subheader("🔍 키워드 검색")
    query = st.text_input("검색할 단어를 입력하세요", placeholder="검색어 입력 후 Enter...")

    if query:
        search_results = search_messages(query, selected_session)
        st.write(f"👉 **'{query}'** 검색 결과: 총 **{len(search_results)}**건")

        for res in search_results:
            # res = (id, role, content, created_at, session_id)
            with st.container(border=True):
                col_r1, col_r2 = st.columns([3, 1])
                with col_r1:
                    st.markdown(f"**작성자:** `{res[1]}` | **세션:** `{res[4]}`")
                with col_r2:
                    st.caption(f"🕒 {res[3]}")
                st.write(res[2])
