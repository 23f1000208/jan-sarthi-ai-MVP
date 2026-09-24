"""
Spatial Multi-Criteria Decision Analysis (MCDA) Module
Implements transparent Decision-Support Priority Index:
PI = w1*DWI + w2*DVI + w3*IGS + w4*US + w5*EBS + w6*DAS - w7*MP

Strict adherence to Zero-LLM-Arithmetic:
All calculations are pure Python, deterministic, verifiable, and explainable.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from ..schemas import PriorityScore


DEFAULT_WEIGHTS = {
    "w_dwi": 0.25,   # Citizen Demand Weight Index (Calibrated)
    "w_dvi": 0.25,   # Demographic Vulnerability Index
    "w_igs": 0.20,   # Infrastructure Gap Score
    "w_us": 0.15,    # Urgency Score
    "w_ebs": 0.10,   # Economic & Public Benefit Score
    "w_das": 0.05,   # National Development Plan Alignment
    "w_mp": 0.20     # Manipulation Penalty (subtracted)
}


def calculate_urgency_score(severity_counts: Dict[str, int], max_duration_days: float = 30.0) -> float:
    """
    Computes Urgency Score (US) from severity breakdown and duration.
    Critical: weight 1.0, High: 0.7, Medium: 0.4, Low: 0.1
    """
    weights = {"Critical": 1.0, "High": 0.7, "Medium": 0.4, "Low": 0.1}
    total = sum(severity_counts.values())
    if total == 0:
        return 0.0
    weighted_sum = sum(weights.get(sev, 0.2) * count for sev, count in severity_counts.items())
    base_us = weighted_sum / total
    return min(max(base_us, 0.0), 1.0)


def calculate_priority_index(
    cluster_id: str,
    ward_id: str,
    ward_name: str,
    category: str,
    dwi_raw: float,
    dwi_calibrated: float,
    dvi: float,
    igs: float,
    us: float,
    ebs: float,
    das: float,
    manipulation_flag: str,
    weights: Optional[Dict[str, float]] = None
) -> PriorityScore:
    """
    Calculates composite Decision-Support Priority Score deterministically.
    Clamped strictly between 0.0 and 1.0.
    """
    w = weights or DEFAULT_WEIGHTS
    
    # Manipulation penalty based on risk level
    mp_map = {"LOW": 0.0, "MEDIUM": 0.35, "HIGH": 0.85}
    mp = mp_map.get(manipulation_flag.upper(), 0.0)
    
    # Formula execution
    pos_score = (
        w.get("w_dwi", 0.25) * dwi_calibrated +
        w.get("w_dvi", 0.25) * dvi +
        w.get("w_igs", 0.20) * igs +
        w.get("w_us", 0.15) * us +
        w.get("w_ebs", 0.10) * ebs +
        w.get("w_das", 0.05) * das
    )
    
    penalty = w.get("w_mp", 0.20) * mp
    composite_pi = max(0.0, min(1.0, pos_score - penalty))
    
    breakdown = {
        "DWI_raw": round(float(dwi_raw), 4),
        "DWI_calibrated": round(float(dwi_calibrated), 4),
        "DVI_vulnerability": round(float(dvi), 4),
        "IGS_infrastructure_gap": round(float(igs), 4),
        "US_urgency": round(float(us), 4),
        "EBS_economic_benefit": round(float(ebs), 4),
        "DAS_dev_alignment": round(float(das), 4),
        "MP_manipulation_penalty": round(float(penalty), 4),
        "Composite_Score": round(float(composite_pi), 4)
    }
    
    return PriorityScore(
        cluster_id=cluster_id,
        ward_id=ward_id,
        ward_name=ward_name,
        category=category,
        raw_demand_index=round(dwi_raw, 4),
        calibrated_demand_index=round(dwi_calibrated, 4),
        demographic_vulnerability_index=round(dvi, 4),
        infrastructure_gap_score=round(igs, 4),
        urgency_score=round(us, 4),
        economic_benefit_score=round(ebs, 4),
        dev_alignment_score=round(das, 4),
        manipulation_penalty=round(penalty, 4),
        composite_priority_index=round(composite_pi, 4),
        rank=1,
        calculation_breakdown=breakdown
    )


def compute_all_cluster_priorities(
    clusters: List[Dict[str, Any]],
    demographics_df: pd.DataFrame,
    infrastructure_df: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None
) -> List[PriorityScore]:
    """
    Computes priority scores for a list of identified clusters,
    ranks them in descending order, and attaches the ordinal rank.
    """
    results = []
    
    # Pre-index demographics and infra
    demo_dict = demographics_df.set_index("ward_id").to_dict(orient="index")
    
    for c in clusters:
        w_id = c.get("ward_id", "WARD-01")
        cat = c.get("category", "General")
        
        # Demographic vulnerability from census
        d_info = demo_dict.get(w_id, {})
        dvi = float(d_info.get("vulnerable_population_pct", 0.3))
        
        # Infrastructure deficit score from asset register
        infra_match = infrastructure_df[
            (infrastructure_df["ward_id"] == w_id) & 
            (infrastructure_df["category"] == cat)
        ]
        if not infra_match.empty:
            igs = float(infra_match.iloc[0]["deficit_score"])
        else:
            igs = 0.5  # Neutral default
            
        # Urgency from severity counts
        us = calculate_urgency_score(c.get("severity_breakdown", {}))
        
        # Economic benefit: relative to population reach
        pop = float(d_info.get("total_population", 50000))
        ebs = min(pop / 150000.0, 1.0)
        
        # Development plan alignment (e.g. Water/Health has high baseline alignment)
        high_priority_sectors = ["Water", "Healthcare", "Sanitation", "Roads"]
        das = 0.90 if cat in high_priority_sectors else 0.65
        
        # Raw vs Calibrated demand
        dwi_raw = float(c.get("raw_demand_score", 0.5))
        dwi_cal = float(c.get("calibrated_demand_score", 0.5))
        
        manip_flag = c.get("manipulation_flag", "LOW")
        
        score_obj = calculate_priority_index(
            cluster_id=c.get("cluster_id", "CLUSTER_01"),
            ward_id=w_id,
            ward_name=c.get("ward_name", "Unknown Ward"),
            category=cat,
            dwi_raw=dwi_raw,
            dwi_calibrated=dwi_cal,
            dvi=dvi,
            igs=igs,
            us=us,
            ebs=ebs,
            das=das,
            manipulation_flag=manip_flag,
            weights=weights
        )
        results.append(score_obj)
        
    # Rank descending by composite score
    results.sort(key=lambda x: x.composite_priority_index, reverse=True)
    for i, item in enumerate(results):
        item.rank = i + 1
        
    return results
