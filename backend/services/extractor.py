import re
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract


# ================================
# 1. EXTRACT TEXT FROM PDF
# ================================

def extract_pdf_pages(path):

    reader = PdfReader(path)
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return pages


# ================================
# 2. OCR FOR SCANNED PDF
# ================================

def extract_scanned_pdf(path):

    images = convert_from_path(path)
    pages = []

    for img in images:
        text = pytesseract.image_to_string(img)
        pages.append(text)

    return pages


# ================================
# 3. FILTER UNWANTED PAGES
# ================================

def is_valid_page(text):

    if not text:
        return False

    text_lower = text.lower()

    unwanted_keywords = [
        "contents",
        "table of contents",
        "index",
        "copyright",
        "isbn",
        "author",
        "preface",
        "acknowledgement",
        "introduction",
        "publisher",
        "all rights reserved",
        "glossary",
        "appendix"
    ]

    for word in unwanted_keywords:
        if word in text_lower:
            return False

    # very small pages are usually noise
    if len(text.strip()) < 200:
        return False

    return True


# ================================
# 4. REMOVE TABLE OF CONTENTS
# ================================

def remove_toc(text):

    # remove dotted lines like "Chapter 1 .... 5"
    text = re.sub(r'.*\.\.\.\.\s*\d+', '', text)

    return text


# ================================
# 5. EXTRACT MAIN CONTENT
# ================================

def extract_main_content(text):

    patterns = ["chapter", "parva", "kanda"]

    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return text[match.start():]

    return text


# ================================
# 6. MAIN FUNCTION
# ================================

def extract_text(path):

    try:
        # Step 1: Try normal extraction
        pages = extract_pdf_pages(path)

        # Step 2: Fallback to OCR if needed
        if not pages or len("".join(pages)) < 100:
            print("⚠️ Using OCR extraction...")
            pages = extract_scanned_pdf(path)

        print(f"Total pages: {len(pages)}")

        # Step 3: Page filtering
        pages = [p for p in pages if is_valid_page(p)]
        print(f"Filtered pages: {len(pages)}")

        # Step 4: Combine
        text = "\n".join(pages)

        # Step 5: Remove TOC
        text = remove_toc(text)

        # Step 6: Extract main content
        text = extract_main_content(text)

        return text

    except Exception as e:
        print("Extraction error:", e)
        return ""