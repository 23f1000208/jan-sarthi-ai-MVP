"""
Temporal Velocity & Spike Detection Engine
Tracks submission frequency over sliding windows to surface emerging civic crises
and identify anomalous submission spikes.
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np


def detect_temporal_spikes(
    feedback_df: pd.DataFrame,
    window_hours: int = 24,
    spike_threshold_multiplier: float = 2.5
) -> List[Dict[str, Any]]:
    """
    Identifies sudden bursts of citizen complaints in specific wards and categories.
    """
    if feedback_df.empty:
        return []
        
    df = feedback_df.copy()
    df["dt"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["dt"]).sort_values(by="dt")
    
    spikes = []
    for (ward, cat), group in df.groupby(["administrative_region", "category"]):
        if len(group) < 4:
            continue
            
        # Resample to hourly counts
        hourly = group.set_index("dt").resample("6h").size()
        if len(hourly) > 2:
            mean_rate = hourly.mean()
            max_rate = hourly.max()
            if mean_rate > 0 and (max_rate / mean_rate) >= spike_threshold_multiplier:
                spikes.append({
                    "ward_id": ward,
                    "category": cat,
                    "max_spike_signals": int(max_rate),
                    "baseline_mean": round(float(mean_rate), 2),
                    "spike_ratio": round(float(max_rate / mean_rate), 2),
                    "is_anomalous": True
                })
                
    return spikes
