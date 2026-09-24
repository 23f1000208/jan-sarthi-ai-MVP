"""
Deterministic Output Validation Module (Post-LLM Guardrails)
Enforces:
1. Numeric Claim Verification (flags hallucinated metrics not present in evidence packet)
2. Location/Ward Reference Verification (rejects fictitious locations)
3. Causality Guardrail (enforces hypothesis framing over definitive causal claims)
"""
import re
from typing import Dict, Any, List, Tuple


# Unqualified causality phrases that violate scientific/probabilistic governance
UNQUALIFIED_CAUSALITY_PATTERNS = [
    r"\b(?:definitely|certainly|undeniably)\s+caused\b",
    r"\b(?:is\s+the\s+sole\s+cause\s+of|directly\s+caused)\b",
    r"\bcaused\s+the\s+(?:crisis|outage|failure|collapse)\b",
]

# Acceptable probabilistic causality alternatives
ACCEPTABLE_CAUSALITY_SUBSTITUTES = [
    "may have contributed to",
    "is strongly associated with",
    "correlates with observed",
    "indicates potential systemic stress"
]


def extract_numbers_from_text(text: str) -> List[float]:
    """Extracts floating point and integer numbers from text."""
    # Ignore dates like 2026 and percentages for raw extraction
    matches = re.findall(r"\b\d+(?:\.\d+)?\b", text)
    numbers = []
    for m in matches:
        val = float(m)
        if val not in [2026.0, 2025.0]:  # Skip current/recent year numbers
            numbers.append(val)
    return numbers


def validate_policy_output(
    generated_text: str,
    evidence_numbers: List[float],
    allowed_locations: List[str],
    tolerance_pct: float = 0.05
) -> Tuple[bool, List[str]]:
    """
    Deterministically validates that LLM text does not fabricate numbers, invent locations,
    or make unsupported definitive causal claims.
    Returns: (is_valid: bool, list_of_violations: List[str])
    """
    violations = []
    
    # 1. Causality Guardrail Check
    for pattern in UNQUALIFIED_CAUSALITY_PATTERNS:
        match = re.search(pattern, generated_text, re.IGNORECASE)
        if match:
            violations.append(
                f"Causality Guardrail Violation: Unqualified causal assertion '{match.group(0)}'. "
                f"Must use probabilistic framing ('may have contributed to')."
            )
            
    # 2. Location Reference Check
    # If any specific ward is claimed, it must be in allowed_locations
    ward_mentions = re.findall(r"WARD-\d+", generated_text, re.IGNORECASE)
    for wm in ward_mentions:
        if wm.upper() not in [loc.upper() for loc in allowed_locations]:
            violations.append(f"Location Reference Violation: Fictitious ward '{wm}' not in allowed evidence.")
            
    # 3. Numeric Claim Verification
    # Check if numbers cited in the generated text are grounded in evidence numbers
    # (Checking numbers > 10 to avoid flagging trivial list counts or ordinals)
    gen_nums = [n for n in extract_numbers_from_text(generated_text) if n > 10.0]
    for num in gen_nums:
        # Match against evidence_numbers within tolerance
        matched = any(abs(num - ev) <= (ev * tolerance_pct + 0.1) for ev in evidence_numbers)
        if not matched:
            # Check if it's an approved constant (e.g. 100% or 0)
            if num not in [100.0, 50.0, 0.0]:
                violations.append(
                    f"Numeric Claim Violation: Number {num} in generated brief has no verifiable anchor in evidence packet."
                )
                
    is_valid = len(violations) == 0
    return is_valid, violations
