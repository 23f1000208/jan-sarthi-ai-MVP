Here is the complete, competition-grade **`README.md`** text for your project. 

You can copy and paste this directly into a file named **`README.md`** in your project root or create/edit it directly on GitHub:

---

# JAN-SARTHI AI (जन-सारथी AI)
### Multilingual AI Citizen Feedback & Infrastructure Prioritization Platform

> **"Every voice becomes evidence. Every evidence-backed need becomes visible."**

**Competition:** Build with AI — Code for Communities  
**Track:** Track 1 — AI for Digital Public Infrastructure & Governance  
**BRICS Theme:** Innovation  
**License:** Apache 2.0 (Designed in alignment with Digital Public Good principles)

---

## 📌 Executive Summary

Governments struggle to consolidate fragmented citizen feedback across diverse regional languages and connect it with national capital expenditure priorities. This results in misaligned public spending, unaddressed infrastructure deficits, linguistic exclusion, and severe demographic representation bias—where digitally connected urban areas generate high complaint volume while marginalized rural and peri-urban communities remain invisible.

**JAN-SARTHI AI** is a multilingual civic intelligence decision-support platform designed as a **Digital Public Good (DPG)**. It transforms unstructured citizen voice and text feedback into structured, geo-referenced, and evidence-fused infrastructure demand hotspots, calculating transparent, auditable priority scores while keeping authorized human officials in full control of sovereign capital allocation.

---

## 🚀 Key Innovations

1. **Zero-LLM Arithmetic Rule:**
   Gemini is strictly barred from calculating numbers, averages, or priority ranks. Pure Python deterministic computation handles all multi-criteria decision analysis (MCDA) and statistical aggregates.
2. **Demographic Representation-Bias Correction:**
   Complaint volume is not treated as equal to public need. Raw demand density is scaled inversely against local digital literacy and internet connectivity metrics to protect marginalized rural/tribal voices.
