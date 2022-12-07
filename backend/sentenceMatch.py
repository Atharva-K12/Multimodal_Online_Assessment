from sentence_transformers import SentenceTransformer, util


def sentence_match(sentence1, sentence2):
    model = SentenceTransformer('stsb-roberta-large')
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    return cosine_scores.item()

def sentence_scoring_metric(cosine_value):
    print(cosine_value)
    return cosine_value