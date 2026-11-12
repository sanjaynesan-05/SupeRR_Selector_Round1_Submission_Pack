SupeRR Selector Season 2 - Round 1 Submission Pack
Exclusive Rajasthan Royals Proprietary War Room Analytics

DELIVERABLES & SUBMISSION FILES:

1. dashboard.html (and index.html)
   Standalone, interactive Rajasthan Royals War Room Web Dashboard.
   Features executive KPIs, Top 10 Batters & Bowlers cards, Sawai Mansingh Stadium
   (Jaipur) pitch tactics, interactive head-to-head radar comparator, full 215-player
   searchable database with CSV export, and Print-to-PDF ready views.
   Open directly in any modern browser.

2. SupeRR_Selector_Round1_Methodology_Report.pdf
   Official 9-page publication-grade methodology and auction strategy report.
   Includes pressure definitions, mathematical formulas, data audit, sensitivity
   analysis, Top 10 evidence tables, visual charts, and Rajasthan Royals 2027 auction roadmap.

3. SupeRR_Selector_Round1_Rankings.xlsx
   Updated professional Excel workbook with Top 10 Batters, Top 10 Bowlers,
   All 84 Eligible Batters, All 131 Eligible Bowlers, Data Audit, and Methodology sheets.

4. Unstop_Rankings_Copy_Paste.txt
   Clean, rule-compliant ordered lists ready to copy-paste directly into the
   Unstop Round 1 submission form dropdowns.

5. superr_pressure_analysis.py
   Fully reproducible Python pipeline. Automatically enforces BCCI/IPL eligibility
   rules by excluding Pakistani players prior to percentile ranking.
   Run:
       python superr_pressure_analysis.py --data-dir "data set" --out-dir .

COMPLIANCE & METHODOLOGY NOTE:
As per official BCCI and IPL player regulations, Pakistani players are ineligible
for the IPL auction and are excluded from candidate pools prior to relative percentile
scoring. The rankings use 837 matches (367 IPL, 470 T20I) and 193,988 legal delivery records
from 2022 to 2026. Innings 1 and 2 are analysed; super overs are excluded.
