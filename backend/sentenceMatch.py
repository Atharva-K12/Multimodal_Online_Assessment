# from sentence_transformers import SentenceTransformer, util
# import torch


# def sentence_encoding(sentence):
#     model = SentenceTransformer('facebook/bart-large-mnli')
#     #model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')    
#     embedding = model.encode(sentence, convert_to_tensor=True)
#     return embedding

# def sentence_match(sentence1, sentence2):
#     #model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
#     model = SentenceTransformer('facebook/bart-large-mnli')
#     embedding1 = model.encode(sentence1, convert_to_tensor=True)
#     embedding2 = model.encode(sentence2, convert_to_tensor=True)
#     cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
#     distance = torch.dist(embedding1, embedding2, p=2)
#     # embedding1 = util.normalize_embeddings(embedding1.unsqueeze(0))
#     # embedding2 = util.normalize_embeddings(embedding2.unsqueeze(0))
#     embedding1 = embedding1.unsqueeze(0)
#     embedding2 = embedding2.unsqueeze(0)
    
#     # compute L2 distance
#     '''
#     print(torch.nn.functional.smooth_l1_loss(embedding1, embedding2))
#     print(torch.nn.functional.mse_loss(embedding1, embedding2))
#     print(torch.nn.functional.cosine_embedding_loss(embedding1, embedding2, torch.tensor([1.0])))
#     print(torch.nn.functional.pairwise_distance(embedding1, embedding2))
#     print(torch.nn.functional.cosine_similarity(embedding1, embedding2))
#     print(torch.nn.functional.l1_loss(embedding1, embedding2))'''

#     l2_distance = torch.nn.functional.pairwise_distance(embedding1, embedding2)
#     #return l2_distance.item()
#     return cosine_scores.item()

# def sentence_scoring_metric(cosine_value):
#     #print(cosine_value)
#     return cosine_value

# if __name__ == '__main__':
#     sentence1 = "Despite being a highly educated individual with an impressive resume and an outstanding track record of success in their field, they struggled to find meaningful employment due to their persistent lack of motivation and commitment."
#     sentence2 = "Their relentless drive and unwavering determination, combined with a wealth of knowledge and experience, made them a valuable asset to any organization and allowed them to excel in their chosen profession, consistently delivering exceptional results and earning recognition for their achievements."
#     sentence3 = "Despite possessing a wealth of qualifications and a strong record of accomplishments in their industry, they faced challenges in securing a fulfilling job due to a persistent lack of inspiration and dedication."
#     #dist_value1 = sentence_match(sentence1, sentence2)
#     #dist_value2 = sentence_match(sentence3, sentence2)
#     #dist_value3 = sentence_match(sentence1, sentence3)
    
#     cosine_value1 = sentence_match(sentence1, sentence2)
#     cosine_value2 = sentence_match(sentence2, sentence3)
#     cosine_value3 = sentence_match(sentence1, sentence3)
#     print(cosine_value1, cosine_value2, cosine_value3)
#     cosine_value = sentence_match(sentence1, sentence3)
#     score = sentence_scoring_metric(cosine_value)





# from transformers import BartTokenizer, BartForSequenceClassification
# import torch

# def sentence_similarity(sentence1, sentence2):
#     model_name = 'facebook/bart-large-mnli'
#     tokenizer = BartTokenizer.from_pretrained(model_name)
#     model = BartForSequenceClassification.from_pretrained(model_name)

#     # Tokenize inputs
#     input_ids = tokenizer.encode(sentence1, sentence2, return_tensors='pt', padding=True)

#     # Compute similarity score
#     outputs = model(input_ids)[0]
#     probs = torch.nn.functional.softmax(outputs, dim=1)
#     for prob in probs[0]:
#         # .2f
#         print("{:.2f}".format(prob.item()))
#     print() 
#     similarity_score = probs[0][0].item()  # probability of being in the same class
    
#     return similarity_score

# if __name__ == '__main__':
#     sentence1 = "Despite being a highly educated individual with an impressive resume and an outstanding track record of success in their field, they struggled to find meaningful employment due to their persistent lack of motivation and commitment."
#     sentence2 = "Their relentless drive and unwavering determination, combined with a wealth of knowledge and experience, made them a valuable asset to any organization and allowed them to excel in their chosen profession, consistently delivering exceptional results and earning recognition for their achievements."
#     sentence3 = "Despite possessing a wealth of qualifications and a strong record of accomplishments in their industry, they faced challenges in securing a fulfilling job due to a persistent lack of inspiration and dedication."
    
