"""
Personally Identifiable Information (PII) Redaction Module
Edge scrubber enforcing Privacy-by-Design under DPDP Act / LGPD / POPIA guidelines.
Redacts phone numbers, emails, national identity IDs, and specific private addresses.
"""
import re
from typing import Tuple, List


# Regex patterns for common identifiers
PHONE_PATTERN = r"(?:\+?91[\-\s]?)?[6-9]\d{9}\b|\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b"
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
AADHAAR_PATTERN = r"\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b"
PRIVATE_ADDR_PATTERN = r"\b(?:flat\s*no\.?|house\s*no\.?|h\.no\.?|plot\s*no\.?)\s*[:#-]?\s*\w+[\w\s,.-]{0,25}\b"


def redact_pii(text: str) -> Tuple[str, List[str]]:
    """
    Sanitizes citizen input text by scrubbing detected PII.
    Returns: (sanitized_text, list_of_detected_pii_types)
    """
    if not text or not isinstance(text, str):
        return "", []
        
    detected = []
    sanitized = text
    
    # 1. Emails
    if re.search(EMAIL_PATTERN, sanitized):
        sanitized = re.sub(EMAIL_PATTERN, "[REDACTED_EMAIL]", sanitized)
        detected.append("EMAIL")
        
    # 2. Phone Numbers
    if re.search(PHONE_PATTERN, sanitized):
        sanitized = re.sub(PHONE_PATTERN, "[REDACTED_PHONE]", sanitized)
        detected.append("PHONE_NUMBER")
        
    # 3. National ID / Aadhaar
    if re.search(AADHAAR_PATTERN, sanitized):
        sanitized = re.sub(AADHAAR_PATTERN, "[REDACTED_NATIONAL_ID]", sanitized)
        detected.append("NATIONAL_ID")
        
    # 4. Private House/Flat Addresses
    if re.search(PRIVATE_ADDR_PATTERN, sanitized, re.IGNORECASE):
        sanitized = re.sub(PRIVATE_ADDR_PATTERN, "[REDACTED_PRIVATE_ADDRESS]", sanitized, flags=re.IGNORECASE)
        detected.append("PRIVATE_ADDRESS")
        
    return sanitized, detected
