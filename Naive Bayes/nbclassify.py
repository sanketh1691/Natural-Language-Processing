import sys
import re
import time
import os
import json
import math
from collections import defaultdict



lst=[]

with open("../work/nbmodel.txt","r") as model_file:
    
  temp=model_file.read()

lst=temp.split("\n")
      
s_dic=json.loads(lst[0])
label_count=json.loads(lst[1])
prior_prob=json.loads(lst[2])
cond_prob=json.loads(lst[3])

unique_count=len(s_dic)




stopwords=["","service","desk","stayed","rooms","they","have","there","you","the","and","a","i","was","in","of","for","it","at","my","is","that","were","with","this","had","on","be","s", "t", "don", "don't", "should", "should've", "now","up","us","one","stay","when", "d", "ll", "m", "o", "re", "ve","y","by","do","and","he","she","them"]




def tokenize(string):
     
   string=string.rstrip("\n");
   string=re.sub("[(|\)|[|\]|:|;|\,|\.|!|\?]",'',string)
   string=string.strip().lower()
   str_list=string.split()
   str_list=[i for i in str_list if ((i not in stopwords) and i.isalpha())]
   return str_list


result=[]

for root, sub_dir, curr_dir_file in os.walk(sys.argv[1]):

  for f in curr_dir_file:
    
         path=os.path.join(root, f)

        
         label_1=""
         label_2=""
         
         if '.txt' in path and "README" not in path:
            
            file_text=open(path,"r", encoding="utf-8")
            temp=file_text.read()
            
            words=tokenize(temp)

            p_val=math.log(label_count["positive"])
            n_val=math.log(label_count["negative"])
            t_val=math.log(label_count["truth"])
            d_val=math.log(label_count["deceptive"])   

            for word in words:
                
                  if word not in s_dic:
                    continue;


                  #if word in cond_prob['positive']:
                  p_val+=math.log((cond_prob['positive'].get(word,0)+1)/(prior_prob['positive']+unique_count))

                  #if word in cond_prob['negative']:
                  n_val+=math.log((cond_prob['negative'].get(word,0)+1)/(prior_prob['negative']+unique_count))                 

                  #if word in cond_prob['truth']:
                  t_val+=math.log((cond_prob['truth'].get(word,0)+1)/(prior_prob['truth']+unique_count))          

                  #if word in cond_prob['deceptive']:
                  d_val+=math.log((cond_prob['deceptive'].get(word,0)+1)/(prior_prob['deceptive']+unique_count))   


            if p_val>=n_val:

                  label_1=label_1+"positive"

            else:
                  label_1=label_1+"negative"      


            if t_val>=d_val:

                   label_2=label_2+"truthful" 
            else:

                   label_2=label_2+"deceptive" 

            temp_result=label_2+" "+label_1+" "+path
            result.append(temp_result);

#print(result)
            
f_out=open("nboutput.txt","w")    
      
for i in result:
    
    f_out.write(i);
    f_out.write("\n")
        
        
f_out.close()            