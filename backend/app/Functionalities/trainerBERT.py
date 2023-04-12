# Import required libraries
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModel, AdamW
from sentence_transformers import SentenceTransformer, SentencesDataset, LoggingHandler, losses, util

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name).to(device)

# Load sentence transformer model
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens').to(device)

# Load dataset in text format
with open('sentence.txt', 'r') as f:
    sentences = f.readlines()

# Preprocess sentences using tokenizer
tokenized_sentences = [tokenizer.encode(sentence, add_special_tokens=True) for sentence in sentences]

# Create dataset and data loader
dataset = SentencesDataset(tokenized_sentences, sbert_model)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# Define optimizer and loss function
optimizer = AdamW(bert_model.parameters(), lr=2e-5)
loss_func = losses.CosineSimilarityLoss(bert_model)

# Train model
bert_model.train()
for epoch in range(3):
    for step, batch in enumerate(dataloader):
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        embeddings = bert_model(input_ids, attention_mask=attention_mask)[1]
        loss = loss_func(embeddings, embeddings)
        loss.backward()
        optimizer.step()
        if step % 100 == 0:
            print(f'Epoch: {epoch}, Step: {step}, Loss: {loss.item()}')
