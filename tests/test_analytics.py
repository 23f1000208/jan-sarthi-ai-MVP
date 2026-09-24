"""
Unit tests for deterministic analytics and Zero-LLM-Arithmetic invariance.
"""
import pytest
import pandas as pd
from jan_sarthi_agent.analytics.deterministic import (
    compute_summary_kpis,
    aggregate_feedback_by_category,
    aggregate_feedback_by_ward
)


@pytest.fixture
def sample_feedback_df():
    data = [
        {"id": "CF-1", "category": "Water", "severity": "Critical", "administrative_region": "WARD-01", "language": "Hindi", "affected_population_estimate": 1000, "evidence_status": "VERIFIED", "manipulation_risk": "LOW"},
        {"id": "CF-2", "category": "Water", "severity": "High", "administrative_region": "WARD-01", "language": "Hindi", "affected_population_estimate": 2000, "evidence_status": "PENDING", "manipulation_risk": "LOW"},
        {"id": "CF-3", "category": "Roads", "severity": "Medium", "administrative_region": "WARD-02", "language": "English", "affected_population_estimate": 500, "evidence_status": "PENDING", "manipulation_risk": "LOW"},
        {"id": "CF-4", "category": "Roads", "severity": "Low", "administrative_region": "WARD-02", "language": "English", "affected_population_estimate": 300, "evidence_status": "PENDING", "manipulation_risk": "HIGH"},
    ]
    return pd.DataFrame(data)


def test_compute_summary_kpis(sample_feedback_df):
    kpis = compute_summary_kpis(sample_feedback_df, cluster_count=2)
    assert kpis["total_signals"] == 4
    assert kpis["valid_signals"] == 3
    assert kpis["flagged_signals"] == 1
    assert kpis["verified_count"] == 1
    assert kpis["critical_issues"] == 1
    assert kpis["languages_detected"] == 2


def test_aggregate_feedback_by_category(sample_feedback_df):
    agg = aggregate_feedback_by_category(sample_feedback_df)
    assert len(agg) == 2
    water_row = agg[agg["category"] == "Water"].iloc[0]
    assert water_row["total_count"] == 2
    assert water_row["critical_count"] == 1
    assert water_row["avg_affected_pop"] == 1500.0


def test_aggregate_feedback_by_ward(sample_feedback_df):
    ward_agg = aggregate_feedback_by_ward(sample_feedback_df)
    assert len(ward_agg) == 2
    w1 = ward_agg[ward_agg["administrative_region"] == "WARD-01"].iloc[0]
    assert w1["total_signals"] == 2
    assert w1["critical_count"] == 1
