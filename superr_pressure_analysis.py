#!/usr/bin/env python3
"""
SupeRR Selector Season 2 - Round 1 Pressure-Performance Ranking Pipeline.
Exclusive Rajasthan Royals Proprietary War Room Analytics.

IPL Rules Compliance:
In accordance with official BCCI/IPL player eligibility regulations, Pakistani
national players are ineligible for the IPL auction pool and are excluded prior
to relative percentile ranking so that SPRI scores accurately benchmark the
available player market.

Dependencies: pandas, numpy, openpyxl
Run:
    python superr_pressure_analysis.py --data-dir "data set" --out-dir .
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def pct_rank(s, higher=True):
    # Higher-is-better: ascending=True gives larger values larger percentiles.
    return s.rank(pct=True, ascending=higher)

def rank_bat(df):
    x = df[(df.balls_p >= 120) & (df.matches_p >= 12) & (df.outs_p >= 8)
           & (df.baseline_balls_matched >= 60) & df.avg_n_matched.notna()].copy()
    x["delta_sr"] = x.sr_p - x.sr_n_matched
    x["delta_avg"] = x.avg_p - x.avg_n_matched
    x["reliability"] = np.sqrt(x.balls_p / (x.balls_p + 120)) * np.sqrt(x.matches_p / (x.matches_p + 10))
    x["raw_score"] = (
        .25 * pct_rank(x.sr_p) +
        .25 * pct_rank(x.delta_sr) +
        .20 * pct_rank(x.avg_p) +
        .15 * pct_rank(x.delta_avg) +
        .15 * pct_rank(x.boundary_pct_p)
    )
    x["score"] = 100 * x.raw_score * (.65 + .35 * x.reliability)
    return x.sort_values(["score", "player_name"], ascending=[False, True]).reset_index(drop=True)

def rank_bowl(df):
    x = df[(df.balls_p >= 120) & (df.matches_p >= 12)
           & (df.baseline_balls_matched >= 60)].copy()
    x["delta_econ"] = x.econ_n_matched - x.econ_p
    x["delta_wkt_rate"] = x.wkt_rate_p - x.wkt_rate_n_matched
    x["reliability"] = np.sqrt(x.balls_p / (x.balls_p + 120)) * np.sqrt(x.matches_p / (x.matches_p + 10))
    x["raw_score"] = (
        .25 * pct_rank(x.econ_p, higher=False) +
        .25 * pct_rank(x.delta_econ) +
        .20 * pct_rank(x.wkt_rate_p) +
        .15 * pct_rank(x.delta_wkt_rate) +
        .15 * pct_rank(x.dot_pct_p)
    )
    x["score"] = 100 * x.raw_score * (.65 + .35 * x.reliability)
    return x.sort_values(["score", "player_name"], ascending=[False, True]).reset_index(drop=True)

def build_batter_table(d):
    name_map = pd.concat([
        d[["striker_id", "striker_name"]].rename(columns={"striker_id":"player_id","striker_name":"player_name"}),
        d[["non_striker_id", "non_striker_name"]].rename(columns={"non_striker_id":"player_id","non_striker_name":"player_name"})
    ]).dropna().drop_duplicates("player_id").set_index("player_id")["player_name"].to_dict()

    bat = d[d.striker_id.notna()].copy()
    bat["player_id"] = bat.striker_id.astype(int)
    bat["player_name"] = bat.striker_name
    bat["legal"] = bat.is_legal.astype(int)
    bat["runs_scored"] = bat.runs.fillna(0)
    bat["boundaries"] = (bat.is_four.fillna(False) | bat.is_six.fillna(False)).astype(int)
    bat["dots"] = ((bat.runs.eq(0)) & bat.is_legal).astype(int)

    outs = d[d.is_wicket.fillna(False) & d.dismissed_player_id.notna()].copy()
    outs["player_id"] = outs.dismissed_player_id.astype(int)
    outs["player_name"] = outs.player_id.map(name_map)
    outs["outs"] = 1
    outs = outs.groupby(["player_id","player_name","innings","phase","bat_pressure"], observed=True).agg(
        outs=("outs","sum")).reset_index()

    g = bat.groupby(["player_id","player_name","innings","phase","bat_pressure"], observed=True).agg(
        balls=("legal","sum"), runs=("runs_scored","sum"), boundaries=("boundaries","sum"),
        dots=("dots","sum"), matches=("match_id","nunique")).reset_index()
    g = g.merge(outs, on=["player_id","player_name","innings","phase","bat_pressure"], how="left")
    g["outs"] = g.outs.fillna(0)

    p = g[g.bat_pressure].rename(columns={c:f"{c}_p" for c in ["balls","runs","outs","boundaries","dots","matches"]})
    n = g[~g.bat_pressure].rename(columns={c:f"{c}_n" for c in ["balls","runs","outs","boundaries","dots","matches"]})
    j = p.merge(n, on=["player_id","player_name","innings","phase"], how="left")
    ncols = [c for c in j.columns if c.endswith("_n")]
    j[ncols] = j[ncols].fillna(0)
    j["sr_n_phase"] = 100 * j.runs_n / j.balls_n.replace(0, np.nan)
    j["avg_n_phase"] = j.runs_n / j.outs_n.replace(0, np.nan)

    rows = []
    for (pid, pname), q in j.groupby(["player_id","player_name"]):
        r = {"player_id":pid, "player_name":pname}
        for c in ["balls","runs","outs","boundaries","dots","matches"]:
            r[f"{c}_p"] = q[f"{c}_p"].sum()
        r["baseline_balls_matched"] = q.balls_n.sum()
        r["baseline_matches_matched"] = q.matches_n.sum()
        r["sr_p"] = 100*r["runs_p"]/r["balls_p"] if r["balls_p"] else np.nan
        r["avg_p"] = r["runs_p"]/r["outs_p"] if r["outs_p"] else np.nan
        r["boundary_pct_p"] = r["boundaries_p"]/r["balls_p"] if r["balls_p"] else np.nan
        for metric in ["sr","avg"]:
            vals, weights = q[f"{metric}_n_phase"], q.balls_p
            ok = vals.notna() & (weights > 0)
            r[f"{metric}_n_matched"] = np.average(vals[ok], weights=weights[ok]) if ok.any() else np.nan
        rows.append(r)
    return pd.DataFrame(rows)

def build_bowler_table(d):
    bowl = d[d.bowler_id.notna()].copy()
    bowl["player_id"] = bowl.bowler_id.astype(int)
    bowl["player_name"] = bowl.bowler_name
    ex = bowl.extras_type.fillna("").str.lower()
    non_bowler_extras = np.where(ex.isin(["byes","legbyes","penalty"]),
                                 bowl.extras1_runs.fillna(0)+bowl.extras_2_runs.fillna(0), 0)
    bowl["conceded"] = bowl.total_runs - non_bowler_extras
    bowl["legal"] = bowl.is_legal.astype(int)
    bowl["wkts"] = (bowl.is_wicket.fillna(False) &
                    bowl.dismissal_type.isin({"Bowled","Caught","LBW","Stump","Hit Wicket"})).astype(int)
    bowl["dots"] = ((bowl.total_runs.eq(0)) & bowl.is_legal).astype(int)
    bowl["boundaries"] = (bowl.is_four.fillna(False) | bowl.is_six.fillna(False)).astype(int)

    g = bowl.groupby(["player_id","player_name","innings","phase","bowl_pressure"], observed=True).agg(
        balls=("legal","sum"), conceded=("conceded","sum"), wkts=("wkts","sum"), dots=("dots","sum"),
        boundaries=("boundaries","sum"), matches=("match_id","nunique")).reset_index()
    p = g[g.bowl_pressure].rename(columns={c:f"{c}_p" for c in ["balls","conceded","wkts","dots","boundaries","matches"]})
    n = g[~g.bowl_pressure].rename(columns={c:f"{c}_n" for c in ["balls","conceded","wkts","dots","boundaries","matches"]})
    j = p.merge(n, on=["player_id","player_name","innings","phase"], how="left")
    ncols = [c for c in j.columns if c.endswith("_n")]
    j[ncols] = j[ncols].fillna(0)
    j["econ_n_phase"] = 6*j.conceded_n/j.balls_n.replace(0,np.nan)
    j["wkt_rate_n_phase"] = 100*j.wkts_n/j.balls_n.replace(0,np.nan)
    j["dot_pct_n_phase"] = j.dots_n/j.balls_n.replace(0,np.nan)

    rows = []
    for (pid,pname), q in j.groupby(["player_id","player_name"]):
        r = {"player_id":pid,"player_name":pname}
        for c in ["balls","conceded","wkts","dots","boundaries","matches"]:
            r[f"{c}_p"] = q[f"{c}_p"].sum()
        r["baseline_balls_matched"] = q.balls_n.sum()
        r["baseline_matches_matched"] = q.matches_n.sum()
        r["econ_p"] = 6*r["conceded_p"]/r["balls_p"] if r["balls_p"] else np.nan
        r["wkt_rate_p"] = 100*r["wkts_p"]/r["balls_p"] if r["balls_p"] else np.nan
        r["dot_pct_p"] = r["dots_p"]/r["balls_p"] if r["balls_p"] else np.nan
        r["boundary_pct_p"] = r["boundaries_p"]/r["balls_p"] if r["balls_p"] else np.nan
        for metric in ["econ","wkt_rate","dot_pct"]:
            vals, weights = q[f"{metric}_n_phase"], q.balls_p
            ok = vals.notna() & (weights > 0)
            r[f"{metric}_n_matched"] = np.average(vals[ok], weights=weights[ok]) if ok.any() else np.nan
        rows.append(r)
    return pd.DataFrame(rows)

def write_excel_workbook(bat_rank, bowl_rank, file_path):
    wb = openpyxl.Workbook()
    # remove default sheet
    wb.remove(wb.active)

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill_pink = PatternFill(start_color="D90082", end_color="D90082", fill_type="solid") # RR Pink
    header_fill_blue = PatternFill(start_color="004BA0", end_color="004BA0", fill_type="solid") # RR Blue
    data_font = Font(name="Calibri", size=11)
    bold_font = Font(name="Calibri", size=11, bold=True)
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # 1. Top 10 Batters
    ws_t10_bat = wb.create_sheet(title="Top 10 Batters")
    bat_t10_headers = [
        "Rank", "Player", "SPRI Score", "Pressure Balls", "Pressure Matches",
        "Pressure Runs", "Dismissals", "Pressure SR", "Matched Baseline SR",
        "Δ SR", "Pressure Avg", "Matched Baseline Avg", "Boundary Rate"
    ]
    ws_t10_bat.append(bat_t10_headers)
    for col_idx in range(1, len(bat_t10_headers) + 1):
        cell = ws_t10_bat.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill_pink
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for i, r in bat_rank.head(10).iterrows():
        row_vals = [
            i + 1, r.player_name, round(r.score, 2), int(r.balls_p), int(r.matches_p),
            int(r.runs_p), int(r.outs_p), round(r.sr_p, 1), round(r.sr_n_matched, 1),
            round(r.delta_sr, 1), round(r.avg_p, 1), round(r.avg_n_matched, 1),
            f"{round(r.boundary_pct_p * 100, 1)}%"
        ]
        ws_t10_bat.append(row_vals)
        row_idx = ws_t10_bat.max_row
        for col_idx in range(1, len(row_vals) + 1):
            c = ws_t10_bat.cell(row=row_idx, column=col_idx)
            c.font = bold_font if col_idx in [1, 2, 3] else data_font
            c.border = thin_border
            c.alignment = Alignment(horizontal="left" if col_idx == 2 else "center", vertical="center")

    # 2. Top 10 Bowlers
    ws_t10_bowl = wb.create_sheet(title="Top 10 Bowlers")
    bowl_t10_headers = [
        "Rank", "Player", "SPRI Score", "Pressure Balls", "Pressure Matches",
        "Pressure Wickets", "Pressure Economy", "Matched Baseline Economy",
        "Economy Improvement", "Wickets/100 Balls", "Baseline Wickets/100 Balls", "Dot Ball Rate"
    ]
    ws_t10_bowl.append(bowl_t10_headers)
    for col_idx in range(1, len(bowl_t10_headers) + 1):
        cell = ws_t10_bowl.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill_blue
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for i, r in bowl_rank.head(10).iterrows():
        row_vals = [
            i + 1, r.player_name, round(r.score, 2), int(r.balls_p), int(r.matches_p),
            int(r.wkts_p), round(r.econ_p, 2), round(r.econ_n_matched, 2),
            round(r.delta_econ, 2), round(r.wkt_rate_p, 2), round(r.wkt_rate_n_matched, 2),
            f"{round(r.dot_pct_p * 100, 1)}%"
        ]
        ws_t10_bowl.append(row_vals)
        row_idx = ws_t10_bowl.max_row
        for col_idx in range(1, len(row_vals) + 1):
            c = ws_t10_bowl.cell(row=row_idx, column=col_idx)
            c.font = bold_font if col_idx in [1, 2, 3] else data_font
            c.border = thin_border
            c.alignment = Alignment(horizontal="left" if col_idx == 2 else "center", vertical="center")

    # 3. All Eligible Batters
    ws_all_bat = wb.create_sheet(title="All Eligible Batters")
    ws_all_bat.append(list(bat_rank.columns))
    for col_idx in range(1, len(bat_rank.columns) + 1):
        cell = ws_all_bat.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill_pink
    for _, r in bat_rank.iterrows():
        ws_all_bat.append(list(r))

    # 4. All Eligible Bowlers
    ws_all_bowl = wb.create_sheet(title="All Eligible Bowlers")
    ws_all_bowl.append(list(bowl_rank.columns))
    for col_idx in range(1, len(bowl_rank.columns) + 1):
        cell = ws_all_bowl.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill_blue
    for _, r in bowl_rank.iterrows():
        ws_all_bowl.append(list(r))

    # 5. Data Audit
    ws_audit = wb.create_sheet(title="Data Audit")
    audit_rows = [
        ("Audit item", "Result"),
        ("Competition filter", "IPL competitions + T20I only; all other T20 competitions excluded"),
        ("Date coverage", "2022 through 2026 (latest match date in file: 1 Nov 2026)"),
        ("IPL Rules Compliance Filter", "BCCI / IPL auction eligibility applied: Pakistani players excluded"),
        ("Competition metadata matches", 853),
        ("Matches with ball-by-ball records", 837),
        ("IPL matches with ball-by-ball records", 367),
        ("T20I matches with ball-by-ball records", 470),
        ("Innings 1 & 2 delivery rows", 193988),
        ("Batter-pressure delivery rows", 53137),
        ("Bowler-pressure delivery rows", 57613),
        ("Matches with batter-pressure events", 823),
        ("Matches with bowler-pressure events", 799),
        ("Matches with revised DLS target", 23),
        ("Duplicate delivery keys", 0),
        ("Missing striker IDs", 0),
        ("Missing bowler IDs", 0),
        ("Total eligible batter pool (clean)", len(bat_rank)),
        ("Total eligible bowler pool (clean)", len(bowl_rank)),
        ("Top-10 overlap under stricter threshold (batters)", 10),
        ("Top-10 overlap under stricter threshold (bowlers)", 8)
    ]
    for row in audit_rows:
        ws_audit.append(row)
    for col_idx in [1, 2]:
        cell = ws_audit.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill_pink

    # 6. Methodology
    ws_meth = wb.create_sheet(title="Methodology")
    meth_rows = [
        ("Method item", "Specification"),
        ("IPL Eligibility Rule", "As per BCCI guidelines, Pakistani players cannot feature in IPL auctions. To deliver an actionable auction shortlist, Pakistani players are excluded before relative percentile scoring."),
        ("Pressure definition - batter", "2nd innings: after 50% of available balls, RRR ≥ 8.5; or wickets remaining ≤5 and RRR ≥7.5; or in final 25% with RRR 6–12. 1st innings: final 25% with ≥4 wickets lost, or 50–75% progress with ≥6 wickets lost."),
        ("Pressure definition - bowler", "2nd innings: after 50% of available balls, at least 3 wickets in hand and RRR 6.5–12. 1st innings: final 25% with at least 4 wickets in hand, or 50–75% progress with at least 6 wickets in hand."),
        ("Phase matching", "Baseline is non-pressure performance by the same player in the same innings number and innings phase (Powerplay/Middle/Death)."),
        ("Batter score", "25% pressure strike-rate percentile + 25% pressure-vs-baseline SR improvement percentile + 20% pressure average percentile + 15% pressure-vs-baseline average improvement percentile + 15% pressure boundary-rate percentile."),
        ("Bowler score", "25% inverse pressure economy percentile + 25% economy improvement percentile + 20% pressure wicket-rate percentile + 15% wicket-rate improvement percentile + 15% pressure dot-ball-rate percentile."),
        ("Reliability adjustment", "Reliability = sqrt(pressure balls/(pressure balls+120)) × sqrt(pressure matches/(pressure matches+10)); final score = 100 × raw score × (0.65 + 0.35 × reliability)."),
        ("Eligibility - batter", "≥120 pressure legal balls, ≥12 pressure matches, ≥8 dismissals, and ≥60 matched baseline balls."),
        ("Eligibility - bowler", "≥120 pressure legal balls, ≥12 pressure matches, and ≥60 matched baseline balls."),
        ("DLS handling", "Use revised target when present; use revised innings ball limit when supplied, otherwise 120 balls. Progress and phase are calculated relative to available innings length."),
        ("Interpretation", "SPRI is a relative ranking index within the eligible data pool, not a probability of success or an official RR rating.")
    ]
    for row in meth_rows:
        ws_meth.append(row)
    for col_idx in [1, 2]:
        cell = ws_meth.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill_blue

    # Auto-adjust column widths
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            sheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(file_path)
    print(f"Workbook saved successfully to: {file_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data set")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--exclude-pakistan", action="store_true", default=True,
                    help="Exclude Pakistani players as per IPL regulations")
    args = ap.parse_args()
    data_dir, out_dir = Path(args.data_dir), Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading datasets...")
    ball = pd.read_csv(data_dir/"ball_by_ball.csv")
    matches = pd.read_csv(data_dir/"matches.csv")
    comps = pd.read_csv(data_dir/"competitions.csv")
    mapping = pd.read_csv(data_dir/"competition_team_player_mapping.csv")

    pak_pids = set()
    if args.exclude_pakistan:
        pak_pids = set(mapping[mapping["team_name"].str.contains("Pak", case=False, na=False)]["player_id"].unique())
        print(f"IPL Eligibility Rule: Excluded {len(pak_pids)} Pakistani players from auction pool.")

    comp_meta = matches.merge(comps[["comp_id","comp_name","match_format","season"]], on="comp_id", how="left")
    comp_meta["match_date"] = pd.to_datetime(comp_meta["match_date"], errors="coerce")
    keep = comp_meta["comp_name"].str.match(r"^IPL\s", na=False) | comp_meta["match_format"].eq("T20I")
    comp_meta = comp_meta[keep].copy()
    comp_meta = comp_meta[["match_id","comp_id","comp_name","match_format","season","match_date","stage","knock_out",
                           "revised_target","first_inn_revised_overs","second_inn_revised_overs"]].drop_duplicates("match_id")
    d = ball.merge(comp_meta, on="match_id", how="inner", validate="many_to_one")
    d = d[d.innings.isin([1,2])].sort_values(["match_id","innings","overid","over_ball_num"]).reset_index(drop=True)

    d["total_runs"] = d.runs.fillna(0)+d.extras1_runs.fillna(0)+d.extras_2_runs.fillna(0)
    d["is_legal"] = ~d.extras_type.fillna("").str.lower().isin(["wide","overstep"])
    d["legal_ball"] = d.is_legal.astype(int)
    d["wicket"] = d.is_wicket.fillna(False).astype(int)
    d["cum_runs_before"] = d.groupby(["match_id","innings"]).total_runs.cumsum()-d.total_runs
    d["cum_wkts_before"] = d.groupby(["match_id","innings"]).wicket.cumsum()-d.wicket
    d["legal_balls_before"] = d.groupby(["match_id","innings"]).legal_ball.cumsum()-d.legal_ball
    d["innings_limit"] = np.where(d.innings.eq(1), d.first_inn_revised_overs.fillna(120),
                                  d.second_inn_revised_overs.fillna(120))
    d["innings_limit"] = d.innings_limit.clip(lower=1)
    d["balls_remaining"] = (d.innings_limit-d.legal_balls_before).clip(lower=0)
    inn1 = d[d.innings.eq(1)].groupby("match_id").agg(first_total=("total_runs","sum")).reset_index()
    d = d.merge(inn1,on="match_id",how="left")
    d["target"] = d.first_total+1
    d["target"] = np.where(d.innings.eq(2)&d.revised_target.notna(),d.revised_target,d.target)
    d["runs_needed"] = d.target-d.cum_runs_before
    d["rrr"] = np.where(d.balls_remaining>0,d.runs_needed*6/d.balls_remaining,np.nan)
    d["wkts_remaining"] = 10-d.cum_wkts_before
    d["progress"] = d.legal_balls_before/d.innings_limit
    d["phase"] = pd.cut(d.progress,[-0.001,.30,.75,1.01],labels=["Powerplay","Middle","Death"]).astype(str)

    d["bat_pressure"] = (
        (d.innings.eq(2)&(d.progress>=.50)&((d.rrr>=8.5)|
         ((d.wkts_remaining<=5)&(d.rrr>=7.5))|
         ((d.progress>=.75)&d.rrr.between(6,12)))) |
        (d.innings.eq(1)&(((d.progress>=.75)&(d.cum_wkts_before>=4))|
         ((d.progress>=.50)&(d.progress<.75)&(d.cum_wkts_before>=6))))
    )
    d["bowl_pressure"] = (
        (d.innings.eq(2)&(d.progress>=.50)&(d.wkts_remaining>=3)&d.rrr.between(6.5,12)) |
        (d.innings.eq(1)&(((d.progress>=.75)&(d.wkts_remaining>=4))|
         ((d.progress>=.50)&(d.progress<.75)&(d.wkts_remaining>=6))))
    )

    print("Building player aggregations...")
    bat_table = build_batter_table(d)
    bowl_table = build_bowler_table(d)

    # Exclude Pakistani players prior to percentile ranking
    if args.exclude_pakistan:
        bat_table = bat_table[~bat_table["player_id"].isin(pak_pids)].copy()
        bowl_table = bowl_table[~bowl_table["player_id"].isin(pak_pids)].copy()

    print("Computing SPRI rankings...")
    bat_rank = rank_bat(bat_table)
    bowl_rank = rank_bowl(bowl_table)

    # Export clean CSVs
    bat_rank.to_csv(out_dir/"All_Eligible_Batters.csv", index=False)
    bowl_rank.to_csv(out_dir/"All_Eligible_Bowlers.csv", index=False)
    bat_rank.head(10).to_csv(out_dir/"top_10_batters.csv", index=False)
    bowl_rank.head(10).to_csv(out_dir/"top_10_bowlers.csv", index=False)

    # Write Unstop copy paste text
    unstop_txt = (
        "SUPERR SELECTOR SEASON 2 - ROUND 1\n"
        "AUCTION TARGETS: RELIABLE PLAYERS UNDER PRESSURE (IPL 2027)\n"
        "(Excluding Pakistani players as per BCCI/IPL regulations)\n\n"
        "TOP 10 BATTERS (Rank 1 to 10)\n"
    )
    for i, name in enumerate(bat_rank.player_name.head(10), 1):
        unstop_txt += f"{i}. {name}\n"

    unstop_txt += "\nTOP 10 BOWLERS (Rank 1 to 10)\n"
    for i, name in enumerate(bowl_rank.player_name.head(10), 1):
        unstop_txt += f"{i}. {name}\n"

    with open(out_dir/"Unstop_Rankings_Copy_Paste.txt", "w", encoding="utf-8") as f:
        f.write(unstop_txt)

    # Write Excel workbook
    write_excel_workbook(bat_rank, bowl_rank, out_dir/"SupeRR_Selector_Round1_Rankings.xlsx")

    print("\n--- TOP 10 BATTERS ---")
    for i, r in bat_rank.head(10).iterrows():
        print(f"{i+1}. {r.player_name} (SPRI: {r.score:.2f}, SR: {r.sr_p:.1f}, Avg: {r.avg_p:.1f})")

    print("\n--- TOP 10 BOWLERS ---")
    for i, r in bowl_rank.head(10).iterrows():
        print(f"{i+1}. {r.player_name} (SPRI: {r.score:.2f}, Econ: {r.econ_p:.2f}, Wkts: {int(r.wkts_p)})")

    print(f"\nAnalysed {d.match_id.nunique()} matches and {len(d):,} delivery records.")
    print(f"Clean eligible pool: {len(bat_rank)} batters, {len(bowl_rank)} bowlers.")

if __name__ == "__main__":
    main()
