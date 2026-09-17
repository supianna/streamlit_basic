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

    # 세션 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

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


def get_all_sessions() -> list[dict[str, str]]:
    """저장된 모든 세션 목록을 최신순으로 가져옵니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, title, created_at FROM sessions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    sessions = []
    for r in rows:
        sessions.append({
            "session_id": r[0],
            "title": r[1],
            "created_at": r[2],
        })
    return sessions


def prune_old_sessions() -> None:
    """저장된 세션이 10개를 초과할 경우 오래된 세션부터 자동 삭제합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 최신 10개를 제외한 나머지 오래된 세션 조회
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


def create_new_session(title: str = "") -> str:
    """새로운 채팅 세션을 생성하고 10개 초과 시 오래된 세션을 정리합니다."""
    now_str = datetime.now().strftime("%m/%d %H:%M:%S")
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    session_title = title if title else f"대화 {now_str}"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (session_id, title) VALUES (?, ?)",
        (session_id, session_title),
    )
    conn.commit()
    conn.close()

    # 세션 10개 초과 시 자동 정리
    prune_old_sessions()
    logger.info("새 세션 생성 완료: %s (%s)", session_id, session_title)
    return session_id


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
    """새로운 메시지를 특정 세션에 저장하고 100개 대화 초과 시 오래된 대화를 정리합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content, files) VALUES (?, ?, ?, '')",
        (session_id, role, content),
    )
    conn.commit()
    conn.close()

    # 세션당 100개 대화 초과 시 정리
    prune_session_messages(session_id)


def update_session_title_if_default(session_id: str, first_prompt: str) -> None:
    """첫 질문 내용을 기반으로 세션 제목을 직관적으로 업데이트합니다."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    if row and row[0].startswith("대화 "):
        new_title = first_prompt[:18] + ("..." if len(first_prompt) > 18 else "")
        cursor.execute(
            "UPDATE sessions SET title = ? WHERE session_id = ?",
            (new_title, session_id),
        )
        conn.commit()
    conn.close()


# ==============================================================================
# [단계 2] DB 초기화 및 기본 활성 세션 보장
# ==============================================================================
init_db()
all_sessions = get_all_sessions()

if not all_sessions:
    new_id = create_new_session()
    all_sessions = get_all_sessions()
    st.session_state["current_session_id"] = new_id

if "current_session_id" not in st.session_state or not any(s["session_id"] == st.session_state["current_session_id"] for s in all_sessions):
    st.session_state["current_session_id"] = all_sessions[0]["session_id"]


# ==============================================================================
# [단계 3] 사이드바 설정 (API 키 등록, 모델 선택, 세션 관리)
# ==============================================================================
with st.sidebar:
    st.header("⚙️ 챗봇 설정")

    # 1. API Key 등록 옵션 (DB나 파일에 절대 저장되지 않고 세션 메모리에만 유지)
    st.markdown("#### 🔑 OpenAI API Key 등록")
    saved_key = st.session_state.get("user_api_key", "")

    input_key = st.text_input(
        "API 키 입력 (필수)",
        type="password",
        value=saved_key,
        placeholder="sk-...",
        help="입력하신 키는 DB나 디스크에 저장되지 않으며 현재 브라우저 메모리에만 유지됩니다.",
    )

    if input_key.strip():
        st.session_state["user_api_key"] = input_key.strip()
        st.success("✅ API 키 등록 완료")
    else:
        st.session_state["user_api_key"] = ""
        st.warning("⚠️ API 키가 등록되지 않았습니다.")

    st.caption("🔒 민감한 API Key는 보안을 위해 서버 DB나 로컬 파일에 일절 저장되지 않습니다.")
    st.divider()

    # 2. 모델 선택 (규칙 10: gpt-5.6-luna 기본)
    model_options = [
        "gpt-5.6-luna",
        "gpt-5.6-terra",
        "gpt-5.6-sol",
        "gpt-5.5",
        "gpt-6-astra",
        "직접 입력...",
    ]
    selected_option = st.selectbox(
        "OpenAI 모델 선택 (기본: gpt-5.6-luna)",
        options=model_options,
        index=0,
    )
    if selected_option == "직접 입력...":
        model_name = st.text_input("모델명 직접 입력", value=DEFAULT_MODEL)
    else:
        model_name = selected_option

    st.divider()

    # 3. 세션 관리 영역 (최대 10개 세션, 세션당 100개 대화 유지)
    st.markdown("#### 💬 채팅 세션 관리")
    st.caption("최대 10개 세션까지 유지되며, 초과 시 오래된 세션부터 자동 정리됩니다.")

    if st.button("➕ 새 채팅 세션 시작", use_container_width=True):
        new_sid = create_new_session()
        st.session_state["current_session_id"] = new_sid
        st.rerun()

    # 세션 선택 셀렉트박스
    session_id_list = [s["session_id"] for s in all_sessions]
    session_label_map = {s["session_id"]: f"{s['title']} ({s['created_at'][:16]})" for s in all_sessions}

    current_idx = session_id_list.index(st.session_state["current_session_id"]) if st.session_state["current_session_id"] in session_id_list else 0

    chosen_session_id = st.selectbox(
        "세션 전환",
        options=session_id_list,
        index=current_idx,
        format_func=lambda sid: session_label_map.get(sid, sid),
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

# 페이지 제목 및 세션 현황
st.title("💬 실시간 텍스트 채팅")
col_info1, col_info2 = st.columns([3, 1])
with col_info1:
    st.caption("깨끗한 순수 텍스트 대화를 지원하며, 한 세션당 최대 100개의 대화(질문+답변)가 보관됩니다.")
with col_info2:
    st.info(f"대화 수: **{dialogue_pair_count} / {MAX_CONVERSATIONS_PER_SESSION} 쌍**")

# 대화 내용 화면 렌더링
for msg in current_messages:
    with st.chat_message(msg["role"]):
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
    # 1. 사용자 질문 화면 표시 및 DB 저장
    with st.chat_message("user"):
        st.write(user_prompt)

    save_session_message(
        session_id=active_session_id,
        role="user",
        content=user_prompt,
    )

    # 첫 메시지인 경우 세션 제목을 알기 쉽게 갱신
    if len(current_messages) == 0:
        update_session_title_if_default(active_session_id, user_prompt)

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
