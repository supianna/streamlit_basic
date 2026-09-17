# Streamlit 기초 & OpenAI 멀티모달 챗봇 실습 프로젝트

Streamlit의 주요 기능(위젯, 레이아웃, 데이터, 차트 등)을 둘러볼 수 있는 종합 탐색기와, OpenAI 최신 모델(GPT-5.5+) 기반 멀티모달 챗봇을 학습하고 실습하는 프로젝트입니다.

---

## 📌 주요 구성 및 기능

### 1. 🎛️ Streamlit 기본 컴포넌트 종합 탐색 (`app.py`)
공식 API 레퍼런스를 기반으로 6대 대분류 탭과 세부 소분류 탭으로 구성된 기능 탐색기입니다.
- **인풋 위젯**: 한 줄/장문 텍스트, 숫자, 슬라이더, 라디오, 선택상자, 체크박스, 토글 등
- **레이아웃 & 컨테이너**: 다단 컬럼(`st.columns`), 카드형/스크롤 컨테이너(`st.container`), 아코디언(`st.expander`), 팝오버(`st.popover`), 모달 다이얼로그(`st.dialog`), 사이드바 및 하단 고정(`st.bottom`)
- **데이터 & 차트**: 데이터프레임(`st.dataframe`, `st.data_editor`), 메트릭 카드, 라인/바/영역/산점도 차트 및 지도(`st.map`)
- **텍스트/미디어 & 상태**: 마크다운 서식, 코드, 수식(LaTeX), 이미지/음성/영상, 알림 배너 및 상태 진행률

### 2. 💬 OpenAI 멀티모달 챗봇 & 과거 내역 뷰어 (`app2.py`)
Streamlit의 최신 공식 멀티페이지 네비게이션(`st.navigation`, `st.Page`)을 적용한 대화형 AI 챗봇입니다.
- **최신 프론티어 모델 지원**: `gpt-5.6-luna` (기본), `gpt-5.6-terra`, `gpt-5.6-sol`, `gpt-5.5`, `gpt-6-astra`
- **팝업 드래그앤드롭 첨부**: 이미지 및 문서 파일 업로드 버튼 분리 및 모달 팝업(`@st.dialog`) 지원
- **SQLite 영구 보존**: 모든 대화 내역과 세션은 로컬 SQLite(`chat_history.db`)에 영구 저장
- **과거 내역 뷰어**: 이전 대화 세션별 타임라인 조회, 텍스트 다운로드 및 키워드 검색

---

## 🚀 실행 방법

### 1. 의존성 설치
본 프로젝트는 `uv` 패키지 관리자를 사용합니다.
```bash
uv sync
```

### 2. 환경변수 설정
`.env` 파일에 OpenAI API Key를 설정합니다:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 3. 애플리케이션 실행
- **Streamlit 종합 컴포넌트 탐색기 실행**:
  ```bash
  .\run.bat
  # 또는
  uv run streamlit run app.py
  ```

- **OpenAI 멀티모달 챗봇 실행**:
  ```bash
  .\run2.bat
  # 또는
  uv run streamlit run app2.py
  ```

- **과거 대화 내역 단독 실행**:
  ```bash
  .\run_history.bat
  # 또는
  uv run streamlit run app2_history.py
  ```
