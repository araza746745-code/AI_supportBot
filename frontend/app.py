import streamlit as st
import tempfile
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.retrieval.rag_pipeline import build_rag_pipeline

st.set_page_config(
    page_title="DocMind AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 DocMind AI")
st.caption("Your AI-powered PDF assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)

# Reset chat when a different PDF is uploaded
if uploaded_file is not None:
    if st.session_state.pdf_name != uploaded_file.name:
        st.session_state.messages = []
        st.session_state.pdf_bytes = uploaded_file.getvalue()
        st.session_state.pdf_name = uploaded_file.name

if st.session_state.pdf_bytes:
    st.success(f"PDF ready: {st.session_state.pdf_name}")

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and message.get("sources"):
                with st.expander("📚 Source References"):
                    for i, source in enumerate(message["sources"], start=1):
                        st.markdown(f"**Source {i}**")
                        st.write(source["text"])
                        st.caption(
                            f"Similarity score: {source['score']}"
                        )

    # Ask a question
    question = st.chat_input("Ask a question about your PDF...")

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Reading PDF and generating answer..."):
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:
                        temp_file.write(st.session_state.pdf_bytes)
                        pdf_path = temp_file.name

                    try:
                        result = build_rag_pipeline(
                            pdf_path,
                            question
                        )
                    finally:
                        Path(pdf_path).unlink(missing_ok=True)

                # Support the updated answer + sources response
                if isinstance(result, dict):
                    answer = result.get(
                        "answer",
                        "No answer was generated."
                    )
                    sources = result.get("sources", [])
                else:
                    answer = str(result)
                    sources = []

                st.markdown(answer)

                if sources:
                    with st.expander("📚 Source References"):
                        for i, source in enumerate(sources, start=1):
                            st.markdown(f"**Source {i}**")
                            st.write(source["text"])
                            st.caption(
                                f"Similarity score: {source['score']}"
                            )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as error:
                st.error(f"Error: {error}")

else:
    st.info("Please upload a PDF to start chatting.")

if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()