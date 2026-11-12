#!/usr/bin/env python3
"""
Dashboard Builder for SupeRR Selector Round 1: Pressure Reliability Analysis.
Builds an interactive, publication-grade analytics dashboard for Rajasthan Royals War Room.
"""
import json
import pandas as pd
from pathlib import Path

# Load data
bat_df = pd.read_csv('All_Eligible_Batters.csv')
bowl_df = pd.read_csv('All_Eligible_Bowlers.csv')
mapping = pd.read_csv('data set/competition_team_player_mapping.csv')

top_meta = {
    'Shashank Singh': {
        'nat': 'India', 'role': 'Finisher / Lower-Middle Order', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm off break', 'tier': 'Tier 1 Priority Target',
        'why_pressure': 'Phenomenal 185.5 strike rate under pressure (+71.5 jump over non-pressure baseline) and 47.6 pressure average (+31.1 leap). 25.9% boundary rate across 45 pressure matches.',
        'rr_fit': 'Directly solves RR lower-order finishing void at #6/#7 alongside Shimron Hetmyer and Dhruv Jurel. As an Indian power finisher, he eliminates the need to burn an overseas slot on a lower-order hitter, enabling RR to field two frontline overseas bowlers and an overseas anchor.'
    },
    'Naman Dhir': {
        'nat': 'India', 'role': 'Top/Middle Order Aggressor', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm off break', 'tier': 'Tier 1 Priority Target',
        'why_pressure': 'Highest boundary percentage in the top 10 (30.2%) with a blistering 198.2 strike rate under high pressure (+57.2 over baseline). Only 15 dismissals in 222 pressure balls.',
        'rr_fit': 'High-ceiling Indian batting asset. Can bat anywhere in the top 5, counter-attacking pace and spin alike from ball one. Absorbs pressure during powerplay collapses and counter-punches immediately.'
    },
    'Mark Chapman': {
        'nat': 'New Zealand', 'role': 'Middle Order Spin Enforcer', 'bat_style': 'Left Hand Bat', 'bowl_style': 'Slow left-arm orthodox', 'tier': 'Tier 2 Value Pick',
        'why_pressure': '183.3 pressure strike rate (+49.5 over baseline) and 36.0 pressure average. Exceptional clutch record in subcontinental conditions across 25 high-pressure matches.',
        'rr_fit': 'Provides an elite left-handed spin-destroyer in the middle overs. At Sawai Mansingh Stadium, where slow grip defines middle overs, Chapman sweeps, reverses, and lofts with surgical precision.'
    },
    'Shreyas Iyer': {
        'nat': 'India', 'role': 'Middle Order Anchor / Captaincy Core', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm leg break', 'tier': 'Marquee Indian Core',
        'why_pressure': '196.3 pressure strike rate (+27.8 over baseline) with 41.1 pressure average across 44 matches. 699 pressure runs scored under demanding conditions.',
        'rr_fit': 'Elite Indian middle-order anchor and IPL-winning tactical leader. Complements Sanju Samson and Riyan Parag, stabilizing early collapses and unleashing devastation in overs 14–20.'
    },
    'Heinrich Klaasen': {
        'nat': 'South Africa', 'role': 'Middle Order Power Hitter / WK', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm off break', 'tier': 'Marquee Elite',
        'why_pressure': '418 pressure balls (54 matches), 788 runs, 188.5 SR. The undisputed premier spin punisher in world cricket with unmatched bat speed.',
        'rr_fit': 'Transformative game-breaker. Would turn RR middle order into the most feared in the IPL, making 200+ totals at Sawai Mansingh Stadium routine.'
    },
    'Donovan Ferreira': {
        'nat': 'South Africa', 'role': 'Finisher / WK / Utility All-Rounder', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm off break', 'tier': 'Tier 2 Value Pick (Ex-RR)',
        'why_pressure': '199.3 strike rate under pressure (+65.0 over baseline), 28.7% boundary rate, ice-cold finishing temperament across 23 matches.',
        'rr_fit': 'Former Rajasthan Royals squad member with known culture fit. Offers 3-in-1 value: 200-strike-rate finisher, backup wicketkeeper to Sanju Samson, and handy off-spin in powerplay/middle.'
    },
    'Jitesh Sharma': {
        'nat': 'India', 'role': 'Wicketkeeper-Finisher', 'bat_style': 'Right Hand Bat', 'bowl_style': 'None', 'tier': 'Tier 1 Target',
        'why_pressure': '178.2 pressure strike rate (+46.8 over baseline) across 53 matches (363 balls). Attacking mindset from delivery one with 25.3% boundary rate.',
        'rr_fit': 'High-demand Indian wicketkeeper-finisher. Strengthens lower-order firepower and allows Sanju Samson to play purely as a top-order batter or share wicketkeeping duties.'
    },
    'Ishan Kishan': {
        'nat': 'India', 'role': 'Aggressive Top-Order WK-Batter', 'bat_style': 'Left Hand Bat', 'bowl_style': 'None', 'tier': 'Marquee Indian Target',
        'why_pressure': '182.6 strike rate under pressure (+47.6 delta) with 25.0% boundary rate. Lethal counter-puncher against high pace.',
        'rr_fit': 'Can form a destructive opening partnership with Yashasvi Jaiswal, dismantling powerplays and eliminating scoreboard pressure before the middle overs.'
    },
    'Rovman Powell': {
        'nat': 'West Indies', 'role': 'Lower Order Finisher (Ex-RR)', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm medium', 'tier': 'Tier 2 Buyback Option',
        'why_pressure': 'Massive sample reliability: 600 pressure balls across 82 matches, 1056 runs, 176.0 strike rate. Demonstrated match-winning pedigree.',
        'rr_fit': 'Deep familiarity with RR setup and Jaipur conditions. Reliable six-hitting monster when RRR exceeds 12 in the final 4 overs.'
    },
    'Romario Shepherd': {
        'nat': 'West Indies', 'role': 'Fast Bowling Finisher / All-Rounder', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm fast-medium', 'tier': 'Tier 2 Target',
        'why_pressure': '573 pressure balls across 76 matches, 936 runs, 163.4 SR (+42.3 over baseline) and 27.5 pressure average (+16.1 improvement).',
        'rr_fit': 'Rare lower-order pace-bowling all-rounder. Provides 30+ strike power in death overs and bowls 2-3 middle/death overs with heavy balls and cutters.'
    },
    'Noor Ahmad': {
        'nat': 'Afghanistan', 'role': 'Left-Arm Wrist Spinner (Mystery)', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Left-arm wrist spin', 'tier': 'Tier 1 Priority Target',
        'why_pressure': '#1 Ranked Bowler. 505 pressure balls across 71 matches, 35 wickets, 8.04 pressure economy, 35.4% dot balls.',
        'rr_fit': 'The crown jewel for RR bowling at SMS Stadium Jaipur. With large square boundaries (70m+), Noor wrist-spin and wrong-un create extreme wicket-taking threat while locking down scoring.'
    },
    'Mujeeb Ur Rahman': {
        'nat': 'Afghanistan', 'role': 'Powerplay & Death Mystery Spinner', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm off break / Mystery', 'tier': 'Tier 2 Value Pick',
        'why_pressure': '7.47 pressure economy, 8.39% wicket rate (12 wickets in 143 balls), 35.7% dot ball rate.',
        'rr_fit': 'Bowls in any phase: powerplay overs 1-6 or death overs 16-20. Carrom ball and seam-up flipper bamboozle batters hunting boundaries.'
    },
    'Sunil Narine': {
        'nat': 'West Indies', 'role': 'Mystery Spin & Powerplay All-Rounder', 'bat_style': 'Left Hand Bat', 'bowl_style': 'Right-arm off break / Mystery', 'tier': 'Marquee Overseas',
        'why_pressure': 'Lowest pressure economy in top 10 (6.92) across 483 balls (71 matches), 36.0% dot ball percentage.',
        'rr_fit': 'Unbreachable spin choke and explosive opening pinch-hitter. Gives RR immense tactical flexibility in both innings.'
    },
    'Nasum Ahmed': {
        'nat': 'Bangladesh', 'role': 'Slow Left-Arm Orthodox Containment', 'bat_style': 'Left Hand Bat', 'bowl_style': 'Slow left-arm orthodox', 'tier': 'Tier 3 Budget Value',
        'why_pressure': '7.23 pressure economy (+1.99 improvement over baseline) and 34.0% dot ball rate across 141 pressure balls.',
        'rr_fit': 'Budget-friendly overseas spin option who excels when introduced in powerplay or middle-overs choke on abrasive Jaipur surfaces.'
    },
    'Nathan Ellis': {
        'nat': 'Australia', 'role': 'Specialist Death Bowler', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm fast-medium', 'tier': 'Tier 1 Must-Have Target',
        'why_pressure': '328 pressure balls, 27 wickets (8.23% wicket rate), 31.7% dot ball rate. Master of slower balls and dipping yorkers.',
        'rr_fit': 'Absolute #1 tactical priority for RR. Partners Sandeep Sharma at the death. Sawai Mansingh Stadium slower surfaces amplify Ellis back-of-the-hand cutters and pinpoint yorkers.'
    },
    'Sai Kishore': {
        'nat': 'India', 'role': 'Tall Left-Arm Orthodox Spinner', 'bat_style': 'Left Hand Bat', 'bowl_style': 'Slow left-arm orthodox', 'tier': 'Tier 1 Prime Indian Target',
        'why_pressure': '8.88% wicket rate under pressure (19 wickets in 214 balls), 30.4% dot ball rate. High release point creates steep trajectory and bounce.',
        'rr_fit': 'Premier Indian spinner target. Allows RR to play an Indian spinner of international quality, unlocking an overseas slot for an extra batter or fast bowler. Perfect for Jaipur dry decks.'
    },
    'Mohsin Khan': {
        'nat': 'India', 'role': 'Left-Arm Fast-Medium Enforcer', 'bat_style': 'Left Hand Bat', 'bowl_style': 'Left-arm fast-medium', 'tier': 'Tier 1 Prime Indian Target',
        'why_pressure': '9.30 pressure economy (+1.69 improvement over baseline), 6.59% wicket rate (+4.32% improvement), 31.3% dot balls.',
        'rr_fit': 'Left-arm Indian fast bowler with steep bounce and lethal yorker. Provides left-arm pace diversity that RR attack crucially needs.'
    },
    'Taskin Ahmed': {
        'nat': 'Bangladesh', 'role': 'Hit-The-Deck Express Pacer (145+)', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm fast', 'tier': 'Tier 2 Strike Pacer',
        'why_pressure': '267 balls, 23 wickets (8.61% wicket rate), 31.8% dot ball rate, bowling express 140-145+ km/h.',
        'rr_fit': 'Enforcer pacer who attacks hard lengths. Punishes batters attempting to clear Jaipur long boundaries on mistimed pull shots.'
    },
    'Sikandar Raza': {
        'nat': 'Zimbabwe', 'role': 'Batting All-Rounder / Spin Choke', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm off break', 'tier': 'Tier 2 Value All-Rounder',
        'why_pressure': '7.40 pressure economy across 394 balls (50 matches), 22 wickets, 31.0% dot ball rate.',
        'rr_fit': 'True 4-dimensional player: middle-order batter, clutch off-spinner, livewire fielder, tactical leader. Exceptional purse value.'
    },
    'Ish Sodhi': {
        'nat': 'New Zealand', 'role': 'Attacking Leg Spinner (Ex-RR)', 'bat_style': 'Right Hand Bat', 'bowl_style': 'Right-arm leg break', 'tier': 'Tier 2 Value Pick (Ex-RR)',
        'why_pressure': '315 pressure balls, 21 wickets (6.67% wicket rate), 8.80 economy, 29.8% dot ball rate.',
        'rr_fit': 'Former Rajasthan Royals player with extensive experience at Sawai Mansingh Stadium. Strong relationship with franchise management and fanbase.'
    }
}

