from transformers import pipeline

pipe = pipeline("question-answering", model="Nadav/bert-base-cased-finetuned-runaways")

# Example of a typical 18th-century runaway slave advertisement
context= ("""THAT on Thursday 26th inst. deserted from Neil MacNeil of Bristol, 
          merchant, a MULATTO BOY, named PETER, aged 18 years or thereabout, about five feet, 
          of a good complexion, well built, and speaks good English. He had on when he run away, a 
          grey livery, faced with red, wash’d metal buttons to his coat and waistcoat, a brown cut wig, 
          a hat with a gold loop and button to it. Whoever apprehends the said boy, and brings him to Mr. 
          Matthew McAllister merchant in Edinburgh, shall have five guineas reward. - He is supposed to be 
          lurking about Leith or Edinburgh; it is desired that no shipmaster or private family will harbour or
          give him countenance.""")


question = "What is the name of the runaway?"

result = pipe(
    question=question,
    context=context
)

print(result)

