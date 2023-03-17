import pandas as pd
import torch
import transformers
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification, AdamW, get_linear_schedule_with_warmup

# Load the data
df = pd.read_csv('your_data_file.csv')  # Replace with your own data file
df = df[['question', 'sentence', 'label']]  # Replace 'question', 'sentence', and 'label' with your own column names

# Preprocess the data
tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-large')
max_length = 128  # Replace with your desired max sequence length
encoded_data_train = tokenizer.batch_encode_plus(
    df[['question', 'sentence']].values.tolist(),
    add_special_tokens=True,
    return_attention_mask=True,
    pad_to_max_length=True,
    max_length=max_length,
    return_tensors='pt'
)

# Create the dataset and dataloader
input_ids = encoded_data_train['input_ids']
attention_masks = encoded_data_train['attention_mask']
labels = torch.tensor(df['label'].values)
dataset = torch.utils.data.TensorDataset(input_ids, attention_masks, labels)
batch_size = 32  # Replace with your desired batch size
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size)

# Initialize the model and optimizer
model = XLMRobertaForSequenceClassification.from_pretrained('xlm-roberta-large', num_labels=2)  # Replace '2' with the number of labels in your data
optimizer = AdamW(model.parameters(), lr=2e-5, eps=1e-8)
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(dataloader) * 5)

# Train the model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.train()
for epoch in range(5):  # Replace '5' with the number of epochs you want to train for
    for batch in dataloader:
        batch_input_ids = batch[0].to(device)
        batch_attention_masks = batch[1].to(device)
        batch_labels = batch[2].to(device)
        model.zero_grad()
        outputs = model(batch_input_ids, token_type_ids=None, attention_mask=batch_attention_masks, labels=batch_labels)
        loss = outputs[0]
        loss.backward()
        optimizer.step()
        scheduler.step()

# Use the model to predict if a given sentence is an answer to a given question
def is_answer_to_question(question, sentence, model, tokenizer):
    inputs = tokenizer(question, sentence, add_special_tokens=True, return_tensors="pt", max_length=max_length, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).tolist()[0]
    return probabilities[1] >= 0.5

# Example usage
question = "What is the capital of France?"
sentence = "The capital of France is Paris."
result = is_answer_to_question(question, sentence, model, tokenizer)
print(result)  # Output: True
