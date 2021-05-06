import sys
import re
import time
import os
import json
import math
from collections import defaultdict, Counter


posneg={"positive":[], "negative":[]}
trudec={"truthful":[],"deceptive":[]}

#stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll","you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at','by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've",'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',"didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',"shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

stopwords=["","would","hotel","rooms",'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',  'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',"room","stay", 'during', 'before', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'if', 'or', 'because', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'as', 'until', 'while', 'of']


def tokenize(string):
     
   string=string.rstrip("\n");
   string=re.sub("[(|\)|[|\]|:|;|\,|\.|!|\?]",'',string)
   string=string.strip().lower()
   str_list=string.split()
   str_list=[i for i in str_list if ((i not in stopwords) and i.isalpha())]
   return str_list




for root, sub_dir, curr_dir_file in os.walk(sys.argv[1]):

  for f in curr_dir_file:
         path=os.path.join(root, f)
         #print(path)
          
         if '.txt' in path and 'README' not in path:
            
            file_text=open(path,"r", encoding="utf-8")
            temp=file_text.read()

            #total_label_count+=1;
            if 'positive' in path:

                posneg["positive"].append(temp)

                if 'truthful' in path:
                      
                    trudec['truthful'].append(temp); 
              
                elif 'deceptive' in path:

                    trudec['deceptive'].append(temp);
            
            elif  'negative' in path:
              
                posneg["negative"].append(temp)

                if 'truthful' in path:
 
                    trudec['truthful'].append(temp);

                elif 'deceptive' in path:
  
                    trudec['deceptive'].append(temp);

  

classes={"truthful":1,"positive":1,"deceptive":-1,"negative":-1}
    
num_iter=100
learning_rate=0.0005

pos_neg_w=defaultdict(lambda : 0)
pos_neg_w['b']=0
tru_dec_w=defaultdict(lambda : 0)
tru_dec_w['b']=0

avg_pos_neg_w=defaultdict(lambda : 0)
avg_pos_neg_w['b']=0
avg_tru_dec_w=defaultdict(lambda : 0)
avg_tru_dec_w['b']=0


# Updating both normal and average weights for Positive_Negative
C=1
for iter in range(1,num_iter+1):

    for nature in posneg:
       
       label=classes[nature]
       for st in posneg[nature]:

            words=tokenize(st);
            words=Counter(words)
            percep_sum=pos_neg_w['b'];

            for word in words:
                percep_sum=percep_sum+(words[word]*pos_neg_w[word])

            if label*percep_sum<=0:

                pos_neg_w['b']+=(label*learning_rate) 
                for word in words:
                     pos_neg_w[word]+=(learning_rate*words[word]*label)

                avg_pos_neg_w['b']+=(label*learning_rate*(C))     
                for word in words:
                     avg_pos_neg_w[word]+=(learning_rate*words[word]*label*(C))
            C+=1

for wrd in avg_pos_neg_w:
     
     avg_pos_neg_w[wrd]=pos_neg_w[wrd]-((1/C)*avg_pos_neg_w[wrd]);
    
    
# Updating both normal and average weights for Truthful_Deceptive
C=1
for iter in range(1,num_iter+1):

    for nature in trudec:
       
       label=classes[nature]
       for st in trudec[nature]:

            words=tokenize(st);
            words=Counter(words)
            percep_sum=tru_dec_w['b'];

            for word in words:
                percep_sum=percep_sum+(words[word]*tru_dec_w[word])

            if label*percep_sum<=0:

                tru_dec_w['b']+=(label*learning_rate) 
                for word in words:
                     tru_dec_w[word]+=(learning_rate*words[word]*label)

                avg_tru_dec_w['b']+=(label*learning_rate*(C))     
                for word in words:
                     avg_tru_dec_w[word]+=(learning_rate*words[word]*label*(C))
            C+=1

for wrd in avg_tru_dec_w:
     
     avg_tru_dec_w[wrd]=tru_dec_w[wrd]-((1/C)*avg_tru_dec_w[wrd]);
    
    

f1=open("vanillamodel.txt","w")
f1.write(json.dumps(pos_neg_w))
f1.write("\n")
f1.write(json.dumps(tru_dec_w))
f1.close()


f2=open("averagedmodel.txt","w")
f2.write(json.dumps(avg_pos_neg_w))
f2.write("\n")
f2.write(json.dumps(avg_tru_dec_w))
f2.close()



