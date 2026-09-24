"""
Pure Python Deterministic Analytics Engine
Zero-LLM-Arithmetic: Aggregates, KPI summaries, and statistical breakdowns.
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np


def compute_summary_kpis(feedback_df: pd.DataFrame, cluster_count: int = 5) -> Dict[str, Any]:
    """
    Computes top-level executive KPI metrics from the feedback dataset.
    """
    total_signals = len(feedback_df)
    
    # Filter valid vs flagged
    valid_signals = feedback_df[feedback_df["manipulation_risk"] != "HIGH"]
    flagged_signals = feedback_df[feedback_df["manipulation_risk"] == "HIGH"]
    
    # Status counts
    verified_count = len(feedback_df[feedback_df["evidence_status"] == "VERIFIED"])
    pending_count = len(feedback_df[feedback_df["evidence_status"] == "PENDING"])
    
    # Severity breakdown
    critical_count = len(feedback_df[feedback_df["severity"] == "Critical"])
    high_count = len(feedback_df[feedback_df["severity"] == "High"])
    high_priority_zones = feedback_df[feedback_df["severity"].isin(["Critical", "High"])]["administrative_region"].nunique()
    
    # Languages
    languages = feedback_df["language"].dropna().unique().tolist()
    
    return {
        "total_signals": total_signals,
        "valid_signals": len(valid_signals),
        "flagged_signals": len(flagged_signals),
        "active_hotspots": cluster_count,
        "high_priority_zones": high_priority_zones,
        "verified_count": verified_count,
        "pending_verification": pending_count,
        "critical_issues": critical_count,
        "high_issues": high_count,
        "languages_detected": len(languages),
        "language_list": languages
    }


def aggregate_feedback_by_category(feedback_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates signal volume and severity by infrastructure category.
    """
    cat_summary = feedback_df.groupby("category").agg(
        total_count=("id", "count"),
        critical_count=("severity", lambda s: (s == "Critical").sum()),
        high_count=("severity", lambda s: (s == "High").sum()),
        avg_affected_pop=("affected_population_estimate", "mean")
    ).reset_index()
    return cat_summary.sort_values(by="total_count", ascending=False)


def aggregate_feedback_by_ward(feedback_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates feedback metrics per administrative ward.
    """
    ward_summary = feedback_df.groupby("administrative_region").agg(
        total_signals=("id", "count"),
        critical_count=("severity", lambda s: (s == "Critical").sum()),
        unique_categories=("category", "nunique"),
        manipulation_flags=("manipulation_risk", lambda r: (r == "HIGH").sum())
    ).reset_index()
    return ward_summary.sort_values(by="total_signals", ascending=False)
