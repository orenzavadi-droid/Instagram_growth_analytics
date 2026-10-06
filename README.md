# uniqueoren Growth Ops

A lightweight analytics workflow for connecting creative performance to a simple conversion funnel for a tattoo / illustration page.

## Why I built it

Creative metrics are easy to look at in isolation. I wanted one place that connects what gets attention to what actually moves a person closer to booking.

The funnel is intentionally simple:

**Content reach → profile visit → bio link click → inquiry → booking**

Calendly acts as a low-friction conversion endpoint in the bio, while this workflow helps review the numbers around it and decide what to test next.

## What it does

- Loads a CSV export of post / funnel metrics.
- Calculates stage-by-stage conversion rates.
- Identifies the biggest drop-off in the funnel.
- Ranks content by downstream value, not just reach.
- Builds an AI-analysis prompt that asks for hypotheses and next experiments rather than generic advice.
- Includes synthetic sample data so the repo is safe to share publicly.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How I use the logic

The point is not to let AI "decide" what content to make. The workflow gives me a compact weekly view of the funnel, highlights where attention is being lost, and helps generate testable hypotheses. I can then compare those hypotheses with the actual creative context and decide what to change next.
