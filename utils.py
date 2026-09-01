import PyPDF2
from docx import Document
from model import summarizer
from model import summarizer, qa_model


def summarize_text(text, summary_type="Medium"):
    """
    Generate summary using Hugging Face model.
    """

    if not text or len(text.strip()) == 0:
        return "Please enter some text."

    text = text.strip()

    # Limit input size
    text = text[:4000]

    if summary_type == "Short":
        max_length = 80
        min_length = 30

    elif summary_type == "Detailed":
        max_length = 180
        min_length = 70

    else:
        max_length = 130
        min_length = 45

    # Prevent max_length problems for very short text
    if len(text.split()) < 50:
        max_length = min(max_length, 60)
        min_length = min(min_length, 15)

    summary = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )

    return summary[0]["summary_text"]


def read_pdf(file):
    """
    Extract text from PDF.
    """

    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def read_docx(file):
    """
    Extract text from DOCX.
    """

    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"

    return text
# --------------------------------------------------
# CHAT WITH DOCUMENT
# --------------------------------------------------

def answer_question(question, document_text):
    """
    Answer user question using the uploaded document.
    """

    if not question.strip():
        return "Please enter a question."

    if not document_text.strip():
        return "Please upload a document first."

    # Convert text into paragraphs
    paragraphs = [
        p.strip()
        for p in document_text.split("\n")
        if p.strip()
    ]

    if not paragraphs:
        return "No readable text found in the document."

    # --------------------------------------------------
    # FIND RELEVANT PARAGRAPHS
    # --------------------------------------------------

    question_words = set(
        question.lower().split()
    )

    scored_paragraphs = []

    for paragraph in paragraphs:

        paragraph_words = set(
            paragraph.lower().split()
        )

        score = len(
            question_words.intersection(
                paragraph_words
            )
        )

        scored_paragraphs.append(
            (score, paragraph)
        )

    # Sort according to relevance
    scored_paragraphs.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # Select top relevant paragraphs
    selected_paragraphs = [
        item[1]
        for item in scored_paragraphs[:5]
    ]

    context = " ".join(
        selected_paragraphs
    )

    # Limit context size
    context = context[:3000]

    # --------------------------------------------------
    # QUESTION ANSWERING
    # --------------------------------------------------

    try:

        result = qa_model(
            question=question,
            context=context
        )

        answer = result["answer"]
        confidence = result["score"]

        if confidence < 0.10:
            return (
                "I could not find a reliable answer "
                "in the uploaded document."
            )

        return answer

    except Exception as e:

        return f"Error while answering question: {e}"