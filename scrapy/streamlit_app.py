import os

import pandas as pd
import plotly.express as px
import pymongo
import streamlit as st
from dotenv import load_dotenv
from textblob import TextBlob


@st.cache_data(ttl=300)
def load_articles() -> pd.DataFrame:
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not set. Add it to .env or your shell environment.")

    client = pymongo.MongoClient(mongo_uri)
    df = pd.DataFrame(list(client["newsdb"]["articles"].find({}, {"_id": 0})))

    if df.empty:
        return pd.DataFrame(columns=["date", "title", "source", "sentiment"])

    df = df.dropna(subset=["title", "date"]).copy()
    df["date"] = pd.to_datetime(df["date"].astype(str).str.split().str[0], errors="coerce")
    df = df.dropna(subset=["date"])
    df["title"] = df["title"].astype(str).str.strip()

    if "source" not in df.columns:
        df["source"] = "Unknown"

    df["sentiment"] = df["title"].apply(lambda title: TextBlob(title).sentiment.polarity)
    return df.sort_values("date", ascending=False)


st.set_page_config(page_title="MP Media Monitor", layout="wide")
st.title("MP Media Monitor")

try:
    df = load_articles()
except Exception as exc:
    st.error(str(exc))
    st.stop()

daily_count = df.groupby(df["date"].dt.date).size().reset_index(name="count")
daily_sentiment = df.groupby(df["date"].dt.date)["sentiment"].mean().reset_index()

col1, col2, col3 = st.columns(3)
col1.metric("Total articles", len(df))
col2.metric("Avg sentiment", round(df["sentiment"].mean(), 2) if not df.empty else 0)
col3.metric("Sources", df["source"].nunique() if not df.empty else 0)

st.plotly_chart(
    px.line(daily_count, x="date", y="count", title="Articles per day"),
    width="stretch",
)
st.plotly_chart(
    px.bar(
        daily_sentiment,
        x="date",
        y="sentiment",
        title="Sentiment over time",
        color="sentiment",
        color_continuous_scale="RdYlGn",
    ),
    width="stretch",
)

query = st.text_input("Search articles")
filtered = df[df["title"].str.contains(query, case=False, na=False)]
st.dataframe(filtered[["date", "title", "source", "sentiment"]], width="stretch")
