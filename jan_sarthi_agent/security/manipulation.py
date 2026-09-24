"""
Anti-Astroturfing & Sybil Manipulation Risk Engine
Detects coordinated artificial feedback surges, duplicate complaints,
and anomalous temporal submission velocities.
"""
from typing import Dict, Any, List, Tuple
from collections import Counter
import re


def calculate_lexical_similarity(s1: str, s2: str) -> float:
    """Computes Jaccard word-level similarity between two texts."""
    w1 = set(re.findall(r"\w+", s1.lower()))
    w2 = set(re.findall(r"\w+", s2.lower()))
    if not w1 or not w2:
        return 0.0
    intersection = len(w1.intersection(w2))
    union = len(w1.union(w2))
    return float(intersection) / float(union)


def detect_manipulation_risk(
    text: str,
    recent_texts: List[str],
    rapid_velocity_count: int = 1
) -> Tuple[str, List[str]]:
    """
    Evaluates manipulation risk for incoming feedback.
    Returns: (risk_level: 'LOW' | 'MEDIUM' | 'HIGH', reasons: List[str])
    """
    reasons = []
    
    # 1. Exact Duplicate Check
    clean_curr = text.strip().lower()
    exact_matches = sum(1 for t in recent_texts if t.strip().lower() == clean_curr)
    if exact_matches >= 3:
        reasons.append(f"Found {exact_matches} exact duplicate submissions in recent window")
        
    # 2. Near-duplicate / Templated Submissions
    high_sim_count = sum(1 for t in recent_texts if calculate_lexical_similarity(clean_curr, t) >= 0.85)
    if high_sim_count >= 4:
        reasons.append(f"Identified {high_sim_count} highly similar templated submissions")
        
    # 3. High-velocity burst check
    if rapid_velocity_count >= 5:
        reasons.append(f"Abnormal submission velocity: {rapid_velocity_count} inputs within 15 minutes")
        
    # Risk categorization
    if len(reasons) >= 2 or exact_matches >= 5 or rapid_velocity_count >= 6:
        return "HIGH", reasons
    elif len(reasons) == 1 or exact_matches >= 2 or high_sim_count >= 2:
        return "MEDIUM", reasons
    else:
        return "LOW", ["Normal baseline citizen submission"]
