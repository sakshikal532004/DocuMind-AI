import streamlit as st
import time
import os
import tempfile

from pdf_processor import extract_text
from embeddings import create_embeddings
from gemini_chat import ask_pdf

from chat_manager import (
    create_chat,
    load_chat,
    save_chat,
    get_all_chats,
    rename_chat,
    delete_chat,
    archive_chat,
    get_archived_chats,
    restore_chat,
    pin_chat,
    unpin_chat
)

# Export PDF
from fpdf import FPDF

# Voice Output
from gtts import gTTS

# Voice Input
from streamlit_mic_recorder import mic_recorder


# ---------------- Config ---------------- #

st.set_page_config(
    page_title="AI PDF Assistant Pro",
    page_icon="🤖",
    layout="wide"
)


# ---------------- Current Chat ---------------- #

if "chat_id" not in st.session_state:

    chats = get_all_chats()

    if chats:

        st.session_state.chat_id = chats[0][0]

    else:

        st.session_state.chat_id = create_chat()

chat_data = load_chat(
    st.session_state.chat_id
)

st.session_state.messages = chat_data["messages"]


# ---------------- Export TXT ---------------- #

def export_txt():

    text = ""

    for msg in st.session_state.messages:

        text += f"{msg['role']}:\n"

        text += msg["content"]

        text += "\n\n"

    return text


# ---------------- Export PDF ---------------- #

def export_pdf():

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )

    for msg in st.session_state.messages:

        text = f"{msg['role']}:\n{msg['content']}"

        # Unsupported characters remove
        text = text.encode(
            "latin-1",
            "replace"
        ).decode(
            "latin-1"
        )

        pdf.multi_cell(
            0,
            10,
            text
        )

        pdf.ln()

    pdf_path = "conversation.pdf"

    pdf.output(pdf_path)

    return pdf_path


# ---------------- Speak Answer ---------------- #

def speak_text(text):

    tts = gTTS(text)

    audio_path = "speech.mp3"

    tts.save(audio_path)

    return audio_path


# ---------------- Voice Input ---------------- #

voice = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    just_once=True
)

if voice:

    st.success(
        "Voice captured successfully!"
    )


# ---------------- Session Variables ---------------- #

if "search_chat" not in st.session_state:

    st.session_state.search_chat = ""

if "theme" not in st.session_state:

    st.session_state.theme = "dark"

if "sources" not in st.session_state:

    st.session_state.sources = []

if "last_audio" not in st.session_state:

    st.session_state.last_audio = None
# ---------------- Professional CSS ---------------- #

