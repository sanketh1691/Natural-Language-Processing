import sys
import re
import time
import os
import json
import math
from collections import defaultdict, Counter


#stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll","you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at','by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've",'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',"didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',"shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

stopwords=["","would","hotel","rooms",'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',  'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',"room","stay", 'during', 'before', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'if', 'or', 'because', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'as', 'until', 'while', 'of']

def tokenize(string):
     
   string=string.rstrip("\n");
   string=re.sub("[(|\)|[|\]|:|;|\,|\.|!|\?]",'',string)
   string=string.strip().lower()
   str_list=string.split()
   str_list=[i for i in str_list if ((i not in stopwords) and i.isalpha())]
   return str_list


lst=[]
with open(sys.argv[1],"r") as out_file:
  temp=out_file.read()

lst=temp.split("\n")

pos_neg_weights=json.loads(lst[0])
tru_dec_weights=json.loads(lst[1])


f_out=open("percepoutput.txt","w")

for root, sub_dir, curr_dir_file in os.walk(sys.argv[2]):

  for f in curr_dir_file:
         path=os.path.join(root, f)
         #print(path)
          
         if '.txt' in path and 'README' not in path:
            
            file_text=open(path,"r", encoding="utf-8")
            temp=file_text.read()

            label1=""
            label2=""

            word_lst=tokenize(temp)
            word_lst=Counter(word_lst)
            p_sum1=tru_dec_weights['b']
            p_sum2=pos_neg_weights['b']

            for wd in word_lst:
              p_sum1+=(word_lst[wd]*tru_dec_weights.get(wd,0))
              p_sum2+=(word_lst[wd]*pos_neg_weights.get(wd,0))
                   
            if p_sum1<=0:
              label1=label1+"deceptive"
            else:
              label1=label1+"truthful"

            if p_sum2<=0:
              label2=label2+"negative"
            else:
              label2=label2+"positive"  
              
            temp_result=label1+" "+label2+" "+path
            f_out.write(temp_result)
            f_out.write("\n")
               

f_out.close()         