# Attach metadata to dataframes
def enrich_bat(df):
    rows = []
    for _, r in df.iterrows():
        name = r['player_name']
        meta = top_meta.get(name, {
            'nat': 'India' if any(w in str(name).lower() for w in ['singh', 'kumar', 'patel', 'sharma', 'iyer', 'khan', 'reddy', 'yadav', 'pandya', 'dhoni', 'pant', 'patidar', 'gill', 'varma', 'rana', 'tewatia', 'dubey', 'dube', 'parag', 'samson', 'jaiswal', 'jurel']) else 'Overseas',
            'role': 'Top/Middle Order Batter', 'bat_style': 'RHB', 'bowl_style': 'None', 'tier': 'Squad Asset',
            'why_pressure': f'SPRI Score {r.score:.2f} with {r.sr_p:.1f} strike rate across {int(r.balls_p)} pressure balls.',
            'rr_fit': 'Squad depth asset for high-pressure match situations.'
        })
        d = r.to_dict()
        d.update(meta)
        rows.append(d)
    return pd.DataFrame(rows)

def enrich_bowl(df):
    rows = []
    for _, r in df.iterrows():
        name = r['player_name']
        meta = top_meta.get(name, {
            'nat': 'India' if any(w in str(name).lower() for w in ['singh', 'kumar', 'patel', 'sharma', 'iyer', 'khan', 'reddy', 'yadav', 'kishore', 'chahal', 'ashwin', 'shami', 'bumrah', 'siraj', 'tyagi', 'krishna', 'bishnoi', 'arshdeep', 'pandya']) else 'Overseas',
            'role': 'Bowler', 'bat_style': 'RHB', 'bowl_style': 'Pace/Spin', 'tier': 'Squad Asset',
            'why_pressure': f'SPRI Score {r.score:.2f} with {r.econ_p:.2f} economy across {int(r.balls_p)} pressure balls.',
            'rr_fit': 'Bowler depth option for death/middle overs choke.'
        })
        d = r.to_dict()
        d.update(meta)
        rows.append(d)
    return pd.DataFrame(rows)

bat_enriched = enrich_bat(bat_df)
bowl_enriched = enrich_bowl(bowl_df)

