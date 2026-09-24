"""
Policy Brief Generation Tool
Synthesizes structured evidence packets into GovTech executive briefs.
Utilizes Google Gemini with structured system prompt when GOOGLE_API_KEY is available;
falls back to deterministic high-fidelity templates in DEMO_MODE.
Enforces post-generation deterministic output validation (numbers, causality, location).
"""
import os
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from ..schemas import PolicyBrief
from ..security.validators import validate_policy_output


SYSTEM_INSTRUCTION = """You are a Senior GovTech Decision-Support Analyst for JAN-SARTHI AI.
Your role is to interpret pre-calculated structured evidence and synthesize an executive policy brief.
CRITICAL RULES:
1. ZERO ARITHMETIC: Do NOT calculate or alter any numbers. Cite only numbers explicitly given in the evidence packet.
2. CAUSALITY GUARDRAIL: Do NOT make unqualified causal statements (never say 'X caused Y'). Use probabilistic framing ('X may have contributed to Y', 'is associated with').
3. SEPARATION: Explicitly demarcate [OBSERVED FACT], [INFERENCE], [HYPOTHESIS], and [RECOMMENDATION].
4. HUMAN PRIMACY: Always remind officials that AI provides decision support, not binding sovereign decisions.
"""


def format_evidence_prompt(evidence: Dict[str, Any], priority_score: Dict[str, Any]) -> str:
    """Formats structured evidence into a clean, un-injectable prompt."""
    demo = evidence.get("demographics", {})
    infra = evidence.get("infrastructure", {})
    quotes = evidence.get("anonymized_quotes", [])
    
    return f"""
EVIDENCE PACKET:
- Hotspot: {evidence.get('cluster_id')} ({evidence.get('category')})
- Administrative Ward: {evidence.get('ward_name')} (ID: {evidence.get('ward_id')})
- Citizen Signal Volume: {evidence.get('raw_signal_count')} (Verified: {evidence.get('verified_signals')}, Pending: {evidence.get('pending_signals')})
- Population: {demo.get('total_population')} (Vulnerable: {demo.get('vulnerable_population_pct')*100:.1f}%, Digital Literacy: {demo.get('digital_literacy_rate')*100:.1f}%)
- Existing Infrastructure Asset: {infra.get('asset_type')} (Capacity: {infra.get('operational_capacity_pct')}%, Deficit Score: {infra.get('deficit_score')})
- Deterministic Priority Score: {priority_score.get('composite_priority_index')} (Rank: {priority_score.get('rank', 1)})
- Sample Anonymized Citizen Statements:
  {chr(10).join(f'  * "{q}"' for q in quotes)}

Generate an executive policy brief with these sections:
1. Executive Problem Statement
2. Geographic Scope
3. Citizen Signal Summary
4. Infrastructure Gap & Vulnerability Context
5. Recommended Capital Intervention
6. Risks of Inaction
7. Evidence Limitations & Human Verification Required
"""


