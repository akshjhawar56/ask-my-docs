from pypdf import PdfReader
r = PdfReader(r"C:\Users\akshj\Downloads\Greenfield_Student_Handbook_2026-27.pdf")
chunks=[]
chunk_size=800
for page_number, page in enumerate(r.pages, start=1):
    text = page.extract_text() or ""
    words = text.split()

    for start in range (0,len(words), chunk_size):
        chunk_words = words[start : start +chunk_size]
        chunks.append({
            "page_number":page_number,
            "text":" ".join(chunk_words),
        })
print(chunks)