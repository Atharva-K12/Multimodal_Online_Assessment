# Import necessary libraries
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification

# Load the XLMRoberta tokenizer and model
tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base')
model = XLMRobertaForSequenceClassification.from_pretrained('xlm-roberta-base', num_labels=2)

# Define the input sentences
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "The speedy brown fox leaps over the indolent hound."

# Tokenize the input sentences
encoded_dict = tokenizer.encode_plus(
                    sentence1,                      # Sentence to encode
                    sentence2,                      # Sentence to encode
                    add_special_tokens = True,      # Add '[CLS]' and '[SEP]'              # Pad & truncate all sentences
                    pad_to_max_length = True,
                    return_attention_mask = True,   # Construct attn. masks
                    return_tensors = 'pt',
         # Return 
         # pytorch tensors
               )




# Get the model's prediction
outputs = model(**encoded_dict)

# Get the probability of the first label (entailment)

print("121212133232323\n\n\n\n\n")
print(outputs.logits)
print(outputs)

outputs = outputs.logits.squeeze(0).softmax(0)
print(outputs)
probs = outputs
entail_prob = probs

# Print the results
print(entail_prob)

# print("The probability that the second sentence entails the first sentence is: {:.2f}%".format(entail_prob*100))
