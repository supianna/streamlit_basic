"""
파일명: app2_chat.py
목적: 배포 환경을 위한 API Key 세션 등록 기반 순수 텍스트 AI 챗봇 (세션 관리 및 대화 수 제한 기능 포함)
"""

import logging
from datetime import datetime
import sqlite3
from openai import OpenAI
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

# 데이터베이스 파일 경로 및 기본 모델 상수
DB_FILE: str = "chat_history.db"
DEFAULT_MODEL: str = "gpt-5.6-luna"
MAX_SESSIONS_LIMIT: int = 10       # 최대 유지 세션 수 (초과 시 오래된 세션부터 삭제)
MAX_CONVERSATIONS_PER_SESSION: int = 100  # 세션당 최대 대화 쌍(내채팅+AI답변) = 200개 메시지


# ==============================================================================
# [단계 1] SQLite 데이터베이스 초기화 및 세션/메시지 관리 함수
# ==============================================================================
def init_db() -> None:
    """세션 및 메시지 저장용 SQLite 테이블을 생성하고 스키마를 정비합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 세션 테이블 (닉네임 및 삭제 비밀번호 컬럼 포함)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            nickname TEXT DEFAULT '익명',
            delete_pw TEXT DEFAULT ''
        )
    """)

    # 기존 테이블 컬럼 보정 (안전한 마이그레이션)
    cols = [col[1] for col in cursor.execute("PRAGMA table_info(sessions)").fetchall()]
    if "nickname" not in cols:
        cursor.execute("ALTER TABLE sessions ADD COLUMN nickname TEXT DEFAULT '익명'")
    if "delete_pw" not in cols:
        cursor.execute("ALTER TABLE sessions ADD COLUMN delete_pw TEXT DEFAULT ''")

    # 메시지 테이블 (API 키 등의 민감 정보는 절대 저장하지 않음)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            files TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_current_local_time() -> str:
    """현재 한국 로컬 시간을 YYYY-MM-DD HH:MM:SS 포맷 문자열로 반환합니다."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_all_sessions() -> list[dict[str, str]]:
    """대화 메시지가 존재하는 유효 세션 목록을 최신순으로 가져옵니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.session_id, s.title, s.created_at, s.nickname, s.delete_pw
        FROM sessions s
        WHERE EXISTS (SELECT 1 FROM messages m WHERE m.session_id = s.session_id)
        ORDER BY s.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    sessions = []
    for r in rows:
        sessions.append({
            "session_id": r[0],
            "title": r[1],
            "created_at": r[2],
            "nickname": r[3] if len(r) > 3 and r[3] else "익명",
            "delete_pw": r[4] if len(r) > 4 and r[4] else "",
        })
    return sessions


def prune_old_sessions() -> None:
    """저장된 세션이 10개를 초과할 경우 오래된 세션부터 자동 삭제합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id FROM sessions
        ORDER BY created_at DESC
        LIMIT -1 OFFSET ?
    """, (MAX_SESSIONS_LIMIT,))
    expired_sessions = [row[0] for row in cursor.fetchall()]

    if expired_sessions:
        logger.info("오래된 세션 %d개 자동 삭제 진행", len(expired_sessions))
        for s_id in expired_sessions:
            cursor.execute("DELETE FROM messages WHERE session_id = ?", (s_id,))
            cursor.execute("DELETE FROM sessions WHERE session_id = ?", (s_id,))
        conn.commit()

    conn.close()


def generate_new_session_id() -> str:
    """메모리상에 사용할 새로운 세션 식별자를 생성합니다 (DB 미저장)."""
    return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"


def ensure_session_in_db(session_id: str, first_prompt: str = "") -> None:
    """
    세션이 DB에 없으면 첫 질문 입력 시점에 닉네임과 삭제 비밀번호를 함께 저장합니다 (지연 생성).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sessions WHERE session_id = ?", (session_id,))
    exists = cursor.fetchone()

    if not exists:
        now_local = get_current_local_time()
        title_summary = first_prompt[:18] + ("..." if len(first_prompt) > 18 else "")
        session_title = title_summary if title_summary else f"대화 {now_local[5:16]}"
        nickname = st.session_state.get("nickname", "익명")
        delete_pw = st.session_state.get("delete_pw", "")

        cursor.execute(
            "INSERT INTO sessions (session_id, title, created_at, nickname, delete_pw) VALUES (?, ?, ?, ?, ?)",
            (session_id, session_title, now_local, nickname, delete_pw),
        )
        conn.commit()
        logger.info("첫 대화 발생으로 세션 DB 등록: %s (작성자: %s)", session_id, nickname)
        conn.close()

        # 세션 수 10개 초과 시 오래된 세션 정리
        prune_old_sessions()
    else:
        conn.close()


def verify_and_delete_session(session_id: str, input_pw: str) -> tuple[bool, str]:
    """
    입력된 비밀번호가 세션의 삭제 비밀번호와 일치하는지 확인 후 세션을 삭제합니다.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT delete_pw, nickname FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False, "존재하지 않는 세션입니다."

    stored_pw, nickname = row[0], row[1]
    if stored_pw and stored_pw != input_pw.strip():
        conn.close()
        return False, "삭제 비밀번호가 일치하지 않습니다."

    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
    logger.info("대화 세션 삭제 승인 완료: %s (작성자: %s)", session_id, nickname)
    return True, "대화가 성공적으로 삭제되었습니다."


