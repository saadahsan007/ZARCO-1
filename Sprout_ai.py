import os
import streamlit as st
import google.generativeai as genai
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Superior AI",
    page_icon="🌿",
    layout="wide"
)

# ---------------- SESSION STATES ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "eye_state" not in st.session_state:
    st.session_state.eye_state = "green"

if "is_speaking" not in st.session_state:
    st.session_state.is_speaking = False

# ---------------- STYLING ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #e8f5e9, #d0f0dc, #b9e4c9);
    color: #1b4332;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Robot */
.robot-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.robot-head {
    width: 95px;
    height: 75px;
    border-radius: 18px;
    background: #ffc0cb;  /* Pink Face */
    display: flex;
    justify-content: center;
    align-items: center;
}

.eye-row { display: flex; gap: 20px; }

.eye {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    animation: blink 3s infinite;
    transition: 0.3s ease;
}

.eye-green {
    background-color: #66bb6a;
    box-shadow: 0 0 8px #66bb6a;
}

.eye-red {
    background-color: #ef5350;
    box-shadow: 0 0 8px #ef5350;
}

@keyframes blink {
    0%, 92%, 100% { transform: scaleY(1); }
    95% { transform: scaleY(0.2); }
}

/* Title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 600;
    color: #ffeb3b;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: #0000ff;
}

.credit {
    text-align: center;
    font-size: 14px;
    color: #a5d6a7;
    margin-bottom: 25px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 10px;
    margin-bottom: 10px;
    backdrop-filter: blur(8px);
}

/* Cute AI Human */
.ai-human {
    position: fixed;
    bottom: 40px;
    right: 40px;
    width: 130px;
    animation: floaty 3s ease-in-out infinite;
    z-index: 999;
}

@keyframes floaty {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.talking {
    filter: drop-shadow(0 0 10px #66bb6a);
    animation: talkGlow 0.8s infinite alternate;
}

@keyframes talkGlow {
    from { opacity: 0.8; }
    to { opacity: 1; }
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    eye_class = "eye-green" if st.session_state.eye_state == "green" else "eye-red"

    st.markdown(f"""
    <div class="robot-container">
        <div class="robot-head">
            <div class="eye-row">
                <div class="eye {eye_class}"></div>
                <div class="eye {eye_class}"></div>
            </div>
        </div>
        <h3 style='margin-top:15px;'>Zarco Unit 01</h3>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    model_choice = st.selectbox(
        "Select Model",
        ["gemini-1.5-flash", "gemini-1.5-pro"]
    )

    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.session_state.eye_state = "green"
        st.session_state.is_speaking = False
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>SPROUT AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Calm. Intelligent. Refined.</div>", unsafe_allow_html=True)
st.markdown("<div class='credit'>Developed by <b>Zainab Ahsan</b><br>Presented at <b>Superior Expo 2026</b></div>", unsafe_allow_html=True)

# ---------------- API CONFIG ----------------
API_KEY = os.environ.get("GENAI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- DISPLAY OLD MESSAGES ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
if prompt := st.chat_input("Ask something..."):

    # 🔴 Eyes turn red when user asks
    st.session_state.eye_state = "red"
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # 🟢 AI answering
    st.session_state.eye_state = "green"
    st.session_state.is_speaking = True

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + " ▌")
                    time.sleep(0.01)

            response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ Error: {str(e)}"
            response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.session_state.is_speaking = False

# ---------------- SHOW CUTE AI HUMAN ----------------
if st.session_state.is_speaking:
    st.markdown("""
    <div class="ai-human talking">
        <img src="https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif" width="130">
    </div>
    """, unsafe_allow_html=True)
