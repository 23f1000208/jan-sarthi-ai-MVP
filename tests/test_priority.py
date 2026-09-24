"""
Unit tests for deterministic MCDA Priority calculation.
"""
import pytest
from jan_sarthi_agent.analytics.mcda import calculate_priority_index, calculate_urgency_score


def test_calculate_urgency_score():
    sev_counts = {"Critical": 3, "High": 2, "Medium": 0, "Low": 0}
    # Weighted: (3*1.0 + 2*0.7) / 5 = (3.0 + 1.4) / 5 = 4.4 / 5 = 0.88
    us = calculate_urgency_score(sev_counts)
    assert round(us, 2) == 0.88


def test_priority_score_deterministic_invariants():
    score = calculate_priority_index(
        cluster_id="CLUSTER_WATER_01",
        ward_id="WARD-01",
        ward_name="Rampur Rural",
        category="Water",
        dwi_raw=0.8,
        dwi_calibrated=0.9,
        dvi=0.7,
        igs=0.85,
        us=0.9,
        ebs=0.6,
        das=0.9,
        manipulation_flag="LOW"
    )
    
    assert 0.0 <= score.composite_priority_index <= 1.0
    assert score.manipulation_penalty == 0.0
    assert score.calculation_breakdown["Composite_Score"] == score.composite_priority_index


def test_manipulation_penalty_application():
    normal_score = calculate_priority_index(
        cluster_id="TEST_01",
        ward_id="W-1",
        ward_name="Test",
        category="Roads",
        dwi_raw=0.5,
        dwi_calibrated=0.5,
        dvi=0.5,
        igs=0.5,
        us=0.5,
        ebs=0.5,
        das=0.5,
        manipulation_flag="LOW"
    )
    
    penalized_score = calculate_priority_index(
        cluster_id="TEST_01",
        ward_id="W-1",
        ward_name="Test",
        category="Roads",
        dwi_raw=0.5,
        dwi_calibrated=0.5,
        dvi=0.5,
        igs=0.5,
        us=0.5,
        ebs=0.5,
        das=0.5,
        manipulation_flag="HIGH"
    )
    
    assert penalized_score.composite_priority_index < normal_score.composite_priority_index
    assert penalized_score.manipulation_penalty > 0.0
