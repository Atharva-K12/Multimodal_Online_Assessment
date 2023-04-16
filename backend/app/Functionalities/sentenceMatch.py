from sentence_transformers import SentenceTransformer, util
from transfomers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# def sentence_encoding(sentence):
#     model = SentenceTransformer('facebook/bart-large-mnli')
#     embedding = model.encode(sentence, convert_to_tensor=True)
#     return embedding

# def sentence_match(sentence1, sentence2):
#     model = SentenceTransformer('facebook/bart-large-mnli')
#     embedding1 = model.encode(sentence1, convert_to_tensor=True)
#     embedding2 = model.encode(sentence2, convert_to_tensor=True)
#     cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)

#     return cosine_scores.item()
def sentence_encoding(sentence):
    pass
    

def sentence_match(sentence1, sentence2):
    nli_model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')
    tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')
    x = tokenizer.encode(sentence1, sentence2 return_tensors='pt')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    nli_model.to(device)
    logits = nli_model(x.to(device))[0]
    entail_contradiction_logits = logits[:,[0,2]]
    probs = entail_contradiction_logits.softmax(dim=1)
    prob_label_is_true = probs[:,1]
    return prob_label_is_true.item()

