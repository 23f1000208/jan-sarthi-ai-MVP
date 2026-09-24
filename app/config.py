"""
Configuration and Environment Settings for JAN-SARTHI AI
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Mode Settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes") or not GOOGLE_API_KEY
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
APP_ENV = os.getenv("APP_ENV", "development")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FEEDBACK_DATA_PATH = os.path.join(DATA_DIR, "demo_feedback.csv")
INFRA_DATA_PATH = os.path.join(DATA_DIR, "infrastructure.csv")
DEMO_DATA_PATH = os.path.join(DATA_DIR, "demographics.csv")
BOUNDARIES_PATH = os.path.join(DATA_DIR, "boundaries.geojson")

# System Constants
SUPPORTED_LANGUAGES = ["Hindi", "English", "Bengali", "Tamil", "Marathi", "Telugu"]
INFRASTRUCTURE_CATEGORIES = [
    "Water",
    "Roads",
    "Electricity",
    "Healthcare",
    "Education",
    "Sanitation",
    "Waste Management",
    "Public Transport",
    "Digital Connectivity",
    "Public Safety"
]

SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]

# Decision Support Priority Index Weights (Default AHP/TOPSIS weights)
DEFAULT_WEIGHTS = {
    "w_dwi": 0.25,   # Citizen Demand Weight Index (Raw / Calibrated)
    "w_dvi": 0.25,   # Demographic Vulnerability Index (Poverty, marginalization)
    "w_igs": 0.20,   # Infrastructure Gap Score (Baseline capacity deficit)
    "w_us": 0.15,    # Urgency Score (Severity & duration)
    "w_ebs": 0.10,   # Economic & Public Benefit Score
    "w_das": 0.05,   # National Development Plan Alignment
    "w_mp": 0.20     # Manipulation Penalty (Subtracted)
}
