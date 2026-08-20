from transformers import pipeline
import pandas as pd

pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")

df = pd.read_csv("/Users/mirayozmutlu/Documents/GitHub/DH-Project---Runaway-Slave-Advertisements/Runaway Slave Ads - primary sources.csv")

queries = {
    "Given Name": "What is the given name of the runaway?",
    "Language": "What are the communication skills of the runaway?",
    "Skills": "What is the set of skills of the runaway?",
    "Clothing": "What clothes did the runaway wear?",
    "Alias": "What other aliases does the runaway have?"
}

# Add new columns dynamically with default value "NA"
for attribute in queries.keys():
    df[attribute] = "NA"

# Iterate through the rows and perform QA
for i in range(len(df)):
    ad_text = df.iloc[i]['Content']

    for attribute, question in queries.items():
        result = pipe(question=question, context=ad_text)
        answer = result.get("answer", "[No answer found]")
        df.at[i, attribute] = answer  # Use .at for setting values

# Save the updated DataFrame to a CSV file
df.to_csv("/Users/mirayozmutlu/Documents/GitHub/DH-Project---Runaway-Slave-Advertisements/Extractive Question Answering (QA)/(uncleaned) attributes.csv", index=False)