@st.dialog("🗑️ 대화 삭제 (비밀번호 확인)")
def open_delete_chat_dialog(session_id: str) -> None:
    """대화 삭제를 위한 비밀번호 입력 확인 다이얼로그를 표시합니다."""
    st.write("선택하신 대화 세션을 완전히 삭제하시겠습니까?")
    st.caption("대화 등록 시 설정한 **삭제 비밀번호**를 입력해야 삭제가 처리됩니다.")
    del_pw_input = st.text_input("삭제 비밀번호", type="password", key="chat_del_pw_input")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("삭제 확인", use_container_width=True):
            if not del_pw_input.strip():
                st.error("삭제 비밀번호를 입력하세요.")
            else:
                success, msg = verify_and_delete_session(session_id, del_pw_input)
                if success:
                    st.success(msg)
                    st.session_state["current_session_id"] = generate_new_session_id()
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
    with col_btn2:
        if st.button("취소", use_container_width=True):
            st.rerun()


def load_session_messages(session_id: str) -> list[dict[str, str]]:
    """특정 세션의 대화 메시지들을 시간순으로 불러옵니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    return [{"role": r[0], "content": r[1]} for r in rows]


def prune_session_messages(session_id: str) -> None:
    """
    한 세션당 최대 100개 대화(내채팅 + AI답변 = 200개 메시지)만 유지되도록
    초과된 오래된 메시지를 삭제합니다.
    """
    max_message_count = MAX_CONVERSATIONS_PER_SESSION * 2

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM messages WHERE session_id = ?",
        (session_id,),
    )
    total_count = cursor.fetchone()[0]

    if total_count > max_message_count:
        excess = total_count - max_message_count
        logger.info("세션 %s 메시지 수 초과(%d개), 오래된 %d개 삭제", session_id, total_count, excess)
        cursor.execute("""
            DELETE FROM messages
            WHERE id IN (
                SELECT id FROM messages
                WHERE session_id = ?
                ORDER BY id ASC
                LIMIT ?
            )
        """, (session_id, excess))
        conn.commit()

    conn.close()


def save_session_message(session_id: str, role: str, content: str) -> None:
    """새로운 메시지를 한국 로컬 시간으로 DB에 저장하고 100개 대화 초과 시 오래된 대화를 정리합니다."""
    now_local = get_current_local_time()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content, files, created_at) VALUES (?, ?, ?, '', ?)",
        (session_id, role, content, now_local),
    )
    conn.commit()
    conn.close()

    # 세션당 100개 대화 초과 시 정리
    prune_session_messages(session_id)


# ==============================================================================
# [단계 2] DB 초기화 및 기본 활성 세션 보장 (지연 생성)
# ==============================================================================
init_db()
all_sessions = get_all_sessions()

if "current_session_id" not in st.session_state:
    if all_sessions:
        st.session_state["current_session_id"] = all_sessions[0]["session_id"]
    else:
        st.session_state["current_session_id"] = generate_new_session_id()


# ==============================================================================
# [단계 3] 사이드바 설정 (컴팩트 스크롤 프리 레이아웃)
# ==============================================================================
with st.sidebar:
    st.caption("⚙️ **챗봇 환경 설정**")

    # 1. API Key 등록 (상태 인라인 표시로 공간 절약, DB 미저장)
    saved_key = st.session_state.get("user_api_key", "").strip()
    key_label = "🔑 API Key (등록완료 ✅)" if saved_key else "🔑 API Key (미등록 ⚠️)"

    input_key = st.text_input(
        key_label,
        type="password",
        value=saved_key,
        placeholder="sk-...",
        help="입력하신 키는 DB/파일에 저장되지 않고 현재 브라우저 메모리에만 안전하게 유지됩니다.",
    )
    if input_key.strip() != saved_key:
        st.session_state["user_api_key"] = input_key.strip()
        st.rerun()

    # 2. 모델 선택 (기본: gpt-5.6-luna)
    model_name = st.selectbox(
        "🤖 모델 선택",
        options=["gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol", "gpt-5.5"],
        index=0,
    )

    # 3. 세션 관리 (새 대화 버튼 + 대화 목록 드롭다운 결합, 지연 생성)
    st.caption("💬 **채팅 세션 관리 (최대 10개)**")
    if st.button("➕ 새 대화 시작", use_container_width=True):
        st.session_state["current_session_id"] = generate_new_session_id()
        st.rerun()

    current_sid = st.session_state["current_session_id"]
    session_id_list = [s["session_id"] for s in all_sessions]
    session_label_map = {s["session_id"]: f"{s['title']} ({s['nickname']})" for s in all_sessions}

    # 아직 메시지가 없는 신규 세션일 경우 임시 표시
    if current_sid not in session_id_list:
        session_id_list = [current_sid] + session_id_list
        session_label_map[current_sid] = "✨ 새 대화 (작성 중)"

    current_idx = session_id_list.index(current_sid)

    chosen_session_id = st.selectbox(
        "대화 목록",
        options=session_id_list,
        index=current_idx,
        format_func=lambda sid: session_label_map.get(sid, sid),
        label_visibility="collapsed",
    )

    if chosen_session_id != st.session_state["current_session_id"]:
        st.session_state["current_session_id"] = chosen_session_id
        st.rerun()


# ==============================================================================
# [단계 4] 현재 세션 대화 내역 조회 및 상태 표시
# ==============================================================================
active_session_id = st.session_state["current_session_id"]
current_messages = load_session_messages(active_session_id)
dialogue_pair_count = len(current_messages) // 2

# 활성 세션의 작성자 닉네임 탐색
active_author = next(
    (s["nickname"] for s in all_sessions if s["session_id"] == active_session_id),
    st.session_state.get("nickname", "익명"),
)

# 페이지 제목 및 세션 현황
st.title("💬 실시간 텍스트 채팅")
col_info1, col_info2, col_info3 = st.columns([3, 1.2, 0.9], vertical_alignment="center")
with col_info1:
    st.caption(f"작성자: **🏷️ {active_author}** | 세션당 최대 100개 대화 보관")
with col_info2:
    st.info(f"대화: **{dialogue_pair_count} / {MAX_CONVERSATIONS_PER_SESSION} 쌍**")
with col_info3:
    if any(s["session_id"] == active_session_id for s in all_sessions):
        if st.button("🗑️ 삭제", use_container_width=True, help="비밀번호 확인 후 현재 대화를 삭제합니다."):
            open_delete_chat_dialog(active_session_id)

# 대화 내용 화면 렌더링
for msg in current_messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.caption(f"🏷️ {active_author}")
        st.write(msg["content"])


# ==============================================================================
# [단계 5] 채팅 입력 처리 (API Key 없으면 동작 차단)
# ==============================================================================
user_api_key = st.session_state.get("user_api_key", "").strip()

# API 키 등록 여부 검증
if not user_api_key:
    st.warning(
        "🔑 **OpenAI API Key 등록이 필요합니다.**\n\n"
        "채팅 기능을 사용하시려면 좌측 사이드바의 **'OpenAI API Key 등록'** 항목에 유효한 API 키를 입력해 주세요.\n"
        "- 키가 등록되지 않으면 채팅이 동작하지 않습니다.\n"
        "- 입력된 키는 DB에 저장되지 않고 현재 브라우저 메모리에만 안전하게 보관됩니다."
    )
    st.stop()

# 텍스트 채팅 입력 위젯 (이미지 및 파일 업로드 기능 완전 배제)
user_prompt = st.chat_input("메시지를 입력하세요 (Enter로 전송)...")

if user_prompt:
    # 1. DB에 세션이 없으면 첫 질문으로 정식 등록 (로컬 시간 자동 적용)
    ensure_session_in_db(active_session_id, user_prompt)

    # 2. 사용자 질문 화면 표시 및 DB 저장 (로컬 시간)
    with st.chat_message("user"):
        st.write(user_prompt)

    save_session_message(
        session_id=active_session_id,
        role="user",
        content=user_prompt,
    )

    # 2. OpenAI API 요청 메시지 포맷팅
    api_messages = [{"role": m["role"], "content": m["content"]} for m in current_messages]
    api_messages.append({"role": "user", "content": user_prompt})

    client = OpenAI(api_key=user_api_key)

    # 3. AI 답변 스트리밍 렌더링 및 DB 저장
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model_name,
            messages=api_messages,
            stream=True,
        )
        response_text = st.write_stream(stream)

    save_session_message(
        session_id=active_session_id,
        role="assistant",
        content=response_text,
    )

    # UI 동기화
    st.rerun()
