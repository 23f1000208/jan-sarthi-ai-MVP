"""
Deterministic Analytics Package for JAN-SARTHI AI
Strict adherence to Zero-LLM-Arithmetic Rule: All mathematical calculations,
indices, weights, and aggregates are executed in pure Python/Pandas.
"""
from .deterministic import compute_summary_kpis, aggregate_feedback_by_category, aggregate_feedback_by_ward
from .mcda import calculate_priority_index, compute_all_cluster_priorities
from .bias import calculate_calibrated_demand
from .trends import detect_temporal_spikes

__all__ = [
    "compute_summary_kpis",
    "aggregate_feedback_by_category",
    "aggregate_feedback_by_ward",
    "calculate_priority_index",
    "compute_all_cluster_priorities",
    "calculate_calibrated_demand",
    "detect_temporal_spikes"
]