3. **Multi-Tier Security & Untrusted Boundary Firewall:**
   Pre-LLM prompt-injection defense, edge PII scrubbing (compliant with India's DPDP Act, Brazil's LGPD, and South Africa's POPIA), anti-astroturfing velocity detection, and post-LLM numeric/causality verification.
4. **Google ADK & Gemini Orchestration:**
   Google ADK acts as the orchestrator coordinating modular Python tools; Google Gemini 2.5 Flash synthesizes structured, evidence-grounded policy briefs.
5. **Human-in-the-Loop Sovereign Governance:**
   AI provides decision support; authorized officials verify evidence, challenge scores, and record justifications in an immutable audit ledger.

---

## 🏛️ System Architecture


flowchart TD
    subgraph Ingestion["1. Ingestion & Security Boundary"]
        A1["Citizen Input: Web / WhatsApp / IVR / SMS"] --> B1["Prompt-Injection Scanner"]
        B1 -->|Allowed| B2["Edge PII Scrubber (DPDP Act / LGPD)"]
    end

    subgraph NLP["2. Multilingual Processing & Extraction"]
        B2 --> C1["Language Identifier (Hindi, Bengali, Tamil, English)"]
        C1 --> C2["Text Normalizer & Canonicalization"]
        C2 --> C3["Category & Severity Extractor"]
        C3 --> C4["Anti-Astroturfing & Sybil Detector"]
    end

    subgraph Spatial["3. Spatial-Temporal Intelligence Engine"]
        C4 --> D1["DBSCAN Geospatial Clustering"]
        D1 --> D2["Temporal Sliding Window Anomaly Detection"]
        D2 --> D3["Dynamic Hotspot Identification"]
    end

    subgraph Fusion["4. Multi-Domain Evidence Fusion"]
        D3 --> E1["Ward Demographics & Vulnerability (Census)"]
        D3 --> E2["Municipal Asset Inventory & Deficits"]
        E1 & E2 --> E4["Structured Evidence Packet"]
    end

    subgraph Deterministic["5. Deterministic Priority Engine (Zero-LLM Math)"]
        E4 --> F1["Raw Demand Index (DWI_raw)"]
        F1 --> F2["Representation-Bias Calibration (DWI_cal)"]
        E4 --> F3["Demographic Vulnerability Index (DVI)"]
        E4 --> F4["Infrastructure Gap Score (IGS)"]
        E4 --> F5["Urgency & Duration Score (US)"]
        F2 & F3 & F4 & F5 --> F6["Composite Priority Score (Spatial MCDA)"]
    end

    subgraph Orchestration["6. Google ADK & Gemini Synthesis"]
        F6 & E4 --> G1["Google ADK Orchestrator Root Agent"]
        G1 --> G2["Google Gemini 2.5 Flash"]
        G2 --> G3["Deterministic Output Validator"]
    end

    subgraph Governance["7. Human-in-the-Loop Sovereign Review"]
        G3 --> H1["GovTech Command Center & Policy Brief"]
        H1 --> H2["Official Review: Verify / Challenge / Re-weight"]
        H2 --> H3["Immutable Audit Ledger & Action Dispatch"]
    end
```

---

## 📊 Priority Scoring Methodology (MCDA)

Priority is calculated deterministically using spatial Multi-Criteria Decision Analysis:

$$PI = w_1 \cdot \text{DWI}_{\text{cal}} + w_2 \cdot \text{DVI} + w_3 \cdot \text{IGS} + w_4 \cdot \text{US} + w_5 \cdot \text{EBS} + w_6 \cdot \text{DAS} - w_7 \cdot \text{MP}$$

* **$\text{DWI}_{\text{cal}}$ (Calibrated Demand Weight Index):** Representation-bias adjusted feedback volume.
  $$\text{DWI}_{\text{calibrated}, i} = \text{DWI}_{\text{raw}, i} \times \left(\frac{1}{\text{Digital Literacy Rate}_i \times \text{Connectivity Index}_i}\right)$$
* **$\text{DVI}$ (Demographic Vulnerability Index):** Socio-economic vulnerability from census records.
* **$\text{IGS}$ (Infrastructure Gap Score):** Measured baseline asset capacity deficit.
* **$\text{US}$ (Urgency Score):** Severity distribution weighting (Critical = 1.0, High = 0.7, Medium = 0.4, Low = 0.1).
* **$\text{EBS}$ (Economic & Public Reach Score):** Population beneficiary reach.
* **$\text{DAS}$ (National Development Plan Alignment):** Alignment with national infrastructure missions.
* **$\text{MP}$ (Manipulation Penalty):** Penalty applied if astroturfing bot surges are flagged.

---

## 🛠️ Technology Stack

| Component | Technology | Role |
|---|---|---|
| **Deterministic Math** | Python 3.12, Pandas, NumPy, Scikit-learn | Multi-criteria scoring, clustering, KPI math |
| **Agent Orchestration** | Google ADK (`google-adk` 2.9.2) | Root orchestrator agent coordinating modular tools |
| **Generative AI** | Google Gemini (`google-genai` 2.23.0) | Context-bounded policy brief synthesis |
| **GovTech Portal** | Streamlit, PyDeck, Altair | 10-page executive command center & interactive maps |
| **Data Validation** | Pydantic v2 | Strict schema validation across all data layers |
| **Automated Testing** | Pytest, Pytest-Cov | Comprehensive automated unit and guardrail test suite |
| **Containerization** | Docker, OCI Standards | Non-root production container for Google Cloud Run |

---

## 🧪 Automated Test Suite (100% Pass Rate)

Run the test suite to verify ingestion, deterministic scoring, and security guardrails:

```bash
pytest -v
```

### Test Coverage Summary:
* `tests/test_agent.py`: Google ADK Root Agent tool coordination & policy brief pipeline.
* `tests/test_analytics.py`: Zero-LLM deterministic KPI metrics & distributions.
* `tests/test_bias.py`: Representation-bias inverse access weighting & zero-division guards.
* `tests/test_feedback.py`: Multilingual script detection, normalization, category extraction.
* `tests/test_priority.py`: MCDA formula execution, weight configurations, penalty deductions.
* `tests/test_security.py`: Prompt injection interception, PII scrubbing, rejection of hallucinated numbers, fictitious locations, and unqualified causality.

**Result:** `21 passed in 4.19s (100% pass rate)`

---

## 💻 Quickstart (Local Run)

### 1. Prerequisites
* Python 3.10+ (tested on Python 3.12)
* Optional: Google Gemini API Key (if omitted, platform runs seamlessly in **DEMO MODE**)

### 2. Setup Virtual Environment
```bash
# Clone repository
git clone https://github.com/23f1000208/jan-sarthi-ai-MVP.git
cd jan-sarthi-ai-MVP

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
cp .env.example .env
```

### 3. Launch GovTech Command Center
```bash
python -m streamlit run app/streamlit_app.py --server.port 8501
```
Open **http://localhost:8501** in your browser.

---

## 🐳 Docker & Google Cloud Run Deployment

### Run Container Locally
```bash
docker build -t jan-sarthi-ai:v1 .
docker run -p 8080:8080 -e DEMO_MODE=true jan-sarthi-ai:v1
```

### Deploy to Google Cloud Run (Serverless Scale-to-Zero)
```bash
gcloud run deploy jan-sarthi-ai-portal \
    --source . \
    --region us-central1 \
    --port 8080 \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 2 \
    --set-env-vars DEMO_MODE=true,GOOGLE_API_KEY=$GOOGLE_API_KEY,GEMINI_MODEL=gemini-2.5-flash
```

---

## 🌐 BRICS Economy Portability Matrix

The platform is configured via `country_config.yaml` to ensure zero code modification when deploying across BRICS nations:

| Domain | India (IN) | Brazil (BR) | South Africa (ZA) | China (CN) |
|---|---|---|---|---|
| **Primary Languages** | Hindi, Bengali, Tamil, English, 22 Scheduled | Portuguese, Indigenous Dialects | English, Zulu, Xhosa, Afrikaans | Mandarin, Regional Dialects |
| **Identity DPI** | Aadhaar / MOSIP | CPF / Gov.br | National Smart ID / MOSIP | Resident Identity Card |
| **Privacy Framework** | DPDP Act 2023 | LGPD | POPIA | PIPL |
| **National Portal** | CPGRAMS / Bhashini | Fala.BR (CGU) | Presidential Hotline | 12345 Hotlines / City Brain |

---

## 📄 Digital Public Good Alignment

Built in accordance with the 9 standards of the **Digital Public Goods Alliance (DPGA)**:
* **Open Source:** Permissive Apache 2.0 license.
* **Open Standards:** GeoJSON boundaries, OpenAPI schemas, REST/gRPC interoperability.
* **Privacy by Design:** Automated edge scrubbing of PII prior to data fusion.
* **Do No Harm:** Representation-bias recalibration and human-in-the-loop sovereign decision boundaries.

---

## ⚖️ Governance Mandate
*JAN-SARTHI AI provides decision support. AI never autonomously commits public capital or makes binding sovereign choices. Authorized human officials remain responsible for all final infrastructure allocations.*
```
