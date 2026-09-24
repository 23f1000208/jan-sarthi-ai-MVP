"""
Google ADK Root Agent for JAN-SARTHI AI
Orchestrates the entire decision-support lifecycle using modular Python tools.
Strictly separates orchestration (ADK) from deterministic computation (Python)
and qualitative interpretation (Gemini).
"""
import os
from typing import Dict, Any, List, Optional
import pandas as pd
from google.adk import Agent

from .schemas import (
    CitizenFeedback,
    Cluster,
    PriorityScore,
    PolicyBrief,
    SecurityAssessment
)
from .security.prompt_guard import scan_prompt_injection
from .security.pii import redact_pii
from .security.manipulation import detect_manipulation_risk
from .security.validators import validate_policy_output
from .tools.language import detect_language, normalize_text
from .tools.extraction import extract_category_and_severity
from .tools.clustering import BasicClusterEngine
from .tools.evidence import fuse_evidence_packet
from .tools.priority import evaluate_cluster_priority
from .tools.policy import generate_policy_brief_doc


# ---------------------------------------------------------------------------
# ADK Tool Definitions
# ---------------------------------------------------------------------------

def validate_feedback(text: str) -> Dict[str, Any]:
    """Pre-scans input for prompt injection attacks and safety violations."""
    is_inj, pattern = scan_prompt_injection(text)
    return {
        "is_safe": not is_inj,
        "is_prompt_injection": is_inj,
        "matched_pattern": pattern
    }


def process_feedback_intake(
    text: str,
    location_name: str,
    ward_id: str,
    latitude: float,
    longitude: float,
    reported_duration: str = "Unknown",
    recent_submissions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    End-to-end intake processing tool:
    1. Prompt-injection defense
    2. PII redaction
    3. Language detection
    4. Text normalization
    5. Category & severity extraction
    6. Manipulation risk scoring
    """
    # 1. Untrusted Boundary Check
    is_inj, pattern = scan_prompt_injection(text)
    if is_inj:
        return {
            "status": "BLOCKED",
            "security": SecurityAssessment(
                input_text=text,
                is_prompt_injection=True,
                injection_pattern_matched=pattern,
                contains_pii=False,
                sanitized_text="",
                manipulation_risk="HIGH",
                passed_validation=False,
                action_taken="BLOCKED_FOR_REVIEW"
            ).model_dump()
        }
        
    # 2. Privacy-by-design: PII Edge Scrubbing
    sanitized_text, detected_pii = redact_pii(text)
    
    # 3. Multilingual Understanding
    detected_lang = detect_language(sanitized_text)
    normalized = normalize_text(sanitized_text)
    
    # 4. Intent & Severity Extraction
    cat, subcat, sev = extract_category_and_severity(normalized)
    
    # 5. Anti-Astroturfing & Manipulation Check
    recent_texts = recent_submissions or []
    manip_risk, manip_reasons = detect_manipulation_risk(normalized, recent_texts)
    
    # 6. Structured Model Construct
    feedback_id = f"CF-2026-{abs(hash(normalized)) % 100000:05d}"
    feedback = CitizenFeedback(
        id=feedback_id,
        language=detected_lang,
        original_text=text,
        normalized_text=normalized,
        category=cat,
        subcategory=subcat,
        severity=sev,  # type: ignore
        location=location_name,
        latitude=latitude,
        longitude=longitude,
        administrative_region=ward_id,
        duration=reported_duration,
        affected_population_estimate=1000,
        evidence_status="PENDING",
        privacy_status="SANITIZED",
        manipulation_risk=manip_risk,  # type: ignore
        cluster_id=None
    )
    
    sec_assessment = SecurityAssessment(
        input_text=text,
        is_prompt_injection=False,
        contains_pii=len(detected_pii) > 0,
        pii_entities_detected=detected_pii,
        sanitized_text=sanitized_text,
        manipulation_risk=manip_risk,  # type: ignore
        passed_validation=True,
        action_taken="ALLOWED" if len(detected_pii) == 0 else "SANITIZED"
    )
    
    return {
        "status": "ACCEPTED",
        "feedback": feedback.model_dump(),
        "security": sec_assessment.model_dump()
    }


def detect_hotspots(feedback_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Runs spatial-temporal clustering engine across feedback records."""
    df = pd.DataFrame(feedback_records)
    engine = BasicClusterEngine(eps_km=3.0, min_samples=2)
    return engine.fit_predict(df)


def run_evidence_and_priority_pipeline(
    cluster_dict: Dict[str, Any],
    demographics_df: pd.DataFrame,
    infrastructure_df: pd.DataFrame,
    feedback_df: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Fuses evidence and evaluates deterministic Decision-Support Priority Score.
    """
    evidence_packet = fuse_evidence_packet(cluster_dict, demographics_df, infrastructure_df, feedback_df)
    priority_score = evaluate_cluster_priority(cluster_dict, evidence_packet, weights=weights)
    return {
        "evidence_packet": evidence_packet,
        "priority_score": priority_score.model_dump()
    }


def produce_policy_brief(
    evidence_packet: Dict[str, Any],
    priority_score: Dict[str, Any]
) -> Dict[str, Any]:
    """Generates policy brief with Gemini or deterministic demo template."""
    brief, warnings = generate_policy_brief_doc(evidence_packet, priority_score)
    return {
        "policy_brief": brief.model_dump(),
        "validation_warnings": warnings
    }


# ---------------------------------------------------------------------------
# Google ADK Root Agent Specification
# ---------------------------------------------------------------------------

root_agent = Agent(
    name="jan_sarthi_agent",
    description="Multilingual AI Agent for Citizen Feedback Ingestion, Spatial Clustering, and Infrastructure Prioritization.",
    instruction=(
        "You are the Jan-Sarthi GovTech Orchestrator. "
        "Coordinate multilingual citizen feedback analysis, spatial clustering, "
        "evidence fusion, and policy brief generation. "
        "NEVER perform manual arithmetic. Delegate computation to deterministic tools."
    ),
    tools=[
        validate_feedback,
        process_feedback_intake,
        detect_hotspots,
        run_evidence_and_priority_pipeline,
        produce_policy_brief
    ]
)
