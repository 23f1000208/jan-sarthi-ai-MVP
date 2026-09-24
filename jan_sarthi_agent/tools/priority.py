"""
Priority Calculation Tool Wrapper
Bridges deterministic MCDA scoring into the agent and dashboard workflow.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
from ..analytics.mcda import calculate_priority_index, compute_all_cluster_priorities
from ..schemas import PriorityScore


def evaluate_cluster_priority(
    cluster_dict: Dict[str, Any],
    evidence_packet: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None
) -> PriorityScore:
    """
    Computes deterministic priority score for an individual cluster given its evidence packet.
    """
    demo = evidence_packet.get("demographics", {})
    infra = evidence_packet.get("infrastructure", {})
    
    dwi_raw = float(cluster_dict.get("raw_demand_score", 0.5))
    dwi_cal = float(cluster_dict.get("calibrated_demand_score", 0.5))
    dvi = float(demo.get("vulnerable_population_pct", 0.35))
    igs = float(infra.get("deficit_score", 0.60))
    
    # Urgency from severity counts
    sev_counts = cluster_dict.get("severity_breakdown", {})
    total = sum(sev_counts.values()) or 1
    weighted_sev = (
        sev_counts.get("Critical", 0) * 1.0 +
        sev_counts.get("High", 0) * 0.7 +
        sev_counts.get("Medium", 0) * 0.4 +
        sev_counts.get("Low", 0) * 0.1
    )
    us = min(1.0, weighted_sev / total)
    
    # EBS: population reach
    pop = float(demo.get("total_population", 50000))
    ebs = min(1.0, pop / 150000.0)
    
    # DAS: alignment with national SDG/Infrastructure missions
    das = 0.90 if cluster_dict.get("category") in ["Water", "Healthcare", "Sanitation", "Roads"] else 0.70
    
    return calculate_priority_index(
        cluster_id=cluster_dict.get("cluster_id", "CLUSTER_01"),
        ward_id=cluster_dict.get("ward_id", "WARD-01"),
        ward_name=cluster_dict.get("ward_name", "Unknown Ward"),
        category=cluster_dict.get("category", "General"),
        dwi_raw=dwi_raw,
        dwi_calibrated=dwi_cal,
        dvi=dvi,
        igs=igs,
        us=us,
        ebs=ebs,
        das=das,
        manipulation_flag=cluster_dict.get("manipulation_flag", "LOW"),
        weights=weights
    )