st.markdown("""
<style>

.stApp{
background:linear-gradient(
135deg,
#0f172a,
#1e293b,
#312e81,
#581c87
);
background-size:400% 400%;
animation:bg 15s ease infinite;
color:white;
}

@keyframes bg{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

.title{
font-size:55px;
font-weight:bold;
text-align:center;
background:linear-gradient(
90deg,
#60a5fa,
#c084fc
);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.subtitle{
text-align:center;
color:#d1d5db;
font-size:18px;
margin-bottom:25px;
}

[data-testid="stSidebar"]{
background:rgba(17,24,39,.88);
backdrop-filter:blur(25px);
border-right:1px solid rgba(255,255,255,.08);
}

.stButton button{
width:100%;
border-radius:14px;
transition:0.3s;
}

.stButton button:hover{
transform:scale(1.02);
box-shadow:0px 0px 15px rgba(96,165,250,.4);
}

div[data-testid="stChatMessage"]{
background:rgba(255,255,255,.05);
backdrop-filter:blur(15px);
border-radius:20px;
padding:12px;
margin-bottom:15px;
animation:fade .4s ease;
}

@keyframes fade{
from{
opacity:0;
transform:translateY(10px);
}
to{
opacity:1;
transform:translateY(0px);
}
}

.chat-card:hover{
background:rgba(255,255,255,.08);
border-radius:12px;
transition:.3s;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Header ---------------- #

st.markdown("""
<div class="title">
🤖 AI PDF Assistant Pro
</div>

<div class="subtitle">
⚡ Powered by Gemini + Ollama • Memory Enabled • Multi Chat
</div>
""", unsafe_allow_html=True)

# ---------------- Search ---------------- #

search = st.text_input(
    "🔍 Search Chats",
    placeholder="Search previous conversations..."
)

# ---------------- Theme ---------------- #

theme = st.toggle(
    "🌙 Dark Mode",
    value=True
)

# ---------------- Pinned Chats ---------------- #

st.subheader("⭐ Pinned Chats")

chats = get_all_chats()

filtered_chats = []

for chat in chats:

    chat_id = chat[0]
    title = chat[1]

    if search.lower() in title.lower():

        filtered_chats.append(chat)
# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.header("📄 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDF Files",
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("🚀 Process PDFs"):

        if uploaded_files:

            with st.spinner("Processing PDFs..."):

                text = extract_text(uploaded_files)

                create_embeddings(text)

            st.success("✅ PDFs Processed Successfully!")

    st.divider()

    # ---------- Export ---------- #

    st.subheader("📄 Export Conversation")

    txt_data = export_txt()

    st.download_button(
        "⬇ Export TXT",
        txt_data,
        file_name="conversation.txt"
    )

    pdf_file = export_pdf()

    with open(pdf_file, "rb") as f:

        st.download_button(
            "⬇ Export PDF",
            f,
            file_name="conversation.pdf"
        )

    st.divider()

    # ---------- New Chat ---------- #

    if st.button("➕ New Chat"):

        st.session_state.chat_id = create_chat()

        st.rerun()

    if st.button("🗑 Clear Current Chat"):

        st.session_state.messages = []

        chat_data["messages"] = []

        save_chat(
            st.session_state.chat_id,
            chat_data
        )

        st.rerun()

    st.divider()

    # ---------- Recent Chats ---------- #

    st.subheader("💬 Recent Chats")

    chats = get_all_chats()

    for chat_id, title, pinned in chats:

        if search.lower() not in title.lower():

            continue

        col1, col2 = st.columns([6,1])

        with col1:

            icon = "⭐" if pinned else "💬"

            if st.button(
                icon + " " + title,
                key="chat_" + chat_id,
                use_container_width=True
            ):

                st.session_state.chat_id = chat_id

                st.rerun()

        with col2:

            with st.popover("⋮"):

                new_name = st.text_input(
                    "Rename Chat",
                    value=title,
                    key="rename_" + chat_id
                )

                if st.button(
                    "✏ Save Name",
                    key="save_" + chat_id
                ):

                    rename_chat(
                        chat_id,
                        new_name
                    )

                    st.rerun()

                if pinned:

                    if st.button(
                        "📌 Unpin",
                        key="unpin_"+chat_id
                    ):

                        unpin_chat(chat_id)

                        st.rerun()

                else:

                    if st.button(
                        "⭐ Pin",
                        key="pin_"+chat_id
                    ):

                        pin_chat(chat_id)

                        st.rerun()

                if st.button(
                    "📦 Archive",
                    key="archive_" + chat_id
                ):

                    archive_chat(chat_id)

                    st.rerun()

                if st.button(
                    "🗑 Delete",
                    key="delete_" + chat_id
                ):

                    delete_chat(chat_id)

                    st.rerun()

    st.divider()

    # ---------- Archived Chats ---------- #

    with st.expander("📦 Archived Chats"):

        archived = get_archived_chats()

        for chat_id, title in archived:

            col1, col2 = st.columns([5,1])

            with col1:

                st.write("💬", title)

            with col2:

                if st.button(
                    "🔄",
                    key="restore_"+chat_id
                ):

                    restore_chat(chat_id)

                    st.rerun()

# ---------------- Previous Messages ---------------- #

for idx, message in enumerate(st.session_state.messages):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # 🔊 Speak Answer

        if message["role"] == "assistant":

            col1, col2 = st.columns([1,1])

            with col1:

               if st.button(
                  "🔊 Speak",
                   key=f"speak_{idx}"
       ):

                    audio_file = speak_text(
                        message["content"]
                    )

                    st.audio(audio_file)

            with col2:

                st.code(
                    message["content"]
                )


# ---------------- Voice Input ---------------- #

voice_text = ""

if voice:

    try:

        voice_text = voice["text"]

    except:

        voice_text = ""

# ---------------- Chat Input ---------------- #

prompt = st.chat_input(
    "💬 Ask anything from your PDFs..."
)

if voice_text:

    prompt = voice_text

# ---------------- User Prompt ---------------- #

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        # ---------- Memory ---------- #

        history = ""

        for msg in st.session_state.messages[-6:]:

            history += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        # ---------- Thinking ---------- #

        with st.spinner(
            "⚡ AI is thinking..."
        ):

            answer = ask_pdf(
                prompt,
                history
            )

        # ---------- Typing Animation ---------- #

        full_response = ""

        for word in answer.split():

            full_response += word + " "

            placeholder.markdown(
                full_response + "▌"
            )

            time.sleep(
                0.015
            )

        placeholder.markdown(
            full_response
        )

        # ---------- Source Pages ---------- #

        st.info(
            "📚 Answer generated from uploaded PDFs."
        )

    # ---------- Save ---------- #

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

    chat_data["messages"] = (
        st.session_state.messages
    )

    # ---------- Auto Title ---------- #

    if (
        len(chat_data["messages"]) > 0
        and chat_data["title"] == "New Chat"
    ):

        for msg in chat_data["messages"]:

            if msg["role"] == "user":

                chat_data["title"] = (
                    msg["content"][:30]
                )

                break

    save_chat(
        st.session_state.chat_id,
        chat_data
    )

    st.rerun()
# ---------------- Welcome Screen ---------------- #

if len(st.session_state.messages) == 0:

    st.markdown(
    """
    <h2 style='text-align:center'>
    👋 Welcome to AI PDF Assistant Pro
    </h2>

    <p style='text-align:center;color:gray'>
    Upload PDFs and start chatting intelligently
    </p>
    """,
    unsafe_allow_html=True
    )

    col1,col2 = st.columns(2)

    with col1:

        if st.button(
            "📌 Summarize PDF",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "Summarize this document."
            )

    with col2:

        if st.button(
            "📝 Generate MCQs",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "Generate MCQs from this PDF."
            )

    col3,col4 = st.columns(2)

    with col3:

        if st.button(
            "📚 Explain Chapter",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "Explain this chapter in simple words."
            )

    with col4:

        if st.button(
            "💼 Interview Questions",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "Generate interview questions."
            )


# ---------------- Status Cards ---------------- #

st.divider()

c1,c2,c3 = st.columns(3)

with c1:

    st.metric(
        "💬 Chats",
        len(get_all_chats())
    )

with c2:

    st.metric(
        "📄 Messages",
        len(st.session_state.messages)
    )

with c3:

    st.metric(
        "🧠 Memory",
        "Enabled"
    )


# ---------------- Quick Actions ---------------- #

with st.expander(
    "⚡ Quick Actions"
):

    if st.button(
        "📑 Summarize PDF"
    ):

        st.session_state.quick_prompt = (
            "Summarize this PDF."
        )

    if st.button(
        "📝 Generate Quiz"
    ):

        st.session_state.quick_prompt = (
            "Generate MCQs."
        )

    if st.button(
        "📚 Key Points"
    ):

        st.session_state.quick_prompt = (
            "Give key points."
        )

    if st.button(
        "💼 Interview Questions"
    ):

        st.session_state.quick_prompt = (
            "Generate interview questions."
        )


# ---------------- Footer ---------------- #

st.divider()

st.markdown(
"""
<center>

<h4>🤖 AI PDF Assistant Pro</h4>

⚡ Powered by Gemini + Ollama

<br><br>

🧠 Memory Enabled |
📚 Multi PDF Support |
🎤 Voice Input |
📄 Export PDF/TXT |
⭐ Pin Chats |
📦 Archive Chats

<br><br>

Made with ❤️ using Streamlit

</center>
""",
unsafe_allow_html=True
)