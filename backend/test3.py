from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

text = "This is some is some text to encode with the XLM-RoBERTa tokenizer, and then decode back to text, and then encode again."
inputs = tokenizer.encode_plus(text, add_special_tokens=True, return_tensors='pt')

encoded_dict = tokenizer.encode_plus(
                    text   ,                   # Sentence to encode
                    add_special_tokens = True,      # Add '[CLS]' and '[SEP]'              # Pad & truncate all sentences
                    pad_to_max_length = True,
                    return_attention_mask = True,   # Construct attn. masks
                    return_tensors = 'pt',
         # Return 
         # pytorch tensors
               )


print("encoded_dict")
for u in encoded_dict:
    print(u)
for i in encoded_dict["input_ids"]:
    tokens = tokenizer.convert_ids_to_tokens(i)
    print(tokens)
# tokens = tokenizer.convert_ids_to_tokens(encoded_dict["input_ids"]/)
# tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
keywords = [token for token in tokens if token.isalnum()]

print(tokens)
print(keywords)