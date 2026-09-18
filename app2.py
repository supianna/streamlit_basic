# app2.py - .env 환경변수 기반 Streamlit ASGI 앱 런처
import os
from dotenv import load_dotenv
import streamlit as st

# [1. .env 환경변수 로드]
load_dotenv()

# [2. .env에서 인증 설정 불러와 Streamlit secrets 딕셔너리 구성]
auth_secrets = {
    "auth": {
        "redirect_uri": os.getenv(
            "AUTH_REDIRECT_URI", "http://localhost:8501/oauth2callback"
        ),
        "cookie_secret": os.getenv("AUTH_COOKIE_SECRET", ""),
        "google": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "server_metadata_url": os.getenv(
                "GOOGLE_SERVER_METADATA_URL",
                "https://accounts.google.com/.well-known/openid-configuration",
            ),
        },
    }
}

# [3. st.App에 programmatic secrets 전달하여 초기화]
app = st.App(r"stream_pages\main.py", secrets=auth_secrets)

if __name__ == "__main__":
    app.run()