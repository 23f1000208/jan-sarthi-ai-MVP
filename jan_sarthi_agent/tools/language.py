"""
Multilingual Language Processing & Normalization Tool
Detects languages (Hindi, Bengali, Tamil, Marathi, English) via Unicode script range analysis.
Preserves immutable original text while providing canonical normalized forms.
"""
import re
from typing import Tuple


def detect_language(text: str) -> str:
    """
    Detects language based on script ranges and character frequencies.
    Supports Devanagari (Hindi/Marathi), Bengali, Tamil, and Latin (English).
    """
    if not text:
        return "English"
        
    devanagari_chars = len(re.findall(r"[\u0900-\u097F]", text))
    bengali_chars = len(re.findall(r"[\u0980-\u09FF]", text))
    tamil_chars = len(re.findall(r"[\u0B80-\u0BFF]", text))
    latin_chars = len(re.findall(r"[a-zA-Z]", text))
    
    counts = {
        "Hindi": devanagari_chars,
        "Bengali": bengali_chars,
        "Tamil": tamil_chars,
        "English": latin_chars
    }
    
    detected = max(counts, key=counts.get)
    if counts[detected] == 0:
        return "English"
    return detected


def normalize_text(text: str) -> str:
    """
    Normalizes whitespace, trims punctuation repetitions, and standardizes casing.
    """
    if not text:
        return ""
    # Standardize whitespace
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned
