import pandas as pd
import time
import re
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/Users/mirayozmutlu/Documents/GitHub/DH-Project---Runaway-Slave-Advertisements/_Pretends To Be Free_ - Runaway Slave Ads - Sheet1 (1).csv')
# find a date-like column (case-insensitive); set `date_col` manually if detection fails
date_col = next((c for c in df.columns if 'date' in c.lower()), None)
if date_col is None:
    raise ValueError("No column with 'date' in its name found. Set `date_col` to the correct column name.")

# convert only that column to datetime (coerce invalid parsing to NaT)
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# create Year and Month columns
df['Year'] = df[date_col].dt.year
df['Month'] = df[date_col].dt.month

# quick check
print(df[[date_col, 'Year', 'Month']].head())
print(f"Parsed {df[date_col].notna().sum()} valid dates out of {len(df)} rows.")

#classify ads by gendered language
def classify_gendered_language(text):
    text = text.lower()
    if 'himself' in text or 'his' in text:
        return 'male gendered'
    elif 'herself' in text or 'her' in text:
        return 'female gendered'
    else:
        return 'neutral'

df['gendered_language'] = df['Content'].apply(classify_gendered_language)

# show the distribution of gendered language classifications
gender_counts = df['gendered_language'].value_counts()
print(gender_counts)

#show the distribution of gendered language classifications by year
gender_year_counts = df.groupby('Year')['gendered_language'].value_counts().unstack().fillna(0)
#make line chart showing the distribution of gendered language classifications by year
plt.figure(figsize=(12, 6))
for gender in gender_year_counts.columns:
    plt.plot(gender_year_counts.index, gender_year_counts[gender], label=gender)
plt.title('Distribution of Gendered Language Classifications by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.show()

#show the distribution of gendered language classifications by month
gender_month_counts = df.groupby('Month')['gendered_language'].value_counts().unstack().fillna(0)
#make line chart showing the distribution of gendered language classifications by month
plt.figure(figsize=(12, 6))
for gender in gender_month_counts.columns:
    plt.plot(gender_month_counts.index, gender_month_counts[gender], label=gender)
plt.title('Distribution of Gendered Language Classifications by Month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.show()

#show the distribution of gendered language classifications by year as stacked bar chart
gender_year_counts.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Distribution of Gendered Language Classifications by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend(title='Gendered Language')
plt.tight_layout()
plt.show()

#show the distribution of gendered language classifications by month as stacked bar chart
gender_month_counts.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Distribution of Gendered Language Classifications by Month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.legend(title='Gendered Language')
plt.tight_layout()
plt.show()
