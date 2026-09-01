from transformers import pipeline

# --------------------------------------------------
# SUMMARIZATION MODEL
# --------------------------------------------------

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

print("✅ Summarization Model Loaded Successfully!")


# --------------------------------------------------
# QUESTION ANSWERING MODEL
# --------------------------------------------------

qa_model = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)

print("✅ Question Answering Model Loaded Successfully!")