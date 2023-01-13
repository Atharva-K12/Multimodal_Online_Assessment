from sentence_transformers import SentenceTransformer, util



def sentence_encoding(sentence):
    #model = SentenceTransformer('stsb-roberta-large')
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')    
    embedding = model.encode(sentence, convert_to_tensor=True)
    return embedding

def sentence_match(sentence1, sentence2):
    model = SentenceTransformer('flax-sentence-embeddings/all_datasets_v3_roberta-large')
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)
    print(embedding1)
    print(embedding2)
    print(embedding1.shape)
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    return cosine_scores.item()

def sentence_scoring_metric(cosine_value):
    print(cosine_value)
    return cosine_value

if __name__ == '__main__':
    sentence1 = "You better take this deal"
    sentence2 = "Please don't take the deal"
    cosine_value = sentence_match(sentence1, sentence2)
    score = sentence_scoring_metric(cosine_value)
