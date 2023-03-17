import torch
from transformers import XLMRobertaTokenizer, XLMRobertaModel

# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# Sentences we want sentence embeddings for
sentences = ["The quick brown fox jumps over the lazy dog.","The speedy brown fox leaps over the indolent hound.","The slow brown fox crawls under the energetic dog."]

# Load tokenizer and model
tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-large')
model = XLMRobertaModel.from_pretrained('xlm-roberta-large')

# Tokenize sentences
inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

# Compute token embeddings
with torch.no_grad():
    model_output = model(**inputs)

# Perform pooling. In this case, mean pooling.
sentence_embeddings = mean_pooling(model_output, inputs['attention_mask'])

print("Sentence embeddings:")
print(sentence_embeddings)

# Cosine similarity
cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
cos_sim = cos(sentence_embeddings[0].unsqueeze(0), sentence_embeddings[1].unsqueeze(0))

print("Cosine similarity: ")
print(cos_sim)

# Cosine similarity
cos_sim = cos(sentence_embeddings[0].unsqueeze(0), sentence_embeddings[2].unsqueeze(0))

print("Cosine similarity: ")
print(cos_sim)

# Cosine similarity
cos_sim = cos(sentence_embeddings[1].unsqueeze(0), sentence_embeddings[2].unsqueeze(0))

print("Cosine similarity: ")
print(cos_sim)
