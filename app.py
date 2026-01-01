import streamlit as st
from google import genai

# ------------------- LOAD API KEY -------------------
# Streamlit Cloud uses Secrets instead of .env
api_key = st.secrets["GOOGLE_API_KEY"]

# Initialize Gemini Client
client = genai.Client(api_key=api_key)


# ------------------- SYSTEM PROMPT -------------------
SYSTEM_PROMPT = """
You are a friendly Travel Booking & Policy Explainer Bot.

You explain clearly:
- booking steps
- cancellation & refund rules
- documentation requirements
- travel policy guidance
- safe travel tips

Rules:
- Do NOT book or cancel tickets
- Do NOT take payments
- Do NOT ask personal details
- Do NOT provide exact fares

Style:
- Friendly
- Step-by-step
- Easy to understand
"""
# ------------------- PAGE SETTINGS -------------------
st.set_page_config(page_title="TravelBot", page_icon="✈️")

st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:32px;
    font-weight:900;
    color:#0B5345;
}
.sub-title {
    text-align:center;
    color:#555;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">✈️ TravelBot – Smart Travel Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Get help with booking, cancellations, refunds, policies & travel documents</div>', unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.header("📌 Quick Help")
    
    if st.button("Booking Process"):
        st.session_state.auto_question = "Explain travel ticket booking process"
    if st.button("Cancellation Rules"):
        st.session_state.auto_question = "Explain flight cancellation policy"
    if st.button("Refund Policy"):
        st.session_state.auto_question = "Explain refund rules for cancelled tickets"
    if st.button("Travel Documents"):
        st.session_state.auto_question = "What documents are required for international travel?"
    if st.button("General Travel Tips"):
        st.session_state.auto_question = "Give important travel safety & preparation tips"

    st.markdown("---")
    st.markdown("🔐 **No transactions** | ❌ **No personal data**")
    st.markdown("Powered by **Google Gemini**")

# ------------------- CHAT MEMORY -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        ("Bot", "👋 Hello! I'm **TravelBot**. Ask me about booking steps, cancellations, refunds, documents, or travel rules!")
    )

# ------------------- DISPLAY CHAT -------------------
for role, msg in st.session_state.messages:
    with st.chat_message("user" if role == "You" else "assistant"):
        st.write(msg)

# ------------------- CHAT INPUT -------------------
auto_question = st.session_state.get("auto_question", "")
user_input = st.chat_input("Type your question...") or auto_question
st.session_state.auto_question = ""

# ------------------- HANDLE REPLY -------------------
if user_input:
    st.session_state.messages.append(("You", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("✈️ TravelBot is thinking..."):
            try:
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash",
                    contents=[SYSTEM_PROMPT + "\nUser: " + user_input]
                )

                bot_reply = response.text
                st.write(bot_reply)
                st.session_state.messages.append(("Bot", bot_reply))

            except Exception as e:
                st.error(f"Error: {e}")
