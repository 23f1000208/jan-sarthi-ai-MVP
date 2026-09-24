"""
Unit tests for Google ADK Root Agent and decision-support pipeline execution.
"""
import pytest
import pandas as pd
from jan_sarthi_agent.agent import (
    root_agent,
    process_feedback_intake,
    detect_hotspots,
    run_evidence_and_priority_pipeline,
    produce_policy_brief
)


def test_root_agent_initialization():
    assert root_agent.name == "jan_sarthi_agent"
    assert len(root_agent.tools) >= 4


def test_hotspot_detection_from_records():
    records = [
        {"id": "CF-1", "category": "Water", "severity": "High", "location": "Rampur", "latitude": 28.74, "longitude": 77.14, "administrative_region": "WARD-01", "original_text": "Water problem", "timestamp": "2026-09-20T10:00:00", "manipulation_risk": "LOW"},
        {"id": "CF-2", "category": "Water", "severity": "Critical", "location": "Rampur", "latitude": 28.742, "longitude": 77.141, "administrative_region": "WARD-01", "original_text": "Water broken", "timestamp": "2026-09-20T11:00:00", "manipulation_risk": "LOW"},
        {"id": "CF-3", "category": "Water", "severity": "High", "location": "Rampur", "latitude": 28.739, "longitude": 77.139, "administrative_region": "WARD-01", "original_text": "No water supply", "timestamp": "2026-09-20T12:00:00", "manipulation_risk": "LOW"},
    ]
    hotspots = detect_hotspots(records)
    assert len(hotspots) >= 1
    h = hotspots[0]
    assert h["category"] == "Water"
    assert h["ward_id"] == "WARD-01"


def test_policy_brief_generation_pipeline():
    demo_df = pd.DataFrame([{
        "ward_id": "WARD-01",
        "ward_name": "Rampur Rural",
        "zone": "North",
        "total_population": 45000,
        "vulnerable_population_pct": 0.65,
        "digital_literacy_rate": 0.30,
        "connectivity_index": 0.40,
        "poverty_rate": 0.40,
        "source": "SIMULATED",
        "date": "2026-01-01",
        "status": "SIMULATED"
    }])
    
    infra_df = pd.DataFrame([{
        "ward_id": "WARD-01",
        "ward_name": "Rampur Rural",
        "category": "Water",
        "asset_type": "Overhead Tank",
        "operational_capacity_pct": 30.0,
        "deficit_score": 0.80,
        "distance_to_nearest_facility_km": 10.0,
        "status": "SIMULATED",
        "source": "SIMULATED"
    }])
    
    feedback_df = pd.DataFrame([{
        "id": "CF-01",
        "normalized_text": "Drinking water pipeline fractured",
        "evidence_status": "VERIFIED",
        "severity": "Critical"
    }])
    
    cluster = {
        "cluster_id": "CLUSTER-WATER-WARD-01",
        "category": "Water",
        "title": "Rampur Water Deficit",
        "ward_id": "WARD-01",
        "ward_name": "Rampur Rural",
        "centroid_lat": 28.74,
        "centroid_lon": 77.14,
        "raw_signal_count": 5,
        "raw_demand_score": 0.7,
        "calibrated_demand_score": 0.85,
        "severity_breakdown": {"Critical": 3, "High": 2},
        "manipulation_flag": "LOW",
        "feedback_ids": ["CF-01"]
    }
    
    res = run_evidence_and_priority_pipeline(cluster, demo_df, infra_df, feedback_df)
    assert "evidence_packet" in res
    assert "priority_score" in res
    
    brief_res = produce_policy_brief(res["evidence_packet"], res["priority_score"])
    assert "policy_brief" in brief_res
    pb = brief_res["policy_brief"]
    assert pb["cluster_id"] == "CLUSTER-WATER-WARD-01"
    assert pb["ward_name"] == "Rampur Rural"
