import sys
import re
import time
import os
import json
import math
from collections import defaultdict

positive={"truth":[], "deceptive":[]}
negative={"truth":[],"deceptive":[]}
label_count=defaultdict(lambda : 0)
total_label_count=0;




stopwords=["","service","desk","stayed","rooms","they","have","there","you","the","and","a","i","was","in","of","for","it","at","my","is","that","were","with","this","had","on","be","s", "t", "don", "don't", "should", "should've", "now","up","us","one","stay","when", "d", "ll", "m", "o", "re", "ve","y","by","do","and","he","she","them"]


input_file_path=sys.argv[1]

def tokenize(string):
     
   string=string.rstrip("\n");
   string=re.sub("[(|\)|[|\]|:|;|\,|\.|!|\?]",'',string)
   string=string.strip().lower()
   str_list=string.split()
   str_list=[i for i in str_list if ((i not in stopwords) and i.isalpha())]
   return str_list



for root, sub_dir, curr_dir_file in os.walk(input_file_path):

  for f in curr_dir_file:
         path=os.path.join(root, f)
         #print(path)
          
         if '.txt' in path and 'README' not in path:
            
            file_text=open(path,"r", encoding="utf-8")
            temp=file_text.read()
            total_label_count+=1;
            
            if 'positive' in path:
                
                label_count["positive"]=label_count["positive"]+1

                if 'truthful' in path:
                    
                    label_count["truth"]=label_count["truth"]+1   
                    positive['truth'].append(temp); 
              
                elif 'deceptive' in path:

                    label_count["deceptive"]=label_count["deceptive"]+1   
                    positive['deceptive'].append(temp);
            
            elif  'negative' in path:

                label_count["negative"]=label_count["negative"]+1

                if 'truthful' in path:

                    label_count["truth"]=label_count["truth"]+1   
                    negative['truth'].append(temp);

                elif 'deceptive' in path:

                    label_count["deceptive"]=label_count["deceptive"]+1   
                    negative['deceptive'].append(temp);

          
                    
                    
prior_prob=defaultdict(lambda : 0)
cond_prob={'positive':defaultdict(lambda : 0),'negative':defaultdict(lambda : 0),'truth':defaultdict(lambda : 0),'deceptive':defaultdict(lambda : 0)}
s=defaultdict(lambda : 0)
total_word_count=0;


for nature in positive:
   for st in positive[nature]:
     
     words=tokenize(st);
     for word in words:
        s[word]=0
        total_word_count+=1;
        cond_prob['positive'][word]+=1;
        cond_prob[nature][word]+=1;
        prior_prob['positive']+=1;
        prior_prob[nature]+=1;


for nature in negative:
   for st in negative[nature]:

     words=tokenize(st);
     for word in words:
        s[word]=0
        total_word_count+=1;
        cond_prob['negative'][word]+=1;
        cond_prob[nature][word]+=1;
        prior_prob['negative']+=1;
        prior_prob[nature]+=1;

        
for i in label_count:
  label_count[i]=label_count[i]/total_label_count        
        
total_words={"count":total_word_count}

f=open("nbmodel.txt","w");

f.write(json.dumps(s))
f.write("\n")
f.write(json.dumps(label_count))
f.write("\n")
f.write(json.dumps(prior_prob))
f.write("\n")
f.write(json.dumps(cond_prob))
#print (total_word_count)

#print(len(prior_prob))
#print(len(cond_prob))

f.close()

