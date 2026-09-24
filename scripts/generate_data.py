"""
Dataset Generator for JAN-SARTHI AI
Generates:
1. data/demographics.csv
2. data/infrastructure.csv
3. data/boundaries.geojson
4. data/demo_feedback.csv (60+ multimodal feedback records)
"""
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Demographics Data
# Covers 6 diverse administrative wards (Urban affluent, Urban dense, Industrial, Peri-urban, Rural, Remote)
demographics_data = [
    {
        "ward_id": "WARD-01",
        "ward_name": "Rampur Rural",
        "zone": "North Zone",
        "total_population": 45000,
        "vulnerable_population_pct": 0.68,
        "digital_literacy_rate": 0.28,
        "connectivity_index": 0.35,
        "poverty_rate": 0.42,
        "source": "SIMULATED - National Census Office",
        "date": "2026-01-15",
        "status": "SIMULATED"
    },
    {
        "ward_id": "WARD-02",
        "ward_name": "Anand Vihar Urban",
        "zone": "East Zone",
        "total_population": 120000,
        "vulnerable_population_pct": 0.22,
        "digital_literacy_rate": 0.85,
        "connectivity_index": 0.92,
        "poverty_rate": 0.12,
        "source": "SIMULATED - National Census Office",
        "date": "2026-01-15",
        "status": "SIMULATED"
    },
    {
        "ward_id": "WARD-03",
        "ward_name": "Sitapur Industrial",
        "zone": "South Zone",
        "total_population": 85000,
        "vulnerable_population_pct": 0.55,
        "digital_literacy_rate": 0.45,
        "connectivity_index": 0.58,
        "poverty_rate": 0.36,
        "source": "SIMULATED - National Census Office",
        "date": "2026-01-15",
        "status": "SIMULATED"
    },
    {
        "ward_id": "WARD-04",
        "ward_name": "Subhash Nagar Peri-Urban",
        "zone": "West Zone",
        "total_population": 65000,
        "vulnerable_population_pct": 0.48,
        "digital_literacy_rate": 0.52,
        "connectivity_index": 0.60,
        "poverty_rate": 0.29,
        "source": "SIMULATED - National Census Office",
        "date": "2026-01-15",
        "status": "SIMULATED"
    },
    {
        "ward_id": "WARD-05",
        "ward_name": "Kalyanpur Tribal Belt",
        "zone": "East Zone",
        "total_population": 32000,
        "vulnerable_population_pct": 0.82,
        "digital_literacy_rate": 0.19,
        "connectivity_index": 0.24,
        "poverty_rate": 0.58,
        "source": "SIMULATED - National Census Office",
        "date": "2026-01-15",
        "status": "SIMULATED"
    },
    {
        "ward_id": "WARD-06",
        "ward_name": "Central Metro Core",
        "zone": "Central Zone",
        "total_population": 150000,
        "vulnerable_population_pct": 0.18,
        "digital_literacy_rate": 0.91,
        "connectivity_index": 0.96,
        "poverty_rate": 0.08,
        "source": "SIMULATED - National Census Office",
        "date": "2026-01-15",
        "status": "SIMULATED"
    }
]
pd.DataFrame(demographics_data).to_csv(os.path.join(DATA_DIR, "demographics.csv"), index=False)

