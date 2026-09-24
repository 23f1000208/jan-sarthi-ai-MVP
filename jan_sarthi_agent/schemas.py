"""
Pydantic Data Schemas for JAN-SARTHI AI
Enforces strict schema validation across all pipeline layers.
"""
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator


class CitizenFeedback(BaseModel):
    id: str = Field(..., description="Unique feedback identifier (e.g. CF-2026-001)")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    language: str = Field(..., description="Detected or declared input language")
    original_text: str = Field(..., description="Original raw citizen submission preserved immutable")
    normalized_text: str = Field(..., description="Cleaned, normalized, canonical representation")
    category: str = Field(..., description="Infrastructure category")
    subcategory: str = Field(..., description="Granular issue subcategory")
    severity: Literal["Low", "Medium", "High", "Critical"] = Field(default="Medium")
    location: str = Field(..., description="Human-readable ward or landmark name")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    administrative_region: str = Field(..., description="Ward/Block ID, e.g. WARD-01")
    duration: str = Field(default="Unknown", description="Citizen-reported issue duration")
    affected_population_estimate: int = Field(default=0, ge=0)
    evidence_status: Literal["PENDING", "VERIFIED", "REJECTED"] = Field(default="PENDING")
    privacy_status: Literal["RAW", "SANITIZED", "REDACTED"] = Field(default="SANITIZED")
    manipulation_risk: Literal["LOW", "MEDIUM", "HIGH"] = Field(default="LOW")
    cluster_id: Optional[str] = Field(default=None, description="Assigned spatial-temporal cluster")


class DemographicData(BaseModel):
    ward_id: str
    ward_name: str
    zone: str
    total_population: int
    vulnerable_population_pct: float = Field(..., ge=0.0, le=1.0)
    digital_literacy_rate: float = Field(..., ge=0.0, le=1.0)
    connectivity_index: float = Field(..., ge=0.0, le=1.0)
    poverty_rate: float = Field(..., ge=0.0, le=1.0)
    source: str
    date: str
    status: Literal["REAL", "DEMO", "SIMULATED"] = "SIMULATED"


class InfrastructureAsset(BaseModel):
    ward_id: str
    ward_name: str
    category: str
    asset_type: str
    operational_capacity_pct: float = Field(..., ge=0.0, le=100.0)
    deficit_score: float = Field(..., ge=0.0, le=1.0)
    distance_to_nearest_facility_km: float = Field(..., ge=0.0)
    status: Literal["REAL", "DEMO", "SIMULATED"] = "SIMULATED"
    source: str


class Cluster(BaseModel):
    cluster_id: str
    category: str
    title: str
    ward_id: str
    ward_name: str
    centroid_lat: float
    centroid_lon: float
    raw_signal_count: int
    calibrated_demand_score: float
    severity_breakdown: Dict[str, int]
    top_keywords: List[str]
    earliest_signal: str
    latest_signal: str
    manipulation_flag: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    feedback_ids: List[str] = []


class EvidenceRecord(BaseModel):
    ward_id: str
    cluster_id: str
    signal_count: int
    verified_signals: int
    demographic_vulnerability: float
    digital_literacy: float
    infrastructure_gap: float
    nearest_asset_deficit_pct: float
    evidence_strength: Literal["WEAK", "MODERATE", "STRONG", "ROBUST"]
    data_sources: List[str]


class PriorityScore(BaseModel):
    cluster_id: str
    ward_id: str
    ward_name: str
    category: str
    raw_demand_index: float = Field(..., ge=0.0, le=1.0, description="DWI Raw")
    calibrated_demand_index: float = Field(..., ge=0.0, le=1.0, description="DWI Calibrated (Bias Adjusted)")
    demographic_vulnerability_index: float = Field(..., ge=0.0, le=1.0, description="DVI")
    infrastructure_gap_score: float = Field(..., ge=0.0, le=1.0, description="IGS")
    urgency_score: float = Field(..., ge=0.0, le=1.0, description="US")
    economic_benefit_score: float = Field(..., ge=0.0, le=1.0, description="EBS")
    dev_alignment_score: float = Field(..., ge=0.0, le=1.0, description="DAS")
    manipulation_penalty: float = Field(..., ge=0.0, le=1.0, description="MP")
    composite_priority_index: float = Field(..., ge=0.0, le=1.0, description="Final Deterministic MCDA Score")
    rank: int = 1
    calculation_breakdown: Dict[str, float]


class PolicyRecommendation(BaseModel):
    cluster_id: str
    priority_rank: int
    composite_priority_index: float
    recommended_intervention: str
    department_assigned: str
    budgetary_estimate_inr: str
    estimated_timeline: str
    target_beneficiaries: int
    risks_of_inaction: str


class PolicyBrief(BaseModel):
    brief_id: str
    cluster_id: str
    ward_name: str
    generated_at: str
    executive_problem_statement: str
    geographic_bounding: str
    empirical_evidence_base: str
    citizen_signal_summary: str
    infrastructure_gap: str
    vulnerability_context: str
    recommended_capital_intervention: str
    risk_projection: str
    evidence_limitations: str
    human_verification_required: str
    disclaimer: str = "AI-generated decision support. Human verification required. Authorized officials retain final decision responsibility."


class SecurityAssessment(BaseModel):
    input_text: str
    is_prompt_injection: bool = False
    injection_pattern_matched: Optional[str] = None
    contains_pii: bool = False
    pii_entities_detected: List[str] = []
    sanitized_text: str
    manipulation_risk: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    passed_validation: bool = True
    action_taken: Literal["ALLOWED", "SANITIZED", "BLOCKED_FOR_REVIEW"] = "ALLOWED"


class AuditLogEntry(BaseModel):
    log_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    cluster_id: str
    officer_id: str
    action: Literal["CHALLENGE_SCORE", "OVERRIDE_PRIORITY", "VERIFY_EVIDENCE", "ASSIGN_DEPARTMENT", "STATUS_CHANGE"]
    original_value: Any
    updated_value: Any
    justification: str = Field(..., min_length=5, description="Mandatory official justification")
