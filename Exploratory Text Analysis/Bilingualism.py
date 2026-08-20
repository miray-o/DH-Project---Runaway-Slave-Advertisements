#load the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import Cleaning

df = Cleaning.df

#count the number of ads that mention "dutch" and "english" in the same ad
def count_bilingual_ads(text):
    if 'dutch' in text and 'english' in text:
        return 1
    else:
        return 0

df['bilingual'] = df['tokens'].apply(count_bilingual_ads)
bilingual_count = df['bilingual'].sum()
print(f'The number of ads that mention both "dutch" and "english" is: {bilingual_count}')

#count the number of ads that mention "dutch" and "english" separately over the years
def count_language_mentions(text):
    dutch = 1 if 'dutch' in text else 0
    english = 1 if 'english' in text else 0
    return pd.Series({'dutch': dutch, 'english': english})

language_counts = df['tokens'].apply(count_language_mentions)
df = pd.concat([df, language_counts], axis=1)
language_year_counts = df.groupby('Year')[['dutch', 'english']].sum()
# Group data by 5-year intervals
df['FiveYear'] = (df['Year'] // 5 * 5).astype(int)

# Aggregate bilingual, Dutch, and English mentions by 5-year intervals
bilingual_5yr_counts = df.groupby('FiveYear')['bilingual'].sum()
language_5yr_counts = df.groupby('FiveYear')[['dutch', 'english']].sum()

# Combine the data into a single DataFrame for plotting
combined_5yr_counts = pd.DataFrame({
    'Bilingual Ads': bilingual_5yr_counts,
    'Dutch Mentions': language_5yr_counts['dutch'],
    'English Mentions': language_5yr_counts['english']
})

# Plot the combined line chart
plt.figure(figsize=(12, 6))
plt.plot(combined_5yr_counts.index, combined_5yr_counts['Bilingual Ads'], label='Bilingual Ads (Dutch & English)', marker='o')
plt.plot(combined_5yr_counts.index, combined_5yr_counts['Dutch Mentions'], label='Dutch Mentions', marker='s')
plt.plot(combined_5yr_counts.index, combined_5yr_counts['English Mentions'], label='English Mentions', marker='^')
plt.title('Bilingualism, Dutch, and English Mentions in Ads (Grouped by 5-Year Intervals)')
plt.xlabel('5-Year Interval')
plt.ylabel('Count')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Visualize 100% stacked bar chart of dutch and english mentions by decade
# Group ads by decade
language_year_counts['Decade'] = (language_year_counts.index // 10 * 10).astype(str) + 's'
language_decade_counts = language_year_counts.groupby('Decade').sum()

# Normalize the counts for 100% stacked bar chart
language_decade_counts_normalized = language_decade_counts.div(language_decade_counts.sum(axis=1), axis=0)

# Plot the 100% stacked bar chart
language_decade_counts_normalized.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Proportion of Dutch and English Mentions in Ads by Decade')
plt.xlabel('Decade')
plt.ylabel('Proportion')
plt.legend(title='Language Mentions')
plt.tight_layout()
plt.show()

# Extract decade from Year and search for language skill phrases
df['Decade'] = (df['Year'] // 10 * 10).astype(str) + 's'

def count_language_skills(text):
    speaks_dutch = 1 if 'speaks dutch' in text else 0
    speaks_broken_english = 1 if 'speaks broken english' in text else 0
    speaks_very_good_english = 1 if 'speaks very good english' in text else 0
    return pd.Series({
        'speaks_dutch': speaks_dutch,
        'speaks_broken_english': speaks_broken_english,
        'speaks_very_good_english': speaks_very_good_english
    })

language_skills = df['tokens'].apply(count_language_skills)
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