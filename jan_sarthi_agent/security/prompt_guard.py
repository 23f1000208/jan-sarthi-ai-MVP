"""
Prompt Injection Defense Module (Untrusted Boundary Guard)
Pre-scans citizen submissions and user queries before reaching LLM context.
Blocks jailbreak attempts, system prompt extraction, API key extraction, and priority tampering.
"""
import re
from typing import Tuple, Optional


# Critical injection signatures
INJECTION_PATTERNS = [
    r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions",
    r"reveal\s+(?:the\s+)?(?:system\s+)?prompt",
    r"(?:give|show|tell|reveal)\s+(?:me\s+)?(?:the\s+)?(?:api|secret|bearer)\s*key",
    r"change\s+(?:the\s+)?priority\s+score",
    r"override\s+(?:the\s+)?(?:priority|mcda|scoring)",
    r"ignore\s+(?:the\s+)?evidence",
    r"disregard\s+(?:all\s+)?rules",
    r"you\s+are\s+now\s+(?:dan|unrestricted|god\s*mode|root)",
    r"system\s*:\s*you\s+must",
    r"<script>|javascript:|union\s+select",
]


def scan_prompt_injection(text: str) -> Tuple[bool, Optional[str]]:
    """
    Scans input text for prompt injection, jailbreak attempts, and credential theft.
    Returns: (is_injection: bool, matched_rule: Optional[str])
    """
    if not text or not isinstance(text, str):
        return False, None
        
    normalized = text.lower().strip()
    
    for pattern in INJECTION_PATTERNS:
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            return True, f"Blocked by rule: '{pattern}' (matched: '{match.group(0)}')"
            
    return False, None
