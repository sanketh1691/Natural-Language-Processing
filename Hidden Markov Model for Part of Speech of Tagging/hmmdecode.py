import sys
import re
import time
import os
import json
import math
import numpy as np
from collections import defaultdict, Counter


file_model=open("../work/hmmmodel.txt","r")
model_data=file_model.read()
model_data=model_data.split("\n")

# Have to write the code for loading that data using json in to the dictionary variables
initial_state=json.loads(model_data[0])
transition=json.loads(model_data[1])
emission=json.loads(model_data[2])
vocabulary=json.loads(model_data[3])
tag_count=json.loads(model_data[4])


tag_keys=[i for i in range(len(tag_count))]
vocab_keys=[i for i in range(len(vocabulary))]


new_tags=dict(list(zip(list(tag_count.keys()),tag_keys)))
new_vocab=dict(list(zip(list(vocabulary.keys()),vocab_keys)))
size=len(tag_count)
voc_len=len(vocabulary)

trans_matrix = np.zeros((size,size))
emis_matrix = np.zeros((size,voc_len))
smoothing=np.ones((size,1))


for tag in transition:
  for i in transition[tag]:

    trans_matrix[new_tags[tag]][new_tags[i]]=transition[tag][i]
    
    
trans_matrix=trans_matrix+smoothing


for i in range(len(trans_matrix)):

  trans_matrix[i]=trans_matrix[i]/sum(trans_matrix[i])


top_tags = sorted(tag_count.items(),key=lambda x : x[1],reverse=True)[:7]
for i in range(len(top_tags)):
    top_tags[i]=top_tags[i][0]
    
    
for tag in emission:
  for word in emission[tag]:
 
   
       emis_matrix[new_tags[tag]][new_vocab[word]]=emission[tag][word]

      # emis_matrix[new_tags[tag]][new_vocab[word]]=emission[tag][word]

pi_prob=np.zeros(size)
for tag in initial_state:
  pi_prob[new_tags[tag]]=initial_state[tag]/float(sum(initial_state.values()))


def decoding_algo(trans_matrix,emis_matrix,pi_prob,line):
   line=line.split(" ")

   for token in line:
   
     if token not in new_vocab:
   
       temp_val=list(new_vocab.values())[-1]
       new_vocab[token]=temp_val+1
   
       temp_prob=math.pow(10,-10)
   
       new_col=np.full((len(emis_matrix),1),temp_prob)
       emis_matrix=np.append(emis_matrix,new_col,axis=1)
    
   target=[new_vocab[i] for i in line]  
   r=len(trans_matrix) 
   c=len(target)
  
   decoding=np.empty((r,c))
   backpointer=np.empty((r,c))
  
   # Initialisation
   try:
      decoding[:,0]= pi_prob * emis_matrix[:,target[0]]
   except IndexError as Error:
      decoding[:,0]=pi_prob

   backpointer[:,0]=0

   for i in range(1,c):
     try:

       decoding[:,i]=np.max(decoding[:,i-1] * trans_matrix.T * emis_matrix[np.newaxis, :, target[i]].T,1)
       backpointer[:,i]=np.argmax(decoding[:,i-1] * trans_matrix.T,1)

     except IndexError as Error:

       decoding[:,i]=np.max(decoding[:,i-1] * trans_matrix.T , 1)
       backpointer[:,i]=np.argmax(decoding[:,i-1] * trans_matrix.T,1)


   solution = np.empty(c,'B')
   solution[-1]=np.argmax(decoding[:,c-1])

   for j in range(c-1,0,-1):
     solution[j-1]=backpointer[solution[j],j]

   final_path=[]

   for x in solution:
       
     temp=list(new_tags.values()).index(x)
     final_path.append(list(new_tags.keys())[temp])

   final_solution=[]

   for x in range(len(line)):
     temp=line[x]+"/"+final_path[x]
     final_solution.append(temp)

   return final_solution;  


test_file=open(sys.argv[1],"r",encoding="utf-8")
data=test_file.read()
data=data.split("\n")

output=[]
for line in data[:-1]:

  ret_val=decoding_algo(trans_matrix,emis_matrix,pi_prob,line)
  output.append(ret_val)
    
out_file=open("hmmoutput.txt","w", encoding="utf-8");

for list_tags in output[:-1]:
    if list_tags !=[]:
        temp=" ".join(list_tags)
        out_file.write(temp)
        out_file.write("\n")

temp=" ".join(output[-1])
out_file.write(temp)

out_file.close()