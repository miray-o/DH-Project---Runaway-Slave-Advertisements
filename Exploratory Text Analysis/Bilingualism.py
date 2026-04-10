#load the necessary libraries
import pandas as pd
import time
import re
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import Cleaning

df = Cleaning.df
#count the number of ads that mention "dutch" and "english" in the same ad
def count_bilingual_ads(text):
    text = text.lower()
    if 'dutch' in text and 'english' in text:
        return 1
    else:
        return 0

df['bilingual'] = df['Content'].apply(count_bilingual_ads)
bilingual_count = df['bilingual'].sum()
print(f'The number of ads that mention both "dutch" and "english" is: {bilingual_count}')
#visualize the count of bilingual ads over the years
bilingual_year_counts = df.groupby('Year')['bilingual'].sum()
plt.figure(figsize=(12, 6))
plt.plot(bilingual_year_counts.index, bilingual_year_counts.values, label='Bilingual Ads (Dutch & English)')
plt.title('Count of Bilingual Ads (Dutch & English) by Year')
plt.xlabel('Year')
plt.ylabel('Count of Bilingual Ads')
plt.legend()
plt.tight_layout()
plt.show()
#count the number of ads that mention "dutch" and "english" separately over the years
def count_language_mentions(text):
    text = text.lower()
    dutch = 1 if 'dutch' in text else 0
    english = 1 if 'english' in text else 0
    return pd.Series({'dutch': dutch, 'english': english})

language_counts = df['Content'].apply(count_language_mentions)
df = pd.concat([df, language_counts], axis=1)
language_year_counts = df.groupby('Year')[['dutch', 'english']].sum()
#visualize the counts over the years
plt.figure(figsize=(12, 6))
plt.plot(language_year_counts.index, language_year_counts['dutch'], label='Dutch Mentions')
plt.plot(language_year_counts.index, language_year_counts['english'], label='English Mentions')
plt.title('Mentions of Dutch and English in Ads by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.show()

# Visualize 100% stacked bar chart of dutch and english mentions by year
language_year_counts_normalized = language_year_counts.div(language_year_counts.sum(axis=1), axis=0)

language_year_counts_normalized.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Proportion of Dutch and English Mentions in Ads by Year')
plt.xlabel('Year')
plt.ylabel('Proportion')
plt.legend(title='Language Mentions')
plt.tight_layout()
plt.show()

# Extract decade from Year and search for language skill phrases
df['Decade'] = (df['Year'] // 10 * 10).astype(str) + 's'

def count_language_skills(text):
    text = text.lower()
    speaks_dutch = 1 if 'speaks dutch' in text else 0
    speaks_broken_english = 1 if 'speaks broken english' in text else 0
    speaks_very_good_english = 1 if 'speaks very good english' in text else 0
    return pd.Series({
        'speaks_dutch': speaks_dutch,
        'speaks_broken_english': speaks_broken_english,
        'speaks_very_good_english': speaks_very_good_english
    })

language_skills = df['Content'].apply(count_language_skills)
df = pd.concat([df, language_skills], axis=1)

# Track frequency by decade
skills_by_decade = df.groupby('Decade')[['speaks_dutch', 'speaks_broken_english', 'speaks_very_good_english']].sum()

# Visualize the trends
plt.figure(figsize=(12, 6))
plt.plot(skills_by_decade.index, skills_by_decade['speaks_dutch'], marker='o', label='Speaks Dutch')
plt.plot(skills_by_decade.index, skills_by_decade['speaks_broken_english'], marker='s', label='Speaks Broken English')
plt.plot(skills_by_decade.index, skills_by_decade['speaks_very_good_english'], marker='^', label='Speaks Very Good English')
plt.title('Diachronic Analysis of Language Skills (1720s–1770s)')
plt.xlabel('Decade')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Print summary statistics
print(skills_by_decade)

#visualize langauge skills as 100% stacked bar chart by year
#filter df by years 1730-1770
df = df[(df['Year'] >= 1730) & (df['Year'] <= 1770)]
skills_by_year = df.groupby('Decade')[['speaks_dutch', 'speaks_broken_english', 'speaks_very_good_english']].sum()
skills_by_year_normalized = skills_by_year.div(skills_by_year.sum(axis=1), axis=0)
skills_by_year_normalized.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Proportion of Language Skills in Ads by Year')
plt.xlabel('Year')
plt.ylabel('Proportion of Language Skills')
plt.legend(title='Language Skills')
plt.tight_layout()
plt.show()