bat_json = bat_enriched.to_json(orient='records')
bowl_json = bowl_enriched.to_json(orient='records')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rajasthan Royals War Room | SupeRR Selector Round 1 Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {{
      --rr-pink: #EA1B86;
      --rr-pink-glow: rgba(234, 27, 134, 0.35);
      --rr-blue: #004BA0;
      --rr-blue-light: #1E6BE6;
      --rr-gold: #FFB800;
      --bg-dark: #0B1120;
      --bg-card: #131E36;
      --bg-card-hover: #1A284A;
      --border-color: rgba(255, 255, 255, 0.08);
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --success: #10B981;
      --danger: #EF4444;
      --radius: 12px;
      --font-main: 'Plus Jakarta Sans', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font-main);
      background-color: var(--bg-dark);
      color: var(--text-main);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* Top Navigation Header */
    header {{
      background: linear-gradient(135deg, #0B1120 0%, #170A24 50%, #00224D 100%);
      border-bottom: 1px solid rgba(234, 27, 134, 0.3);
      padding: 18px 32px;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(12px);
    }}
    .header-content {{
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .brand-logo {{
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--rr-pink), var(--rr-blue));
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 20px;
      color: #fff;
      box-shadow: 0 0 20px var(--rr-pink-glow);
    }}
    .brand-title h1 {{
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.3px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .brand-title h1 span {{
      color: var(--rr-pink);
    }}
    .brand-title p {{
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 500;
    }}
    .compliance-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34D399;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
    }}
    .compliance-pill::before {{
      content: '';
      width: 8px;
      height: 8px;
      background-color: #34D399;
      border-radius: 50%;
      box-shadow: 0 0 8px #34D399;
    }}

    /* Global Container */
    .container {{
      max-width: 1440px;
      width: 100%;
      margin: 0 auto;
      padding: 24px 32px 60px;
      flex: 1;
    }}

    /* Quick KPI Banner */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 18px 20px;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }}
    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(234, 27, 134, 0.4);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--rr-pink), var(--rr-blue));
    }}
    .kpi-title {{
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }}
    .kpi-value {{
      font-size: 26px;
      font-weight: 800;
      color: #fff;
      font-family: var(--font-mono);
    }}
    .kpi-subtitle {{
      font-size: 12px;
      color: #38BDF8;
      margin-top: 4px;
      font-weight: 500;
    }}

    /* Tab Navigation */
    .tab-bar {{
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 28px;
      overflow-x: auto;
      padding-bottom: 4px;
    }}
    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: var(--font-main);
      font-size: 14px;
      font-weight: 600;
      padding: 10px 18px;
      border-radius: 8px 8px 0 0;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      position: relative;
      white-space: nowrap;
    }}
    .tab-btn:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.04);
    }}
    .tab-btn.active {{
      color: #fff;
      background: var(--bg-card);
    }}
    .tab-btn.active::after {{
      content: '';
      position: absolute;
      bottom: -4px;
      left: 0; right: 0;
      height: 3px;
      background: var(--rr-pink);
      border-radius: 3px 3px 0 0;
      box-shadow: 0 0 10px var(--rr-pink);
    }}

    /* Tab Content Panes */
    .tab-pane {{
      display: none;
      animation: fadeIn 0.3s ease;
    }}
    .tab-pane.active {{
      display: block;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Top Picks Grid & Cards */
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .section-title {{
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .section-title .badge {{
      background: var(--rr-pink);
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      text-transform: uppercase;
    }}

    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 20px;
      margin-bottom: 32px;
    }}
    .player-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      transition: all 0.25s ease;
      position: relative;
    }}
    .player-card:hover {{
      border-color: rgba(234, 27, 134, 0.5);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
      transform: translateY(-2px);
    }}
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }}
    .player-rank-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 34px;
      height: 34px;
      background: linear-gradient(135deg, var(--rr-pink), var(--rr-blue));
      color: #fff;
      font-weight: 800;
      font-size: 16px;
      border-radius: 8px;
      font-family: var(--font-mono);
    }}
    .player-main-info {{
      flex: 1;
      margin-left: 14px;
    }}
    .player-name {{
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .player-role {{
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 500;
    }}
    .spri-badge {{
      text-align: right;
    }}
    .spri-num {{
      font-size: 24px;
      font-weight: 800;
      color: var(--rr-pink);
      font-family: var(--font-mono);
      line-height: 1;
    }}
    .spri-label {{
      font-size: 10px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
    }}

    .stats-chips {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      background: rgba(0, 0, 0, 0.25);
      border-radius: 8px;
      padding: 12px;
      border: 1px solid rgba(255, 255, 255, 0.04);
    }}
    .stat-chip {{
      text-align: center;
    }}
    .stat-chip .val {{
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      font-family: var(--font-mono);
    }}
    .stat-chip .lbl {{
      font-size: 10px;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-top: 2px;
    }}

    .card-insight {{
      background: rgba(234, 27, 134, 0.06);
      border-left: 3px solid var(--rr-pink);
      padding: 10px 14px;
      border-radius: 0 6px 6px 0;
      font-size: 12.5px;
      color: #E2E8F0;
    }}
    .card-insight strong {{
      color: var(--rr-pink);
    }}

    .card-rr-fit {{
      background: rgba(0, 75, 160, 0.12);
      border-left: 3px solid var(--rr-blue-light);
      padding: 10px 14px;
      border-radius: 0 6px 6px 0;
      font-size: 12.5px;
      color: #E2E8F0;
    }}
    .card-rr-fit strong {{
      color: #60A5FA;
    }}

    .tier-tag {{
      display: inline-block;
      align-self: flex-start;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(255, 184, 0, 0.15);
      color: var(--rr-gold);
      border: 1px solid rgba(255, 184, 0, 0.3);
    }}

    /* Data Tables */
    .table-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      overflow-x: auto;
      margin-bottom: 32px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}
    thead th {{
      background: rgba(0, 0, 0, 0.4);
      padding: 14px 16px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      font-weight: 700;
      border-bottom: 1px solid var(--border-color);
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    }}
    thead th:hover {{
      color: #fff;
    }}
    tbody tr {{
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      transition: background 0.15s ease;
    }}
    tbody tr:hover {{
      background: var(--bg-card-hover);
    }}
    tbody td {{
      padding: 12px 16px;
      color: #E2E8F0;
      white-space: nowrap;
    }}
    td.mono {{
      font-family: var(--font-mono);
      font-weight: 600;
    }}
    td.highlight {{
      color: var(--rr-pink);
      font-weight: 700;
    }}
    .tag {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
    }}
    .tag-ind {{ background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .tag-ovs {{ background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); }}

    /* Filter & Search Bar */
    .filter-bar {{
      display: flex;
      gap: 12px;
      margin-bottom: 18px;
      flex-wrap: wrap;
      align-items: center;
    }}
    .search-input {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: #fff;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      min-width: 240px;
      outline: none;
      font-family: var(--font-main);
    }}
    .search-input:focus {{
      border-color: var(--rr-pink);
      box-shadow: 0 0 10px var(--rr-pink-glow);
    }}
    .filter-select {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: #fff;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 13px;
      outline: none;
      font-family: var(--font-main);
      cursor: pointer;
    }}
    .btn {{
      background: linear-gradient(135deg, var(--rr-pink), #C2006A);
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}
    .btn:hover {{
      opacity: 0.95;
      transform: translateY(-1px);
      box-shadow: 0 4px 14px var(--rr-pink-glow);
    }}
    .btn-secondary {{
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
    }}
    .btn-secondary:hover {{
      background: rgba(255, 255, 255, 0.14);
      box-shadow: none;
    }}

    /* Strategy & Tactics Pane */
    .strategy-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }}
    .strategy-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 24px;
    }}
    .strategy-card h3 {{
      font-size: 16px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }}
    .strategy-card p {{
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 12px;
    }}
    .strategy-card ul {{
      list-style: none;
      padding-left: 0;
    }}
    .strategy-card li {{
      font-size: 13px;
      color: #CBD5E1;
      padding: 6px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .strategy-card li::before {{
      content: '⚡';
      font-size: 11px;
    }}

    /* Methodology Panels */
    .formula-box {{
      background: rgba(0, 0, 0, 0.35);
      border: 1px dashed rgba(234, 27, 134, 0.4);
      border-radius: 8px;
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 12px;
      color: #38BDF8;
      margin: 14px 0;
      line-height: 1.6;
    }}

    /* Radar / Head-to-Head comparator */
    .compare-container {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 30px;
    }}
    .compare-controls {{
      display: flex;
      gap: 16px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}
    .compare-box {{
      flex: 1;
      min-width: 260px;
    }}
    .compare-box label {{
      display: block;
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 6px;
      font-weight: 600;
    }}
    .compare-box select {{
      width: 100%;
      background: #0B1120;
      border: 1px solid var(--border-color);
      color: #fff;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 14px;
      outline: none;
    }}

    /* Charts Container */
    .chart-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 20px;
      margin-bottom: 24px;
    }}
    .chart-card h4 {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    /* Footer */
    footer {{
      background: #070B14;
      border-top: 1px solid var(--border-color);
      padding: 24px 32px;
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      margin-top: auto;
    }}

    /* Responsive */
    @media (max-width: 768px) {{
      .container {{ padding: 16px; }}
      .cards-grid {{ grid-template-columns: 1fr; }}
      .stats-chips {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>

  <!-- Top Header -->
  <header>
    <div class="header-content">
      <div class="brand">
        <div class="brand-logo">RR</div>
        <div class="brand-title">
          <h1>Rajasthan Royals <span>War Room</span> | SupeRR Selector</h1>
          <p>Round 1: Pressure Reliability Analytics & IPL 2027 Auction Target Portfolio</p>
        </div>
      </div>
      <div style="display: flex; gap: 12px; align-items: center;">
        <div class="compliance-pill">IPL Rules Compliant: Pakistan Players Excluded</div>
        <button class="btn btn-secondary" onclick="window.print()">🖨️ Export PDF</button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="container">

    <!-- KPI Summary Ribbon -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">Deliveries Analysed</div>
        <div class="kpi-value">193,988</div>
        <div class="kpi-subtitle">Innings 1 & 2 (2022–2026)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Matches Analysed</div>
        <div class="kpi-value">837</div>
        <div class="kpi-subtitle">367 IPL | 470 T20I Matches</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Pressure Events</div>
        <div class="kpi-value">110,750</div>
        <div class="kpi-subtitle">53,137 Bat | 57,613 Bowl</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Clean Eligible Pool</div>
        <div class="kpi-value">84 / 131</div>
        <div class="kpi-subtitle">84 Batters | 131 Bowlers</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Top Pressure Batter</div>
        <div class="kpi-value" style="font-size: 20px; color: var(--rr-pink);">Shashank Singh</div>
        <div class="kpi-subtitle">SPRI 87.29 | SR 185.5 (+71.5)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Top Pressure Bowler</div>
        <div class="kpi-value" style="font-size: 20px; color: #38BDF8;">Noor Ahmad</div>
        <div class="kpi-subtitle">SPRI 81.08 | Econ 8.04 (35 Wkts)</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('overview')">📊 War Room Executive Brief</button>
      <button class="tab-btn" onclick="switchTab('batters')">🏏 Top 10 Batters</button>
      <button class="tab-btn" onclick="switchTab('bowlers')">🎯 Top 10 Bowlers</button>
      <button class="tab-btn" onclick="switchTab('tactics')">🏰 RR 2027 Tactical Fit</button>
      <button class="tab-btn" onclick="switchTab('compare')">⚔️ Head-to-Head Compare</button>
      <button class="tab-btn" onclick="switchTab('database')">📂 Full Database (215 Players)</button>
      <button class="tab-btn" onclick="switchTab('methodology')">📐 Methodology & SPRI Model</button>
    </div>

    <!-- TAB 1: EXECUTIVE OVERVIEW -->
    <div id="overview" class="tab-pane active">
      <div class="section-header">
        <div class="section-title">
          Executive War Room Summary
          <span class="badge">IPL 2027 Focus</span>
        </div>
      </div>

      <div class="strategy-grid">
        <div class="strategy-card">
          <h3>🎯 The Core Objective</h3>
          <p>
            Rajasthan Royals enter the 2027 auction cycle needing ice-cold performers under extreme match pressure. 
            Historically, T20 auctions overpay for reputation, recency bias, or bulk raw runs. 
            The <strong>SupeRR Pressure Reliability Index (SPRI)</strong> isolates performance strictly during crunch situations 
            (steep chases, late-innings wicket constraints, death overs, and competitive middle overs) relative to matched non-pressure baselines.
          </p>
          <ul>
            <li><strong>BCCI/IPL Rule Compliance:</strong> Excluded 68 Pakistani players from the candidate pool prior to percentile scoring.</li>
            <li><strong>Phase-Matched Normalization:</strong> Controls for death-overs inflation by comparing pressure deliveries to non-pressure deliveries in the exact same match phase.</li>
            <li><strong>Sample Reliability Shrinkage:</strong> Penalizes small sample noise to ensure top recommendations are reliable.</li>
          </ul>
        </div>

        <div class="strategy-card">
          <h3>🏆 Top 3 Batting Recommendations</h3>
          <p>
            <strong>1. Shashank Singh (SPRI: 87.29)</strong> — The supreme domestic finisher. Under pressure, his strike rate leaps by +71.5 to 185.5 with an incredible 47.6 average. Perfect fit at #6/#7.<br><br>
            <strong>2. Naman Dhir (SPRI: 82.33)</strong> — Elite Indian boundary hitter (30.2% boundary rate, 198.2 SR). High-ceiling aggressor who can take down spin and high pace.<br><br>
            <strong>3. Mark Chapman (SPRI: 81.06)</strong> — Overseas spin destroyer (183.3 SR, 36.0 Avg) suited for Sawai Mansingh Stadium pitch conditions.
          </p>
        </div>

        <div class="strategy-card">
          <h3>🔥 Top 3 Bowling Recommendations</h3>
          <p>
            <strong>1. Noor Ahmad (SPRI: 81.08)</strong> — Premier left-arm wrist spin asset. 505 pressure balls, 35 wickets, 8.04 economy. Elite weapon for Jaipur's big square boundaries.<br><br>
            <strong>2. Mujeeb Ur Rahman (SPRI: 76.28)</strong> — Mystery off-spin, carrom ball, and powerplay/death containment (7.47 economy, 8.39% wicket rate).<br><br>
            <strong>3. Sunil Narine (SPRI: 75.57)</strong> — The gold standard of pressure containment (6.92 economy, 36.0% dot balls across 483 balls).
          </p>
        </div>
      </div>

      <!-- Overview Charts -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap: 20px;">
        <div class="chart-card">
          <h4>Top 10 Batters SPRI Comparison</h4>
          <canvas id="batOverviewChart" height="220"></canvas>
        </div>
        <div class="chart-card">
          <h4>Top 10 Bowlers SPRI Comparison</h4>
          <canvas id="bowlOverviewChart" height="220"></canvas>
        </div>
      </div>
    </div>

    <!-- TAB 2: TOP 10 BATTERS -->
    <div id="batters" class="tab-pane">
      <div class="section-header">
        <div class="section-title">
          Top 10 Pressure Batters
          <span class="badge">SPRI Ranked</span>
        </div>
        <div style="color: var(--text-muted); font-size: 13px;">
          Sorted by SupeRR Pressure Reliability Index (100-point scale)
        </div>
      </div>

      <!-- Batters Cards Grid -->
      <div class="cards-grid" id="battersCards"></div>

      <!-- Batters Table -->
      <div class="section-header">
        <div class="section-title" style="font-size: 16px;">Complete Top 10 Batters Evidence Table</div>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Player</th>
              <th>Nationality</th>
              <th>SPRI</th>
              <th>Pressure Balls</th>
              <th>Runs</th>
              <th>Outs</th>
              <th>Pressure SR</th>
              <th>Base SR</th>
              <th>Δ SR</th>
              <th>Pressure Avg</th>
              <th>Boundary %</th>
              <th>Matches</th>
            </tr>
          </thead>
          <tbody id="battersTableBody"></tbody>
        </table>
      </div>
    </div>

    <!-- TAB 3: TOP 10 BOWLERS -->
    <div id="bowlers" class="tab-pane">
      <div class="section-header">
        <div class="section-title">
          Top 10 Pressure Bowlers
          <span class="badge">SPRI Ranked</span>
        </div>
        <div style="color: var(--text-muted); font-size: 13px;">
          Sorted by SupeRR Pressure Reliability Index (100-point scale)
        </div>
      </div>

      <!-- Bowlers Cards Grid -->
      <div class="cards-grid" id="bowlersCards"></div>

      <!-- Bowlers Table -->
      <div class="section-header">
        <div class="section-title" style="font-size: 16px;">Complete Top 10 Bowlers Evidence Table</div>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Player</th>
              <th>Nationality</th>
              <th>SPRI</th>
              <th>Pressure Balls</th>
              <th>Conceded</th>
              <th>Wickets</th>
              <th>Pressure Econ</th>
              <th>Base Econ</th>
              <th>Econ Imprv</th>
              <th>Wkt Rate %</th>
              <th>Dot Ball %</th>
              <th>Matches</th>
            </tr>
          </thead>
          <tbody id="bowlersTableBody"></tbody>
        </table>
      </div>
    </div>

    <!-- TAB 4: RR TACTICAL FIT & 2027 AUCTION STRATEGY -->
    <div id="tactics" class="tab-pane">
      <div class="section-header">
        <div class="section-title">
          Rajasthan Royals Tactical Fit & Auction Blueprint 2027
          <span class="badge">War Room Strategy</span>
        </div>
      </div>

      <div class="strategy-grid">
        <div class="strategy-card" style="border-top: 3px solid var(--rr-pink);">
          <h3>🏟️ Sawai Mansingh Stadium (Jaipur) Blueprint</h3>
          <p>
            Jaipur's home ground features some of the longest square boundaries (70m to 76m) in the IPL. 
            Pitches progressively grip and slow down as matches wear on, especially during the second innings.
          </p>
          <ul>
            <li><strong>Spin Choke:</strong> Large pockets make wrist-spinners (Noor Ahmad) and tall release-point spinners (Sai Kishore) lethal, as batters cannot easily miscue over the ropes.</li>
            <li><strong>Pace-off Death Bowling:</strong> Flat hit-the-deck bowling often gets punished; bowlers with back-of-the-hand slower balls and dipping yorkers (Nathan Ellis) dominate.</li>
            <li><strong>Finishing Against Spin:</strong> When RR chase at Jaipur, teams choke them with spin. Having batters like Shashank Singh (+71.5 Delta SR) and Mark Chapman (+49.5 Delta SR) eliminates chasing collapses.</li>
          </ul>
        </div>

        <div class="strategy-card" style="border-top: 3px solid var(--rr-blue);">
          <h3>🎯 Target Priority Tiers for 2027 Auction</h3>
          <p>How Rajasthan Royals should allocate purse and overseas slots:</p>
          <ul>
            <li><strong>Tier 1 Must-Haves:</strong> 
              <br>• <em>Nathan Ellis</em> (Overseas Death Bowler — pair with Sandeep Sharma)
              <br>• <em>Shashank Singh</em> (Indian Finisher — resolves lower-order power)
              <br>• <em>Sai Kishore</em> (Elite Indian Spinner — replaces Ashwin/Chahal role)
            </li>
            <li><strong>Tier 2 High-Ceiling Buys:</strong>
              <br>• <em>Noor Ahmad / Mujeeb Ur Rahman</em> (Overseas Mystery Spin weapon)
              <br>• <em>Naman Dhir</em> (Explosive Indian Top/Middle batter)
              <br>• <em>Mohsin Khan</em> (Indian Left-arm Fast Bowling Enforcer)
            </li>
            <li><strong>Tier 3 Value & Familiarity:</strong>
              <br>• <em>Donovan Ferreira / Ish Sodhi</em> (Ex-RR players with proven franchise fit)
              <br>• <em>Sikandar Raza</em> (Budget 4D All-Rounder)
            </li>
          </ul>
        </div>

        <div class="strategy-card" style="border-top: 3px solid var(--rr-gold);">
          <h3>👑 Simulated Rajasthan Royals 2027 Playing XI</h3>
          <p>With our SPRI target recruits integrated alongside retained core:</p>
          <ul>
            <li><strong>1. Yashasvi Jaiswal</strong> (Indian Opener — Aggressor)</li>
            <li><strong>2. Sanju Samson (C/WK)</strong> (Indian Anchor / Counter-Puncher)</li>
            <li><strong>3. Naman Dhir / Shreyas Iyer</strong> (High-Tempo Middle Order)</li>
            <li><strong>4. Riyan Parag</strong> (Indian Spin Punisher & Float)</li>
            <li><strong>5. Dhruv Jurel / Mark Chapman</strong> (Middle-Overs Stabilizer / Finisher)</li>
            <li><strong>6. Shashank Singh</strong> (Premier Indian Finisher)</li>
            <li><strong>7. Donovan Ferreira / Romario Shepherd</strong> (Overseas Power Finisher [OS 1])</li>
            <li><strong>8. Sai Kishore</strong> (Indian Left-Arm Spin Specialist)</li>
            <li><strong>9. Noor Ahmad / Mujeeb</strong> (Overseas Mystery Spinner [OS 2])</li>
            <li><strong>10. Nathan Ellis</strong> (Overseas Death Specialist [OS 3])</li>
            <li><strong>11. Sandeep Sharma / Mohsin Khan</strong> (Indian Swing & Death Enforcer)</li>
            <li><strong>Impact Player:</strong> Prasidh Krishna / Rovman Powell</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- TAB 5: COMPARE -->
    <div id="compare" class="tab-pane">
      <div class="section-header">
        <div class="section-title">
          Interactive Head-to-Head Player Comparator
          <span class="badge">Radar Analysis</span>
        </div>
      </div>

      <div class="compare-container">
        <div class="compare-controls">
          <div class="compare-box">
            <label>Select Player A:</label>
            <select id="compareSelectA" onchange="updateComparison()"></select>
          </div>
          <div class="compare-box">
            <label>Select Player B:</label>
            <select id="compareSelectB" onchange="updateComparison()"></select>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px;">
          <div id="compareCardA"></div>
          <div id="compareCardB"></div>
        </div>

        <div class="chart-card" style="margin-top: 24px;">
          <h4>Head-to-Head Metric Radar</h4>
          <div style="max-width: 600px; margin: 0 auto;">
            <canvas id="radarChart" height="320"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 6: FULL DATABASE -->
    <div id="database" class="tab-pane">
      <div class="section-header">
        <div class="section-title">
          Complete Eligible Players Database
          <span class="badge" id="dbCountBadge">215 Players</span>
        </div>
      </div>

      <div class="filter-bar">
        <input type="text" id="dbSearch" class="search-input" placeholder="🔍 Search player name..." oninput="renderDatabase()">
        <select id="dbRoleFilter" class="filter-select" onchange="renderDatabase()">
          <option value="all">All Roles (Batters & Bowlers)</option>
          <option value="batters">Batters Only (84)</option>
          <option value="bowlers">Bowlers Only (131)</option>
        </select>
        <select id="dbNatFilter" class="filter-select" onchange="renderDatabase()">
          <option value="all">All Nationalities</option>
          <option value="India">Indian Players Only</option>
          <option value="Overseas">Overseas Players Only</option>
        </select>
        <button class="btn btn-secondary" onclick="exportDatabaseCSV()">📥 Export Filtered CSV</button>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr id="dbTableHeader">
              <th>Type</th>
              <th>Player</th>
              <th>Nationality</th>
              <th>SPRI Score</th>
              <th>Pressure Balls</th>
              <th>Matches</th>
              <th>Primary Metric</th>
              <th>Baseline Metric</th>
              <th>Improvement (Δ)</th>
              <th>Secondary Rate</th>
            </tr>
          </thead>
          <tbody id="dbTableBody"></tbody>
        </table>
      </div>
    </div>

    <!-- TAB 7: METHODOLOGY -->
    <div id="methodology" class="tab-pane">
      <div class="section-header">
        <div class="section-title">
          Methodology & Mathematical Framework
          <span class="badge">SPRI v2.0</span>
        </div>
      </div>

      <div class="strategy-grid">
        <div class="strategy-card">
          <h3>📐 Batter SPRI Formula</h3>
          <div class="formula-box">
Raw Score = 0.25 × Pctl(Pressure SR)
          + 0.25 × Pctl(Δ Strike Rate)
          + 0.20 × Pctl(Pressure Average)
          + 0.15 × Pctl(Δ Average)
          + 0.15 × Pctl(Boundary Rate)

Reliability = √(Balls / [Balls + 120]) × √(Matches / [Matches + 10])

Final SPRI = 100 × Raw Score × (0.65 + 0.35 × Reliability)
          </div>
          <p>
            Percentile ranks ensure metrics on different units (strike rate vs average) are mathematically comparable.
            Reliability shrinkage tempers small-sample volatility while preventing high-volume accumulation from overshadowing superior efficiency.
          </p>
        </div>

        <div class="strategy-card">
          <h3>🎯 Bowler SPRI Formula</h3>
          <div class="formula-box">
Raw Score = 0.25 × Pctl(–Pressure Economy)
          + 0.25 × Pctl(Economy Improvement)
          + 0.20 × Pctl(Pressure Wkts / 100 Balls)
          + 0.15 × Pctl(Δ Wickets / 100 Balls)
          + 0.15 × Pctl(Dot Ball Rate)

Reliability = √(Balls / [Balls + 120]) × √(Matches / [Matches + 10])

Final SPRI = 100 × Raw Score × (0.65 + 0.35 × Reliability)
          </div>
          <p>
            Bowling metrics penalize leaked runs while rewarding clutch wickets and dot balls. 
            Delta economy compares a bowler's pressure overs against their own non-pressure overs in the same innings and phase.
          </p>
        </div>

        <div class="strategy-card">
          <h3>⚖️ Pressure Definition Matrix</h3>
          <p>Pressure is defined contextually based on match state:</p>
          <ul>
            <li><strong>Chasing (Innings 2):</strong> Progress ≥ 50% AND (RRR ≥ 8.5 OR Wickets Remaining ≤ 5 with RRR ≥ 7.5 OR Death Overs 75-100% with RRR 6–12).</li>
            <li><strong>Setting (Innings 1):</strong> Progress ≥ 75% with ≥ 4 wickets down; or Progress 50-75% with ≥ 6 wickets down (batting collapses).</li>
            <li><strong>Bowler Pressure (Innings 2):</strong> Progress ≥ 50%, opposition has ≥ 3 wickets in hand, and RRR is tight (6.5 to 12.0).</li>
            <li><strong>Bowler Pressure (Innings 1):</strong> Opposition has ≥ 4 wickets in hand at death (overs 16-20), or ≥ 6 wickets in hand in middle overs.</li>
          </ul>
        </div>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer>
    <p>SupeRR Selector Season 2 — Round 1 Submission Pack | Prepared for Rajasthan Royals War Room</p>
    <p style="margin-top: 4px; font-size: 11px;">Exclusively complies with BCCI/IPL player eligibility regulations. All data audited from 837 IPL & T20I matches (2022–2026).</p>
  </footer>

  <!-- Embedded Data & Scripts -->
  <script>
    const battersData = {bat_json};
    const bowlersData = {bowl_json};

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      event.currentTarget.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    }}

    // Render Batters Cards & Table
    function renderBatters() {{
      const top10 = battersData.slice(0, 10);
      const cardsContainer = document.getElementById('battersCards');
      const tableBody = document.getElementById('battersTableBody');

      let cardsHtml = '';
      let tableHtml = '';

      top10.forEach((p, idx) => {{
        const isInd = p.nat === 'India';
        const natBadge = isInd ? '<span class="tag tag-ind">India</span>' : `<span class="tag tag-ovs">${{p.nat}}</span>`;

        cardsHtml += `
          <div class="player-card">
            <div class="card-top">
              <div class="player-rank-badge">#${{idx + 1}}</div>
              <div class="player-main-info">
                <div class="player-name">${{p.player_name}} ${{natBadge}}</div>
                <div class="player-role">${{p.role}} • ${{p.bat_style}}</div>
              </div>
              <div class="spri-badge">
                <div class="spri-num">${{p.score.toFixed(1)}}</div>
                <div class="spri-label">SPRI Score</div>
              </div>
            </div>
            <div class="tier-tag">${{p.tier}}</div>
            <div class="stats-chips">
              <div class="stat-chip"><div class="val">${{p.sr_p.toFixed(1)}}</div><div class="lbl">Pressure SR</div></div>
              <div class="stat-chip"><div class="val" style="color: #34D399;">+${{p.delta_sr.toFixed(1)}}</div><div class="lbl">Δ vs Base</div></div>
              <div class="stat-chip"><div class="val">${{p.avg_p.toFixed(1)}}</div><div class="lbl">Pressure Avg</div></div>
              <div class="stat-chip"><div class="val">${{(p.boundary_pct_p * 100).toFixed(1)}}%</div><div class="lbl">Boundary %</div></div>
            </div>
            <div class="card-insight">
              <strong>Why Clutch:</strong> ${{p.why_pressure}}
            </div>
            <div class="card-rr-fit">
              <strong>RR 2027 Value:</strong> ${{p.rr_fit}}
            </div>
          </div>
        `;

        tableHtml += `
          <tr>
            <td class="mono" style="color: var(--rr-pink);">#${{idx + 1}}</td>
            <td style="font-weight: 700;">${{p.player_name}}</td>
            <td>${{natBadge}}</td>
            <td class="mono highlight">${{p.score.toFixed(2)}}</td>
            <td class="mono">${{p.balls_p}}</td>
            <td class="mono">${{p.runs_p}}</td>
            <td class="mono">${{p.outs_p}}</td>
            <td class="mono">${{p.sr_p.toFixed(1)}}</td>
            <td class="mono">${{p.sr_n_matched.toFixed(1)}}</td>
            <td class="mono" style="color: #34D399; font-weight: 700;">+${{p.delta_sr.toFixed(1)}}</td>
            <td class="mono">${{p.avg_p.toFixed(1)}}</td>
            <td class="mono">${{(p.boundary_pct_p * 100).toFixed(1)}}%</td>
            <td class="mono">${{p.matches_p}}</td>
          </tr>
        `;
      }});

      cardsContainer.innerHTML = cardsHtml;
      tableBody.innerHTML = tableHtml;
    }}

    // Render Bowlers Cards & Table
    function renderBowlers() {{
      const top10 = bowlersData.slice(0, 10);
      const cardsContainer = document.getElementById('bowlersCards');
      const tableBody = document.getElementById('bowlersTableBody');

      let cardsHtml = '';
      let tableHtml = '';

      top10.forEach((p, idx) => {{
        const isInd = p.nat === 'India';
        const natBadge = isInd ? '<span class="tag tag-ind">India</span>' : `<span class="tag tag-ovs">${{p.nat}}</span>`;

        cardsHtml += `
          <div class="player-card">
            <div class="card-top">
              <div class="player-rank-badge" style="background: linear-gradient(135deg, var(--rr-blue), #00C6FF);">#${{idx + 1}}</div>
              <div class="player-main-info">
                <div class="player-name">${{p.player_name}} ${{natBadge}}</div>
                <div class="player-role">${{p.role}} • ${{p.bowl_style}}</div>
              </div>
              <div class="spri-badge">
                <div class="spri-num" style="color: #38BDF8;">${{p.score.toFixed(1)}}</div>
                <div class="spri-label">SPRI Score</div>
              </div>
            </div>
            <div class="tier-tag">${{p.tier}}</div>
            <div class="stats-chips">
              <div class="stat-chip"><div class="val">${{p.econ_p.toFixed(2)}}</div><div class="lbl">Pressure Econ</div></div>
              <div class="stat-chip"><div class="val">${{p.wkts_p}}</div><div class="lbl">Wickets</div></div>
              <div class="stat-chip"><div class="val">${{p.wkt_rate_p.toFixed(2)}}%</div><div class="lbl">Wkt Rate</div></div>
              <div class="stat-chip"><div class="val">${{(p.dot_pct_p * 100).toFixed(1)}}%</div><div class="lbl">Dot Ball %</div></div>
            </div>
            <div class="card-insight" style="border-left-color: #38BDF8; background: rgba(56, 189, 248, 0.06);">
              <strong style="color: #38BDF8;">Why Clutch:</strong> ${{p.why_pressure}}
            </div>
            <div class="card-rr-fit">
              <strong>RR 2027 Value:</strong> ${{p.rr_fit}}
            </div>
          </div>
        `;

        tableHtml += `
          <tr>
            <td class="mono" style="color: #38BDF8;">#${{idx + 1}}</td>
            <td style="font-weight: 700;">${{p.player_name}}</td>
            <td>${{natBadge}}</td>
            <td class="mono highlight" style="color: #38BDF8;">${{p.score.toFixed(2)}}</td>
            <td class="mono">${{p.balls_p}}</td>
            <td class="mono">${{p.conceded_p}}</td>
            <td class="mono" style="font-weight: 700;">${{p.wkts_p}}</td>
            <td class="mono">${{p.econ_p.toFixed(2)}}</td>
            <td class="mono">${{p.econ_n_matched.toFixed(2)}}</td>
            <td class="mono" style="color: ${{p.delta_econ >= 0 ? '#34D399' : '#EF4444'}};">${{p.delta_econ >= 0 ? '+' : ''}}${{p.delta_econ.toFixed(2)}}</td>
            <td class="mono">${{p.wkt_rate_p.toFixed(2)}}%</td>
            <td class="mono">${{(p.dot_pct_p * 100).toFixed(1)}}%</td>
            <td class="mono">${{p.matches_p}}</td>
          </tr>
        `;
      }});

      cardsContainer.innerHTML = cardsHtml;
      tableBody.innerHTML = tableHtml;
    }}

    // Database View
    function renderDatabase() {{
      const query = document.getElementById('dbSearch').value.toLowerCase();
      const roleFilter = document.getElementById('dbRoleFilter').value;
      const natFilter = document.getElementById('dbNatFilter').value;

      let combined = [];
      if (roleFilter === 'all' || roleFilter === 'batters') {{
        battersData.forEach(p => combined.push({{ ...p, type: 'Batter' }}));
      }}
      if (roleFilter === 'all' || roleFilter === 'bowlers') {{
        bowlersData.forEach(p => combined.push({{ ...p, type: 'Bowler' }}));
      }}

      // Filter
      const filtered = combined.filter(p => {{
        const matchesQuery = p.player_name.toLowerCase().includes(query);
        const matchesNat = natFilter === 'all' || (natFilter === 'India' ? p.nat === 'India' : p.nat !== 'India');
        return matchesQuery && matchesNat;
      }});

      document.getElementById('dbCountBadge').innerText = `${{filtered.length}} Players`;

      const tbody = document.getElementById('dbTableBody');
      let html = '';
      filtered.forEach(p => {{
        const isBat = p.type === 'Batter';
        const isInd = p.nat === 'India';
        const natBadge = isInd ? '<span class="tag tag-ind">India</span>' : `<span class="tag tag-ovs">${{p.nat}}</span>`;
        const typeBadge = isBat ? '<span class="tag" style="background: rgba(234, 27, 134, 0.15); color: var(--rr-pink);">BAT</span>' : '<span class="tag" style="background: rgba(56, 189, 248, 0.15); color: #38BDF8;">BOWL</span>';

        html += `
          <tr>
            <td>${{typeBadge}}</td>
            <td style="font-weight: 700;">${{p.player_name}}</td>
            <td>${{natBadge}}</td>
            <td class="mono highlight">${{p.score.toFixed(2)}}</td>
            <td class="mono">${{p.balls_p}}</td>
            <td class="mono">${{p.matches_p}}</td>
            <td class="mono">${{isBat ? p.sr_p.toFixed(1) + ' SR' : p.econ_p.toFixed(2) + ' Econ'}}</td>
            <td class="mono">${{isBat ? p.sr_n_matched.toFixed(1) + ' Base' : p.econ_n_matched.toFixed(2) + ' Base'}}</td>
            <td class="mono" style="color: #34D399;">${{isBat ? '+' + p.delta_sr.toFixed(1) : (p.delta_econ >= 0 ? '+' : '') + p.delta_econ.toFixed(2)}}</td>
            <td class="mono">${{isBat ? (p.boundary_pct_p * 100).toFixed(1) + '% Bound' : (p.dot_pct_p * 100).toFixed(1) + '% Dot'}}</td>
          </tr>
        `;
      }});
      tbody.innerHTML = html;
    }}

    function exportDatabaseCSV() {{
      let csv = 'Type,Player Name,Nationality,SPRI Score,Pressure Balls,Matches,Primary Metric,Baseline Metric,Delta,Secondary Metric\\n';
      battersData.forEach(p => {{
        csv += `Batter,"${{p.player_name}}",${{p.nat}},${{p.score.toFixed(2)}},${{p.balls_p}},${{p.matches_p}},${{p.sr_p.toFixed(1)}},${{p.sr_n_matched.toFixed(1)}},${{p.delta_sr.toFixed(1)}},${{(p.boundary_pct_p * 100).toFixed(1)}}%\\n`;
      }});
      bowlersData.forEach(p => {{
        csv += `Bowler,"${{p.player_name}}",${{p.nat}},${{p.score.toFixed(2)}},${{p.balls_p}},${{p.matches_p}},${{p.econ_p.toFixed(2)}},${{p.econ_n_matched.toFixed(2)}},${{p.delta_econ.toFixed(2)}},${{(p.dot_pct_p * 100).toFixed(1)}}%\\n`;
      }});
      const blob = new Blob([csv], {{ type: 'text/csv' }});
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', 'SupeRR_Selector_Round1_Database.csv');
      a.click();
    }}

    // Comparison Setup
    function populateCompareSelects() {{
      const selA = document.getElementById('compareSelectA');
      const selB = document.getElementById('compareSelectB');

      let allPlayers = [
        ...battersData.map(p => ({{ name: p.player_name, type: 'Batter', data: p }})),
        ...bowlersData.map(p => ({{ name: p.player_name, type: 'Bowler', data: p }}))
      ];

      let opts = '';
      allPlayers.forEach(p => {{
        opts += `<option value="${{p.name}}">${{p.name}} (${{p.type}} - SPRI: ${{p.data.score.toFixed(1)}})</option>`;
      }});

      selA.innerHTML = opts;
      selB.innerHTML = opts;

      selA.value = 'Shashank Singh';
      selB.value = 'Noor Ahmad';
      updateComparison();
    }}

    let radarChart = null;
    function updateComparison() {{
      const nameA = document.getElementById('compareSelectA').value;
      const nameB = document.getElementById('compareSelectB').value;

      const pA = battersData.find(p => p.player_name === nameA) || bowlersData.find(p => p.player_name === nameA);
      const pB = battersData.find(p => p.player_name === nameB) || bowlersData.find(p => p.player_name === nameB);

      const renderCompCard = (p) => `
        <div class="player-card" style="border-color: rgba(234, 27, 134, 0.4);">
          <div class="card-top">
            <div class="player-main-info" style="margin-left: 0;">
              <div class="player-name">${{p.player_name}}</div>
              <div class="player-role">${{p.role || p.nat}}</div>
            </div>
            <div class="spri-badge">
              <div class="spri-num">${{p.score.toFixed(1)}}</div>
              <div class="spri-label">SPRI</div>
            </div>
          </div>
          <div class="stats-chips">
            <div class="stat-chip"><div class="val">${{p.balls_p}}</div><div class="lbl">Balls</div></div>
            <div class="stat-chip"><div class="val">${{p.matches_p}}</div><div class="lbl">Matches</div></div>
            <div class="stat-chip"><div class="val">${{p.sr_p ? p.sr_p.toFixed(1) + ' SR' : p.econ_p.toFixed(2) + ' Econ'}}</div><div class="lbl">Rate</div></div>
            <div class="stat-chip"><div class="val">${{p.reliability.toFixed(2)}}</div><div class="lbl">Reliability</div></div>
          </div>
          <div class="card-insight"><strong>Why Clutch:</strong> ${{p.why_pressure || 'Solid performance across matches.'}}</div>
        </div>
      `;

      document.getElementById('compareCardA').innerHTML = renderCompCard(pA);
      document.getElementById('compareCardB').innerHTML = renderCompCard(pB);

      // Radar metrics
      const ctx = document.getElementById('radarChart');
      if (!ctx) return;

      const norm = (val, min, max) => Math.min(100, Math.max(10, ((val - min) / (max - min)) * 100));

      const dataA = [
        pA.score,
        norm(pA.balls_p, 120, 600),
        pA.sr_p ? norm(pA.sr_p, 140, 200) : norm(12 - pA.econ_p, 2, 6),
        norm(pA.reliability, 0.5, 0.9),
        pA.boundary_pct_p ? norm(pA.boundary_pct_p * 100, 15, 35) : norm(pA.dot_pct_p * 100, 20, 40)
      ];

      const dataB = [
        pB.score,
        norm(pB.balls_p, 120, 600),
        pB.sr_p ? norm(pB.sr_p, 140, 200) : norm(12 - pB.econ_p, 2, 6),
        norm(pB.reliability, 0.5, 0.9),
        pB.boundary_pct_p ? norm(pB.boundary_pct_p * 100, 15, 35) : norm(pB.dot_pct_p * 100, 20, 40)
      ];

      if (radarChart) radarChart.destroy();
      radarChart = new Chart(ctx, {{
        type: 'radar',
        data: {{
          labels: ['SPRI Score', 'Sample Volume', 'Pressure Rate (SR/Econ)', 'Reliability Shrinkage', 'Aggression/Dot %'],
          datasets: [
            {{
              label: pA.player_name,
              data: dataA,
              borderColor: '#EA1B86',
              backgroundColor: 'rgba(234, 27, 134, 0.25)',
              borderWidth: 2
            }},
            {{
              label: pB.player_name,
              data: dataB,
              borderColor: '#38BDF8',
              backgroundColor: 'rgba(56, 189, 248, 0.25)',
              borderWidth: 2
            }}
          ]
        }},
        options: {{
          scales: {{
            r: {{
              angleLines: {{ color: 'rgba(255, 255, 255, 0.1)' }},
              grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
              pointLabels: {{ color: '#94A3B8', font: {{ size: 12 }} }},
              suggestedMin: 0,
              suggestedMax: 100,
              ticks: {{ display: false }}
            }}
          }},
          plugins: {{
            legend: {{ labels: {{ color: '#fff', font: {{ family: "'Plus Jakarta Sans'" }} }} }}
          }}
        }}
      }});
    }}

    // Overview Bar Charts
    function renderOverviewCharts() {{
      const top10Bat = battersData.slice(0, 10);
      const top10Bowl = bowlersData.slice(0, 10);

      const batCtx = document.getElementById('batOverviewChart');
      if (batCtx) {{
        new Chart(batCtx, {{
          type: 'bar',
          data: {{
            labels: top10Bat.map(p => p.player_name.split(' ')[0]),
            datasets: [{{
              label: 'SPRI Score',
              data: top10Bat.map(p => p.score),
              backgroundColor: '#EA1B86',
              borderRadius: 6
            }}]
          }},
          options: {{
            responsive: true,
            scales: {{
              y: {{ min: 60, max: 95, grid: {{ color: 'rgba(255, 255, 255, 0.06)' }}, ticks: {{ color: '#94A3B8' }} }},
              x: {{ grid: {{ display: false }}, ticks: {{ color: '#E2E8F0', font: {{ size: 11 }} }} }}
            }},
            plugins: {{ legend: {{ display: false }} }}
          }}
        }});
      }}

      const bowlCtx = document.getElementById('bowlOverviewChart');
      if (bowlCtx) {{
        new Chart(bowlCtx, {{
          type: 'bar',
          data: {{
            labels: top10Bowl.map(p => p.player_name.split(' ')[0]),
            datasets: [{{
              label: 'SPRI Score',
              data: top10Bowl.map(p => p.score),
              backgroundColor: '#0066CC',
              borderRadius: 6
            }}]
          }},
          options: {{
            responsive: true,
            scales: {{
              y: {{ min: 60, max: 95, grid: {{ color: 'rgba(255, 255, 255, 0.06)' }}, ticks: {{ color: '#94A3B8' }} }},
              x: {{ grid: {{ display: false }}, ticks: {{ color: '#E2E8F0', font: {{ size: 11 }} }} }}
            }},
            plugins: {{ legend: {{ display: false }} }}
          }}
        }});
      }}
    }}

    // Init
    window.addEventListener('DOMContentLoaded', () => {{
      renderBatters();
      renderBowlers();
      renderDatabase();
      populateCompareSelects();
      renderOverviewCharts();
    }});
  </script>
</body>
</html>
"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Dashboard generated successfully: dashboard.html ({len(html_content):,} chars)")

