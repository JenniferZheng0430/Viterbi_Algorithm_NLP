#!/usr/bin/env python
# coding: utf-8

# In[58]:


import numpy as np
import pandas as pd


# In[59]:


file_path = "WSJ_final_training_set.pos"
test_corpora = "WSJ_23.words"


# In[60]:


emission = {}
transmission = {}

count = 0
with open(file_path,'r') as lines:
    tag_list = []
    for l in lines:
        count += 1
        word_pos = l.split('\t')
#         if count == 26:
#             print(type(word_pos[0].strip('\n')))
        if len(word_pos) == 1: # if it is an empty line, treat as a word with tag ''
            tag = str(word_pos[0].strip('\n'))
        else:
            word = word_pos[0]#.lower() #regardless of capital
            tag = word_pos[1].strip('\n')
        tag_list.append(tag)
        if tag not in emission:
            emission[tag] = {}
        if word not in emission[tag]:
            emission[tag][word] = 1
        else:
            emission[tag][word] += 1


# In[61]:


for i in range(len(tag_list)-1):
	if tag_list[i] not in transmission:
		transmission[tag_list[i]]={}
	if tag_list[i+1] not in transmission[tag_list[i]]:
		transmission[tag_list[i]][tag_list[i+1]] = 1
	else:
		transmission[tag_list[i]][tag_list[i+1]] += 1


# In[62]:


def transmission_probability(cur_tag,prev_tag): 
	denominator = sum(transmission[prev_tag].values())
	if cur_tag in transmission[prev_tag]:
		numerator = transmission[prev_tag][cur_tag]
	else:
		numerator = 0 
	return numerator/denominator

tag_list_unique = list(set(tag_list)) #delete replicates
tags_matrix = np.zeros((len(tag_list_unique), len(tag_list_unique)), dtype='float32')

print("the length of the unique tag list: ", len(tag_list_unique))


# In[63]:


def get_emission(word,tag):
    if tag == '':
        return 0
    denominator = sum(emission[tag].values())
    if word in emission[tag]:
        numerator = emission[tag][word]
    else: 
        #use hard coded probability
        if any(c.isdigit() for c in word) and tag == "CD": #contains digits
            return 1 / sum(emission["CD"].values())
        elif word.endswith('s') and tag == "NNS": #ends with s
            return  0.5 / sum(emission["NNS"].values())
        elif word[0].isupper() and tag == "NNP": #first letter capitalized
            return  0.5 / sum(emission["NNP"].values())
        elif not any(c.isalnum() for c in word) and tag == ".": #has neither digits nor letter
            return 0.5 / sum(emission["."].values())
        #elif word #punctuation?
        else:
            numerator = 0.00001
    return numerator/denominator


# In[64]:


for i,prev_tag in enumerate(tag_list_unique):
    for j,cur_tag in enumerate(tag_list_unique):
        tags_matrix[i, j] = transmission_probability(cur_tag,prev_tag) # row is the current tag, column is the previous tag


# In[65]:


tags_matrix


# In[66]:


tags_df = pd.DataFrame(tags_matrix, columns = tag_list_unique, index=tag_list_unique)


# In[67]:


# if '' in tag_list:
#     print(True)
# else:
#     print(False)
tags_df


# In[68]:


def Viterbi(words):
    state = [] #to record state that contribute to the maximum
    for index, word in enumerate(words):
        if word == '': 
            state.append('')
        else:
            prob = []

            for tag in tag_list_unique:

                transmission_prob = tags_df.loc['',tag] if (index == 0) else tags_df.loc[state[-1],tag]
                emission_prob = get_emission(word, tag)
                state_prob = emission_prob * transmission_prob
                prob.append(state_prob)
            state.append(tag_list_unique[prob.index(max(prob))]) #record the state with max prob

    return list(zip(words,state))


# In[69]:


with open(test_corpora) as f:
    lines = [line.rstrip() for line in f]
answer = Viterbi(lines)


# In[70]:


file = open('submission.pos','w')
for each in answer:
    if each[0] == '':
        file.write("\n")
    else:
        file.write(each[0]+"\t"+each[1]+"\n")

file.close()


# In[ ]:





# In[ ]:




