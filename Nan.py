import os
import re
from docx import Document
from nltk.corpus import stopwords
import nltk
import mammoth
import html2text

# Make sure you download stopwords once
nltk.download('stopwords')

# -------------------------------
# Step 1: Load DOCX File
# -------------------------------
def load_docx(path):
    return Document(path)

# -------------------------------
# Step 2: Extract Images
# -------------------------------
def extract_images(doc, output_folder="images"):
    os.makedirs(output_folder, exist_ok=True)
    img_count = 0
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            img_count += 1
            img = rel.target_part.blob
            with open(os.path.join(output_folder, f"image_{img_count}.png"), "wb") as f:
                f.write(img)
    print(f"[INFO] Extracted {img_count} images")

# -------------------------------
# Step 3: Extract Text (including tables/textboxes)
# -------------------------------
def extract_text(doc):
    full_text = []
    
    # paragraphs
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    # tables
    for table in doc.tables:
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text.strip())
            full_text.append(" | ".join(row_data))
    
    return "\n".join(full_text)

# -------------------------------
# Step 4: Remove Unwanted Information
# Example: remove references, emails, numbers
# -------------------------------
def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)       # remove [1], [2] like references
    text = re.sub(r'\S+@\S+', '', text)       # remove emails
    text = re.sub(r'\d+', '', text)           # remove numbers
    return text

# -------------------------------
# Step 5: Simplify Nested Tables
# (already flattened in extract_text)
# -------------------------------
# Just return as plain text

# -------------------------------
# Step 6: Stop Word Removal
# -------------------------------
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered = [w for w in words if w.lower() not in stop_words]
    return " ".join(filtered)

# -------------------------------
# Step 7: DOCX → HTML
# -------------------------------
def docx_to_html(path):
    with open(path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value

# -------------------------------
# Step 8: HTML → Markdown
# -------------------------------
def html_to_markdown(html):
    return html2text.html2text(html)

# -------------------------------
# Main Pipeline
# -------------------------------
def process_docx(path):
    doc = load_docx(path)

    # Step 2: Extract images
    extract_images(doc)

    # Step 3-6: Extract + Clean + Stopwords
    raw_text = extract_text(doc)
    cleaned = clean_text(raw_text)
    final_text = remove_stopwords(cleaned)

    print("\n[INFO] Cleaned Text Preview:\n", final_text[:500])

    # Step 7: Convert to HTML
    html = docx_to_html(path)

    # Step 8: Convert HTML to Markdown
    markdown = html_to_markdown(html)

    with open("output.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print("\n[INFO] Markdown file created: output.md")

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    process_docx("input.docx")
