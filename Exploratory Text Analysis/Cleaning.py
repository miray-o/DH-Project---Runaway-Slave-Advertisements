#load the necessary libraries
import pandas as pd
import time
import re
import nltk
from nltk.corpus import stopwords
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

def normalize_text(text):
    if not isinstance(text, str):
        return ""

    # Lowercase for uniformity
    text = text.lower()

    # Standardize common archaic terms found in runaway ads
    text = re.sub(r'\bnegroe\b', 'negro', text)
    text = re.sub(r'\bcloathes\b', 'clothes', text)
    text = re.sub(r'\bcloaths\b', 'clothes', text)
    text = re.sub(r'\bgaol\b', 'jail', text)
    text = re.sub(r'\bgoal\b', 'jail', text)
    text = re.sub(r'\bwest-coat\b', 'waistcoat', text)
    text = re.sub(r'\bwastecoat\b', 'waistcoat', text)
    text = re.sub(r'\bwestcoat\b', 'waistcoat', text)
    text = re.sub(r'\bbritches\b', 'breeches', text)
    text = re.sub(r'\bozenbrigs\b', 'osnaburg', text) # A common coarse fabric
    text = re.sub(r'\bosenbrigs\b', 'osnaburg', text)
    text = re.sub(r'\bozenbrig\b', 'osnaburg', text)

    # Remove punctuation for bag-of-words analysis
    text = re.sub(r'[^\w\s]', '', text)

    return text

df['cleaned_content'] = df['Content'].apply(normalize_text)

# map resource names to nltk.data paths
_RESOURCE_PATHS = {
    'punkt': 'tokenizers/punkt',
    'stopwords': 'corpora/stopwords',
}

def ensure_nltk_resource(name, max_retries=3):
    path = _RESOURCE_PATHS.get(name)
    if not path:
        return False
    try:
        nltk.data.find(path)
        return True
    except LookupError:
        delay = 1.0
        for attempt in range(max_retries):
            try:
                nltk.download(name, quiet=True)
                nltk.data.find(path)
                return True
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    return False

# ensure resources (won't re-download if already present)
punkt_ok = ensure_nltk_resource('punkt')
stopwords_ok = ensure_nltk_resource('stopwords')

# prepare stop words (fallback to empty set if not available)
try:
    stop_words = set(stopwords.words('english')) if stopwords_ok else set()
except Exception:
    stop_words = set()

# add domain-specific boilerplate words
boilerplate = {
    'runaway', 'run', 'away', 'master', 'subscriber', 'whereas',
    'named', 'reward', 'shillings', 'pounds', 'paid', 'charges',
    'reasonable', 'notice', 'give', 'secure', 'bring', 'delivered',
    'whoever', 'takes', 'person', 'negro', 'man', 'fellow', 'woman', 'wench',
    'said', 'return', 'jail', 'gaol', 'shall', 'may', 'went', 'says', 'years'
}
stop_words.update(boilerplate)

# robust tokenizer: use nltk if punkt is available, otherwise a regex fallback
def tokenize_text(text):
    if not isinstance(text, str):
        return []
    if punkt_ok:
        try:
            return nltk.word_tokenize(text)
        except Exception:
            pass
    # fallback: simple word tokenization (keeps only word characters)
    return re.findall(r'\b\w+\b', text.lower())

def remove_stopwords(text):
    tokens = tokenize_text(text)
    return [w for w in tokens if w.lower() not in stop_words]

# Example application (assuming `df` and `cleaned_content` already exist):
df['tokens'] = df['cleaned_content'].apply(remove_stopwords)

words = df['tokens']
