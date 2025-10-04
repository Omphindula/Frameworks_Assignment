import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

sns.set(style="whitegrid")

st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research publications interactively")

# Load data
df = pd.read_csv("data/metadata.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))
df = df.dropna(subset=['year'])

# Sidebar: Year filter
year_range = st.slider("Select year range", int(df['year'].min()), int(df['year'].max()),
                       (int(df['year'].min()), int(df['year'].max())))
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.write(f"Showing papers from {year_range[0]} to {year_range[1]}")
st.dataframe(filtered_df[['title', 'journal', 'year']].head(10))

# Visualization: Publications per year
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values, color='skyblue')
ax.set_title("Publications by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Top 10 journals
top_journals = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots(figsize=(8,4))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis", ax=ax2)
ax2.set_title("Top 10 Journals")
st.pyplot(fig2)
