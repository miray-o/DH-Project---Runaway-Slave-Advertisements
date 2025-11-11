import json
import numpy as np
import random
import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example

# --- Load your data ---
with open("/Users/mirayozmutlu/Documents/GitHub/Journal-Of-Digital-History-Manuscript/script/annotations.json") as f:
    DATA = json.load(f)["annotations"]  # Expecting list of (text, {'entities': [...]})

# --- Split into 80% train, 20% test ---
N = len(DATA)
# Randomly select 20% of the data for testing
test_idx = np.random.randint(N, size=N//5)
TEST_DATA = np.array(DATA)[test_idx].tolist()
# Leave the remaining 80% as training data
train_idx = list(set(np.arange(N))-set(test_idx))
TRAIN_DATA = np.array(DATA)[train_idx].tolist()

# --- Load a pre-existing SpaCy model ---
nlp = spacy.load('en_core_web_sm')  # change to another model if needed

# Getting the pipeline component
ner=nlp.get_pipe("ner")
# Disable pipeline components you dont need to change
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
# Import requirements
import random
from spacy.util import minibatch, compounding
from pathlib import Path
from spacy.training.example import Example
# TRAINING THE MODEL
with nlp.disable_pipes(*unaffected_pipes):
  # Training for 30 iterations
  for iteration in range(30):
    # shuffling examples  before every iteration
    random.shuffle(TRAIN_DATA)
    losses = {}
    # batch up the examples using spaCy's minibatch
    batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
      for text, annotations in batch:
        # create Example
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update(
                 [example],
                 drop=0.5, # dropout - make it harder to memorise data
                 losses=losses,
                 )
print("Losses", losses)

import matplotlib.pyplot as plt
from spacy.scorer import Scorer
from spacy.tokens import Doc
def evaluate(ner_model, examples):
  scorer = Scorer()
  example = []
  for input_, annot in examples:
    pred = ner_model(input_)
    temp = Example.from_dict(pred, annot)
    example.append(temp)
    scores = scorer.score(example)
  return scores
results = evaluate(nlp, TEST_DATA)
print(results)
# Calculate sample size
from collections import Counter
ent = []
for x in TEST_DATA:
  ent += [i[-1] for i in x[1]['entities']]
sample_sizes = Counter(ent)
print(sample_sizes)
import matplotlib.pyplot as plt
import numpy as np

# Data from the second evaluation
tags = [
    "ENSLAVER", "LOCATION", "GENDER", "ENSLAVED_PERSON",
    "AGE", "CLOTHING", "REWARD", "DATE", "LANGUAGE_SKILL"
]

precision = [0.733, 0.615, 1.000, 0.833, 0.200, 0.200, 1.000, 0.600, 0.500]
recall =    [0.846, 0.615, 0.667, 0.833, 0.200, 0.200, 0.833, 0.600, 0.500]
fscore =    [0.786, 0.615, 0.800, 0.833, 0.200, 0.200, 0.909, 0.600, 0.500]

x = np.arange(len(tags))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width, precision, width, label='Precision', color='skyblue')
rects2 = ax.bar(x, recall, width, label='Recall', color='lightgreen')
rects3 = ax.bar(x + width, fscore, width, label='F-score', color='salmon')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('NER Evaluation Metrics by Tag')
ax.set_xticks(x)
ax.set_xticklabels(tags, rotation=45, ha='right')
ax.set_ylim(0, 1.1)
ax.legend()

# Add value labels on bars
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(rects1)
add_labels(rects2)
add_labels(rects3)

plt.tight_layout()
plt.show()
