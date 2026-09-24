"""
Evidence Fusion Tool
Merges unstructured citizen signals with structural datasets:
1. Demographic census (vulnerability, literacy, connectivity, poverty)
2. Municipal infrastructure registry (operational capacity, deficit scores, distances)
Constructs a complete evidence packet with verifiable citations.
"""
from typing import Dict, Any, List
import pandas as pd


def fuse_evidence_packet(
    cluster_dict: Dict[str, Any],
    demographics_df: pd.DataFrame,
    infrastructure_df: pd.DataFrame,
    feedback_df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Constructs an evidence packet for a given hotspot cluster.
    Provides verifiable figures for MCDA scoring and Gemini policy brief generation.
    """
    ward_id = cluster_dict.get("ward_id", "WARD-01")
    cat = cluster_dict.get("category", "General")
    
    # 1. Demographics
    demo_row = demographics_df[demographics_df["ward_id"] == ward_id]
    if not demo_row.empty:
        d = demo_row.iloc[0]
        demo_info = {
            "total_population": int(d["total_population"]),
            "vulnerable_population_pct": float(d["vulnerable_population_pct"]),
            "digital_literacy_rate": float(d["digital_literacy_rate"]),
            "connectivity_index": float(d["connectivity_index"]),
            "poverty_rate": float(d["poverty_rate"]),
            "source": str(d.get("source", "National Census Office")),
            "status": str(d.get("status", "SIMULATED"))
        }
    else:
        demo_info = {
            "total_population": 50000,
            "vulnerable_population_pct": 0.35,
            "digital_literacy_rate": 0.50,
            "connectivity_index": 0.50,
            "poverty_rate": 0.25,
            "source": "SIMULATED - Census Default",
            "status": "SIMULATED"
        }
        
    # 2. Infrastructure Registry Match
    infra_row = infrastructure_df[
        (infrastructure_df["ward_id"] == ward_id) & 
        (infrastructure_df["category"] == cat)
    ]
    if not infra_row.empty:
        i = infra_row.iloc[0]
        infra_info = {
            "asset_type": str(i["asset_type"]),
            "operational_capacity_pct": float(i["operational_capacity_pct"]),
            "deficit_score": float(i["deficit_score"]),
            "distance_to_nearest_facility_km": float(i["distance_to_nearest_facility_km"]),
            "source": str(i.get("source", "Municipal Asset Register")),
            "status": str(i.get("status", "SIMULATED"))
        }
    else:
        infra_info = {
            "asset_type": f"General {cat} Infrastructure",
            "operational_capacity_pct": 40.0,
            "deficit_score": 0.60,
            "distance_to_nearest_facility_km": 5.0,
            "source": "SIMULATED - Asset Register Default",
            "status": "SIMULATED"
        }
        
    # 3. Citizen Evidence Base
    feedback_ids = cluster_dict.get("feedback_ids", [])
    cluster_signals = feedback_df[feedback_df["id"].isin(feedback_ids)]
    
    anonymized_quotes = []
    if not cluster_signals.empty:
        anonymized_quotes = cluster_signals["normalized_text"].head(3).tolist()
        verified_count = int((cluster_signals["evidence_status"] == "VERIFIED").sum())
        pending_count = int((cluster_signals["evidence_status"] == "PENDING").sum())
    else:
        verified_count = 0
        pending_count = 0
        
    return {
        "cluster_id": cluster_dict.get("cluster_id"),
        "ward_id": ward_id,
        "ward_name": cluster_dict.get("ward_name"),
        "category": cat,
        "raw_signal_count": cluster_dict.get("raw_signal_count", len(feedback_ids)),
        "verified_signals": verified_count,
        "pending_signals": pending_count,
        "demographics": demo_info,
        "infrastructure": infra_info,
        "anonymized_quotes": anonymized_quotes,
        "severity_breakdown": cluster_dict.get("severity_breakdown", {}),
        "manipulation_flag": cluster_dict.get("manipulation_flag", "LOW")
    }
