import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
# Set full width layout
st.set_page_config(page_title=" Configuration Page", layout="wide")

# Inject custom CSS for spacing and column borders
st.markdown("""
    <style>
        /* Increase padding to stretch the layout */
        .main > div {
            padding-left: 5rem;
            padding-right: 5rem;
        }

        /* Red Save Button styling */
        div.stButton > button {
            background-color: #cc0000;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }

        /* Border between columns */
        .column-border {
            border-left: 2px solid #d3d3d3;
            padding-left: 2rem;
        }

        /* Optional: add box shadow to sections */
        .config-box {
            background-color: #f9f9f9;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚙️ App Configuration")
st.markdown("Customize your RAG search behavior below:")

# --- Two Columns Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    with st.container():
        st.markdown(
            """
            <div class="config-box column-border">
                <div style="background-color:#e6f0ff; padding:10px; border-radius:10px;">
                    <h4 style="color:#003366;">⚙️ Configure RAG Parameters</h4>
                </div>
            """,
            unsafe_allow_html=True
        )
        top_k = st.slider(
            "🔢 Number of Top Matches to Fetch (top_k)",
            min_value=1,
            max_value=20,
            value=st.session_state.get("top_k_value", 5),
            step=1
        )
        st.markdown("</div>", unsafe_allow_html=True)  # Close config-box
    # Box: Configure RAG Parameters
    with st.container():
        st.markdown(
            """
            <br><div class="config-box column-border">
                <div style="background-color:#e6f0ff; padding:10px; border-radius:10px;">
                    <h4 style="color:#003366;">🧩 Configure LLM Parameters</h4>
                </div>
            """,
            unsafe_allow_html=True
        )
        min_tokens = st.slider(
            "📏 Minimum Tokens in Response",
            min_value=10,
            max_value=500,
            value=st.session_state.get("min_tokens", 50),
            step=10
        )
        max_tokens = st.slider(
            "📐 Maximum Tokens in Response",
            min_value=20,
            max_value=10000,
            value=st.session_state.get("max_tokens", 200),
            step=50
        )
        similarity_threshold = st.slider(
            "🎯 Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.get("similarity_threshold", 0.45),
            step=0.01
        )
        st.markdown("</div>", unsafe_allow_html=True)  # Close config-box
    with st.container():
        st.markdown(
            """
            <br><div class="config-box column-border">
                <div style="background-color:#e6f0ff; padding:10px; border-radius:10px;">
                    <h4 style="color:#003366;">📁 View Database</h4>
                </div><br>
                <p style="font-size:16px;"><strong>🟦 StackOverflow Database Instances:</strong> 10,002</p>
                <p style="font-size:16px;"><strong>🟥 Reddit Database Instances:</strong> 11,536</p>
            </div>
            """,
            unsafe_allow_html=True
        )
            # Create and display Pie Chart
        labels = ['StackOverflow', 'Reddit']
        sizes = [10002, 11536]
        colors = ['#1f77b4', '#d62728']
        explode = (0.05, 0.05)  # slightly explode both for effect

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%',
            shadow=True, startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures pie is circular.

        st.pyplot(fig)
                # Styled button that acts like a hyperlink
        st.markdown(
            """
            <a href="http://localhost:5000/database" target="_blank">
                <button style='font-size: 16px; padding: 8px 16px; background-color:#003366; color:white; border:none; border-radius:6px; cursor:pointer;left-padding:10px;'>📁 View Database</button>
            </a>
            """,
            unsafe_allow_html=True
        )

with col2:
    with st.container():
        st.markdown(
            """
            <div class="config-box column-border">
                <div style="background-color:#e6f0ff; padding:10px; border-radius:10px;">
                    <h4 style="color:#003366;">🧠 Configure Agent Parameters</h4>
                </div>
            """,
            unsafe_allow_html=True
        )
        max_messages = st.slider(
            "💬 Max Messages Per Chat",
            min_value=1,
            max_value=50,
            value=st.session_state.get("max_messages_value", 20),
            step=1
        )
        st.markdown("</div>", unsafe_allow_html=True)  # Close config-box
    with st.container():
        st.markdown(
            """
            <br><div class="config-box column-border">
                <div style="background-color:#e6f0ff; padding:10px; border-radius:10px;">
                    <h4 style="color:#003366;">🤖 Model Configuration</h4>
                </div><br>
                <p style="font-size:16px;"><strong>🔤 Text Embedding Model Used:</strong> all-MiniLM-L6-v2</p>
                <p style="font-size:16px;"><strong>🛜 LLM Used: </strong> Ollama - tinyllama</p>
                <p style="font-size:16px;"><strong>📦 Vector Database:</strong> ChromaDB</p>
                <p style="font-size:16px;"><strong>🕸️ Agentic RAG Framework:</strong> LangGraph</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True) 
with col2:
    # 📊 Database Insights Section
    st.markdown(
        """
        <div class="config-box column-border">
            <div style="background-color:#e6f0ff; padding:10px; border-radius:10px;">
                <h4 style="color:#003366;">📊 Database Insights</h4>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tag Frequency Data
    st.markdown("### 🔖 Top Tags by Source")

    # StackOverflow Tag Counts
    stack_tags = {
        "python": 475,
        "python,oop": 15,
        "python,django": 86,
        "python,file": 21,
        "python,unicode": 6,
        "python,html": 6,
        "python,set": 13,
        "python,xml": 5
    }

    reddit_tags = {
        "python": 552,
        "opencv": 138,
        "computervision": 148,
        "machinelearning": 350
    }

    # StackOverflow Bar Plot
    st.markdown("#### 🟦 StackOverflow Top Tags")
    st.bar_chart(pd.DataFrame.from_dict(stack_tags, orient='index', columns=["Questions"]).sort_values("Questions", ascending=True))

    # Reddit Bar Plot
    st.markdown("#### 🟥 Reddit Top Tags")
    st.bar_chart(pd.DataFrame.from_dict(reddit_tags, orient='index', columns=["Posts"]).sort_values("Posts", ascending=True))
# --- Save Button ---
if st.button("💾 Save Settings"):
    st.session_state.top_k_value = top_k
    st.session_state.max_messages_value = max_messages
    st.session_state.min_tokens = min_tokens
    st.session_state.max_tokens = max_tokens
    st.session_state.similarity_threshold = similarity_threshold
    st.success(f"✅ Saved: top_k = {top_k}, max_messages = {max_messages}, tokens = {min_tokens}-{max_tokens}, threshold = {similarity_threshold}")