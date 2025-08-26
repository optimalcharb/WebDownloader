import os
import pdfplumber
import pymupdf4llm

# Define the root directory
root_dir = r"test"

# Function to sanitize filenames
def sanitize_filename(filename):
    # Replace URL-encoded characters like %20 with spaces and remove invalid characters
    return "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in filename.replace('%20', ' '))

# Function to process a single PDF file
def process_pdf(pdf_path, output_subdir):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    sanitized_base_name = sanitize_filename(base_name)

    # pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        with open(os.path.join(output_subdir, f"{sanitized_base_name}_plumber.txt"), 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Error processing {pdf_path} with pdfplumber: {e}")

    # pymupdf4llm (Markdown)
    try:
        md_text = pymupdf4llm.to_markdown(pdf_path)
        with open(os.path.join(output_subdir, f"{sanitized_base_name}_pymupdf4llm.md"), 'w', encoding='utf-8') as file:
            file.write(md_text)
    except Exception as e:
        print(f"Error processing {pdf_path} with pymupdf4llm: {e}")

# Iterate through all PDF files in the directory
for root, _, files in os.walk(root_dir):
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            print(f"Processing {pdf_path}...")
            process_pdf(pdf_path, root)

print("Processing complete. Extracted files are saved in their respective subdirectories.")