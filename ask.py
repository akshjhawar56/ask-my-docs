from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai
from pathlib import Path
import os, re
from google.genai import types
r = PdfReader(r"C:\Users\akshj\Downloads\Greenfield_Student_Handbook_2026-27.pdf")
load_dotenv(Path(__file__).with_name(".env"), override =True)
api= os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api)

CHUNK_SIZE = 350

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "have", "has", "had",
    "of", "in", "to", "for", "on", "at", "by", "with", "from",
    "as", "it", "its", "this", "that", "these", "those",
    "i", "me", "my", "we", "our", "you", "your", "he", "she", "they",
    "what", "which", "who", "whom", "when", "where", "why", "how",
    "can", "could", "would", "should", "will",
}

def get_keywords(text):
    words = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return {word for word in words if word not in STOP_WORDS}


chunks = []

for page_number, page in enumerate(r.pages, start=1):
    words = (page.extract_text() or "").split()

    for chunk_number, start in enumerate(range(0, len(words), CHUNK_SIZE), start=1):
        chunk_text = " ".join(words[start : start + CHUNK_SIZE])
        chunks.append({
            "page_number": page_number,
            "chunk_number": chunk_number,
            "text": chunk_text,
        })

question = input("Ask a question about the PDF: ")
question_keywords = get_keywords(question)

if not question_keywords:
    print("Please include some meaningful keywords in your question.")
else:
    scored_chunks = []

    for chunk in chunks:
        chunk_keywords = get_keywords(chunk["text"])
        matched = question_keywords & chunk_keywords

        if matched:
            score = len(matched) / len(question_keywords)
            scored_chunks.append((score, matched, chunk))

    score, matched, best_chunk = max(scored_chunks, key=lambda item: item[0])

    print(
            f"\nBest match: page {best_chunk['page_number']} "
        )
    print(f"Matched keywords: {', '.join(sorted(matched))}")
    #print(f"\n{best_chunk['text']}")
    response = client.interactions.create(
        model = "gemini-3.5-flash",
        input = (
            "Answer only from the text below. If the answer is not there, say not found.\n\n"
            + best_chunk["text"]
            + f"\n\nQuestion: {question}"
        ),
    )
    print(response.output_text)
