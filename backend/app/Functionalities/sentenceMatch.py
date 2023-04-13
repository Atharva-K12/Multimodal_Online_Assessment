from sentence_transformers import SentenceTransformer, util

def sentence_encoding(sentence):
    model = SentenceTransformer('facebook/bart-large-mnli')
    embedding = model.encode(sentence, convert_to_tensor=True)
    return embedding

def sentence_match(sentence1, sentence2):
    model = SentenceTransformer('facebook/bart-large-mnli')
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)

    return cosine_scores.item()