from sentence_transformers import SentenceTransformer, util
import csv
import numpy as np

que_list = []
with open('Question Bank.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for i, line in enumerate(reader):
        if(i==10):
            break
        que_list.append(line)
model = SentenceTransformer('stsb-roberta-large')
print("First Question: ", que_list[1])
sentence1 = que_list[1][2]
sentence2 = "OOPS is short form  for Object Oriented Programming system in which programs are considered as a collection of objects. Each object is nothing but an instance of a class."# encode sentences to get their embeddings
embedding1 = model.encode(sentence1, convert_to_tensor=True)
embedding2 = model.encode(sentence2, convert_to_tensor=True) # compute similarity scores of two embeddings
cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
print("Sentence 1:", sentence1)
print("Sentence 2:", sentence2)
print("Similarity score:", cosine_scores.item())

new_que = []
if(cosine_scores.item()>0.75):
    for que in que_list:
        if(que[3] == 'Medium'):
            new_que.append(que)
elif(cosine_scores.item()<0.75):
    
    for que in que_list:
        if(que[3] == 'Easy'):
            new_que.append(que)

print("New Question: ", new_que[0])