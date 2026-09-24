"""
Infrastructure Category & Severity Extraction Tool
Extracts canonical category codes, subcategories, and severity metrics across Hindi, Bengali, and English.
"""
import re
from typing import Tuple, Dict, Any


CATEGORIES = [
    "Water", "Roads", "Electricity", "Healthcare", "Education",
    "Sanitation", "Waste Management", "Public Transport", "Digital Connectivity", "Public Safety"
]

CATEGORY_KEYWORDS = {
    "Water": [
        "पानी", "पेयजल", "जल संकट", "जल आपूर्ति", "जल स्तर", "नल", "हैंडपंप", "टंकी", "पाइप", "दूषित पानी", "पুকুর", "জল",
        "water", "drinking water", "borewell", "leakage", "pipeline", "contamination", "tanker"
    ],
    "Roads": [
        "सड़क", "गड्ढे", "मार्ग", "पुल", "फ्लाईओवर", "रास्ता", "খানাখন্দ",
        "road", "pothole", "highway", "asphalt", "pavement", "bypass", "traffic", "bridge"
    ],
    "Electricity": [
        "बिजली", "करंट", "तार", "ट्रांसफार्मर", "कटौती", "विद्युत", "বিদ্যুৎ", "11kv", "feeder", "सबस्टेशन",
        "electricity", "power", "blackout", "feeder", "transformer", "voltage", "pole", "wires", "grid"
    ],
    "Healthcare": [
        "अस्पताल", "दवा", "डॉक्टर", "स्वास्थ्य", "इलाज", "अस्पताल", "অ্যাম্বুলেন্স", "ওষুধ", "হাসপাতাল",
        "hospital", "doctor", "health", "dispensary", "phc", "ambulance", "medicine", "nurse"
    ],
    "Education": [
        "स्कूल", "विद्यालय", "शिक्षक", "कक्षा", "आंगनवाड़ी", "স্কুল",
        "school", "college", "teacher", "classroom", "anganwadi", "education", "books"
    ],
    "Sanitation": [
        "शौचालय", "सीवर", "गटर", "गंदगी", "नाली", "পয়ঃনিষ্কাশন",
        "toilet", "sewer", "drainage", "sewage", "gutter", "drain", "overflow", "sanitation"
    ],
    "Waste Management": [
        "कूड़ा", "कचरा", "डंपिंग", "सफाई", "ময়লা",
        "garbage", "waste", "trash", "dumping", "rubbish", "sweeping", "debris"
    ],
    "Public Transport": [
        "बस", "मेट्रो", "ऑटो", "टर्मिनल", "বাস",
        "bus", "metro", "transit", "terminal", "depot", "transport", "station"
    ],
    "Digital Connectivity": [
        "इंटरनेट", "नेटवर्क", "मोबाइल", "टावर", "इंटरनेट",
        "internet", "wifi", "broadband", "fiber", "mobile tower", "kiosk", "network"
    ],
    "Public Safety": [
        "सुरक्षा", "स्ट्रीट लाइट", "अंधेरा", "खतरा", "पुलिस", "নিরাপত্তা",
        "safety", "street light", "crime", "lighting", "police", "harassment", "hazard"
    ]
}

SEVERITY_KEYWORDS = {
    "Critical": ["emergency", "urgent", "dying", "deaths", "collapsed", "fatal", "outbreak", "आपातकालीन", "मौतें", "जानलेवा", "पूरी तरह बंद", "বিপদজনক", "জরুরি"],
    "High": ["severe", "broken", "overflowing", "contamination", "heavy", "डेंजरस", "भारी", "गंभीर", "दूषित", "खतरा"],
    "Medium": ["delay", "frequent", "inconvenient", "समस्या", "परेशानी", "धीमा", "महीने से"],
    "Low": ["request", "suggest", "minor", "सुझाव", "अनुरोध"]
}


def extract_category_and_severity(text: str) -> Tuple[str, str, str]:
    """
    Extracts (Category, Subcategory, Severity) from citizen input text.
    """
    normalized = text.lower()
    
    # 1. Category extraction
    detected_cat = "General Infrastructure"
    max_cat_hits = 0
    for cat, kws in CATEGORY_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw.lower() in normalized)
        if hits > max_cat_hits:
            max_cat_hits = hits
            detected_cat = cat
            
    # Default fallback if no match
    if max_cat_hits == 0:
        detected_cat = "Roads"  # Common civic default
        
    # 2. Severity extraction
    detected_sev = "Medium"
    for sev in ["Critical", "High", "Low"]:
        if any(kw in normalized for kw in SEVERITY_KEYWORDS[sev]):
            detected_sev = sev
            break
            
    # 3. Subcategory heuristics
    subcat = f"{detected_cat} Service Deficit"
    if "leak" in normalized or "pipe" in normalized or "लीकेज" in normalized:
        subcat = "Pipeline Damage"
    elif "doctor" in normalized or "medicine" in normalized or "दवा" in normalized:
        subcat = "Medical Staff/Supplies Deficit"
    elif "pothole" in normalized or "गड्ढे" in normalized:
        subcat = "Potholes & Pavement Hazard"
    elif "transformer" in normalized or "ट्रांसफार्मर" in normalized:
        subcat = "Transformer / Substation Failure"
        
    return detected_cat, subcat, detected_sev
