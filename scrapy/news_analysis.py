#Loading and cleaning with pandas
import pymongo, pandas as pd, os
from textblob import TextBlob
from dotenv import load_dotenv
import streamlit as st
import plotly.express as px
load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["newsdb"]

# Put all documents from Atlas into a DataFrame
df = pd.DataFrame(list(db["articles"].find({}, {"_id": 0})))

# Essential cleaning steps
df = df.dropna(subset=["title", "date"]) # Remove rows missing these key fields

# Split at the space and take the first part (the ISO date)
df["date"] = pd.to_datetime(df["date"].str.split(" ").str[0], errors='coerce') # make date sortable

df["title"] = df["title"].str.strip() # strip whitespace
df = df.drop_duplicates(subset=["url"]) # deduplicate by URL
df = df.sort_values("date", ascending=False) # newest first

print(f"{len(df)} clean articles ready")

#Analysis - counts, trends, sentiment
# Add sentiment score: -1 (very negative) to +1 (very positive
df["sentiment"] = df["title"].apply(
    lambda x: TextBlob(x).sentiment.polarity
)

# Articles per day - feeds the volume line chart
daily_count = (df.groupby(df["date"].dt.date).size().reset_index(name="count"))

# Average sentiment per day - feeds the sentiment line chart
daily_sentiment = (df.groupby(df["date"].dt.date)["sentiment"].mean().reset_index()) 

#Streamlit - the "full-stack" browser UI
# (import df, daily_count, daily_sentiment from your process.py)

st.set_page_config(page_title="MP Media Monitor", layout="wide")
st.title("MP Media Monitor")

# Row 1: headline metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total articles", len(df))
col2.metric("Avg sentiment", round(df["sentiment"].mean(), 2))
col3.metric("Sources", df["source"].nunique())

# Row 2: charts
st.plotly_chart(
    px.line(daily_count, x="date", y="count",
            title="Articles per day"), use_container_width=True)
st.plotly_chart(
    px.bar(daily_sentiment, x="date", y="sentiment",
           title="Sentiment over time",
           color="sentiment", color_continuous_scale="RdYlGn"),
    use_container_width=True)

# Row 3: searchable article table
query = st.text_input("Search articles")
filtered = df[df["title"].str.contains(query, case=False, na=False)]
st.dataframe(filtered[["date","title","source","sentiment"]])