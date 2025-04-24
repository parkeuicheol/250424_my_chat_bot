import os
import google.generativeai as genai
import streamlit as st

# ——— 사전에 설정해 둔 유효한 계정 정보(환경변수) ———
VALID_USER_ID = os.getenv("STREAMLIT_USER_ID", "sfteam")
VALID_PASSWORD = os.getenv("STREAMLIT_USER_PW", "css0025248#")

# ——— 로그인 상태 초기화 ———
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ——— 로그인 폼 ———
if not st.session_state.authenticated:
    st.title("⚙️ 로그인 필요")
    with st.form("login_form"):
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if user_id == VALID_USER_ID and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.success("로그인 성공! 챗봇에 접속합니다.")
                # st.experimental_rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
    # 로그인 전에는 여기서 중단
    if not st.session_state.authenticated:
        st.stop()

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY='AIzaSyCjheud_OvTlda5ya7jIEDfOUFl3wbMY10'

genai.configure(api_key=GOOGLE_API_KEY)
st.title("나만의 Chatbot(feat.Gemini)")

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-2.0-flash')
    return model

model = load_model()

if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = model.start_chat(history=[])

for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)
        
if prompt := st.chat_input("질문을 입력하세요."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("ai"):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner("메세지를 생성하는 중입니다..."):
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response)
