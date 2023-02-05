from sentence_transformers import SentenceTransformer, util
import torch


def sentence_encoding(sentence):
    model = SentenceTransformer('stsb-roberta-large')
    #model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')    
    embedding = model.encode(sentence, convert_to_tensor=True)
    return embedding

def sentence_match(sentence1, sentence2):
    #model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    model = SentenceTransformer('stsb-roberta-large')
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    distance = torch.dist(embedding1, embedding2, p=2)
    # embedding1 = util.normalize_embeddings(embedding1.unsqueeze(0))
    # embedding2 = util.normalize_embeddings(embedding2.unsqueeze(0))
    embedding1 = embedding1.unsqueeze(0)
    embedding2 = embedding2.unsqueeze(0)
    
    # compute L2 distance
    '''
    print(torch.nn.functional.smooth_l1_loss(embedding1, embedding2))
    print(torch.nn.functional.mse_loss(embedding1, embedding2))
    print(torch.nn.functional.cosine_embedding_loss(embedding1, embedding2, torch.tensor([1.0])))
    print(torch.nn.functional.pairwise_distance(embedding1, embedding2))
    print(torch.nn.functional.cosine_similarity(embedding1, embedding2))
    print(torch.nn.functional.l1_loss(embedding1, embedding2))'''

    l2_distance = torch.nn.functional.pairwise_distance(embedding1, embedding2)
    #return l2_distance.item()
    return cosine_scores.item()

def sentence_scoring_metric(cosine_value):
    #print(cosine_value)
    return cosine_value

if __name__ == '__main__':
    sentence1 = "Despite being a highly educated individual with an impressive resume and an outstanding track record of success in their field, they struggled to find meaningful employment due to their persistent lack of motivation and commitment."
    sentence2 = "Their relentless drive and unwavering determination, combined with a wealth of knowledge and experience, made them a valuable asset to any organization and allowed them to excel in their chosen profession, consistently delivering exceptional results and earning recognition for their achievements."
    sentence3 = "Despite possessing a wealth of qualifications and a strong record of accomplishments in their industry, they faced challenges in securing a fulfilling job due to a persistent lack of inspiration and dedication."
    #dist_value1 = sentence_match(sentence1, sentence2)
    #dist_value2 = sentence_match(sentence3, sentence2)
    #dist_value3 = sentence_match(sentence1, sentence3)
    
    cosine_value1 = sentence_match(sentence1, sentence2)
    cosine_value2 = sentence_match(sentence2, sentence3)
    cosine_value3 = sentence_match(sentence1, sentence3)
    print(cosine_value1, cosine_value2, cosine_value3)
    cosine_value = sentence_match(sentence1, sentence3)
    score = sentence_scoring_metric(cosine_value)