#     similarity_score1 = sentence_similarity(sentence1, sentence2)
#     similarity_score2 = sentence_similarity(sentence2, sentence3)
#     similarity_score3 = sentence_similarity(sentence1, sentence3)
#     print(similarity_score1, similarity_score2, similarity_score3)



import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
nli_model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')
tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')

# premise = "Despite being a highly educated individual with an impressive resume and an outstanding track record of success in their field, they struggled to find meaningful employment due to their persistent lack of motivation and commitment."
# hypothesis = "Despite possessing a wealth of qualifications and a strong record of accomplishments in their industry, they faced challenges in securing a fulfilling job due to a persistent lack of inspiration and dedication."
# hypothesis2 = "Their relentless drive and unwavering determination, combined with a wealth of knowledge and experience, made them a valuable asset to any organization and allowed them to excel in their chosen profession, consistently delivering exceptional results and earning recognition for their achievements."

# premise = "A class is a blueprint or a template for creating objects that encapsulate data and the functions that operate on that data. It defines the properties and behavior of objects, including their state and methods. The class is a user-defined data type that provides a way to group related data and functions together, making it easier to organize and maintain complex code"
# hypothesis = "A class is a user-defined data type in C++ that defines a set of attributes and methods for a particular type of object. Attributes represent the data that the object contains, while methods represent the actions that the object can perform. A class serves as a blueprint for creating instances of that object, also known as objects or instances of the class. Classes can be used to implement object-oriented programming concepts, such as inheritance, polymorphism, and encapsulation."
# hypothesis2 = "A class is not a user-defined data type that allows the programmer to define their own data structures, including not only the data type of each member but also the methods that operate on that data. The class serves as a template for creating objects, which are instances of the class. Each object of a class has its own copy of the class's data members and can call the methods of the class to manipulate its data."

# premise ="The teacher was pleased with the performance of her students, as they had all excelled in the exam."
# hypothesis = "The instructor was satisfied with the achievement of his pupils, as they had all surpassed expectations in the test."
# hypothesis2 = "The professor was impressed with the aptitude of her students, as they had all demonstrated exceptional skill in their research projects."



premise = "The algorithm employs a heuristic approach to solve the problem by making informed guesses based on prior knowledge."
hypothesis = "The algorithm uses a rule-of-thumb method to resolve the issue by making educated estimations based on previous experience"
hypothesis2 = "The program utilizes a self-referential method to calculate the factorial of a specified value by iteratively invoking itself until the termination condition is met"
# run through model pre-trained on MNLI
x = tokenizer.encode(premise, hypothesis, return_tensors='pt')

x2 = tokenizer.encode(premise, hypothesis2, return_tensors='pt')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

out = nli_model(x.to(device))
logits = out[0]
encodings = out[2]
logits2 = nli_model(x2.to(device))[0]

# print(logits)


# cosine_scores = torch.nn.functional.cosine_similarity(encodings[0], encodings[1], dim=1)
# print("{:.2f}".format(cosine_scores.item()))




# we throw away "neutral" (dim 1) and take the probability of
# "entailment" (2) as the probability of the label being true 
entail_contradiction_logits = logits[:,[0,2]]
probs = entail_contradiction_logits.softmax(dim=1)
print(probs)
prob_label_is_true = probs[:,1]

# probs = logits.softmax(dim=1)
print("Probs of 1,2")
# print(probs)
# prob_label_is_true = probs[:,2]

print("{:.2f}".format(prob_label_is_true.item()))
# print(entail_contradiction_logits)


entail_contradiction_logits2 = logits2[:,[0,2]]
probs2 = entail_contradiction_logits2.softmax(dim=1)
prob_label_is_true2 = probs2[:,1]

# probs2 = logits2.softmax(dim=1)
print("Probs of 1,3")
# print(probs2)
# prob_label_is_true2 = probs2[:,2]

print("{:.2f}".format(prob_label_is_true2.item()))
# print(entail_contradiction_logits2)

x3 = tokenizer.encode(hypothesis, hypothesis2, return_tensors='pt')

logits3 = nli_model(x3.to(device))[0]

entail_contradiction_logits3 = logits3[:,[0,2]]
probs3 = entail_contradiction_logits3.softmax(dim=1)
prob_label_is_true3 = probs3[:,1]

# probs3 = logits3.softmax(dim=1)
print("Probs of 2,3")
# print(probs3)
# prob_label_is_true3 = probs3[:,2]

# .2f
print("{:.2f}".format(prob_label_is_true3.item()))
# print(entail_contradiction_logits3)