# 2. Infrastructure Inventory & Baseline Deficits
infrastructure_data = [
    {"ward_id": "WARD-01", "ward_name": "Rampur Rural", "category": "Water", "asset_type": "Tube Wells & Overhead Tank", "operational_capacity_pct": 32.0, "deficit_score": 0.78, "distance_to_nearest_facility_km": 14.5, "status": "SIMULATED", "source": "State Water Board 2026"},
    {"ward_id": "WARD-01", "ward_name": "Rampur Rural", "category": "Healthcare", "asset_type": "Primary Health Sub-Center", "operational_capacity_pct": 40.0, "deficit_score": 0.70, "distance_to_nearest_facility_km": 18.2, "status": "SIMULATED", "source": "District Health Office"},
    {"ward_id": "WARD-01", "ward_name": "Rampur Rural", "category": "Roads", "asset_type": "Unpaved Arterial Link", "operational_capacity_pct": 25.0, "deficit_score": 0.82, "distance_to_nearest_facility_km": 8.0, "status": "SIMULATED", "source": "PWD Rural Roads"},
    {"ward_id": "WARD-02", "ward_name": "Anand Vihar Urban", "category": "Roads", "asset_type": "Secondary Paved Road", "operational_capacity_pct": 85.0, "deficit_score": 0.20, "distance_to_nearest_facility_km": 1.2, "status": "SIMULATED", "source": "Municipal Corp"},
    {"ward_id": "WARD-02", "ward_name": "Anand Vihar Urban", "category": "Waste Management", "asset_type": "Waste Segregation Center", "operational_capacity_pct": 50.0, "deficit_score": 0.52, "distance_to_nearest_facility_km": 2.5, "status": "SIMULATED", "source": "Sanitation Board"},
    {"ward_id": "WARD-03", "ward_name": "Sitapur Industrial", "category": "Electricity", "asset_type": "11kV Distribution Substation", "operational_capacity_pct": 45.0, "deficit_score": 0.65, "distance_to_nearest_facility_km": 5.4, "status": "SIMULATED", "source": "Power Discom"},
    {"ward_id": "WARD-03", "ward_name": "Sitapur Industrial", "category": "Sanitation", "asset_type": "Industrial Drainage Trunk", "operational_capacity_pct": 30.0, "deficit_score": 0.75, "distance_to_nearest_facility_km": 3.8, "status": "SIMULATED", "source": "Pollution Control Board"},
    {"ward_id": "WARD-04", "ward_name": "Subhash Nagar Peri-Urban", "category": "Education", "asset_type": "Government Senior Secondary", "operational_capacity_pct": 55.0, "deficit_score": 0.48, "distance_to_nearest_facility_km": 4.1, "status": "SIMULATED", "source": "Education Dept"},
    {"ward_id": "WARD-04", "ward_name": "Subhash Nagar Peri-Urban", "category": "Water", "asset_type": "Municipal Piped Line", "operational_capacity_pct": 60.0, "deficit_score": 0.45, "distance_to_nearest_facility_km": 3.2, "status": "SIMULATED", "source": "Jal Sansthan"},
    {"ward_id": "WARD-05", "ward_name": "Kalyanpur Tribal Belt", "category": "Water", "asset_type": "Community Borewells", "operational_capacity_pct": 20.0, "deficit_score": 0.88, "distance_to_nearest_facility_km": 22.0, "status": "SIMULATED", "source": "Tribal Welfare Dept"},
    {"ward_id": "WARD-05", "ward_name": "Kalyanpur Tribal Belt", "category": "Healthcare", "asset_type": "Community Dispensary", "operational_capacity_pct": 15.0, "deficit_score": 0.92, "distance_to_nearest_facility_km": 26.5, "status": "SIMULATED", "source": "State Health Mission"},
    {"ward_id": "WARD-06", "ward_name": "Central Metro Core", "category": "Public Transport", "asset_type": "City Bus Terminal & Metro Link", "operational_capacity_pct": 90.0, "deficit_score": 0.15, "distance_to_nearest_facility_km": 0.8, "status": "SIMULATED", "source": "Urban Transport Authority"}
]
pd.DataFrame(infrastructure_data).to_csv(os.path.join(DATA_DIR, "infrastructure.csv"), index=False)

