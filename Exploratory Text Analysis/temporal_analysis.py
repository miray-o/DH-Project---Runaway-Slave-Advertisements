import Cleaning
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = Cleaning.df


# Create a new column for decade
df['Decade'] = (df['Year'] // 10) * 10

# Group ads by decade and produce corpora
corpora_by_decade = {}
for decade, group in df.groupby('Decade'):
    # Flatten the list of tokens for each decade and join them into a single string
    corpora_by_decade[decade] = " ".join([" ".join(tokens) for tokens in group['tokens'].dropna()])

# Generate and display word clouds for each decade
for decade, text in corpora_by_decade.items():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Word Cloud for {decade}s")
    plt.show()



