import base64
from datetime import datetime
import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# .env 환경변수 자동 로드
load_dotenv()

DB_FILE = "chat_history.db"

st.title("💬 OpenAI 멀티모달 채팅 (gpt-5.6-luna)")
st.caption("이전 대화 불러오기, 팝업 드래그앤드롭 이미지/파일 첨부, SQLite 영구 저장을 지원하는 챗봇입니다.")


# ==============================================================================
# SQLite 데이터베이스 관리 함수
# ==============================================================================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 대화 세션 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 메시지 테이블 (세션 ID와 연동)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT DEFAULT 'default_session',
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            files TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 기존 테이블 호환성을 위한 session_id 컬럼 마이그레이션
    cursor.execute("PRAGMA table_info(messages)")
    columns = [col[1] for col in cursor.fetchall()]
    if "session_id" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN session_id TEXT DEFAULT 'default_session'")
    conn.commit()
    conn.close()


def get_all_sessions():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, title, created_at FROM sessions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def create_session(session_id: str, title: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO sessions (session_id, title) VALUES (?, ?)",
        (session_id, title),
    )
    conn.commit()
    conn.close()


def load_messages_by_session(session_id: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content, files FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    messages = []
    for r in rows:
        files_list = r[2].split(", ") if r[2] else []
        messages.append({
            "role": r[0],
            "content": r[1],
            "files": files_list,
        })
    return messages


def save_message(session_id: str, role: str, content: str, files: str = ""):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content, files) VALUES (?, ?, ?, ?)",
        (session_id, role, content, files),
    )
    conn.commit()
    conn.close()


def delete_session(session_id: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()


# DB 초기화
init_db()

# 세션 상태 초기화
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = datetime.now().strftime("chat_%Y%m%d_%H%M%S")
    create_session(st.session_state.current_session_id, f"대화 {datetime.now().strftime('%m/%d %H:%M')}")

if "messages" not in st.session_state:
    st.session_state.messages = load_messages_by_session(st.session_state.current_session_id)

# 첨부 대기 중인 이미지/파일 저장소
if "pending_images" not in st.session_state:
    st.session_state.pending_images = []
if "pending_files" not in st.session_state:
    st.session_state.pending_files = []


# ==============================================================================
# 팝업 다이얼로그 (이미지 및 파일 업로드)
# ==============================================================================
@st.dialog("🖼️ 이미지 드래그앤드롭 첨부")
def open_image_upload_dialog():
    st.write("첨부할 이미지 파일을 드래그하거나 선택하세요.")
    uploaded = st.file_uploader(
        "이미지 선택 (PNG, JPG, WEBP)",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
    )
    if st.button("첨부 확인", use_container_width=True):
        if uploaded:
            for f in uploaded:
                st.session_state.pending_images.append({
                    "name": f.name,
                    "bytes": f.getvalue(),
                    "type": f.type,
                })
        st.rerun()


@st.dialog("📁 문서/파일 첨부")
def open_file_upload_dialog():
    st.write("첨부할 텍스트 및 코드/데이터 문서를 드래그하거나 선택하세요.")
    uploaded = st.file_uploader(
        "파일 선택 (TXT, CSV, PY, MD, JSON)",
        type=["txt", "csv", "py", "md", "json"],
        accept_multiple_files=True,
    )
    if st.button("첨부 확인", use_container_width=True):
        if uploaded:
            for f in uploaded:
                try:
                    text_str = f.getvalue().decode("utf-8")
                except Exception:
                    text_str = "[바이너리 또는 디코딩 불가 파일]"
                st.session_state.pending_files.append({
                    "name": f.name,
                    "content": text_str,
                })
        st.rerun()


# ==============================================================================
# 사이드바 설정 (이전 대화 불러오기, API Key 및 모델)
# ==============================================================================
with st.sidebar:
    st.header("⚙️ 챗봇 설정")

    # 1. API 키 설정 (.env 우선)
    env_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input(
        "OpenAI API Key",
        value=env_api_key,
        type="password",
        placeholder="sk-...",
        help=".env 파일의 OPENAI_API_KEY를 자동으로 가져옵니다.",
    )

    if env_api_key:
        st.success("✅ .env 환경변수 로드 완료", icon="🔑")
    else:
        st.warning("⚠️ .env에 OPENAI_API_KEY가 없습니다.", icon="⚠️")

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
        "OpenAI 모델 선택 (GPT-5.5+)",
        options=model_options,
        index=0,
    )
    if selected_option == "직접 입력...":
        model_name = st.text_input("모델명 직접 입력", value="gpt-5.6-luna")
    else:
        model_name = selected_option

    st.divider()

    # 3. 이전 채팅 내역 불러오기 & 세션 관리
    st.subheader("📂 이전 대화 기록 관리")

    if st.button("➕ 새 대화 시작하기", use_container_width=True):
        new_sid = datetime.now().strftime("chat_%Y%m%d_%H%M%S")
        st.session_state.current_session_id = new_sid
        create_session(new_sid, f"대화 {datetime.now().strftime('%m/%d %H:%M')}")
        st.session_state.messages = []
        st.session_state.pending_images = []
        st.session_state.pending_files = []
        st.rerun()

    # DB에 저장된 과거 대화 세션 목록
    all_sessions = get_all_sessions()
    if all_sessions:
        session_dict = {f"{s[1]} ({s[0]})": s[0] for s in all_sessions}
        selected_session_label = st.selectbox(
            "불러올 이전 대화 선택",
            options=list(session_dict.keys()),
        )

        col_load, col_del = st.columns(2)
        with col_load:
            if st.button("📥 불러오기", use_container_width=True):
                target_sid = session_dict[selected_session_label]
                st.session_state.current_session_id = target_sid
                st.session_state.messages = load_messages_by_session(target_sid)
                st.success("대화 내역을 불러왔습니다!")
                st.rerun()

        with col_del:
            if st.button("🗑️ 세션 삭제", use_container_width=True):
                target_sid = session_dict[selected_session_label]
                delete_session(target_sid)
                new_sid = datetime.now().strftime("chat_%Y%m%d_%H%M%S")
                st.session_state.current_session_id = new_sid
                create_session(new_sid, f"대화 {datetime.now().strftime('%m/%d %H:%M')}")
                st.session_state.messages = []
                st.rerun()
    else:
        st.caption("저장된 과거 대화가 없습니다.")


