# ID_zero_shot_sentiment_analysis

As explained by the name, this repository is used to store materials needed to attempt zero-shot sentiment analysis in Indonesian.

This project is far from finished and the current result is far from satisfactory. The main idea is simple: create text embeddings from tweets and cluster them into N clusters that hopefully represent each tweet's sentiment.
The model used to create the embeddings is Word2Vec, which I'm aware is not a state-of-the-art NLP model as of the time I'm writing this. Word2Vec is flawed since it 
doesn't take into account the context in which each word is used in a text and context is paramount in determining the sentiment of a text. I'm currently still learning about other, more
sophisticated methods to create embeddings and I'll update the project when I have the means to create better embeddings and when I have the time.
