import sys
import re
import time
import os
import json
import math
import numpy as np
from collections import defaultdict, Counter

transition=defaultdict(lambda : defaultdict(lambda : 0))
emission=defaultdict(lambda : defaultdict(lambda : 0))
initial_state=defaultdict(lambda : 0)
vocabulary = defaultdict(lambda : 0)
tag_count=defaultdict(lambda : 0)


path=sys.argv[1]

file_text=open(path,"r", encoding="utf-8")
lst=file_text.readlines()

for line in lst:

    line=line.rstrip()
    line=line.split(" ")

    first = line[0]
    f_index= first.rfind("/")
    #transition["q0"][first[f_index+1:]]+=1;
    initial_state[first[f_index+1:]]+=1;
    vocabulary[first[0:f_index]]=1;
    tag_count[first[f_index+1:]]+=1

    for i in range(len(line)-1):
      
        emission[first[f_index+1:]][first[0:f_index]]+=1;
        second = line[i+1]
        s_index=second.rfind("/")
        transition[first[f_index+1:]][second[s_index+1:]]+=1;

        vocabulary[second[0:s_index]]=1;
        tag_count[second[s_index+1:]]+=1

        first=second
        f_index=s_index

    last=line[-1]
    l_index=last.rfind("/")
    emission[last[l_index+1:]][last[0:l_index]]+=1;
    
    
    
for tag in emission:

   tag_sum=sum(emission[tag].values())

   for i in emission[tag]:
     emission[tag][i]=emission[tag][i]/float(tag_sum)
    
    
    
f_out=open("hmmmodel.txt","w")
f_out.write(json.dumps(initial_state))
f_out.write("\n")
f_out.write(json.dumps(transition))
f_out.write("\n")
f_out.write(json.dumps(emission))
f_out.write("\n")
f_out.write(json.dumps(vocabulary))
f_out.write("\n")
f_out.write(json.dumps(tag_count))
f_out.close()    

