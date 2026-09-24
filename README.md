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

```mermaid
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
