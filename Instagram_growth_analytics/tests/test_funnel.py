import pandas as pd
from funnel import summarize_funnel, biggest_dropoff


def test_summary_and_dropoff():
    df = pd.DataFrame([{ "reach":1000, "profile_visits":100, "link_clicks":20, "inquiries":10, "bookings":5 }])
    totals, rates = summarize_funnel(df)
    assert totals["bookings"] == 5
    key, value = biggest_dropoff(rates)
    assert key == "reach_to_profile_visits"
    assert value == 0.1
