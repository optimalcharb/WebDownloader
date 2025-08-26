import os
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
import pymupdf4llm

# Define input and output directories
pdf_dir = r"PDFs"
output_dir = r"TXTs"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to process a single PDF file
def process_pdf(pdf_path, output_subdir):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # PyPDF2
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        with open(os.path.join(output_subdir, f"{base_name}_pypdf2.txt"), 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Error processing {pdf_path} with PyPDF2: {e}")

    # pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        with open(os.path.join(output_subdir, f"{base_name}_plumber.txt"), 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Error processing {pdf_path} with pdfplumber: {e}")

    # PyMuPDF
    try:
        with fitz.open(pdf_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
        with open(os.path.join(output_subdir, f"{base_name}_fitz.txt"), 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Error processing {pdf_path} with PyMuPDF: {e}")

    # pymupdf4llm (Markdown)
    try:
        md_text = pymupdf4llm.to_markdown(pdf_path)
        with open(os.path.join(output_subdir, f"{base_name}_pymupdf4llm.md"), 'w', encoding='utf-8') as file:
            file.write(md_text)
    except Exception as e:
        print(f"Error processing {pdf_path} with pymupdf4llm: {e}")

# Iterate through all PDF files in the directory, limiting to 3 per subfolder
for root, _, files in os.walk(pdf_dir):
    pdf_count = 0
    relative_path = os.path.relpath(root, pdf_dir)
    output_subdir = os.path.join(output_dir, relative_path)
    os.makedirs(output_subdir, exist_ok=True)
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            print(f"Processing {pdf_path}...")
            process_pdf(pdf_path, output_subdir)
            pdf_count += 1
            if pdf_count >= 3:  # Limit to 3 PDFs per subfolder
                break

print(f"Processing complete. Extracted files are saved in {output_dir}.")