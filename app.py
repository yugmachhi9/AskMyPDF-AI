import streamlit as st
import os
import tempfile
import hashlib
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="DocMind",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #f8f9fb !important;
    color: #1a1a2e !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 2rem 2rem !important; max-width: 860px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #1a1a2e !important;
    border-right: none !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }

.sb-logo {
    padding: 2rem 1.5rem 1.5rem;
    border-bottom: 1px solid #2a2a45;
}
.sb-logo-text {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff !important;
    letter-spacing: -0.3px;
}
.sb-logo-text span { color: #7c6af7 !important; }
.sb-logo-sub {
    font-size: 0.68rem;
    color: #5a5a7a !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4px;
}

.sb-section { padding: 1.2rem 1.5rem 0; }
.sb-label {
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #5a5a7a !important;
    margin-bottom: 0.6rem;
    display: block;
}

.status-dot {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 6px 12px;
    border-radius: 20px;
    margin-bottom: 1.2rem;
    margin-left: 1.5rem;
    margin-top: 0.8rem;
}
.status-on  { background: rgba(52,199,89,.12); color: #34c759 !important; border: 1px solid rgba(52,199,89,.25); }
.status-off { background: rgba(90,90,122,.12); color: #5a5a7a !important; border: 1px solid #2a2a45; }

.doc-pill {
    background: #252540;
    border: 1px solid #2e2e50;
    border-radius: 8px;
    padding: 10px 12px;
    margin: 0 1.5rem 1rem;
}
.doc-pill-name { font-size: 0.8rem; font-weight: 600; color: #e8e8f0 !important; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.doc-pill-meta { font-size: 0.68rem; color: #5a5a7a !important; margin-top: 2px; }
.doc-pill-meta b { color: #7c6af7 !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: #252540 !important;
    border: 1.5px dashed #3a3a60 !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"]:hover { border-color: #7c6af7 !important; }
[data-testid="stFileUploader"] * { color: #9898b8 !important; }
[data-testid="stFileUploader"] svg { color: #5a5a7a !important; }

/* Buttons */
.stButton button {
    background: #7c6af7 !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1rem !important;
    letter-spacing: 0.01em !important;
    transition: background .15s, box-shadow .15s !important;
    box-shadow: 0 1px 8px rgba(124,106,247,.3) !important;
}
.stButton button:hover {
    background: #6a58e0 !important;
    box-shadow: 0 2px 14px rgba(124,106,247,.45) !important;
}

.ghost button {
    background: transparent !important;
    color: #5a5a7a !important;
    border: 1px solid #2a2a45 !important;
    box-shadow: none !important;
    font-size: 0.75rem !important;
}
.ghost button:hover { color: #9898b8 !important; border-color: #3a3a60 !important; box-shadow: none !important; }

/* Chat window */
.chat-window {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 16px;
    padding: 1.5rem;
    min-height: 0;
    max-height: 540px;
    overflow-y: auto;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
}

.empty {
    display: flex; flex-direction: column;
    align-items: center;
    padding: 1.5rem 1rem;
    text-align: center;
}

/* Steps */
.steps {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
    max-width: 480px;
    text-align: left;
}
.step {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    background: #f7f8fc;
    border: 1px solid #e8eaf0;
    border-radius: 12px;
    padding: 14px 16px;
}
.step-num {
    width: 28px; height: 28px; flex-shrink: 0;
    background: #7c6af7;
    color: #fff;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin-top: 1px;
}
.step-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 3px;
}
.step-desc {
    font-size: 0.75rem;
    color: #888;
    line-height: 1.5;
}

/* Messages */
.msgs { display: flex; flex-direction: column; gap: 1.1rem; }

.row-user { display: flex; justify-content: flex-end; }
.row-ai   { display: flex; justify-content: flex-start; gap: 10px; align-items: flex-start; }

.ai-av {
    width: 30px; height: 30px; flex-shrink: 0;
    background: #f0eeff; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; margin-top: 2px;
}

.bubble-user {
    background: #7c6af7;
    color: #fff;
    padding: 10px 14px;
    border-radius: 14px 14px 4px 14px;
    font-size: 0.875rem;
    line-height: 1.6;
    max-width: 75%;
}
.bubble-ai {
    background: #f7f8fc;
    color: #1a1a2e;
    padding: 10px 14px;
    border-radius: 4px 14px 14px 14px;
    font-size: 0.875rem;
    line-height: 1.6;
    max-width: 78%;
    border: 1px solid #e8eaf0;
}

/* Input bar — chat_input */
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1.5px solid #e0e2ee !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 3px rgba(124,106,247,.1) !important;
}
[data-testid="stChatInput"] textarea {
    color: #1a1a2e !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #bbb !important; }
[data-testid="stChatInputSubmitButton"] button {
    background: #7c6af7 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

.bubble-ai-wrap { display: flex; flex-direction: column; align-items: flex-start; max-width: 78%; }

.copy-btn {
    margin-top: 5px;
    background: none;
    border: 1px solid #e0e2ee;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.7rem;
    font-family: 'Inter', sans-serif;
    color: #888;
    cursor: pointer;
    transition: all .15s;
    align-self: flex-end;
}
.copy-btn:hover { background: #f0eeff; border-color: #7c6af7; color: #7c6af7; }
.copy-btn.copied { background: #f0fff4; border-color: #34c759; color: #34c759; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #e0e2ee; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ── Cached functions ──────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings()


@st.cache_resource(show_spinner=False)
def build_vectorstore(_pdf_bytes: bytes, file_hash: str):
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(_pdf_bytes)
        tmp_path = tmp.name
    try:
        loader  = PyPDFLoader(tmp_path)
        docs    = loader.load()
        chunks  = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(docs)
        vs      = Chroma.from_documents(
            documents=chunks,
            embedding=load_embedding_model(),
            persist_directory=f"chroma_{file_hash[:8]}",
        )
        return vs, len(docs), len(chunks)
    finally:
        os.unlink(tmp_path)


@st.cache_resource(show_spinner=False)
def get_llm():
    from langchain_mistralai import ChatMistralAI
    return ChatMistralAI(model="mistral-small-latest")


def ask(query: str, vectorstore):
    from langchain_core.prompts import ChatPromptTemplate
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5},
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the user's question using only the provided context. If the answer is not in the context, say: not found in the context."),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])
    docs     = retriever.invoke(query)
    context  = "\n".join([d.page_content for d in docs])
    response = get_llm().invoke(prompt.invoke({"context": context, "question": query}))
    return response.content


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {"vectorstore": None, "chat": [], "pdf_info": {}, "fhash": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ═══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-text">Doc<span>Mind</span></div>
        <div class="sb-logo-sub">AI Document Chat</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.vectorstore:
        st.markdown('<div class="status-dot status-on">● Ready</div>', unsafe_allow_html=True)
        info = st.session_state.pdf_info
        st.markdown(f"""
        <div class="doc-pill">
            <div class="doc-pill-name">📄 {info.get('name','')}</div>
            <div class="doc-pill-meta"><b>{info.get('pages','')}p</b> · <b>{info.get('chunks','')}</b> chunks</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-dot status-off">○ No document</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section"><span class="sb-label">Upload PDF</span></div>', unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='padding: 0 1.5rem'>", unsafe_allow_html=True)
        uploaded = st.file_uploader("pdf", type=["pdf"], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='padding: 0.6rem 1.5rem 0'>", unsafe_allow_html=True)
    if uploaded:
        if st.button("Process PDF", use_container_width=True):
            pdf_bytes = uploaded.read()
            fhash     = hashlib.md5(pdf_bytes).hexdigest()
            with st.spinner("Indexing…"):
                try:
                    vs, pages, chunks = build_vectorstore(pdf_bytes, fhash)
                    st.session_state.vectorstore = vs
                    st.session_state.fhash       = fhash
                    st.session_state.pdf_info    = {"name": uploaded.name, "pages": pages, "chunks": chunks}
                    st.session_state.chat        = []
                    st.success("Done!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 1.4rem 1.5rem 0'><div style='height:1px;background:#2a2a45'></div></div>", unsafe_allow_html=True)
    st.markdown("<div style='padding: 0.8rem 1.5rem 0'>", unsafe_allow_html=True)
    st.markdown('<div class="ghost">', unsafe_allow_html=True)
    if st.button("Clear chat", use_container_width=True):
        st.session_state.chat = []
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════
# Chat window
st.markdown('<div class="chat-window">', unsafe_allow_html=True)

if not st.session_state.chat:
    st.markdown("""
    <div class="empty">
        <div style="margin-bottom:1.2rem">
            <div style="font-size:1.1rem;font-weight:700;color:#1a1a2e;margin-bottom:2px">Hello Buddie! 💻</div>
            <div style="font-size:0.78rem;color:#aaa">Follow these steps to get started</div>
        </div>
        <div class="steps">
            <div class="step">
                <div class="step-num">1</div>
                <div class="step-body">
                    <div class="step-title">Upload your PDF 📄</div>
                    <div class="step-desc">Click the file uploader in the left sidebar and select any PDF document.</div>
                </div>
            </div>
            <div class="step">
                <div class="step-num">2</div>
                <div class="step-body">
                    <div class="step-title">Process & Index ⚡</div>
                    <div class="step-desc">Hit <b>Process PDF</b> — the document will be chunked and embedded into the vector store.</div>
                </div>
            </div>
            <div class="step">
                <div class="step-num">3</div>
                <div class="step-body">
                    <div class="step-title">Ask anything 💬</div>
                    <div class="step-desc">Type your question below and get instant answers from your document.</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="msgs">', unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.chat):
        if msg["role"] == "user":
            st.markdown(f'<div class="row-user"><div class="bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            safe = msg["content"].replace("`", "&#96;").replace("\\", "\\\\").replace("\n", "\\n").replace("\"", "&quot;")
            st.markdown(f"""
            <div class="row-ai">
                <div class="ai-av">🤖</div>
                <div class="bubble-ai-wrap">
                    <div class="bubble-ai" id="ans-{i}">{msg["content"]}</div>
                    <button class="copy-btn" onclick="
                        const txt = document.getElementById('ans-{i}').innerText;
                        navigator.clipboard.writeText(txt).then(() => {{
                            this.innerText = '✓ Copied';
                            this.classList.add('copied');
                            setTimeout(() => {{ this.innerText = '⧉ Copy'; this.classList.remove('copied'); }}, 2000);
                        }});
                    ">⧉ Copy</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input — chat_input clears itself after every submission
query = st.chat_input("Ask anything about your document…")

if query and query.strip():
    if not st.session_state.vectorstore:
        st.warning("Please upload and process a PDF first.")
    else:
        st.session_state.chat.append({"role": "user", "content": query.strip()})
        with st.spinner("Thinking…"):
            try:
                answer = ask(query.strip(), st.session_state.vectorstore)
                st.session_state.chat.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.session_state.chat.append({"role": "assistant", "content": f"Error: {e}"})
        st.rerun()