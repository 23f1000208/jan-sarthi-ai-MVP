"""
Demographic Representation-Bias Adjustment Module
Implements the research paper formulation:
DWI_calibrated = DWI_raw * (1 / (Digital Literacy Rate_i * Connectivity Index_i))
Ensures marginalized rural/tribal voices are not overwhelmed by urban tech-savvy volume surges.
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np


def calculate_calibrated_demand(
    raw_signal_count: int,
    digital_literacy_rate: float,
    connectivity_index: float,
    min_access_floor: float = 0.05
) -> float:
    """
    Computes representation-adjusted demand multiplier.
    A ward with low digital literacy (e.g. 0.19) and low connectivity (e.g. 0.24) receives
    a high inverse weighting factor, balancing high-density submissions from affluent wards.
    """
    # Guard against division by zero
    safe_literacy = max(float(digital_literacy_rate), min_access_floor)
    safe_connectivity = max(float(connectivity_index), min_access_floor)
    
    access_product = safe_literacy * safe_connectivity
    inverse_weight = 1.0 / access_product
    
    # Raw adjusted signal volume
    calibrated_volume = float(raw_signal_count) * inverse_weight
    return calibrated_volume


def compute_ward_demand_metrics(
    feedback_df: pd.DataFrame,
    demographics_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates raw vs calibrated demand across all administrative wards.
    Returns normalized indices between 0.0 and 1.0.
    """
    # Count non-astroturfed signals per ward
    valid_signals = feedback_df[feedback_df["manipulation_risk"] != "HIGH"]
    ward_counts = valid_signals.groupby("administrative_region").size().reset_index(name="raw_count")
    
    # Merge with demographics
    merged = pd.merge(demographics_df, ward_counts, left_on="ward_id", right_on="administrative_region", how="left")
    merged["raw_count"] = merged["raw_count"].fillna(0).astype(int)
    
    # Calculate calibrated demand
    merged["calibrated_volume"] = merged.apply(
        lambda row: calculate_calibrated_demand(
            row["raw_count"],
            row["digital_literacy_rate"],
            row["connectivity_index"]
        ),
        axis=1
    )
    
    # Normalize Raw DWI (0 to 1)
    max_raw = merged["raw_count"].max()
    merged["dwi_raw"] = merged["raw_count"] / max_raw if max_raw > 0 else 0.0
    
    # Normalize Calibrated DWI (0 to 1)
    max_cal = merged["calibrated_volume"].max()
    merged["dwi_calibrated"] = merged["calibrated_volume"] / max_cal if max_cal > 0 else 0.0
    
    return merged[[
        "ward_id",
        "ward_name",
        "zone",
        "raw_count",
        "dwi_raw",
        "digital_literacy_rate",
        "connectivity_index",
        "calibrated_volume",
        "dwi_calibrated",
        "vulnerable_population_pct",
        "poverty_rate"
    ]]
