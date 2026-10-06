import pandas as pd

STAGES = ["reach", "profile_visits", "link_clicks", "inquiries", "bookings"]


def summarize_funnel(df: pd.DataFrame):
    totals = {stage: float(df[stage].sum()) for stage in STAGES}
    rates = {}
    for before, after in zip(STAGES, STAGES[1:]):
        denom = totals[before]
        rates[f"{before}_to_{after}"] = (totals[after] / denom) if denom else 0.0
    return totals, rates


def biggest_dropoff(rates: dict):
    if not rates:
        return None, None
    key = min(rates, key=rates.get)
    return key, rates[key]


def score_content(df: pd.DataFrame):
    out = df.copy()
    out["booking_rate_from_profile"] = out["bookings"] / out["profile_visits"].replace(0, pd.NA)
    out["inquiry_rate_from_click"] = out["inquiries"] / out["link_clicks"].replace(0, pd.NA)
    out["downstream_score"] = (
        out["bookings"] * 5 + out["inquiries"] * 2 + out["link_clicks"]
    )
    return out.sort_values("downstream_score", ascending=False)


def build_ai_prompt(df: pd.DataFrame, totals: dict, rates: dict) -> str:
    top = score_content(df).head(3)[
        ["post_id", "format", "theme", "reach", "profile_visits", "link_clicks", "inquiries", "bookings"]
    ].to_dict(orient="records")
    return f"""You are helping review a creator-to-booking funnel.
Do not optimize for vanity metrics alone. Use the funnel numbers to identify where attention is lost and propose testable hypotheses.

FUNNEL TOTALS
{totals}

CONVERSION RATES
{rates}

TOP CONTENT BY DOWNSTREAM SCORE
{top}

Return:
1. The most important bottleneck.
2. Two plausible hypotheses for why it is happening.
3. Two small experiments for the next content cycle.
4. One metric that should NOT be over-interpreted and why.
Keep the recommendations specific and measurable.
"""
