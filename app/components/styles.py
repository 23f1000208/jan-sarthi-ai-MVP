"""
UI Styles and GovTech Theme for JAN-SARTHI AI
Provides accessible, serious public-sector intelligence dashboard styling.
"""

GOVTECH_CSS = """
<style>
    /* Main Layout & Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Top Banner Header */
    .gov-header {
        background: linear-gradient(135deg, #0b2545 0%, #133c55 100%);
        color: white;
        padding: 1.2rem 1.8rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 6px solid #ff9933;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .gov-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .gov-subtitle {
        font-size: 0.95rem;
        color: #d8e2dc;
        margin-top: 0.3rem;
        margin-bottom: 0;
    }
    
    /* KPI Metric Cards */
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border-top: 3px solid #133c55;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #0b2545;
        margin: 0;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748b;
        margin-top: 0.2rem;
    }
    
    /* Badge styling */
    .badge-demo {
        background-color: #fef3c7;
        color: #92400e;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #fcd34d;
        display: inline-block;
    }
    .badge-live {
        background-color: #d1fae5;
        color: #065f46;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #6ee7b7;
        display: inline-block;
    }
    .badge-critical {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    
    /* Policy Brief Paper style */
    .policy-brief-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 1.8rem;
        border-left: 5px solid #0284c7;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-top: 1rem;
    }
    
    /* Audit Callout */
    .audit-card {
        background-color: #f1f5f9;
        border-left: 4px solid #64748b;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.6rem;
        border-radius: 4px;
        font-size: 0.85rem;
    }
</style>
"""
