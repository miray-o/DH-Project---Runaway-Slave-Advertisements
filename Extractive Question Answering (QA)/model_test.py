from transformers import pipeline

pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Example of a typical 18th-century runaway slave advertisement
ad_text = """
Runaway from William Yard of Trenton in West-Jersey, the Fifth Day of this Instant November, 
a Negroe Man named Fransh Manuel, but commonly called Manuel, of a pretty tall stature, and speaks 
indifferent English. He wears a dark coloured homespun coat, an Ozenbrig Jacket, old Leather breeches, 
Sheep-russet Stockings, new Shoes and an old Beveret hat. He pretended formerly to be a Freeman and had 
Passes; but he did belong to one John Raymond of Fairfield in New England and I bought him of said Raymond. 
And the said Negro boy has told since he has run away, That he found a Quantity of Ore for his Master, and that 
his Master had given him Free. Whoever takes up the said Negroe, secures him and brings him to Mr. William 
Bradford of New York, or to Mr. William Burge of Philadelphia or to his said Master at Trenton, shall have 
forty shillings Reward, beside all reasonable charges, paid by me, William Yard.
"""

queries = {
    "Given Name": "What is the given name of the runaway?",
    "Language": "What are the communication skills of the runaway?",
    "Skills": "What is the set of skills of the runaway?",
    "Clothing": "What clothes did the runaway wear?",
    "Alias": "What other aliases does the runaway have?"
}

print("--- Extracted Information ---")
for attribute, question in queries.items():
    result = pipe(question=question, context=ad_text)
    answer = result.get("answer", "[No answer found]")
    print(result)


# Second Example of a typical 18th-century runaway slave advertisement
ad_text_2 = """
Ran away from Joseph Reade of New York City, merchant, the 14th of November, 1732, 
a likely mullatto servant woman, named Sarah. She is about 24 years of age, and she has 
taken with her a callico Suit of Cloathes, a striped Satteen silk wastecoat, Two Homespun 
waste-Coates and Petty-coat; she is a handy Wench, can do all sorts of House­ work, speaks 
good English and some Dutch. Whoever takes up the said Servant, and will bring her to her late 
Master, shall have five pounds as a Reward and all reasonable Charges paid.
"""

print("--- Extracted Information ---")
for attribute, question in queries.items():
    result = pipe(question=question, context=ad_text_2)
    answer = result.get("answer", "[No answer found]")
    print(result)


ad_text_3 = """Run Away from Solomon Baites of Elizabeth Town in NewJersey, 
a Negro Man named Clauss, about 28 years old, but he sometimes calls himself Nicolas, 
he formerly belonged to Daniel Bagley. He has taken with him a grey Home spun Drugget 
Coat trim’d with Black, a homespun Kearsey Vest, a Pair of Leather Breeches with red Puffs 
and Shoes and Stockings, he can play on a Fiddle tolerable well, He is of a middle Stature. 
Whoever takes up the said Negro and give Notice, so that his Master can have him again, shall 
have a reasonable reward besides reasonable Charge. And all persons are hereby forbid to 
entertain said Negro as they will answer at the utmost Severity of the Law."""

print("--- Extracted Information ---")
for attribute, question in queries.items():
    result = pipe(question=question, context=ad_text_3)
    answer = result.get("answer", "[No answer found]")
    print(result)