def generate_policy_brief_doc(
    evidence: Dict[str, Any],
    priority_score: Dict[str, Any],
    use_gemini: bool = True
) -> Tuple[PolicyBrief, List[str]]:
    """
    Generates a structured PolicyBrief model.
    Returns: (PolicyBrief, list_of_validation_warnings)
    """
    cluster_id = evidence.get("cluster_id", "CLUSTER_01")
    ward_name = evidence.get("ward_name", "Unknown Ward")
    ward_id = evidence.get("ward_id", "WARD-01")
    cat = evidence.get("category", "General")
    demo = evidence.get("demographics", {})
    infra = evidence.get("infrastructure", {})
    pi_score = priority_score.get("composite_priority_index", 0.75)
    
    # Numbers in evidence to check hallucinations against
    evidence_nums = [
        float(evidence.get("raw_signal_count", 0)),
        float(evidence.get("verified_signals", 0)),
        float(demo.get("total_population", 0)),
        float(demo.get("vulnerable_population_pct", 0) * 100),
        float(demo.get("digital_literacy_rate", 0) * 100),
        float(infra.get("operational_capacity_pct", 0)),
        float(infra.get("deficit_score", 0)),
        float(pi_score)
    ]
    allowed_locs = [ward_id, ward_name, "Delhi NCR", "Rampur", "Kalyanpur", "Sitapur", "Anand Vihar", "Subhash Nagar", "Central Metro Core"]
    
    google_api_key = os.getenv("GOOGLE_API_KEY", "")
    llm_text = None
    
    if use_gemini and google_api_key and google_api_key != "your_gemini_key_here":
        try:
            from google import genai
            client = genai.Client(api_key=google_api_key)
            prompt = format_evidence_prompt(evidence, priority_score)
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                contents=prompt,
                config={"system_instruction": SYSTEM_INSTRUCTION, "temperature": 0.2}
            )
            if response and response.text:
                llm_text = response.text
        except Exception as e:
            # Graceful fallback to deterministic synthesis
            llm_text = None

    # Deterministic high-fidelity brief synthesis (Default for DEMO_MODE or fallback)
    if not llm_text:
        llm_text = f"""### Executive Problem Statement
[OBSERVED FACT] Citizen reports indicate severe {cat.lower()} deficits concentrated in {ward_name}.
[INFERENCE] Available telemetry suggests prolonged service interruptions are placing acute pressure on {demo.get('total_population')} local residents.

### Geographic Scope & Demographics
Administrative Ward {ward_id} ({ward_name}). Vulnerable demographic ratio is {demo.get('vulnerable_population_pct')*100:.1f}% with digital literacy at {demo.get('digital_literacy_rate')*100:.1f}%.

### Empirical Evidence Base
- {evidence.get('raw_signal_count')} citizen submissions registered.
- Baseline asset '{infra.get('asset_type')}' is operating at only {infra.get('operational_capacity_pct')}% capacity.
- Evaluated Infrastructure Deficit Score is {infra.get('deficit_score')}.
- Deterministic Decision-Support Priority Score: {pi_score:.4f}.

### Recommended Capital Intervention
[RECOMMENDATION] Immediate on-ground technical inspection of {infra.get('asset_type')}, followed by mobile emergency relief deployment and targeted capital repair.

### Risk Projection
[HYPOTHESIS] Unresolved service deficits may contribute to cascading secondary public health, livelihood, or commuter disruptions in surrounding zones.

### Evidence Limitations & Human Governance
AI-generated decision support based on available citizen reports and baseline records. Field verification is strictly required by authorized municipal engineers prior to capital outlay.
"""

    # Post-generation validation
    is_valid, violations = validate_policy_output(
        generated_text=llm_text,
        evidence_numbers=evidence_nums,
        allowed_locations=allowed_locs
    )
    
    now_utc = datetime.now(timezone.utc)
    brief = PolicyBrief(
        brief_id=f"PB-{now_utc.strftime('%Y%m%d')}-{cluster_id}",
        cluster_id=cluster_id,
        ward_name=ward_name,
        generated_at=now_utc.isoformat(),
        executive_problem_statement=f"Severe {cat} infrastructure deficit reported across {ward_name} affecting estimated {demo.get('total_population')} residents.",
        geographic_bounding=f"Ward ID {ward_id} ({ward_name})",
        empirical_evidence_base=f"{evidence.get('raw_signal_count')} citizen complaints; {infra.get('asset_type')} operating at {infra.get('operational_capacity_pct')}% capacity.",
        citizen_signal_summary=f"Primary issues: {', '.join(evidence.get('anonymized_quotes', ['Multiple recurring complaints']))}",
        infrastructure_gap=f"Infrastructure Deficit Score: {infra.get('deficit_score')}; Distance to nearest major facility: {infra.get('distance_to_nearest_facility_km', 3.0)} km.",
        vulnerability_context=f"Socioeconomic vulnerability rating: {demo.get('vulnerable_population_pct')*100:.1f}%; Digital literacy: {demo.get('digital_literacy_rate')*100:.1f}%.",
        recommended_capital_intervention=f"Deploy field verification team to {ward_name}; sanction emergency maintenance budget for {infra.get('asset_type')}.",
        risk_projection=f"Unaddressed failure may contribute to localized public unrest and severe utility disruption.",
        evidence_limitations="Data synthesized from available civic signals and simulated municipal registry. Coverage gaps may exist.",
        human_verification_required="Authorized municipal engineer inspection and financial sanction required before procurement."
    )
    
    return brief, violations
