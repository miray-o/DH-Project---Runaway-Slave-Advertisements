import string
from string import punctuation

import nltk

import Cleaning
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
punct = set(string.punctuation)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(Cleaning.df['tokens'].apply(lambda tokens: ' '.join(tokens)))

# Convert the TF-IDF matrix to a heatmap
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# select top terms by mean TF-IDF
top_n = 30
term_means = df_tfidf.mean(axis=0).sort_values(ascending=False)
top_terms = term_means.head(top_n).index.tolist()

# limit rows (documents) to a reasonable number for visualization
max_docs = 40
subset = df_tfidf.loc[:max_docs-1, top_terms]

# heatmap (no annotations, readable size)
plt.figure(figsize=(14, max(4, len(subset)*0.18)))
sns.heatmap(subset, cmap='viridis', cbar=True, xticklabels=True, yticklabels=True)
plt.title(f'TF-IDF heatmap (top {top_n} terms, first {len(subset)} ads)')
plt.xlabel('Terms')
plt.ylabel('Ads')
plt.tight_layout()
plt.show()

# bar plot of global top terms
plt.figure(figsize=(10,5))
term_means.head(20).plot(kind='bar', color='C0')
plt.title('Top 20 terms by mean TF-IDF')
plt.ylabel('Mean TF-IDF')
plt.tight_layout()
plt.show()

