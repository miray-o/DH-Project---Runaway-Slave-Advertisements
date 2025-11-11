I have started a journey to explore numerous machine learning tools specifically to research African American history and document where these tools fall short in historical research. 

SpaCy - the most well-known NER library has a few already trained models to run NER on textual documents. 

The smallest model in English language have the 87% accuracy rate overall. 
SMALL MODEL - First Ad:
![[Pasted image 20250527125339.png]]
Sixth Ad: 
![[Pasted image 20250527125600.png]]

Since I wanted a more detailed entity separation, such as enslaved and enslaver instead of simply people, I have decided to train a simple SPaCY model myself.

First, I started with manually annotating a few of the ads on a web annotator. 
I have decided on 8 tags that would be necessary to be in the metadata. 
Annotator: https://github.com/tecoholic/ner-annotator 
![[Pasted image 20250621114835.png]]

To annotate, I picked 30 slave advertisements (every fifth one when listed chronically)
After manually tagging, I split 20% of the tagged advertisements to be the training data. 

My goals with this methodology are to combine distant and close reading methods. While distant reading provided me with the distribution of people, locations, and other characteristics, I wanted to dive deeper into the trends I observed. 
