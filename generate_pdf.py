import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, ListFlowable, ListItem
)

def build_pdf(output_filename="sanjeevi_ai_ml_data_engineer.pdf"):
    # Target 0.5 in margins for maximum content space and clean layout
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = HexColor("#0f172a")      # Slate 900
    ACCENT = HexColor("#2563eb")       # Royal Blue
    TEXT_MAIN = HexColor("#1e293b")    # Slate 800
    TEXT_MUTED = HexColor("#475569")   # Slate 600
    BORDER_COLOR = HexColor("#cbd5e1") # Slate 300

    # Custom Styles
    name_style = ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        alignment=1 # Center
    )

    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        alignment=1
    )

    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
        alignment=1
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_MAIN,
        alignment=4 # Justify
    )

    bullet_style = ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_MAIN,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=2.5
    )

    role_title_style = ParagraphStyle(
        'RoleTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=PRIMARY,
        keepWithNext=True
    )

    company_sub_style = ParagraphStyle(
        'CompanySub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=ACCENT,
        keepWithNext=True
    )

    subpart_heading_style = ParagraphStyle(
        'SubpartHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=TEXT_MAIN,
        spaceBefore=3,
        spaceAfter=2,
        keepWithNext=True
    )

    story = []

    # --- Header ---
    story.append(Paragraph("SANJEEVI M", name_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("AI/ML Data Engineer", title_style))
    story.append(Spacer(1, 4))
    
    contacts = (
        'Chennai, Tamil Nadu, India &nbsp;|&nbsp; +91 8610889030 &nbsp;|&nbsp; '
        '<a href="mailto:sanjayvm66@gmail.com"><font color="#2563eb">sanjayvm66@gmail.com</font></a> &nbsp;|&nbsp; '
        '<a href="https://www.linkedin.com/in/sanjeevi-m"><font color="#2563eb">LinkedIn</font></a> &nbsp;|&nbsp; '
        '<a href="https://github.com/askmrsanjay"><font color="#2563eb">GitHub</font></a> &nbsp;|&nbsp; '
        '<a href="https://public.tableau.com/app/profile/sanjeevi.m/vizzes"><font color="#2563eb">Tableau</font></a> &nbsp;|&nbsp; '
        '<a href="https://askmrsanjay.github.io/sanjeevi_portfolio/"><font color="#2563eb">Online Portfolio</font></a>'
    )
    story.append(Paragraph(contacts, contact_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=4))

    # --- Professional Summary ---
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=0, spaceAfter=3))
    summary_text = (
        "<b>AI/ML Data Engineer</b> with 4.5+ years of enterprise experience specializing in cloud data platform automation "
        "(Snowflake, Databricks, Delta Lake, PySpark) and applied GenAI/agentic tooling (Anthropic Claude API, multi-agent systems, "
        "tool-use/function calling). Proven expertise architecting metadata-driven dynamic data masking frameworks auto-generating "
        "124+ role-aware Snowflake views and deploying resilient multi-agent platforms with circuit breakers and backoff retries. "
        "Comfortable owning high-impact initiatives from analysis through POC, production deployment, and executive stakeholder demos."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 3))

    # --- Technical Expertise ---
    story.append(Paragraph("TECHNICAL EXPERTISE", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=0, spaceAfter=3))
    skills = [
        "<b>AI / GenAI & Agentic Systems:</b> Anthropic Claude API (tool-use / function calling), Multi-agent orchestration (Supervisor-Specialist architecture), Stateful memory, Prompt-driven tool routing, LLM workflow automation.",
        "<b>Data Platforms & Lakehouse:</b> Snowflake (Stored procedures, dynamic SQL, Masking policies, Row access policies), Databricks (Jobs, Delta Lake, notebooks, Unity Catalog), ADLS Gen2, Apache Iceberg, Kafka.",
        "<b>Languages:</b> Python, SQL, PySpark.",
        "<b>Integration & DevOps:</b> REST APIs (Azure DevOps, SharePoint / Microsoft Graph, GitHub), HashiCorp Vault, Power Automate, ADF, Docker, Git, CI/CD, Airflow.",
        "<b>Practices & Governance:</b> Production hardening (Circuit breakers, Exponential backoff/retry, Automated testing), Data Governance (DGO certification), Agile / SAFe delivery.",
        "<b>BI & Visualization:</b> Tableau Desktop / Server, Streamlit."
    ]
    for s in skills:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{s}", bullet_style))
    story.append(Spacer(1, 3))

    # --- Verified Certifications ---
    story.append(Paragraph("VERIFIED CERTIFICATIONS", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=0, spaceAfter=3))
    certs = [
        "<b>Claude Certified Architect Foundations</b> &mdash; <a href=\"https://www.credly.com/badges/90042b67-2d12-4936-84d1-f3e9f82de530\"><font color=\"#2563eb\">Verify on Credly</font></a>",
        "<b>Databricks Certified Generative AI Engineer Associate</b> &mdash; <a href=\"https://credentials.databricks.com/4405b202-1f50-4869-949f-a65244adac1a#acc.8CUuo6BV\"><font color=\"#2563eb\">Verify on Databricks</font></a>",
        "<b>Databricks Certified Machine Learning Engineer Associate</b> &mdash; <a href=\"https://credentials.databricks.com/b022c191-8dab-41a1-9047-67e312877d6e#acc.2cIUZfC3\"><font color=\"#2563eb\">Verify on Databricks</font></a>",
        "<b>Databricks Certified Data Engineer Professional</b> &mdash; <a href=\"https://credentials.databricks.com/2a57bd0c-b169-48ce-a646-180184bc704a\"><font color=\"#2563eb\">Verify on Databricks</font></a>"
    ]
    for c in certs:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{c}", bullet_style))
    story.append(Spacer(1, 3))

    # --- Professional Experience ---
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=0, spaceAfter=3))

    # Cognizant
    cog_header = "<b>Cognizant Technology Solutions</b> (Client: Humana) &nbsp;|&nbsp; <i>Oct 2025 – Present</i>"
    story.append(Paragraph(cog_header, role_title_style))
    story.append(Paragraph("AI/ML Data Engineer — ODMP (Operational Data Management Platform)", company_sub_style))
    story.append(Spacer(1, 2))

    # Part 1
    story.append(Paragraph("<u>Snowflake Provisioning & Dynamic Field-Masking Automation</u>", subpart_heading_style))
    cog_bullets_1 = [
        "<b>Metadata-Driven Masking Framework:</b> Designed and deployed a dynamic masking engine via a Python stored procedure (<code>SP_GENERATE_MASKED_VIEW</code>) reading role/entitlement config rules to auto-generate secure, role-aware Snowflake views with column masking and row-level filtering.",
        "<b>Enterprise Scale (POC to 124+ Views):</b> Scaled framework from a single-view POC to 124 production views across the Sales Consumer schema, handling complex wide schemas with 160+ columns.",
        "<b>Automated Provisioning Ingestion:</b> Built the <code>ACCOUNT_PROVISIONING</code> and <code>FIELD_MASKING</code> data models with a Databricks ingestion pipeline from business SharePoint Excel files (via Microsoft Graph/REST API) into Snowflake with automated IT email alerts.",
        "<b>Data Quality & Governance:</b> Triaged and resolved production schema drift, DDL mismatches, and role-masking validation defects; conducted milestone architecture demos for product owners and analytics leads."
    ]
    for b in cog_bullets_1:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{b}", bullet_style))

    # Part 2
    story.append(Spacer(1, 2))
    story.append(Paragraph("<u>Data Acquisition & Cross-Platform Lakehouse Integration</u>", subpart_heading_style))
    cog_bullets_2 = [
        "<b>End-to-End API Acquisition Pipeline:</b> Delivered a compliant API pipeline acquiring 10-year historical and incremental Call Simulator training data into Snowflake (staging → target, compliance schema, DGO-certified source) and authored the Interface Control Document (ICD).",
        "<b>Delta Lake Hydration (Microsoft Fabric POC):</b> Hydrated priority fact tables from Snowflake into Databricks Delta tables, including a dedicated round powering a Microsoft Fabric AI Analytics POC.",
        "<b>MADL Access Governance:</b> Led analysis and access provisioning for Member Admin Data Lake (MADL) policy data, orchestrating intake requests, cross-team approvals, and Databricks table readiness for downstream analytics.",
        "<b>Architecture POCs & Production Triage:</b> Conducted architectural POCs on Apache Iceberg integration for Snowflake ODMP domains and sourcing Milestone Tracker data from external DEP systems; resolved UAT reporting pipeline defects (e.g., Genesys enriched voice mismatches)."
    ]
    for b in cog_bullets_2:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{b}", bullet_style))

    story.append(Spacer(1, 4))

    # Infosys
    inf_header = "<b>Infosys Ltd</b> (Clients: Nike and Apple) &nbsp;|&nbsp; <i>May 2022 – Oct 2025</i>"
    story.append(Paragraph(inf_header, role_title_style))
    story.append(Paragraph("Technology Analyst", company_sub_style))
    story.append(Spacer(1, 2))
    inf_bullets = [
        "Designed and maintained end-to-end ETL pipelines in Azure Databricks processing large-scale enterprise data for Nike and Apple.",
        "Engineered Change Data Capture (CDC) pipelines for customer billing and sales orders achieving &lt;1% latency.",
        "Built automated reporting pipelines eliminating manual Tableau refreshes across multiple operational units.",
        "Developed real-time anomaly detection dashboards for Apple’s Data Operations team with automated Slack alerts for incident escalation."
    ]
    for b in inf_bullets:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{b}", bullet_style))

    story.append(Spacer(1, 3))

    # --- Key Projects & Initiatives ---
    story.append(Paragraph("KEY PROJECTS & INITIATIVES", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=0, spaceAfter=3))

    projects = [
        ("<b>ODMP Multi-Agent Engineering Assistant</b> | <i>Claude API, Multi-Agent, Python, Azure DevOps, Databricks</i>",
         "Built a Claude API-powered multi-agent assistant enabling natural-language platform operations across 5 engineering systems (Azure DevOps, Git, Databricks, ADLS, SharePoint). Designed with a Supervisor-Specialist architecture, multi-turn memory, and 7 production-hardened resilience patterns including circuit breakers and exponential backoff."),
        ("<b>Snowpark Rule Framework</b> | <i>Humana Inc. | Snowpark, Snowflake, JSON</i>",
         "Config-driven Snowpark transformation engine dynamically parsing rules from JSON specifications, dramatically reducing manual SQL boilerplate and maintenance overhead."),
        ("<b>Extract Framework</b> | <i>Humana Inc. | PySpark, Databricks, Unity Catalog, ADLS Gen2</i>",
         "Parameter-driven PySpark framework to extract Snowflake datasets into Delta format on ADLS Gen2 with zero pipeline code modifications."),
        ("<b>Real-Time E-Commerce Data Lakehouse</b> | <i>Apache Iceberg, Kafka, Spark Streaming, MinIO, Airflow, Great Expectations</i>",
         "Engineered a medallion architecture (Bronze/Silver/Gold) streaming lakehouse with automated schema validation and data quality assertions. (<a href=\"https://github.com/askmrsanjay/data_engineering_projects.git\"><font color=\"#2563eb\">GitHub</font></a>)"),
        ("<b>Real-Time Analytics Pipeline</b> | <i>Kafka, PySpark, Elasticsearch, Kibana</i>",
         "Implemented high-throughput streaming analytics pipeline ingesting e-commerce clickstream and transaction events with sub-second Elasticsearch indexing. (<a href=\"https://github.com/askmrsanjay/Real-Time-E-Commerce-Analytics-Pipeline\"><font color=\"#2563eb\">GitHub</font></a>)"),
        ("<b>Career Flow Engine</b> | <i>Python, Selenium, BeautifulSoup, Pandas</i>",
         "Automated job market intelligence scraper monitoring job openings across 15+ global markets with personalized alert filtering. (<a href=\"https://github.com/askmrsanjay/Product_company_job_alert.git\"><font color=\"#2563eb\">GitHub</font></a>)")
    ]

    for p_title, p_desc in projects:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{p_title}", bullet_style))
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{p_desc}", bullet_style))
        story.append(Spacer(1, 1))

    story.append(Spacer(1, 2))

    # --- Education ---
    story.append(Paragraph("EDUCATION", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=0, spaceAfter=3))
    story.append(Paragraph("<b>Post Graduate in Statistics</b> &nbsp;|&nbsp; Presidency College, Chennai (May 2019)", body_style))

    # Build Document
    doc.build(story)
    print(f"Successfully generated {output_filename} ({os.path.getsize(output_filename)} bytes)")

if __name__ == '__main__':
    build_pdf()