# ==============================================================================
# 기존 대화 히스토리 화면 출력
# ==============================================================================
st.info(f"현재 대화방: **{st.session_state.current_session_id}** (저장된 메시지: {len(st.session_state.messages)}개)")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "files" in msg and msg["files"]:
            for fname in msg["files"]:
                st.caption(f"📎 첨부: {fname}")
        if "images" in msg and msg["images"]:
            for img in msg["images"]:
                st.image(img, width=280)
        st.write(msg["content"])


# ==============================================================================
# 첨부 버튼 영역 (이미지 팝업 버튼 / 파일 팝업 버튼 분리)
# ==============================================================================
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])

with col_btn1:
    if st.button("🖼️ 이미지 첨부 (팝업)", use_container_width=True):
        open_image_upload_dialog()

with col_btn2:
    if st.button("📁 파일 첨부 (팝업)", use_container_width=True):
        open_file_upload_dialog()

with col_btn3:
    if st.session_state.pending_images or st.session_state.pending_files:
        if st.button("❌ 모든 첨부 취소"):
            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()

# 첨부 대기 상태 미리보기 카드
if st.session_state.pending_images or st.session_state.pending_files:
    with st.container(border=True):
        st.write("📎 **전송 대기 중인 첨부 목록:**")
        if st.session_state.pending_images:
            img_cols = st.columns(min(len(st.session_state.pending_images), 4))
            for idx, img_item in enumerate(st.session_state.pending_images):
                with img_cols[idx % 4]:
                    st.image(img_item["bytes"], caption=img_item["name"], width=120)
        if st.session_state.pending_files:
            file_names = [f["name"] for f in st.session_state.pending_files]
            st.caption(f"📄 문서: {', '.join(file_names)}")


# ==============================================================================
# 채팅 입력 위젯 (st.chat_input)
# ==============================================================================
user_prompt = st.chat_input("메시지를 입력하세요 (Enter로 전송)...")

if user_prompt:
    if not api_key:
        st.error("OpenAI API Key를 먼저 입력하거나 .env 파일에 설정해주세요!")
        st.stop()

    client = OpenAI(api_key=api_key)

    openai_content = []
    user_file_names = []
    cached_images = []

    openai_content.append({"type": "text", "text": user_prompt})

    for img_item in st.session_state.pending_images:
        user_file_names.append(f"[이미지] {img_item['name']}")
        cached_images.append(img_item["bytes"])
        b64_str = base64.b64encode(img_item["bytes"]).decode("utf-8")
        openai_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{img_item['type']};base64,{b64_str}"},
        })

    for f_item in st.session_state.pending_files:
        user_file_names.append(f"[문서] {f_item['name']}")
        openai_content.append({
            "type": "text",
            "text": f"\n\n[첨부문서: {f_item['name']}]\n{f_item['content']}",
        })

    st.session_state.pending_images = []
    st.session_state.pending_files = []

    with st.chat_message("user"):
        for fname in user_file_names:
            st.caption(f"📎 첨부: {fname}")
        for img_bytes in cached_images:
            st.image(img_bytes, width=280)
        st.write(user_prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt,
        "images": cached_images,
        "files": user_file_names,
        "openai_content": openai_content,
    })
    save_message(
        session_id=st.session_state.current_session_id,
        role="user",
        content=user_prompt,
        files=", ".join(user_file_names),
    )

    api_messages = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            api_messages.append({
                "role": "user",
                "content": msg.get("openai_content", msg["content"]),
            })
        else:
            api_messages.append({
                "role": "assistant",
                "content": msg["content"],
            })

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model_name,
            messages=api_messages,
            stream=True,
        )
        response_text = st.write_stream(stream)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
    })
    save_message(
        session_id=st.session_state.current_session_id,
        role="assistant",
        content=response_text,
    )

