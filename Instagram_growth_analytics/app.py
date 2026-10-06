from pathlib import Path
import pandas as pd
import streamlit as st
from funnel import summarize_funnel, biggest_dropoff, score_content, build_ai_prompt

st.set_page_config(page_title="uniqueoren Growth Ops", page_icon="🎨", layout="wide")
st.title("uniqueoren Growth Ops")
st.caption("Creative analytics → funnel signals → next experiment")

sample_path = Path(__file__).with_name("sample_metrics.csv")
upload = st.file_uploader("Upload Instagram / funnel CSV", type="csv")
df = pd.read_csv(upload if upload else sample_path)

required = {"post_id","format","theme","reach","profile_visits","link_clicks","inquiries","bookings"}
missing = required - set(df.columns)
if missing:
    st.error(f"Missing columns: {', '.join(sorted(missing))}")
    st.stop()

totals, rates = summarize_funnel(df)
key, value = biggest_dropoff(rates)

cols = st.columns(5)
for col, stage in zip(cols, ["reach","profile_visits","link_clicks","inquiries","bookings"]):
    col.metric(stage.replace("_"," ").title(), f"{int(totals[stage]):,}")

st.subheader("Stage conversion")
rate_df = pd.DataFrame([
    {"stage": k.replace("_to_", " → ").replace("_", " "), "conversion": v}
    for k, v in rates.items()
])
rate_df["conversion"] = rate_df["conversion"].map(lambda x: f"{x:.1%}")
st.dataframe(rate_df, use_container_width=True, hide_index=True)

if key:
    st.warning(f"Largest drop-off: {key.replace('_to_', ' → ').replace('_',' ')} ({value:.1%} conversion)")

st.subheader("Content ranked by downstream value")
ranked = score_content(df)
st.dataframe(ranked, use_container_width=True, hide_index=True)

st.subheader("AI analysis prompt")
st.code(build_ai_prompt(df, totals, rates), language="text")

st.info("Demo data is synthetic. The real workflow is designed to use exported platform metrics plus booking / inquiry counts.")
