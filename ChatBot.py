import streamlit as st
import requests
from streamlit_chat import message
from fpdf import FPDF
import datetime
import base64
import re
from pathlib import Path

# --- Utility Functions ---

def strip_html_tags(text):
    """Remove HTML tags and base64 images from a string."""
    clean = re.sub(r'<img[^>]+>', '', text)  # remove <img> tags
    clean = re.sub(r'<[^>]+>', '', clean)    # remove all other HTML tags
    return clean

def get_icon_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f'<img src="data:image/png;base64,{encoded}" width="16" style="vertical-align: middle;" />'

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
def truncate_response(answer, max_tokens):
    words = answer.split()
    if len(words) > max_tokens:
        return " ".join(words[:max_tokens]) + "..."
    return answer
# --- Streamlit Config ---
st.set_page_config(page_title="Tech QA Bot", layout="wide")
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)
# --- Go to Top / Bottom Buttons ---
st.markdown("""
<style>
.scroll-buttons {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.scroll-button {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: #ffffff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    border: 1px solid #ccc;
    text-align: center;
    line-height: 48px;
    font-size: 24px;
    color: #333;
    cursor: pointer;
    transition: all 0.2s ease;
}

.scroll-button:hover {
    background-color: #f0f0f0;
}
</style>

<div class="scroll-buttons">
    <a href="#top"><div class="scroll-button">⬆</div></a>
</div>

<div id="bottom"></div>
""", unsafe_allow_html=True)

# Add invisible anchor to scroll to top
st.markdown('<div id="top"></div>', unsafe_allow_html=True)
# --- Add Logo + Title ---
logo_path = "assets/techqa_logo.png"  # change this to your actual logo file
logo_base64 = get_base64_image(logo_path)

