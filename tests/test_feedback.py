"""
Unit tests for Citizen Feedback intake and Multilingual NLP tools.
"""
import pytest
from jan_sarthi_agent.tools.language import detect_language, normalize_text
from jan_sarthi_agent.tools.extraction import extract_category_and_severity
from jan_sarthi_agent.agent import process_feedback_intake


def test_language_detection():
    # Hindi
    assert detect_language("हमारे गांव में पानी नहीं आ रहा है") == "Hindi"
    # Bengali
    assert detect_language("আমাদের গ্রামে জলের সমস্যা") == "Bengali"
    # English
    assert detect_language("Severe pothole issue on main road") == "English"


def test_text_normalization():
    raw = "   Water    supply  is cut off!!!   "
    normalized = normalize_text(raw)
    assert normalized == "Water supply is cut off!!!"


def test_category_and_severity_extraction():
    # Water & Critical
    cat, subcat, sev = extract_category_and_severity("पानी की सप्लाई पूरी तरह बंद है, बहुत गंभीर समस्या है")
    assert cat == "Water"
    assert sev in ["Critical", "High"]
    
    # Roads & High
    cat_r, _, sev_r = extract_category_and_severity("Heavy potholes and road broken near highway")
    assert cat_r == "Roads"
    assert sev_r in ["High", "Medium"]
    
    # Electricity
    cat_e, _, _ = extract_category_and_severity("11kV ट्रांसफार्मर जल गया है")
    assert cat_e == "Electricity"


def test_end_to_end_intake_process():
    res = process_feedback_intake(
        text="रामपुर में पानी नहीं है। संपर्क: 9876543210",
        location_name="Rampur Rural",
        ward_id="WARD-01",
        latitude=28.74,
        longitude=77.14
    )
    assert res["status"] == "ACCEPTED"
    assert res["feedback"]["language"] == "Hindi"
    assert res["feedback"]["category"] == "Water"
    assert "[REDACTED_PHONE]" in res["feedback"]["normalized_text"]
    assert res["security"]["contains_pii"] is True
