import gensim.downloader as api
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import Cleaning
from itertools import chain
import random
from collections import Counter
import numpy as np

top_k = 200        # number of words to keep for embedding projection
label_k = 50       # number of points to annotate (must be <= top_k)
random_seed = 42
jitter = 0.01      # small jitter to spread overlapping points

# flatten words if nested
words = Cleaning.words
if any(isinstance(w, (list, tuple)) for w in words):
    words = list(chain.from_iterable(words))

# load model
model = api.load("glove-wiki-gigaword-50")

# keep only string tokens present in model
valid_words = [w for w in words if isinstance(w, str) and w in model]
if not valid_words:
    raise ValueError("No valid string tokens found in `Cleaning.words` that exist in the model.")

# pick top_k by frequency; fall back to random sample if fewer unique words
counts = Counter(valid_words)
most_common = [w for w, _ in counts.most_common(top_k)]
if len(most_common) < top_k:
    remaining = list(set(valid_words) - set(most_common))
    random.seed(random_seed)
    extra = random.sample(remaining, min(top_k - len(most_common), len(remaining)))
    chosen = most_common + extra
else:
    chosen = most_common

# get vectors and PCA
vectors = np.array([model[w] for w in chosen])
pca = PCA(n_components=2, random_state=random_seed)
vec2d = pca.fit_transform(vectors)

# optional small jitter to reduce exact overlaps
rng = np.random.default_rng(random_seed)
vec2d += rng.normal(scale=jitter, size=vec2d.shape)

# plot
plt.figure(figsize=(10, 7))
plt.scatter(vec2d[:, 0], vec2d[:, 1], s=10, alpha=0.6)
plt.title(f"PCA of {len(chosen)} words (annotating {min(label_k, len(chosen))})")

# annotate only label_k most frequent among the chosen words
label_candidates = [w for w, _ in Counter(chosen).most_common(label_k)]
for w, (x, y) in zip(chosen, vec2d):
    if w in label_candidates:
        plt.annotate(w, (x, y), fontsize=8, alpha=0.9)

plt.tight_layout()
plt.show()