# 3. GeoJSON Boundaries (Sample polygons for Delhi NCR / National Capital District)
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"ward_id": "WARD-01", "name": "Rampur Rural", "zone": "North Zone"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.10, 28.70], [77.18, 28.70], [77.18, 28.78], [77.10, 28.78], [77.10, 28.70]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"ward_id": "WARD-02", "name": "Anand Vihar Urban", "zone": "East Zone"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.28, 28.62], [77.35, 28.62], [77.35, 28.68], [77.28, 28.68], [77.28, 28.62]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"ward_id": "WARD-03", "name": "Sitapur Industrial", "zone": "South Zone"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.20, 28.50], [77.27, 28.50], [77.27, 28.57], [77.20, 28.57], [77.20, 28.50]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"ward_id": "WARD-04", "name": "Subhash Nagar Peri-Urban", "zone": "West Zone"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.08, 28.60], [77.16, 28.60], [77.16, 28.67], [77.08, 28.67], [77.08, 28.60]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"ward_id": "WARD-05", "name": "Kalyanpur Tribal Belt", "zone": "East Zone"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.35, 28.70], [77.44, 28.70], [77.44, 28.79], [77.35, 28.79], [77.35, 28.70]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"ward_id": "WARD-06", "name": "Central Metro Core", "zone": "Central Zone"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[77.18, 28.60], [77.25, 28.60], [77.25, 28.67], [77.18, 28.67], [77.18, 28.60]]]
            }
        }
    ]
}
with open(os.path.join(DATA_DIR, "boundaries.geojson"), "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, indent=2)

# 4. Demo Citizen Feedback Data (70 records across 6 wards, 5 hotspots, 4 languages, astroturfing spikes)
base_time = datetime(2026, 9, 20, 10, 0, 0)
feedback_list = []

# Hotspot 1: Rampur Rural - Chronic Drinking Water Outage (Hindi & English)
h1_samples = [
    ("हमारे गांव रामपुर में पिछले 20 दिनों से पानी की सप्लाई पूरी तरह बंद है। महिलाओं को 3 किलोमीटर दूर जाना पड़ता है।", "Hindi", "Water", "Supply Disruption", "Critical", 28.74, 77.14, "WARD-01", "20 days", 4500),
    ("स्कूल के बच्चों को भी बहुत दूर से पानी लाना पड़ रहा है, हैंडपंप में भी दूषित पानी आ रहा है।", "Hindi", "Water", "Quality & Contamination", "High", 28.75, 77.13, "WARD-01", "15 days", 2500),
    ("Severe water shortage in Rampur Village for 3 weeks. Well water is dirty and undrinkable.", "English", "Water", "Supply Disruption", "Critical", 28.73, 77.15, "WARD-01", "21 days", 5000),
    ("रामपुर मुख्य बस्ती में जल संकट गहरा गया है, तत्काल टैंकर या पाइपलाइन मरम्मत की आवश्यकता है।", "Hindi", "Water", "Infrastructure Failure", "High", 28.74, 77.12, "WARD-01", "18 days", 3200),
    ("Water pipes broken near primary health center Rampur, mud entering supply line.", "English", "Water", "Pipe Damage", "High", 28.76, 77.14, "WARD-01", "12 days", 1800),
    ("पानी की टंकी में लीकेज है और पिछले दो हफ्ते से पानी नहीं पहुंचा है।", "Hindi", "Water", "Supply Disruption", "High", 28.74, 77.15, "WARD-01", "14 days", 2100)
]
for i, item in enumerate(h1_samples):
    feedback_list.append({
        "id": f"CF-2026-H1-{i+1:03d}",
        "timestamp": (base_time - timedelta(hours=i*5)).isoformat(),
        "language": item[1],
        "original_text": item[0],
        "normalized_text": item[0],
        "category": item[2],
        "subcategory": item[3],
        "severity": item[4],
        "location": "Rampur Rural",
        "latitude": item[5],
        "longitude": item[6],
        "administrative_region": item[7],
        "duration": item[8],
        "affected_population_estimate": item[9],
        "evidence_status": "VERIFIED" if i < 3 else "PENDING",
        "privacy_status": "SANITIZED",
        "manipulation_risk": "LOW",
        "cluster_id": "HOTSPOT-WATER-RAMPUR"
    })

# Hotspot 2: Kalyanpur Tribal Belt - Severe Healthcare & Emergency Accessibility Deficit
h2_samples = [
    ("कल्याणपुर स्वास्थ्य केंद्र में 2 महीने से कोई डॉक्टर नहीं है। आपातकालीन मरीज अस्पताल नहीं पहुंच पाते।", "Hindi", "Healthcare", "Staff Shortage", "Critical", 28.75, 77.38, "WARD-05", "60 days", 8500),
    ("আমাদের কল্যাণপুর উপস্বাস্থ্য কেন্দ্রে কোনো ওষুধ নেই, অ্যাম্বুলেন্স রাস্তা খারাপ থাকায় আসে না।", "Bengali", "Healthcare", "Supply & Access Deficit", "Critical", 28.76, 77.40, "WARD-05", "45 days", 6200),
    ("Primary Health Subcenter Kalyanpur lacks antivenom and emergency maternal care facilities.", "English", "Healthcare", "Facility Deficit", "High", 28.74, 77.37, "WARD-05", "30 days", 4500),
    ("गंभीर मरीजों को 26 किमी दूर जिला अस्पताल ले जाना पड़ता है, रास्ते में कई मौतें हो चुकी हैं।", "Hindi", "Healthcare", "Emergency Transit", "Critical", 28.77, 77.41, "WARD-05", "90 days", 12000),
    ("Health workers visiting only once a month, urgent PHC upgrade required in tribal block.", "English", "Healthcare", "Staff Shortage", "High", 28.75, 77.39, "WARD-05", "40 days", 5100)
]
for i, item in enumerate(h2_samples):
    feedback_list.append({
        "id": f"CF-2026-H2-{i+1:03d}",
        "timestamp": (base_time - timedelta(hours=i*8)).isoformat(),
        "language": item[1],
        "original_text": item[0],
        "normalized_text": item[0],
        "category": item[2],
        "subcategory": item[3],
        "severity": item[4],
        "location": "Kalyanpur Tribal Belt",
        "latitude": item[5],
        "longitude": item[6],
        "administrative_region": item[7],
        "duration": item[8],
        "affected_population_estimate": item[9],
        "evidence_status": "VERIFIED" if i < 2 else "PENDING",
        "privacy_status": "SANITIZED",
        "manipulation_risk": "LOW",
        "cluster_id": "HOTSPOT-HEALTH-KALYANPUR"
    })

# Hotspot 3: Sitapur Industrial - Severe Grid Blackouts & Chemical Drainage Overflow
h3_samples = [
    ("सीतापुर औद्योगिक क्षेत्र में लगातार 12 घंटे बिजली कटौती हो रही है, नालों का गंदा पानी सड़कों पर भर गया है।", "Hindi", "Electricity", "Power Outage", "High", 28.53, 77.23, "WARD-03", "14 days", 15000),
    ("11kV feeder tripping multiple times daily, chemical effluent line choked near sector 4.", "English", "Electricity", "Substation Failure", "High", 28.54, 77.24, "WARD-03", "10 days", 12000),
    ("गटर का गंदा पानी ओवरफ्लो होकर मुख्य बाजार में घुस रहा है, बीमारी फैलने का खतरा है।", "Hindi", "Sanitation", "Drainage Overflow", "Critical", 28.52, 77.22, "WARD-03", "7 days", 9000),
    ("Industrial wastewater flooding into residential colonies due to uncleaned trunk drain.", "English", "Sanitation", "Drainage Overflow", "High", 28.55, 77.25, "WARD-03", "15 days", 8000),
    ("सीतापुर में ट्रांसफार्मर जल गया है और 4 दिन से कोई सुनवाई नहीं हुई।", "Hindi", "Electricity", "Equipment Breakdown", "High", 28.53, 77.21, "WARD-03", "4 days", 6000)
]
for i, item in enumerate(h3_samples):
    feedback_list.append({
        "id": f"CF-2026-H3-{i+1:03d}",
        "timestamp": (base_time - timedelta(hours=i*6)).isoformat(),
        "language": item[1],
        "original_text": item[0],
        "normalized_text": item[0],
        "category": item[2],
        "subcategory": item[3],
        "severity": item[4],
        "location": "Sitapur Industrial",
        "latitude": item[5],
        "longitude": item[6],
        "administrative_region": item[7],
        "duration": item[8],
        "affected_population_estimate": item[9],
        "evidence_status": "PENDING",
        "privacy_status": "SANITIZED",
        "manipulation_risk": "LOW",
        "cluster_id": "HOTSPOT-ELEC-SITAPUR"
    })

# Hotspot 4: Subhash Nagar Peri-Urban - Collapsed Arterial Road & School Transit Hazard
h4_samples = [
    ("सुभाष नगर मुख्य सड़क पर 2 फीट गहरे गड्ढे हैं, स्कूल बसें दुर्घटनाग्रस्त हो रही हैं।", "Hindi", "Roads", "Road Damage", "High", 28.63, 77.12, "WARD-04", "25 days", 18000),
    ("The arterial road connecting Subhash Nagar to highway has caved in after rains.", "English", "Roads", "Structural Cave-in", "Critical", 28.64, 77.13, "WARD-04", "10 days", 25000),
    ("पैदल चलना भी दूभर हो गया है, दोपहिया वाहन चालक रोज गिरकर चोटिल हो रहे हैं।", "Hindi", "Roads", "Potholes & Pavement Hazard", "High", 28.62, 77.11, "WARD-04", "30 days", 14000),
    ("Street lights non-functional along damaged road stretch, dangerous at night.", "English", "Roads", "Safety & Lighting", "Medium", 28.65, 77.14, "WARD-04", "18 days", 10000)
]
for i, item in enumerate(h4_samples):
    feedback_list.append({
        "id": f"CF-2026-H4-{i+1:03d}",
        "timestamp": (base_time - timedelta(hours=i*7)).isoformat(),
        "language": item[1],
        "original_text": item[0],
        "normalized_text": item[0],
        "category": item[2],
        "subcategory": item[3],
        "severity": item[4],
        "location": "Subhash Nagar Peri-Urban",
        "latitude": item[5],
        "longitude": item[6],
        "administrative_region": item[7],
        "duration": item[8],
        "affected_population_estimate": item[9],
        "evidence_status": "PENDING",
        "privacy_status": "SANITIZED",
        "manipulation_risk": "LOW",
        "cluster_id": "HOTSPOT-ROADS-SUBHASH"
    })

# Hotspot 5 / ASTROTURFING BURST: Anand Vihar Urban - Suspicious Coordinated Bot / Campaign Flood
# Exact high velocity duplicate/templated submissions within 20 minutes from same IP/ward
bot_templates = [
    "Immediate VIP bypass road needed at Sector 9 Anand Vihar for rapid commute.",
    "Immediate VIP bypass road needed at Sector 9 Anand Vihar for rapid commute.",
    "Urgent need for luxury bypass corridor Sector 9 Anand Vihar immediately.",
    "Immediate VIP bypass road needed at Sector 9 Anand Vihar for rapid commute.",
    "Immediate VIP bypass road needed at Sector 9 Anand Vihar for rapid commute.",
    "Demand VIP bypass corridor Sector 9 Anand Vihar for fast car movement.",
    "Immediate VIP bypass road needed at Sector 9 Anand Vihar for rapid commute."
]
for i, text in enumerate(bot_templates):
    feedback_list.append({
        "id": f"CF-2026-ASTRO-{i+1:03d}",
        "timestamp": (base_time - timedelta(minutes=i*2)).isoformat(), # Rapid burst within 14 minutes
        "language": "English",
        "original_text": text,
        "normalized_text": text,
        "category": "Roads",
        "subcategory": "New Road Construction",
        "severity": "Medium",
        "location": "Anand Vihar Urban",
        "latitude": 28.6500 + (i * 0.0002),
        "longitude": 77.3100 + (i * 0.0002),
        "administrative_region": "WARD-02",
        "duration": "1 day",
        "affected_population_estimate": 400,
        "evidence_status": "PENDING",
        "privacy_status": "SANITIZED",
        "manipulation_risk": "HIGH", # Flagged for review
        "cluster_id": "HOTSPOT-ASTROTURF-ANAND"
    })

# Miscellaneous distributed citizen feedback across categories (Education, Water, Transport, Waste)
misc_samples = [
    ("Government girls school in Rampur lacks functional toilets and boundary wall.", "English", "Education", "Sanitation in Schools", "High", 28.72, 77.16, "WARD-01", "40 days", 1200),
    ("আনন্দ বিহার বাস টার্মিনালে রাতে আলো থাকে না, মহিলা যাত্রীদের পক্ষে খুব অসুরক্ষিত।", "Bengali", "Public Safety", "Lighting & Safety", "High", 28.63, 77.32, "WARD-02", "15 days", 3500),
    ("Garbage dumping yard overflowing into sector 5 park in Anand Vihar.", "English", "Waste Management", "Garbage Dump", "Medium", 28.64, 77.30, "WARD-02", "8 days", 2500),
    ("मेट्रो फीडर बसें पिछले 1 महीने से समय पर नहीं आ रही हैं।", "Hindi", "Public Transport", "Bus Frequency", "Medium", 28.63, 28.21, "WARD-06", "30 days", 4000),
    ("Central Metro station escalator broken and lift out of service for senior citizens.", "English", "Public Transport", "Accessibility Deficit", "Medium", 28.64, 77.22, "WARD-06", "10 days", 6500),
    ("कल्याणपुर के प्राथमिक विद्यालय में छत से पानी टपक रहा है, बारिश में कक्षाएं बंद रहती हैं।", "Hindi", "Education", "School Infrastructure", "High", 28.76, 77.42, "WARD-05", "50 days", 800),
    ("Street dogs menace and unlit alleys near Sitapur residential quarters.", "English", "Public Safety", "Animal Control & Lighting", "Low", 28.51, 77.23, "WARD-03", "12 days", 1500),
    ("Digital service kiosk in Subhash Nagar has internet connection down for 3 weeks.", "English", "Digital Connectivity", "Kiosk Down", "Medium", 28.61, 77.15, "WARD-04", "21 days", 2200),
    ("नल से पीला बदबूदार पानी आ रहा है सुभाष नगर ब्लॉक सी में।", "Hindi", "Water", "Water Contamination", "High", 28.62, 77.14, "WARD-04", "5 days", 3100),
    ("Street garbage bins missing on Main Commercial Road Central Core.", "English", "Waste Management", "Bins Missing", "Low", 28.65, 77.21, "WARD-06", "6 days", 1800)
]
for i, item in enumerate(misc_samples):
    feedback_list.append({
        "id": f"CF-2026-MISC-{i+1:03d}",
        "timestamp": (base_time - timedelta(days=i*2, hours=i)).isoformat(),
        "language": item[1],
        "original_text": item[0],
        "normalized_text": item[0],
        "category": item[2],
        "subcategory": item[3],
        "severity": item[4],
        "location": item[7],
        "latitude": item[5],
        "longitude": item[6],
        "administrative_region": item[7],
        "duration": item[8],
        "affected_population_estimate": item[9],
        "evidence_status": "PENDING",
        "privacy_status": "SANITIZED",
        "manipulation_risk": "LOW",
        "cluster_id": "UNCLUSTERED"
    })

# Additional realistic civic signals to expand dataset to ~75 items
extra_samples = [
    ("रामपुर प्राथमिक स्वास्थ्य केंद्र में एंटीबायोटिक और आवश्यक दवाइयां उपलब्ध नहीं हैं।", "Hindi", "Healthcare", "Medicine Shortage", "High", 28.71, 77.13, "WARD-01", "25 days", 3800),
    ("No solar street lamps working in Rampur village center since last monsoon.", "English", "Electricity", "Street Lighting", "Medium", 28.75, 77.16, "WARD-01", "60 days", 2100),
    ("Borewell pump burned out in Kalyanpur Ward 5, villagers relying on stagnant pond water.", "English", "Water", "Pump Failure", "Critical", 28.78, 77.37, "WARD-05", "14 days", 4200),
    ("পুকুরের জল দূষিত হয়ে ডায়রিয়া ছড়াচ্ছে কল্যাণপুর গ্রামে। অবিলম্বে জল শোধন দরকার।", "Bengali", "Water", "Waterborne Disease", "Critical", 28.74, 77.36, "WARD-05", "10 days", 3900),
    ("Frequent voltage drops damaging home appliances in Sitapur Sector 2.", "English", "Electricity", "Voltage Fluctuation", "Medium", 28.52, 77.24, "WARD-03", "18 days", 5500),
    ("सीतापुर के प्राथमिक स्कूल के पास खुला नाला बच्चों के लिए जानलेवा साबित हो सकता है।", "Hindi", "Sanitation", "Open Drain Hazard", "Critical", 28.54, 77.26, "WARD-03", "30 days", 3200),
    ("Pedestrian foot-overbridge lift non-operational at Central Metro terminal for 2 months.", "English", "Public Transport", "Accessibility Deficit", "Medium", 28.66, 77.23, "WARD-06", "60 days", 8000),
    ("High-mast street light at Central Circle blinking and sparking dangerously.", "English", "Electricity", "Public Safety Hazard", "High", 28.62, 77.24, "WARD-06", "3 days", 5000),
    ("आनंद विहार में कूड़ा उठाने वाली गाड़ी 4 दिन से नहीं आई है, बदबू से सांस लेना मुश्किल है।", "Hindi", "Waste Management", "Waste Collection Delay", "Medium", 28.66, 77.33, "WARD-02", "4 days", 4100),
    ("Sewage backflow into basement shops in Anand Vihar commercial complex.", "English", "Sanitation", "Sewage Backflow", "High", 28.65, 77.34, "WARD-02", "5 days", 2800),
    ("सुभाष नगर के पार्क में टूटे झूले और अंधेरा, असामाजिक तत्वों का जमावड़ा रहता है।", "Hindi", "Public Safety", "Park Maintenance & Safety", "Medium", 28.61, 77.13, "WARD-04", "45 days", 1900),
    ("Broadband fiber lines cut during unauthorized road digging in Subhash Nagar.", "English", "Digital Connectivity", "Fiber Cut Outage", "Medium", 28.63, 77.16, "WARD-04", "7 days", 4500),
    ("Sub-center in Kalyanpur requires an auxiliary nurse midwife (ANM) urgently.", "English", "Healthcare", "Staff Shortage", "High", 28.73, 77.38, "WARD-05", "35 days", 2900),
    ("पानी का प्रेशर इतना कम है कि पहली मंजिल पर भी पानी नहीं चढ़ पा रहा।", "Hindi", "Water", "Low Pressure", "Low", 28.64, 77.31, "WARD-02", "12 days", 1500),
    ("Illegal construction debris dumped along arterial drainage channel in Sitapur.", "English", "Waste Management", "Illegal Dumping", "High", 28.56, 77.22, "WARD-03", "14 days", 6200),
    ("कल्याणपुर से मुख्य सड़क तक का 5 किमी संपर्क मार्ग दलदल बन चुका है।", "Hindi", "Roads", "Unpaved Mud Track", "Critical", 28.76, 77.35, "WARD-05", "90 days", 5000),
    ("Potholes causing frequent traffic jams at Anand Vihar border flyover junction.", "English", "Roads", "Potholes & Congestion", "Medium", 28.67, 77.31, "WARD-02", "20 days", 35000),
    ("Community toilet complex in Rampur has no running water or sanitation staff.", "English", "Sanitation", "Public Toilet Disrepair", "High", 28.73, 77.11, "WARD-01", "30 days", 3000),
    ("बिजली के लटकते नंगे तार बच्चों के स्कूल के रास्ते में खतरनाक बने हुए हैं।", "Hindi", "Electricity", "Exposed Wire Hazard", "Critical", 28.75, 77.17, "WARD-01", "6 days", 2400),
    ("Mobile network signal tower out of battery backup during power cuts in Kalyanpur.", "English", "Digital Connectivity", "Tower Outage", "High", 28.79, 77.40, "WARD-05", "15 days", 7000),
    ("Rampur main canal gate rusted and jammed, causing localized water-logging in fields.", "English", "Water", "Irrigation / Canal Damage", "High", 28.70, 77.15, "WARD-01", "28 days", 4800),
    ("कल्याणपुर के आंगनवाड़ी केंद्र में पीने के पानी और पंखों की व्यवस्था नहीं है।", "Hindi", "Education", "Anganwadi Deficit", "Medium", 28.72, 77.39, "WARD-05", "60 days", 1200),
    ("Traffic signal at Central Ring Road crossing out of order for 48 hours.", "English", "Public Safety", "Traffic Signal Failure", "High", 28.61, 77.20, "WARD-06", "2 days", 25000),
    ("Hospital emergency entry blocked by haphazard roadside parking in Subhash Nagar.", "English", "Healthcare", "Emergency Access Blocked", "High", 28.64, 77.10, "WARD-04", "9 days", 5200),
    ("सार्वजनिक नलों पर पानी के लिए रोज झगड़े हो रहे हैं, समय पर आपूर्ति सुनिश्चित की जाए।", "Hindi", "Water", "Supply Schedule Conflict", "Medium", 28.74, 77.14, "WARD-01", "10 days", 2000),
    ("Street sweeping abandoned for 2 weeks in Sitapur Industrial worker colonies.", "English", "Sanitation", "Sweeping Abandoned", "Medium", 28.51, 77.25, "WARD-03", "14 days", 4500),
    ("Transformer explosion risk: transformer oil leaking continuously near Rampur market.", "English", "Electricity", "Oil Leak & Explosion Risk", "Critical", 28.76, 77.12, "WARD-01", "3 days", 6000),
    ("स्कूल की बाउंड्री वॉल गिर गई है, आवारा पशु स्कूल परिसर में घुस रहे हैं।", "Hindi", "Education", "School Safety", "High", 28.77, 77.42, "WARD-05", "20 days", 950),
    ("Severe waterlogging at Central Bus Underpass during morning rush hours.", "English", "Roads", "Drainage & Waterlogging", "High", 28.65, 77.22, "WARD-06", "5 days", 16000),
    ("Water tanker mafia charging exorbitant rates in Rampur due to municipal dry taps.", "English", "Water", "Supply Exploitation", "High", 28.73, 77.13, "WARD-01", "15 days", 3500)
]

for i, item in enumerate(extra_samples):
    feedback_list.append({
        "id": f"CF-2026-EXT-{i+1:03d}",
        "timestamp": (base_time - timedelta(days=i, hours=i*2)).isoformat(),
        "language": item[1],
        "original_text": item[0],
        "normalized_text": item[0],
        "category": item[2],
        "subcategory": item[3],
        "severity": item[4],
        "location": item[7],
        "latitude": item[5],
        "longitude": item[6],
        "administrative_region": item[7],
        "duration": item[8],
        "affected_population_estimate": item[9],
        "evidence_status": "VERIFIED" if i % 3 == 0 else "PENDING",
        "privacy_status": "SANITIZED",
        "manipulation_risk": "LOW",
        "cluster_id": "HOTSPOT-WATER-RAMPUR" if item[2] == "Water" and item[7] == "WARD-01" else ("HOTSPOT-HEALTH-KALYANPUR" if item[2] == "Healthcare" and item[7] == "WARD-05" else "UNCLUSTERED")
    })

pd.DataFrame(feedback_list).to_csv(os.path.join(DATA_DIR, "demo_feedback.csv"), index=False)
print(f"Data generation complete: {len(feedback_list)} feedback records saved to data/demo_feedback.csv")

