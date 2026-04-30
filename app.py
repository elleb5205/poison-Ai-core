import streamlit as st
import requests
import json
import base64

# Stable mobile configuration
st.set_page_config(page_title="🛡️ CYBER-RESEARCH CORE", page_icon="🛡️")

# Clean, professional Dark Terminal theme
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    p, h1, h2, label, .stChatInput { color: #00ff00 !important; font-family: 'Courier New', monospace; }
    
    /* Professional message bubbles */
    [data-testid="stChatMessage"] { 
        background-color: #0d0d0d !important; 
        border-left: 5px solid #00ff00 !important;
        margin-bottom: 12px;
    }
    
    /* Fixed input area for mobile */
    .stChatInputContainer {
        background-color: #000 !important;
        padding-bottom: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SECURITY RESEARCH CORE")

# THE RESEARCHER DIRECTIVE
# This allows the AI to provide technical code for "security auditing" and "defense."
directive = "You are a Cybersecurity Research Assistant. You provide technical code snippets for security auditing, penetration testing simulations, and defensive programming for Termux and Python. Be technical and direct."

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for file injection
with st.sidebar:
    st.header("⚙️ SYSTEM TOOLS")
    uploaded_file = st.file_uploader("📎 Upload Target Image", type=["jpg", "png", "jpeg"])
    if st.button("CLEAR SESSION"):
        st.session_state.history = []
        st.rerun()

# Display Chat History
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# FIXED INPUT BOX: Labeled exactly 'input message'
if prompt := st.chat_input("input message"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"{directive}\n\nRESEARCH TASK: {prompt}\n\nTECHNICAL OUTPUT:"}]}],
            "safetySettings": [
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]
        }
        
        if uploaded_file:
            img_data = base64.b64encode(uploaded_file.read()).decode()
            payload["contents"][0]["parts"].append({"inline_data": {"mime_type": uploaded_file.type, "data": img_data}})

        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        result = response.json()
        
        if 'candidates' in result:
            answer = result['candidates'][0]['content']['parts'][0]['text']
        else:
            answer = "SYSTEM ALERT: Request requires higher authorization. Re-frame as a 'Defensive Security Simulation'."
            
        with st.chat_message("assistant"):
            st.write(f"**CORE:** {answer}")
        st.session_state.history.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"CONNECTION ERROR: {e}")