st.markdown(
    f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <img src="data:image/png;base64,{logo_base64}" width="200" height="200" style="margin-right: 20px;" />
        <h1 style="font-size: 60px; margin: 0;">Tech QA Bot</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("💬 Ask Me Python Related Questions")
st.sidebar.markdown("### 🧭 Navigation")
# --- Choose RAG Type ---
rag_type = st.sidebar.radio(
    "🧠 Choose RAG Type",
    ["Plain RAG", "Custom Hybrid RAG","Agentic RAG (LangGraph)"],
    index=0,
    key="rag_type"
)

if rag_type == "Plain RAG":
    api_url = "http://localhost:8000/ask"  # plain_rag.py
elif rag_type=="Custom Hybrid RAG":
    api_url = "http://localhost:8002/ask"  # hybrid_rag_api.py
else:
    api_url = "http://localhost:8001/ask"  # langgraph_api.py    

st.markdown(
    f"<span style='font-size:22px'><strong>🧪 RAG Type Selected:</strong> <code>{rag_type}</code></span>",
    unsafe_allow_html=True
)

st.sidebar.markdown("""
    <a href="http://localhost:5000/database" target="_blank">
        <button style='font-size: 16px; padding: 8px 16px; background-color:#fff; border-color:red;'>📁 View Database</button>
    </a><br><br>
""", unsafe_allow_html=True)

# --- Global Platform Filter ---
platform_filter = st.selectbox(
    "🔎 Choose your preferred platform:",
    ["All", "StackOverflow", "Reddit"],
    index=0,
    key="platform_filter"
)

# Init Chat History
if "history" not in st.session_state:
    st.session_state.history = []

# --- Show Chat History ---
for i, chat in enumerate(st.session_state.history):
    message(chat["user"], is_user=True, key=f"user_{i}")
    message(chat["bot"], key=f"bot_{i}", allow_html=True)

    if "source_data" in chat:
        filtered_sources = [
            src for src in chat["source_data"]
            if platform_filter.lower() == "all" or src["platform"].lower() == platform_filter.lower()
        ]

        if filtered_sources:
            with st.expander("📚 Click to view sources", expanded=False):
                source_html = ""
                for j, src in enumerate(filtered_sources, start=1):
                    badge = "✅ Accepted" if src["accepted"] else "❌ Not Accepted"
                    icon_path = "assets/stack.png" if src["platform"] == "stackoverflow" else "assets/reddit.png"
                    icon_html = get_icon_base64(icon_path)
                    source_line = f"🔗 [**Source {j}**]({src['url']}) | ⭐ Score: {src['score']} | {badge} | {icon_html} {src['platform'].capitalize()}"
                    source_html += f"{source_line}\n\n"

                st.markdown(source_html.strip(), unsafe_allow_html=True)

# --- User Input Section ---
chat_container = st.container()
with chat_container:
    col1, col2 = st.columns([9, 1])
    with col1:
        if st.session_state.get("clear_input", False):
            user_input = st.text_input("Ask your tech question", key="input_box", label_visibility="collapsed", value="")
            st.session_state.clear_input = False
        else:
            user_input = st.text_input("Ask your tech question", key="input_box", label_visibility="collapsed")

    with col2:
        send_button = st.button("➤", use_container_width=True)

# --- Handle User Query ---
if send_button and user_input.strip():
    max_allowed = st.session_state.get("max_messages_value", 20)

    # 🚫 Limit reached: show warning and stop
    if len(st.session_state.history) >= max_allowed:
        st.warning(f"⚠️ You've reached the maximum message limit of {max_allowed}. Please clear the chat to continue.")
    else:
        with st.spinner("🤖 Thinking..."):
            try:
                params = {"q": user_input}
                if platform_filter.lower() != "all":
                    params["source"] = platform_filter.lower()
                # 👉 Add top_k from session_state if available
                if "top_k_value" in st.session_state:
                    params["top_k"] = st.session_state["top_k_value"]
                # ✅ Add min_tokens and max_tokens from session_state
                if "min_tokens" in st.session_state:
                    params["min_tokens"] = st.session_state["min_tokens"]
                if "max_tokens" in st.session_state:
                    params["max_tokens"] = st.session_state["max_tokens"]
                if "similarity_threshold" in st.session_state:
                    params["threshold"] = st.session_state["similarity_threshold"]

                response = requests.get(api_url, params=params)
                result = response.json()
                answer = result.get("answer", "No answer returned.")
                max_tokens = st.session_state.get("max_tokens", 800)
                answer = truncate_response(answer, max_tokens)
                source_urls = result.get("source_urls", [])
                source_scores = result.get("source_scores", [])
                is_accepted_flags = result.get("is_accepted_flags", [])
                source_platforms = result.get("source_platforms", [])

                # Initialize source HTML
                source_html = ""
                seen_urls = set()
                for i, (url, score, accepted, platform) in enumerate(zip(source_urls, source_scores, is_accepted_flags, source_platforms), start=1):
                    if url in seen_urls:
                        continue
                    seen_urls.add(url)

                    badge = "✅ Accepted" if accepted else "❌ Not Accepted"
                    icon_path = "assets/stack.png" if platform == "stackoverflow" else "assets/reddit.png"
                    icon_html = get_icon_base64(icon_path)
                    source_line = f"🔗 [**Source {i}**]({url}) | ⭐ Score: {score} | {badge} | {icon_html} {platform.capitalize()}"
                    source_html += f"{source_line}\n\n"
                # Enforce max_messages limit
                max_allowed = st.session_state.get("max_messages_value", 20)

                # Only allow new input if message limit is not reached
                if len(st.session_state.history) >= max_allowed:
                    st.warning(f"⚠️ You've reached the maximum message limit of {max_allowed}. Please clear the chat to continue.")
                else:
                    # Append user input and bot response
                    st.session_state.history.append({
                        "user": user_input,
                        "bot": answer,
                        "source_data": [  # <-- full source info for later dynamic filtering
                            {"url": url, "score": score, "accepted": accepted, "platform": platform}
                            for url, score, accepted, platform in zip(source_urls, source_scores, is_accepted_flags, source_platforms)
                        ]
                    })

                st.session_state.clear_input = True
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {e}")

# --- Export Buttons ---
st.markdown("---")
col3, col4 = st.columns([1, 1])
with col3:
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        st.rerun()

with col4:
    if st.button("⬇️ Export as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        def remove_unicode(text):
            return text.encode("ascii", "ignore").decode("ascii")

        for chat in st.session_state.history:
            user_text = remove_unicode(chat["user"])
            bot_clean = strip_html_tags(chat["bot"])
            bot_text = remove_unicode(bot_clean)
            pdf.multi_cell(0, 10, f"You: {user_text}")
            pdf.multi_cell(0, 10, f"Bot: {bot_text}")
            pdf.ln()

        pdf_filename = f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(pdf_filename)
        st.success(f"Saved chat as {pdf_filename}")
