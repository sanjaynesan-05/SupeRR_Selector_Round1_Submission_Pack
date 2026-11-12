#!/usr/bin/env python3
"""
Publication-Quality PDF Generator for SupeRR Selector Round 1: Pressure Reliability Report.
Generated for Rajasthan Royals War Room using PyMuPDF (fitz).
"""
import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path

def create_report():
    doc = fitz.open()

    # Colors
    c_navy = (0.0, 0.17, 0.38)       # #002B49 / RR Navy
    c_pink = (0.85, 0.0, 0.51)       # #D90082 / RR Pink
    c_dark = (0.07, 0.11, 0.18)      # #121C2E
    c_gray = (0.40, 0.45, 0.52)      # #667385
    c_light_bg = (0.96, 0.97, 0.98)  # #F5F7FA
    c_line = (0.85, 0.88, 0.92)

    bat = pd.read_csv('top_10_batters.csv')
    bowl = pd.read_csv('top_10_bowlers.csv')

    # Helper: draw running header and footer
    def add_decorations(page, page_num, total_pages=9):
        rect = page.rect
        if page_num > 1:
            # Running header
            page.draw_line(fitz.Point(40, 36), fitz.Point(rect.width - 40, 36), color=c_line, width=0.75)
            page.insert_text(fitz.Point(40, 28), "RAJASTHAN ROYALS WAR ROOM | SUPERR SELECTOR SEASON 2", fontsize=8, fontname="helv", color=c_gray)
            page.insert_text(fitz.Point(rect.width - 150, 28), "ROUND 1: PRESSURE REPORT", fontsize=8, fontname="helv", color=c_pink)
        
        # Running footer
        page.draw_line(fitz.Point(40, rect.height - 36), fitz.Point(rect.width - 40, rect.height - 36), color=c_line, width=0.75)
        page.insert_text(fitz.Point(40, rect.height - 24), "IPL 2027 Auction Strategy • Strictly Compliant with BCCI Regulations", fontsize=8, fontname="helv", color=c_gray)
        page.insert_text(fitz.Point(rect.width - 75, rect.height - 24), f"Page {page_num} of {total_pages}", fontsize=8, fontname="helv", color=c_gray)

    # ================= PAGE 1: TITLE & COVER =================
    p1 = doc.new_page(width=595, height=842) # A4
    
    # Top banner background
    p1.draw_rect(fitz.Rect(0, 0, 595, 230), color=None, fill=c_navy)
    p1.draw_rect(fitz.Rect(0, 224, 595, 230), color=None, fill=c_pink)

    p1.insert_text(fitz.Point(45, 65), "SUPERR SELECTOR SEASON 2", fontsize=13, fontname="helv", fontfile=None, color=(1, 1, 1))
    p1.insert_text(fitz.Point(45, 110), "ROUND 1 | PRESSURE RELIABILITY REPORT", fontsize=22, fontname="hebo", color=(1, 1, 1))
    p1.insert_text(fitz.Point(45, 140), "Identifying the Most Reliable Batters & Bowlers Under Pressure for IPL 2027", fontsize=12, fontname="helv", color=(0.9, 0.9, 0.95))
    p1.insert_text(fitz.Point(45, 185), "Rajasthan Royals Proprietary War Room Analytics • 100% IPL Rules Compliant", fontsize=10, fontname="hebo", color=c_pink)

    # Summary Metadata Grid (Card style)
    meta_box = fitz.Rect(45, 260, 550, 480)
    p1.draw_rect(meta_box, color=c_line, fill=c_light_bg)

    grid_items = [
        ("Data Window", "2022 – 2026 (Audited Match Feeds)"),
        ("Competitions", "IPL Competitions + T20 Internationals"),
        ("Matches Analysed", "837 matches with complete ball-by-ball records"),
        ("Deliveries Evaluated", "193,988 legal delivery records (Innings 1 & 2)"),
        ("Pressure Deliveries", "110,750 pressure events (53,137 Bat / 57,613 Bowl)"),
        ("IPL Eligibility Filter", "Compliant: Pakistani players excluded as per BCCI rules"),
        ("Clean Eligible Pool", "84 Qualified Batters | 131 Qualified Bowlers"),
        ("Core Index Model", "SupeRR Pressure Reliability Index (SPRI v2.0)"),
        ("Top Ranked Batter", "Shashank Singh (SPRI: 87.29 | SR: 185.5 | Avg: 47.6)"),
        ("Top Ranked Bowler", "Noor Ahmad (SPRI: 81.08 | Econ: 8.04 | 35 Wickets)")
    ]

    y_pos = 285
    for lbl, val in grid_items:
        p1.insert_text(fitz.Point(65, y_pos), lbl, fontsize=9.5, fontname="hebo", color=c_navy)
        p1.insert_text(fitz.Point(210, y_pos), val, fontsize=9.5, fontname="helv", color=c_dark)
        p1.draw_line(fitz.Point(65, y_pos + 6), fitz.Point(530, y_pos + 6), color=(0.9, 0.92, 0.95), width=0.5)
        y_pos += 20

    # Executive Note Box
    exec_box = fitz.Rect(45, 505, 550, 750)
    p1.draw_rect(exec_box, color=c_line, fill=(1, 1, 1))
    p1.draw_rect(fitz.Rect(45, 505, 50, 750), color=None, fill=c_pink)

    p1.insert_text(fitz.Point(65, 530), "WAR ROOM EXECUTIVE HIGHLIGHT", fontsize=12, fontname="hebo", color=c_navy)
    p1.insert_textbox(
        fitz.Rect(65, 545, 535, 740),
        "This report delivers the finalized, rule-compliant player recommendations for the Rajasthan Royals at the IPL 2027 auction.\n\n"
        "Key Governance & Strategic Enhancements:\n"
        "1. BCCI/IPL Regulations Compliance: Under official tournament rules, Pakistani players cannot feature in IPL auctions. To ensure our auction models reflect actionable talent, all Pakistani players (68 identified) have been removed prior to percentile scoring.\n"
        "2. Strict Phase-Matched Normalization: Every player's performance under pressure is measured against their own phase-matched baseline in the exact same match phase (Powerplay, Middle, Death), eliminating death-over volume bias.\n"
        "3. High-Impact Target Profiles: The model uncovers critical domestic assets like Shashank Singh (#1 Batter, SPRI 87.29) and Naman Dhir (#2 Batter, SPRI 82.33), alongside elite bowling anchors Nathan Ellis (#5 Bowler, specialist death master) and Noor Ahmad (#1 Bowler, wrist-spin master for Jaipur's SMS Stadium).",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.45
    )
    add_decorations(p1, 1)

    # ================= PAGE 2: EXECUTIVE SUMMARY & DATA AUDIT =================
    p2 = doc.new_page(width=595, height=842)
    p2.insert_text(fitz.Point(40, 60), "1. Executive Summary & Regulatory Compliance", fontsize=15, fontname="hebo", color=c_navy)
    p2.insert_textbox(
        fitz.Rect(40, 72, 555, 175),
        "The objective of Round 1 is to evaluate domestic and international performance data, isolate performances where match pressure is peak, and identify the most reliable players whom the Rajasthan Royals should target for the IPL 2027 auction.\n\n"
        "A critical operational constraint for IPL franchises is player availability and league compliance. As per BCCI policy, Pakistani players are ineligible for the IPL. Including them in rankings would distort auction percentiles and provide false targets. We have rigorously audited all player records and removed Pakistani players prior to computing the relative percentile rankings. This ensures the SupeRR Pressure Reliability Index (SPRI) directly represents the genuine auction market.",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )

    p2.insert_text(fitz.Point(40, 195), "Final Compliant Top Picks Overview", fontsize=12, fontname="hebo", color=c_navy)
    
    # Mini table for top 5
    p2.draw_rect(fitz.Rect(40, 205, 555, 335), color=c_line, fill=c_light_bg)
    p2.insert_text(fitz.Point(50, 222), "Rank", fontsize=9, fontname="hebo", color=c_navy)
    p2.insert_text(fitz.Point(90, 222), "Top Batters (Compliant)", fontsize=9, fontname="hebo", color=c_navy)
    p2.insert_text(fitz.Point(230, 222), "SPRI", fontsize=9, fontname="hebo", color=c_navy)
    p2.insert_text(fitz.Point(310, 222), "Top Bowlers (Compliant)", fontsize=9, fontname="hebo", color=c_navy)
    p2.insert_text(fitz.Point(460, 222), "SPRI", fontsize=9, fontname="hebo", color=c_navy)
    p2.draw_line(fitz.Point(40, 230), fitz.Point(555, 230), color=c_pink, width=1)

    y_t = 248
    for i in range(5):
        b_row = bat.iloc[i]
        bw_row = bowl.iloc[i]
        p2.insert_text(fitz.Point(50, y_t), f"#{i+1}", fontsize=9, fontname="hebo", color=c_pink)
        p2.insert_text(fitz.Point(90, y_t), f"{b_row.player_name}", fontsize=9, fontname="helv", color=c_dark)
        p2.insert_text(fitz.Point(230, y_t), f"{b_row.score:.2f}", fontsize=9, fontname="hebo", color=c_navy)
        p2.insert_text(fitz.Point(310, y_t), f"{bw_row.player_name}", fontsize=9, fontname="helv", color=c_dark)
        p2.insert_text(fitz.Point(460, y_t), f"{bw_row.score:.2f}", fontsize=9, fontname="hebo", color=c_navy)
        p2.draw_line(fitz.Point(40, y_t + 5), fitz.Point(555, y_t + 5), color=c_line, width=0.5)
        y_t += 20

    p2.insert_text(fitz.Point(40, 360), "2. Data Preparation & Comprehensive Audit", fontsize=15, fontname="hebo", color=c_navy)
    p2.insert_textbox(
        fitz.Rect(40, 372, 555, 520),
        "The underlying dataset was constructed by joining competition metadata to match schedules and granular delivery records across 2022–2026. Data verification highlights:\n"
        "• Competition Scope: Retained IPL editions and official T20 Internationals. Non-IPL domestic franchise leagues were excluded to ensure high competition standards.\n"
        "• Delivery Data: 193,988 legal delivery records from the first and second innings across 837 matches were evaluated. Super overs were excluded.\n"
        "• DLS Handling: 23 rain-affected matches with revised DLS targets were incorporated. Targets and progress metrics were calibrated against effective revised innings limits.\n"
        "• Dismissal Attribution: Bowler wickets were strictly restricted to Bowled, Caught, LBW, Stumped, and Hit Wicket. Run-outs and obstruction dismissals were not credited to the bowler.",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )

    # Audit Table
    p2.draw_rect(fitz.Rect(40, 530, 555, 760), color=c_line, fill=(1, 1, 1))
    p2.insert_text(fitz.Point(55, 550), "Audit Checkpoint Item", fontsize=9.5, fontname="hebo", color=c_navy)
    p2.insert_text(fitz.Point(350, 550), "Audit Result / Verification Status", fontsize=9.5, fontname="hebo", color=c_navy)
    p2.draw_line(fitz.Point(40, 558), fitz.Point(555, 558), color=c_navy, width=1)

    aud_items = [
        ("Total Match Records in Metadata", "853 matches"),
        ("Matches with Full Ball-by-Ball Data", "837 matches (367 IPL, 470 T20I)"),
        ("Innings 1 & 2 Delivery Rows Analysed", "193,988 deliveries"),
        ("Batter-Pressure Deliveries / Matches", "53,137 deliveries across 823 matches"),
        ("Bowler-Pressure Deliveries / Matches", "57,613 deliveries across 799 matches"),
        ("Pakistani Players Excluded (IPL Rule)", "68 players removed prior to scoring"),
        ("Clean Eligible Candidate Pool", "84 Qualified Batters / 131 Qualified Bowlers"),
        ("Missing Key Identifiers (Striker/Bowler)", "0 (Zero missing keys)"),
        ("Duplicate Delivery Keys", "0 (Zero duplicates)")
    ]
    y_aud = 575
    for lbl, res in aud_items:
        p2.insert_text(fitz.Point(55, y_aud), lbl, fontsize=9, fontname="helv", color=c_dark)
        p2.insert_text(fitz.Point(350, y_aud), res, fontsize=9, fontname="hebo", color=c_navy)
        p2.draw_line(fitz.Point(40, y_aud + 5), fitz.Point(555, y_aud + 5), color=(0.92, 0.93, 0.95), width=0.5)
        y_aud += 19

    add_decorations(p2, 2)

    # ================= PAGE 3: DEFINING PRESSURE =================
    p3 = doc.new_page(width=595, height=842)
    p3.insert_text(fitz.Point(40, 60), "3. Defining Match Pressure Contextually", fontsize=15, fontname="hebo", color=c_navy)
    p3.insert_textbox(
        fitz.Rect(40, 72, 555, 140),
        "A common pitfall in cricket analytics is treating all late-overs deliveries as equally pressurized. In reality, a chase requiring 30 runs from 30 balls with 8 wickets in hand is low pressure for the batter, but high pressure for the bowler. Conversely, chasing 12 runs an over with 5 wickets down represents extreme batting pressure. SPRI deploys role-specific criteria:",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )

    # Box 1: Batter Rules
    p3.draw_rect(fitz.Rect(40, 150, 555, 305), color=c_line, fill=c_light_bg)
    p3.draw_rect(fitz.Rect(40, 150, 44, 305), color=None, fill=c_pink)
    p3.insert_text(fitz.Point(55, 172), "BATTER PRESSURE CRITERIA (53,137 Deliveries Identified)", fontsize=11, fontname="hebo", color=c_navy)
    p3.insert_textbox(
        fitz.Rect(55, 185, 540, 295),
        "• Second Innings (Chasing Demand):\n"
        "   - Innings progress ≥ 50% (overs 11-20) and Required Run Rate (RRR) ≥ 8.5\n"
        "   - Wickets remaining ≤ 5 and RRR ≥ 7.5\n"
        "   - Death overs (progress ≥ 75%, overs 16-20) and RRR is tight between 6.0 and 12.0\n"
        "• First Innings (Collapse & Acceleration Constraint):\n"
        "   - Progress ≥ 75% with at least 4 wickets lost\n"
        "   - Progress 50%–75% with at least 6 wickets lost (rescuing a severe top-order collapse)",
        fontsize=9, fontname="helv", color=c_dark, lineheight=1.4
    )

    # Box 2: Bowler Rules
    p3.draw_rect(fitz.Rect(40, 320, 555, 475), color=c_line, fill=c_light_bg)
    p3.draw_rect(fitz.Rect(40, 320, 44, 475), color=None, fill=c_navy)
    p3.insert_text(fitz.Point(55, 342), "BOWLER PRESSURE CRITERIA (57,613 Deliveries Identified)", fontsize=11, fontname="hebo", color=c_navy)
    p3.insert_textbox(
        fitz.Rect(55, 355, 540, 465),
        "• Second Innings (Defending in Competitive Situations):\n"
        "   - Innings progress ≥ 50%, opposition retains at least 3 wickets, and RRR is between 6.5 and 12.0\n"
        "   (Excludes blowouts where the opposition is already collapsed or victory is guaranteed)\n"
        "• First Innings (Opponent Launch Platform):\n"
        "   - Progress ≥ 75% and batting side has at least 4 wickets in hand\n"
        "   - Progress 50%–75% and batting side has at least 6 wickets in hand",
        fontsize=9, fontname="helv", color=c_dark, lineheight=1.4
    )

    # Explanatory narrative
    p3.insert_text(fitz.Point(40, 495), "Why These Rules Deliver Better Auction Intelligence", fontsize=13, fontname="hebo", color=c_navy)
    p3.insert_textbox(
        fitz.Rect(40, 510, 555, 750),
        "1. Avoids Inflaters and Low-Leverage 'Garbage Time':\n"
        "Many T20 metrics reward batters who smash boundaries when the game is already won or lost. SPRI filters out deliveries where RRR is trivial or hopelessly out of reach (>15 RRR in 17th over with 2 wickets), isolating situations where decisions directly alter match win probability.\n\n"
        "2. Prevents Unfair Bowling Penalties:\n"
        "A bowler bowling in the 19th over against an opposition 9 wickets down needing 45 runs is not under genuine pressure. Conversely, defending 28 off 18 balls against set top-order hitters is maximum pressure. SPRI captures this asymmetry.\n\n"
        "3. Captures Collapse Recovery:\n"
        "First-innings runs scored from 40/4 are vastly more valuable than runs scored from 140/1. The first-innings collapse criteria isolate batters who can rebuild innings without stalling the strike rate.",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )
    add_decorations(p3, 3)

    # ================= PAGE 4: PERFORMANCE MEASUREMENT & SCORING =================
    p4 = doc.new_page(width=595, height=842)
    p4.insert_text(fitz.Point(40, 60), "4. Phase-Matched Baselines & SPRI Framework", fontsize=15, fontname="hebo", color=c_navy)
    p4.insert_textbox(
        fitz.Rect(40, 72, 555, 145),
        "To assess whether a player genuinely elevates their game under pressure, their pressure performance must be compared to a meaningful benchmark. Comparing a death-overs pressure strike rate to an overall T20 career strike rate is mathematically flawed because death overs naturally have higher scoring rates.\n\n"
        "SPRI solves this by computing a Phase-Matched Baseline: comparing each player's pressure balls to their own non-pressure balls within the exact same innings number and phase (Powerplay, Middle, Death).",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )

    # Batting Framework Box
    p4.draw_rect(fitz.Rect(40, 155, 555, 290), color=c_line, fill=c_light_bg)
    p4.insert_text(fitz.Point(55, 178), "BATTING SPRI ARCHITECTURE (Weighted Percentile Aggregate)", fontsize=11, fontname="hebo", color=c_navy)
    
    bat_weights = [
        ("Pressure Strike Rate (Pctl)", "25%", "Measures scoring velocity under demanding pressure conditions"),
        ("Δ Strike Rate Improvement (Pctl)", "25%", "Exceeding own phase-matched baseline (elevation factor)"),
        ("Pressure Batting Average (Pctl)", "20%", "Wicket preservation and ability to finish chases"),
        ("Δ Batting Average Improvement (Pctl)", "15%", "Elevation in dismissal avoidance when stakes are high"),
        ("Boundary Percentage (Pctl)", "15%", "Ability to find the boundary rope without consuming dots")
    ]
    y_bw = 200
    for w_name, w_val, w_desc in bat_weights:
        p4.insert_text(fitz.Point(55, y_bw), f"• {w_name}:", fontsize=9, fontname="hebo", color=c_pink)
        p4.insert_text(fitz.Point(230, y_bw), w_val, fontsize=9, fontname="hebo", color=c_navy)
        p4.insert_text(fitz.Point(270, y_bw), f"— {w_desc}", fontsize=8.5, fontname="helv", color=c_gray)
        y_bw += 17

    # Bowling Framework Box
    p4.draw_rect(fitz.Rect(40, 305, 555, 440), color=c_line, fill=c_light_bg)
    p4.insert_text(fitz.Point(55, 328), "BOWLING SPRI ARCHITECTURE (Weighted Percentile Aggregate)", fontsize=11, fontname="hebo", color=c_navy)

    bowl_weights = [
        ("Inverse Pressure Economy (Pctl)", "25%", "Run containment when batters are aggressively hunting runs"),
        ("Economy Rate Improvement (Pctl)", "25%", "Conceding fewer runs per over under pressure vs baseline"),
        ("Wickets per 100 Balls (Pctl)", "20%", "Clutch breakthrough rate under pressure"),
        ("Δ Wicket Rate Improvement (Pctl)", "15%", "Elevation in breakthrough capability in pressure overs"),
        ("Dot Ball Percentage (Pctl)", "15%", "Ability to bowl scoreless balls and create scoreboard pressure")
    ]
    y_bww = 350
    for w_name, w_val, w_desc in bowl_weights:
        p4.insert_text(fitz.Point(55, y_bww), f"• {w_name}:", fontsize=9, fontname="hebo", color=c_navy)
        p4.insert_text(fitz.Point(230, y_bww), w_val, fontsize=9, fontname="hebo", color=c_pink)
        p4.insert_text(fitz.Point(270, y_bww), f"— {w_desc}", fontsize=8.5, fontname="helv", color=c_gray)
        y_bww += 17

    # Reliability Shrinkage
    p4.insert_text(fitz.Point(40, 460), "Sample Reliability Shrinkage Formula", fontsize=13, fontname="hebo", color=c_navy)
    p4.insert_textbox(
        fitz.Rect(40, 475, 555, 570),
        "A player who faces 20 balls and hits 50 runs has an extraordinary strike rate, but low statistical reliability. To prevent flash-in-the-pan anomalies from ranking ahead of proven campaigners, SPRI applies an empirical shrinkage factor:\n\n"
        "Reliability Multiplier = √[ Balls / (Balls + 120) ] × √[ Matches / (Matches + 10) ]\n"
        "Final SPRI Score = 100 × Raw Score × [ 0.65 + 0.35 × Reliability Multiplier ]\n\n"
        "This formula guarantees that while high volume alone cannot propel an inefficient player to the top, genuine performance over a robust sample receives maximum confidence.",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )

    # Minimum Eligibility Thresholds Box
    p4.draw_rect(fitz.Rect(40, 585, 555, 750), color=c_line, fill=c_light_bg)
    p4.insert_text(fitz.Point(55, 608), "MINIMUM ELIGIBILITY CRITERIA (Audit Gate)", fontsize=11, fontname="hebo", color=c_navy)
    p4.insert_textbox(
        fitz.Rect(55, 620, 540, 740),
        "• Batters: Minimum 120 pressure legal balls faced, across at least 12 pressure matches, with at least 8 dismissals recorded, and at least 60 matched baseline balls.\n"
        "• Bowlers: Minimum 120 pressure legal balls bowled, across at least 12 pressure matches, with at least 60 matched baseline balls.\n\n"
        "Sensitivity Robustness:\n"
        "When the threshold was raised to 150 pressure balls and 15 pressure matches (stricter filter), 10 out of 10 batters remained in the top 10, and 8 out of 10 bowlers remained. This proves the ranking is exceptionally robust and stable against sample size variations.",
        fontsize=9, fontname="helv", color=c_dark, lineheight=1.4
    )
    add_decorations(p4, 4)

    # ================= PAGE 5: TOP 10 BATTERS VISUAL & ANALYSIS =================
    p5 = doc.new_page(width=595, height=842)
    p5.insert_text(fitz.Point(40, 60), "5. Top 10 Batters Analysis & Visual Breakdown", fontsize=15, fontname="hebo", color=c_navy)
    p5.insert_textbox(
        fitz.Rect(40, 72, 555, 125),
        "The chart below displays the Top 10 Batters ranked by SPRI Score (bars) compared against their Pressure Strike Rate (solid line) and their phase-matched Baseline Strike Rate (dashed line). Notice how top performers like Shashank Singh and Naman Dhir dramatically elevate their scoring velocity when pressure peaks.",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )

    # Insert Batters Chart Image
    p5.draw_rect(fitz.Rect(40, 130, 555, 385), color=c_line, fill=(1, 1, 1))
    p5.insert_image(fitz.Rect(45, 135, 550, 380), filename="chart_top10_batters.png")

    # Analytical Commentary
    p5.insert_text(fitz.Point(40, 405), "Key Analytical Takeaways for Batting Recruitment", fontsize=13, fontname="hebo", color=c_navy)
    p5.insert_textbox(
        fitz.Rect(40, 420, 555, 750),
        "1. Shashank Singh (#1, SPRI 87.29) — The Ultimate Domestic Choke-Proof Finisher:\n"
        "Shashank's metrics are extraordinary. Facing 359 balls under pressure across 45 matches, he maintains an average of 47.6 (only 14 dismissals) and strikes at 185.5. His strike rate increases by +71.5 over his non-pressure baseline—the highest delta in the tournament. He represents the cleanest Indian domestic lower-order solution in the entire auction pool.\n\n"
        "2. Naman Dhir (#2, SPRI 82.33) — Maximum Aggression & Boundary Percentage:\n"
        "Naman Dhir boasts the highest boundary rate in the top 10 at 30.2% and a blistering 198.2 strike rate under pressure (+57.2 over baseline). He provides an aggressive counter-punching option who can bat from #3 to #6, preventing pressure from accumulating.\n\n"
        "3. Mark Chapman (#3, SPRI 81.06) — Subcontinental Spin Maestro:\n"
        "Chapman records a 183.3 strike rate under pressure and a 36.0 average. His left-handed ability to sweep and disrupt spin lengths makes him an ideal tactical weapon for Jaipur's slower tracks.\n\n"
        "4. Shreyas Iyer (#4, SPRI 76.50) & Heinrich Klaasen (#5, SPRI 73.50):\n"
        "Iyer scored 699 pressure runs striking at 196.3, proving his clutch credentials in playoff and chase scenarios. Klaasen remains the undisputed global benchmark for middle-overs spin destruction, absorbing 418 pressure balls with an 188.5 strike rate.",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )
    add_decorations(p5, 5)

    # ================= PAGE 6: TOP 10 BATTERS EVIDENCE TABLE =================
    p6 = doc.new_page(width=595, height=842)
    p6.insert_text(fitz.Point(40, 60), "6. Top 10 Batters Evidence Table & Player Profiles", fontsize=15, fontname="hebo", color=c_navy)
    
    # Table headers
    t_box = fitz.Rect(40, 80, 555, 330)
    p6.draw_rect(t_box, color=c_line, fill=(1, 1, 1))
    p6.draw_rect(fitz.Rect(40, 80, 555, 102), color=None, fill=c_pink)

    p6.insert_text(fitz.Point(46, 95), "Rnk", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(68, 95), "Player Name", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(165, 95), "Nat", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(195, 95), "SPRI", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(230, 95), "Balls", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(265, 95), "Runs", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(300, 95), "Outs", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(330, 95), "SR (P)", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(375, 95), "Base SR", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(425, 95), "Δ SR", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(465, 95), "Avg (P)", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p6.insert_text(fitz.Point(510, 95), "Bnd %", fontsize=8, fontname="hebo", color=(1, 1, 1))

    y_row = 120
    for idx, r in bat.head(10).iterrows():
        nat = "IND" if r.player_name in ["Shashank Singh", "Naman Dhir", "Shreyas Iyer", "Jitesh Sharma", "Ishan Kishan"] else "OVS"
        p6.insert_text(fitz.Point(46, y_row), f"#{idx+1}", fontsize=8.5, fontname="hebo", color=c_pink)
        p6.insert_text(fitz.Point(68, y_row), f"{r.player_name}", fontsize=8.5, fontname="hebo", color=c_dark)
        p6.insert_text(fitz.Point(165, y_row), nat, fontsize=8, fontname="helv", color=c_gray)
        p6.insert_text(fitz.Point(195, y_row), f"{r.score:.2f}", fontsize=8.5, fontname="hebo", color=c_navy)
        p6.insert_text(fitz.Point(230, y_row), f"{int(r.balls_p)}", fontsize=8.5, fontname="helv", color=c_dark)
        p6.insert_text(fitz.Point(265, y_row), f"{int(r.runs_p)}", fontsize=8.5, fontname="helv", color=c_dark)
        p6.insert_text(fitz.Point(300, y_row), f"{int(r.outs_p)}", fontsize=8.5, fontname="helv", color=c_dark)
        p6.insert_text(fitz.Point(330, y_row), f"{r.sr_p:.1f}", fontsize=8.5, fontname="hebo", color=c_dark)
        p6.insert_text(fitz.Point(375, y_row), f"{r.sr_n_matched:.1f}", fontsize=8.5, fontname="helv", color=c_gray)
        p6.insert_text(fitz.Point(425, y_row), f"+{r.delta_sr:.1f}", fontsize=8.5, fontname="hebo", color=(0.1, 0.6, 0.3))
        p6.insert_text(fitz.Point(465, y_row), f"{r.avg_p:.1f}", fontsize=8.5, fontname="helv", color=c_dark)
        p6.insert_text(fitz.Point(510, y_row), f"{r.boundary_pct_p*100:.1f}%", fontsize=8.5, fontname="helv", color=c_dark)

        p6.draw_line(fitz.Point(40, y_row + 6), fitz.Point(555, y_row + 6), color=c_line, width=0.5)
        y_row += 21

    # Detailed Tactical Profiles
    p6.insert_text(fitz.Point(40, 355), "Detailed Rajasthan Royals Squad Fit: Top Batters", fontsize=13, fontname="hebo", color=c_navy)

    profiles = [
        ("Shashank Singh (Finisher / #6-#7):",
         "Solves Rajasthan Royals' historic reliance on overseas finishers. Pairing Shashank alongside Shimron Hetmyer and Dhruv Jurel gives RR three clutch finishing options, allowing Rajasthan to field two overseas frontline fast bowlers without compromising lower-order hitting power."),
        ("Donovan Ferreira (3-in-1 Utility Finisher / Ex-RR):",
         "Strikes at 199.3 under pressure with a 28.7% boundary rate. Possesses prior franchise chemistry, provides an overseas wicketkeeper backup to Sanju Samson, and bowls useful off-spin during middle-overs squeezes."),
        ("Jitesh Sharma (Aggressive Indian Keeper-Finisher):",
         "Records a 178.2 pressure SR (+46.8 delta) across 53 matches. Specializes in hitting boundaries from ball one without needing sighter deliveries, reducing pressure on top-order anchors."),
        ("Rovman Powell & Romario Shepherd (Proven Overseas Heavy Hitters):",
         "Both players exhibit massive sample reliability (>570 pressure balls across 75+ matches). Powell's familiarity with Jaipur and Shepherd's 140 km/h pace bowling option make them robust auction options.")
    ]

    y_prof = 375
    for title, desc in profiles:
        p6.insert_text(fitz.Point(40, y_prof), title, fontsize=9.5, fontname="hebo", color=c_pink)
        p6.insert_textbox(fitz.Rect(40, y_prof + 4, 555, y_prof + 55), desc, fontsize=9, fontname="helv", color=c_dark, lineheight=1.35)
        y_prof += 58

    add_decorations(p6, 6)

    # ================= PAGE 7: TOP 10 BOWLERS VISUAL & ANALYSIS =================
    p7 = doc.new_page(width=595, height=842)
    p7.insert_text(fitz.Point(40, 60), "7. Top 10 Bowlers Analysis & Visual Breakdown", fontsize=15, fontname="hebo", color=c_navy)
    p7.insert_textbox(
        fitz.Rect(40, 72, 555, 125),
        "The chart below illustrates the Top 10 Bowlers ranked by SPRI Score (bars) alongside their Pressure Economy (solid line) and phase-matched Baseline Economy (dashed line). Top picks like Noor Ahmad and Sunil Narine choke runs while striking frequently.",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )

    # Insert Bowlers Chart Image
    p7.draw_rect(fitz.Rect(40, 130, 555, 385), color=c_line, fill=(1, 1, 1))
    p7.insert_image(fitz.Rect(45, 135, 550, 380), filename="chart_top10_bowlers.png")

    # Analytical Commentary
    p7.insert_text(fitz.Point(40, 405), "Key Analytical Takeaways for Bowling Recruitment", fontsize=13, fontname="hebo", color=c_navy)
    p7.insert_textbox(
        fitz.Rect(40, 420, 555, 750),
        "1. Noor Ahmad (#1, SPRI 81.08) — The Premier Young Wrist-Spin Asset:\n"
        "Noor Ahmad leads all eligible bowlers in world cricket under pressure. Over 505 pressure balls across 71 matches, he conceded only 8.04 runs per over while taking 35 wickets (6.93% wicket rate) and bowling 35.4% dot balls. At Sawai Mansingh Stadium in Jaipur, where boundary ropes exceed 70 meters, his dipping left-arm wrist-spin makes clearing the fence nearly impossible.\n\n"
        "2. Nathan Ellis (#5, SPRI 74.71) — Specialist Death Bowler Master:\n"
        "Ellis is the absolute premier death-bowling target for RR. Across 328 pressure deliveries, he has taken 27 wickets with an 8.23% wicket rate and 31.7% dot ball rate. His dipping yorkers, back-of-the-hand slower balls, and subtle pace variations make him the perfect partner for Sandeep Sharma in overs 17–20.\n\n"
        "3. Sai Kishore (#6, SPRI 73.75) — Elite Indian Spin Anchor:\n"
        "Sai Kishore delivers a staggering 8.88% wicket rate under pressure (19 wickets in 214 balls) with an economy of 9.20. His tall release point extracts bounce and turn, providing an Indian spin pillar to replace or support the Chahal/Ashwin transition.\n\n"
        "4. Mohsin Khan (#7, SPRI 72.41) — Left-Arm Pace Enforcer:\n"
        "Mohsin Khan offers an elite left-arm pace angle with steep bounce. Under pressure, he improves his economy by +1.69 over his baseline (9.30 vs 10.99) and increases his wicket rate by +4.32%, providing Rajasthan Royals with a devastating powerplay and death enforcer.",
        fontsize=9.5, fontname="helv", color=c_dark, lineheight=1.4
    )
    add_decorations(p7, 7)

    # ================= PAGE 8: TOP 10 BOWLERS EVIDENCE TABLE =================
    p8 = doc.new_page(width=595, height=842)
    p8.insert_text(fitz.Point(40, 60), "8. Top 10 Bowlers Evidence Table & Player Profiles", fontsize=15, fontname="hebo", color=c_navy)

    # Table headers
    t_box = fitz.Rect(40, 80, 555, 330)
    p8.draw_rect(t_box, color=c_line, fill=(1, 1, 1))
    p8.draw_rect(fitz.Rect(40, 80, 555, 102), color=None, fill=c_navy)

    p8.insert_text(fitz.Point(46, 95), "Rnk", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(68, 95), "Player Name", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(165, 95), "Nat", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(195, 95), "SPRI", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(230, 95), "Balls", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(265, 95), "Conc", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(300, 95), "Wkts", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(335, 95), "Econ (P)", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(380, 95), "Base Econ", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(435, 95), "Δ Econ", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(475, 95), "Wkt %", fontsize=8, fontname="hebo", color=(1, 1, 1))
    p8.insert_text(fitz.Point(515, 95), "Dot %", fontsize=8, fontname="hebo", color=(1, 1, 1))

    y_row = 120
    for idx, r in bowl.head(10).iterrows():
        nat = "IND" if r.player_name in ["Sai Kishore", "Mohsin Khan"] else "OVS"
        p8.insert_text(fitz.Point(46, y_row), f"#{idx+1}", fontsize=8.5, fontname="hebo", color=c_pink)
        p8.insert_text(fitz.Point(68, y_row), f"{r.player_name}", fontsize=8.5, fontname="hebo", color=c_dark)
        p8.insert_text(fitz.Point(165, y_row), nat, fontsize=8, fontname="helv", color=c_gray)
        p8.insert_text(fitz.Point(195, y_row), f"{r.score:.2f}", fontsize=8.5, fontname="hebo", color=c_navy)
        p8.insert_text(fitz.Point(230, y_row), f"{int(r.balls_p)}", fontsize=8.5, fontname="helv", color=c_dark)
        p8.insert_text(fitz.Point(265, y_row), f"{int(r.conceded_p)}", fontsize=8.5, fontname="helv", color=c_dark)
        p8.insert_text(fitz.Point(300, y_row), f"{int(r.wkts_p)}", fontsize=8.5, fontname="hebo", color=c_navy)
        p8.insert_text(fitz.Point(335, y_row), f"{r.econ_p:.2f}", fontsize=8.5, fontname="hebo", color=c_dark)
        p8.insert_text(fitz.Point(380, y_row), f"{r.econ_n_matched:.2f}", fontsize=8.5, fontname="helv", color=c_gray)
        econ_sign = "+" if r.delta_econ >= 0 else ""
        econ_color = (0.1, 0.6, 0.3) if r.delta_econ >= 0 else (0.8, 0.2, 0.2)
        p8.insert_text(fitz.Point(435, y_row), f"{econ_sign}{r.delta_econ:.2f}", fontsize=8.5, fontname="hebo", color=econ_color)
        p8.insert_text(fitz.Point(475, y_row), f"{r.wkt_rate_p:.2f}%", fontsize=8.5, fontname="helv", color=c_dark)
        p8.insert_text(fitz.Point(515, y_row), f"{r.dot_pct_p*100:.1f}%", fontsize=8.5, fontname="helv", color=c_dark)

        p8.draw_line(fitz.Point(40, y_row + 6), fitz.Point(555, y_row + 6), color=c_line, width=0.5)
        y_row += 21

    # Detailed Tactical Profiles
    p8.insert_text(fitz.Point(40, 355), "Detailed Rajasthan Royals Squad Fit: Top Bowlers", fontsize=13, fontname="hebo", color=c_navy)

    b_profiles = [
        ("Noor Ahmad (Left-Arm Wrist Spinner / Priority #1):",
         "Jaipur's Sawai Mansingh Stadium features 70m+ square boundaries. Noor's high release, sharp wrong-un, and 8.04 pressure economy give RR an unplayable middle-overs weapon to build pressure and trigger batting collapses."),
        ("Nathan Ellis (Specialist Death Bowler / Priority #1):",
         "The ultimate tactical complement to Sandeep Sharma. Ellis operates with world-class deceptive slower balls and yorkers. Possesses 27 pressure wickets and an 8.23% wicket rate, giving RR a lockdown combination in overs 16–20."),
        ("Sai Kishore (Tall Left-Arm Orthodox Spinner / Domestic Indian Priority):",
         "Gives RR a top-tier Indian spinner who can bowl in the powerplay and middle overs. His domestic Indian status frees up an overseas slot for an extra batter or pace bowling enforcer."),
        ("Mujeeb Ur Rahman & Ish Sodhi (Mystery & Leg-Spin Depth):",
         "Mujeeb (7.47 economy, 8.39% wkt rate) provides powerplay mystery, while Ish Sodhi brings extensive familiarity with Rajasthan Royals' culture and home conditions in Jaipur.")
    ]

    y_prof = 375
    for title, desc in b_profiles:
        p8.insert_text(fitz.Point(40, y_prof), title, fontsize=9.5, fontname="hebo", color=c_navy)
        p8.insert_textbox(fitz.Rect(40, y_prof + 4, 555, y_prof + 55), desc, fontsize=9, fontname="helv", color=c_dark, lineheight=1.35)
        y_prof += 58

    add_decorations(p8, 8)

    # ================= PAGE 9: AUCTION BLUEPRINT, LIMITATIONS & REPRODUCIBILITY =================
    p9 = doc.new_page(width=595, height=842)
    p9.insert_text(fitz.Point(40, 60), "9. Rajasthan Royals 2027 Auction Blueprint & Governance", fontsize=15, fontname="hebo", color=c_navy)
    
    # War Room Blueprint Grid
    p9.draw_rect(fitz.Rect(40, 80, 555, 340), color=c_line, fill=c_light_bg)
    p9.insert_text(fitz.Point(55, 102), "RAJASTHAN ROYALS WAR ROOM AUCTION ROADMAP (IPL 2027)", fontsize=11, fontname="hebo", color=c_navy)

    p9.insert_textbox(
        fitz.Rect(55, 115, 540, 330),
        "• Primary Auction Targets (High Purse Allocation):\n"
        "   1. Nathan Ellis (Overseas Death Specialist) — Non-negotiable bowling priority.\n"
        "   2. Shashank Singh (Indian Lower-Order Finisher) — Fixes finishing and frees overseas slot.\n"
        "   3. Sai Kishore (Indian Left-Arm Spinner) — Locks down Jaipur home advantage.\n\n"
        "• Secondary / Tactical Picks (Purse Maximization):\n"
        "   - Noor Ahmad / Mujeeb Ur Rahman (Overseas Mystery Spin weapon)\n"
        "   - Naman Dhir / Mohsin Khan (High-ceiling domestic Indian power & pace)\n"
        "   - Donovan Ferreira / Ish Sodhi (Proven culture fit and ex-RR loyalty)\n\n"
        "• Simulated 2027 Playing XI Synergy:\n"
        "   Yashasvi Jaiswal, Sanju Samson (C/WK), Naman Dhir / Shreyas Iyer, Riyan Parag, Dhruv Jurel / Chapman, Shashank Singh, Donovan Ferreira [OS1], Sai Kishore, Noor Ahmad [OS2], Nathan Ellis [OS3], Sandeep Sharma / Mohsin Khan. (Impact: Prasidh Krishna).",
        fontsize=9, fontname="helv", color=c_dark, lineheight=1.4
    )

    p9.insert_text(fitz.Point(40, 360), "Analytical Limitations & Appropriate Use", fontsize=13, fontname="hebo", color=c_navy)
    p9.insert_textbox(
        fitz.Rect(40, 375, 555, 570),
        "1. Competition Strength Normalization: While the dataset is restricted to IPL and T20Is, T20I opponents vary in quality. A player who excelled primarily against Associate opposition should be vetted alongside IPL-specific film study before committing top purse.\n"
        "2. Dismissal Opportunity Asymmetry: Lower-order finishers face fewer deliveries per match, creating greater variance in batting averages. SPRI utilizes reliability shrinkage, but scouting teams must assess boundary striking consistency alongside raw averages.\n"
        "3. Relative Index Rather than Future Guarantee: SPRI measures demonstrated past reliability in high-pressure match states. It is not an automated auction valuation model or a physical medical assessment.",
        fontsize=9, fontname="helv", color=c_dark, lineheight=1.4
    )

    p9.insert_text(fitz.Point(40, 585), "Pipeline Reproducibility & Deliverable Verification", fontsize=13, fontname="hebo", color=c_navy)
    p9.insert_textbox(
        fitz.Rect(40, 600, 555, 750),
        "All calculations in this report are 100% reproducible through the accompanying Python pipeline script (`superr_pressure_analysis.py`).\n\n"
        "Accompanying Artifacts in Submission Pack:\n"
        "1. `SupeRR_Selector_Round1_Rankings.xlsx`: Complete workbook containing Top 10 Batters, Top 10 Bowlers, All 84 Eligible Batters, All 131 Eligible Bowlers, Data Audit, and Methodology sheets.\n"
        "2. `dashboard.html` / `index.html`: Fully interactive war room web dashboard featuring real-time filters, radar comparator, and tactical cards.\n"
        "3. `Unstop_Rankings_Copy_Paste.txt`: Clean, rule-compliant list formatted for immediate submission into the Unstop competition dropdowns.",
        fontsize=9, fontname="helv", color=c_dark, lineheight=1.4
    )
    add_decorations(p9, 9)

    # Save document
    out_pdf = "SupeRR_Selector_Round1_Methodology_Report.pdf"
    doc.save(out_pdf)
    doc.close()
    print(f"Report generated successfully: {out_pdf} (9 pages)")

if __name__ == "__main__":
    create_report()
