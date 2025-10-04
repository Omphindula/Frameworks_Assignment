# ===============================================
# CORD-19 Data Analysis Assignment
# ===============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

sns.set(style="whitegrid")

# --------------------------
# Task 1: Load and Explore Dataset
# --------------------------
try:
    df = pd.read_csv("data/metadata.csv")
    print("=== Dataset Shape ===")
    print(df.shape, "\n")
    
    print("=== Dataset Info ===")
    print(df.info(), "\n")
    
    print("=== Missing Values ===")
    print(df.isnull().sum(), "\n")
    
except FileNotFoundError:
    print("Error: metadata.csv not found in data folder.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# --------------------------
# Task 2: Data Cleaning
# --------------------------
# Convert publication date to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

# Drop rows without year
df = df.dropna(subset=['year'])

# Example: create abstract word count
df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))

# --------------------------
# Task 3: Analysis & Visualization
# --------------------------

# Publications per year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,5))
plt.bar(year_counts.index, year_counts.values, color='skyblue')
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.show()

# Top 10 journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.show()

# Most frequent words in titles
titles = " ".join(df['title'].dropna()).lower().split()
common_words = Counter(titles).most_common(20)
words, counts = zip(*common_words)

plt.figure(figsize=(10,5))
sns.barplot(x=list(counts), y=list(words), palette="magma")
plt.title("Top 20 Most Frequent Words in Paper Titles")
plt.xlabel("Frequency")
plt.ylabel("Word")
plt.show()
