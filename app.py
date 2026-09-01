import streamlit as st

from utils import (
    summarize_text,
    read_pdf,
    read_docx,
    answer_question
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Tech Summarizer",
    page_icon="📝",
    layout="wide"
)


# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "file_name" not in st.session_state:
    st.session_state.file_name = ""


# ==================================================
# HEADER
# ==================================================

st.title("📝 AI Tech Summarizer")

st.write(
    "Summarize technical articles, blogs, PDFs and DOCX documents using AI."
)

st.divider()


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Settings")

    summary_type = st.selectbox(
        "Select Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    st.divider()

    st.subheader("📚 Supported Inputs")

    st.write("📝 Text")
    st.write("📄 PDF")
    st.write("📘 DOCX")

    st.divider()

    st.info(
        "Upload a document or paste text, "
        "generate an AI summary, and ask questions "
        "about your document."
    )


# ==================================================
# INPUT TYPE
# ==================================================

st.subheader("📥 Choose Input Type")

option = st.radio(
    "Choose Input Type",
    ["Text", "PDF", "DOCX"],
    horizontal=True
)


# ==================================================
# TEXT INPUT
# ==================================================

if option == "Text":

    text_input = st.text_area(
        "✍️ Paste your technical article or text",
        height=300,
        placeholder="Paste your technical article here..."
    )

    # Store text in session state
    if text_input.strip():

        st.session_state.document_text = text_input

        st.session_state.file_name = "Pasted Text"

    else:

        st.session_state.document_text = ""

        st.session_state.file_name = ""


# ==================================================
# PDF INPUT
# ==================================================

elif option == "PDF":

    pdf = st.file_uploader(
        "📄 Upload your PDF file",
        type=["pdf"]
    )

    if pdf is not None:

        # Check whether a new file was uploaded
        if st.session_state.file_name != pdf.name:

            with st.spinner("📖 Reading PDF..."):

                try:

                    extracted_text = read_pdf(pdf)

                    if extracted_text.strip():

                        st.session_state.document_text = (
                            extracted_text
                        )

                        st.session_state.file_name = (
                            pdf.name
                        )

                        # Clear old summary
                        st.session_state.summary = ""

                        st.success(
                            "✅ PDF successfully loaded!"
                        )

                    else:

                        st.session_state.document_text = ""

                        st.error(
                            "❌ Could not extract text from this PDF."
                        )

                except Exception as e:

                    st.session_state.document_text = ""

                    st.error(
                        f"❌ Error reading PDF: {e}"
                    )

        else:

            st.success(
                "✅ PDF successfully loaded!"
            )


# ==================================================
# DOCX INPUT
# ==================================================

elif option == "DOCX":

    doc = st.file_uploader(
        "📘 Upload your DOCX file",
        type=["docx"]
    )

    if doc is not None:

        # Check whether a new file was uploaded
        if st.session_state.file_name != doc.name:

            with st.spinner("📖 Reading DOCX..."):

                try:

                    extracted_text = read_docx(doc)

                    if extracted_text.strip():

                        st.session_state.document_text = (
                            extracted_text
                        )

                        st.session_state.file_name = (
                            doc.name
                        )

                        # Clear old summary
                        st.session_state.summary = ""

                        st.success(
                            "✅ DOCX successfully loaded!"
                        )

                    else:

                        st.session_state.document_text = ""

                        st.error(
                            "❌ Could not extract text from this DOCX."
                        )

                except Exception as e:

                    st.session_state.document_text = ""

                    st.error(
                        f"❌ Error reading DOCX: {e}"
                    )

        else:

            st.success(
                "✅ DOCX successfully loaded!"
            )


# ==================================================
# DOCUMENT PREVIEW
# ==================================================

if st.session_state.document_text.strip():

    with st.expander("👀 Preview Extracted Text"):

        st.write(
            st.session_state.document_text[:5000]
        )


# ==================================================
# GENERATE SUMMARY
# ==================================================

st.divider()

if st.button(
    "✨ Generate AI Summary",
    use_container_width=True
):

    if not st.session_state.document_text.strip():

        st.warning(
            "⚠️ Please provide text or upload a document first."
        )

    else:

        with st.spinner(
            "🤖 AI is generating your summary..."
        ):

            try:

                summary = summarize_text(
                    st.session_state.document_text,
                    summary_type
                )

                # Save summary
                st.session_state.summary = summary

                st.success(
                    "✅ Summary generated successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Error while generating summary: {e}"
                )


# ==================================================
# SUMMARY DISPLAY
# ==================================================

if st.session_state.summary:

    st.divider()

    st.header("📌 Generated Summary")

    st.success(
        st.session_state.summary
    )

    summary = st.session_state.summary

    document_text = st.session_state.document_text

    # --------------------------------------------------
    # SUMMARY STATISTICS
    # --------------------------------------------------

    st.subheader("📊 Summary Statistics")

    original_words = len(
        document_text.split()
    )

    summary_words = len(
        summary.split()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Original Words",
            original_words
        )

    with col2:

        st.metric(
            "Summary Words",
            summary_words
        )

    with col3:

        if original_words > 0:

            reduction = (
                1 -
                summary_words / original_words
            ) * 100

            st.metric(
                "Text Reduction",
                f"{reduction:.1f}%"
            )

    # --------------------------------------------------
    # DOWNLOAD SUMMARY
    # --------------------------------------------------

    st.download_button(
        label="📥 Download Summary",
        data=summary,
        file_name="AI_Summary.txt",
        mime="text/plain",
        use_container_width=True
    )


# ==================================================
# CHAT WITH DOCUMENT
# ==================================================

if st.session_state.document_text.strip():

    st.divider()

    st.header("💬 Chat with Document")

    st.write(
        "Ask questions about your uploaded document "
        "and get answers using AI."
    )

    # --------------------------------------------------
    # QUESTION INPUT
    # --------------------------------------------------

    question = st.text_input(
        "🔎 Ask a question about your document",
        placeholder=(
            "Example: What is the main topic of this document?"
        )
    )

    # --------------------------------------------------
    # ASK AI BUTTON
    # --------------------------------------------------

    if st.button(
        "🤖 Ask AI",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "⚠️ Please enter a question."
            )

        else:

            with st.spinner(
                "🤖 Searching the document..."
            ):

                try:

                    answer = answer_question(
                        question,
                        st.session_state.document_text
                    )

                    st.subheader("💡 AI Answer")

                    st.success(
                        answer
                    )

                except Exception as e:

                    st.error(
                        f"❌ Error while answering question: {e}"
                    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "AI Tech Summarizer | "
    "Built with Python, Streamlit and Hugging Face Transformers"
)