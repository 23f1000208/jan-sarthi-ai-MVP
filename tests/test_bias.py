"""
Unit tests for representation-bias adjustment formulations.
"""
import pytest
import pandas as pd
from jan_sarthi_agent.analytics.bias import calculate_calibrated_demand, compute_ward_demand_metrics


def test_calculate_calibrated_demand_inverse_weighting():
    # Affluent ward: high digital literacy (0.85) and high connectivity (0.90) -> Product ~0.765 -> Multiplier ~1.307
    affluent_demand = calculate_calibrated_demand(
        raw_signal_count=10,
        digital_literacy_rate=0.85,
        connectivity_index=0.90
    )
    
    # Marginalized ward: low digital literacy (0.20) and low connectivity (0.25) -> Product 0.05 -> Multiplier 20.0
    marginalized_demand = calculate_calibrated_demand(
        raw_signal_count=10,
        digital_literacy_rate=0.20,
        connectivity_index=0.25
    )
    
    # The marginalized ward must receive a strictly higher calibrated demand for the same raw complaints
    assert marginalized_demand > affluent_demand
    assert round(marginalized_demand, 1) == 200.0


def test_division_by_zero_safety():
    # Test boundary condition where literacy or connectivity is 0.0
    safe_demand = calculate_calibrated_demand(
        raw_signal_count=5,
        digital_literacy_rate=0.0,
        connectivity_index=0.0
    )
    assert safe_demand > 0.0
    assert not pd.isna(safe_demand)
