import re


# ================================
# 1. NORMALIZE TEXT
# ================================

def normalize_text(text):

    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# ================================
# 2. REMOVE HEADERS / FOOTERS
# ================================

def remove_headers_footers(text):

    patterns = [
        r'\bMAHABHARATA\b',
        r'\bRAMAYANA\b',
        r'\bPURANA\b',
        r'\bADI PARVA\b',
        r'\bSABHA PARVA\b',
        r'\bCONTO\b',
        r'\bCHAPTER\b',
        r'\bBOOK\b',
        r'\bPAGE\b',

    ]

    for p in patterns:
        text = re.sub(p, '', text, flags=re.IGNORECASE)

    return text


# ================================
# 3. REMOVE PAGE NUMBERS
# ================================

def remove_page_numbers(text):

    text = re.sub(r'\n?\s*\d+\s*\n', ' ', text)

    return text


# ================================
# 4. FIX BROKEN WORDS
# ================================

def fix_broken_words(text):

    text = re.sub(r'-\s+', '', text)

    return text


# ================================
# 5. REMOVE SPECIAL CHARACTERS
# ================================

def remove_special_chars(text):

    text = re.sub(r'[^\w\s\.\,\?\!\'\"]', ' ', text)

    return text


# ================================
# 6. CLEAN OCR NOISE
# ================================

def clean_ocr_noise(text):

    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    text = re.sub(r'\b(?:[a-zA-Z]\s){3,}[a-zA-Z]\b', '', text)

    return text


# ================================
# 7. FILTER SENTENCES
# ================================

def filter_sentences(text):

    sentences = text.split('. ')
    cleaned = []

    for s in sentences:
        if len(s.strip()) > 30:
            cleaned.append(s.strip())

    return ". ".join(cleaned)


# ================================
# 8. MAIN CLEAN FUNCTION
# ================================

def clean_text(text):

    text = normalize_text(text)
    text = remove_headers_footers(text)
    text = remove_page_numbers(text)
    text = fix_broken_words(text)
    text = clean_ocr_noise(text)
    text = remove_special_chars(text)
    text = normalize_text(text)
    text = filter_sentences(text)

    return text.strip()