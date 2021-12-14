#First, convert the cran.qry to list[Q1, Q2, Q3, Q4,...Q255]
#Second, convert the abstract to list[abs1, abs2, abs3,..., abs1400]

#Calculate the TF-IDF for each query
    #Go through the 1400 abstracts and find the TF-IDF for each abstract
    #Calculate the cosine similarity
    #save to the output list


import stop_list
from nltk.stem import PorterStemmer
import numpy as np

from nltk.tokenize import word_tokenize
from numpy import dot
from numpy.linalg import norm

import math

ps = PorterStemmer()


query_file_name = "cran.qry"
abstract_file_name = "cran.all.1400"

query_file = open(query_file_name, "r")
abstract_file = open(abstract_file_name, "r")

query_input = query_file.readlines()
abstract_input = abstract_file.readlines()

query_file.close()
abstract_file.close()

#Creating list for query_input
queries_list = []
queries_dict = {}
current_query_num = 0
text_query = ""
word_list_of_query = []
#index of list is number of query
for line in query_input:
    text = line.split(" ")

    if text[0] == ".I":
        queries_list.append(text_query)
        queries_dict[current_query_num] = text_query
        text_query = ""
        current_query_num += 1

    elif (text[0] == ".W\n"):
        continue
    else:
        for temp_word in text:
            word = ""
            if "\n" in temp_word:
                temp_word.strip("\n")
            for char in temp_word:
                if char.isalpha():
                    word += char
                else:
                    continue
            if word in stop_list.closed_class_stop_words:
                continue
            text_query += word + " "
            word_list_of_query.append(word)
queries_list.append(text_query)
queries_list = queries_list[1:]
queries_dict[current_query_num] = text_query
del queries_dict[0]

# print(len(queries_dict), len(queries_list))
#print(len(queries_list))
# for i in range(len(queries_list)):
#     print(i, queries_list[i])

#Creating dict for query_input
abstract_list = []
abstract_dict = {}
current_abs_num = 0
text_abstract = ""
for line in abstract_input:
    text = line.split(" ")

    if(text[0] == ".I"):
        abstract_list.append(text_abstract)
        abstract_dict[current_abs_num] = text_abstract
        text_abstract = ""
        current_abs_num += 1
    else:
        for temp_word in text:
            word = ""
            if "\n" in temp_word:
                temp_word.strip("\n")
            for char in temp_word:
                if char.isalpha():
                    word += char
                else:
                    continue
            if word in stop_list.closed_class_stop_words:
                continue
            if ps.stem(word) not in word_list_of_query:
                continue
            if word not in word_list_of_query:
                continue
            if word == "":
                continue
            text_abstract += word + " "
abstract_dict[current_abs_num] = text_abstract
abstract_list.append(text_abstract)

# print(0, abstract_dict[0])
del abstract_dict[0]
# print(len(abstract_dict))
#
# for i in abstract_dict.keys():
#     print(i, abstract_dict[i])



#IDF for query
temp_idf_query = {}
#NumberOfDocumentsContaining (t)
for each_query in queries_list:
    query_tokens = word_tokenize(each_query)
    num_of_sameword_in_same_query = 0
    for word in query_tokens:
        if word not in temp_idf_query:
            temp_idf_query[word] = 1
            num_of_sameword_in_same_query += 1
        elif word in temp_idf_query and num_of_sameword_in_same_query == 0:
            temp_idf_query[word] += 1



idf_query = {}
for word in temp_idf_query:
    idf_query[word] = np.log(225/temp_idf_query[word])

# for word in idf_query:
#     if(idf_query[word] < 0):
#         print(word, idf_query[word])
#         break
    # print(word, idf_query[word])

#TF for query
tf_query = {}
for current_num in queries_dict:
    tf_query[current_num] = {}
    query_tokens = word_tokenize(queries_dict[current_num])
    for word in query_tokens:
        if word not in tf_query[current_num]:
            tf_query[current_num][word] = 1
        else:
            tf_query[current_num][word] += 1

#tf-idf for query
tf_idf_query = {}
for current_num in tf_query:
    tf_idf_query[current_num] = {}
    for word in tf_query[current_num]:
        tf_idf_query[current_num][word] = tf_query[current_num][word] * idf_query[word]

# for num in tf_idf_query:
#     print(num, tf_idf_query[num])

#IDF for abstract
temp_idf_abstract = {}
#NumberOfDocumentsContaining (t)
# for current_num in abstract_dict.keys():
#     abstract_tokens = word_tokenize(abstract_dict[current_num])
#     num_of_sameword_in_same_abstract = 0
#     for word in abstract_tokens:
#         if word in temp_idf_abstract and num_of_sameword_in_same_abstract == 0:
#             temp_idf_abstract[word] += 1
#         elif word not in temp_idf_abstract:
#             temp_idf_abstract[word] = 1
#             num_of_sameword_in_same_abstract += 1
for current_num in abstract_dict.keys():
    abstract_tokens = word_tokenize(abstract_dict[current_num])
    num_of_sameword_in_same_abstract = 0
    for word in abstract_tokens:
        if word not in temp_idf_abstract:
            temp_idf_abstract[word]= 1
            num_of_sameword_in_same_abstract += 1
        elif word in temp_idf_abstract and num_of_sameword_in_same_abstract == 0:
            num_of_sameword_in_same_abstract += 1

idf_abstract = {}
for word in temp_idf_abstract:
    idf_abstract[word] = np.log(1400/temp_idf_abstract[word])


# for word in temp_idf_abstract:
#     if temp_idf_abstract[word] < 0:
#         print(word, temp_idf_abstract[word])
#         break

# for word in idf_abstract:
#     if idf_abstract[word] < 0:
#         print(word, idf_abstract[word])
#         break

#TF for abstract
tf_abstract = {}
for current_num in abstract_dict:
    tf_abstract[current_num] = {}
    abstract_tokens = word_tokenize(abstract_dict[current_num])
    for word in abstract_tokens:
        if word not in tf_abstract[current_num]:
            tf_abstract[current_num][word] = 1
        else:
            tf_abstract[current_num][word] += 1


# for n in tf_abstract:
#     for word in tf_abstract[n]:
#         if tf_abstract[n][word] < 0:
#             print(n, tf_abstract[n][word])
#             break
#     print(n, tf_abstract[n])

#tf-idf for abstract
tf_idf_abstract = {}
for current_num in tf_abstract:
    tf_idf_abstract[current_num] = {}
    for word in tf_abstract[current_num]:
        tf_idf_abstract[current_num][word] = tf_abstract[current_num][word] * idf_abstract[word]

# for n in tf_idf_abstract:
#     print(n, tf_idf_abstract[n])



vectors_for_abstract = {} #vectors_for_abstract[Q_num][A_num][word both in Q and A] = [] => vectors(list) for abstract
#Finding vectors for abstract: Later use for cosine similarity
for current_Q_num in tf_idf_query:
    current_query_words = tf_idf_query[current_Q_num].keys()
    # current_query_vector = []
    # for word in current_query_words:
    #     current_query_vector = tf_idf_query[current_Q_num][word]
    vectors_for_abstract[current_Q_num] = {}
    for current_A_num in tf_idf_abstract:
        vectors_for_abstract[current_Q_num][current_A_num] = {}
        for word in current_query_words:
            vectors_for_abstract[current_Q_num][current_A_num][word] = {}
            if word in tf_idf_abstract[current_A_num]:
                # if tf_idf_abstract[current_A_num][word] <0 :
                #     print('here', current_A_num, word)
                #     break
                vectors_for_abstract[current_Q_num][current_A_num][word] = tf_idf_abstract[current_A_num][word]
            else:
                vectors_for_abstract[current_Q_num][current_A_num][word] = 0

# for i in vectors_for_abstract:
#     print(i, vectors_for_abstract[i])


#Find cosine similarity
cosine_similarity_dict = {} #cosine_similarity_dict[Q_num][A_num] = cosine similarity

# for current_Q_num in tf_idf_query:
#     current_query_words = tf_idf_query[current_Q_num].keys()
for q_num in vectors_for_abstract.keys():
    cosine_similarity_dict[q_num] = {}
    q_vector = list(tf_idf_query[q_num].values())
    for a_num in vectors_for_abstract[q_num].keys():
        a_vector = list(vectors_for_abstract[q_num][a_num].values())
        cos_sim = dot(q_vector, a_vector) / (norm(q_vector) * norm(a_vector))
        if math.isnan(cos_sim):
            cos_sim = 0
        cosine_similarity_dict[q_num][a_num] = cos_sim



#Sorting based on the cos_sim
sorted_output = {}
for q_num in cosine_similarity_dict:
    sorted_output[q_num] = sorted(cosine_similarity_dict[q_num].items(), key=lambda item: item[1], reverse=True)

f_output=open("output.txt","w")
for q_num in sorted_output:
    for abs_data in sorted_output[q_num]:
        if(abs_data[1]==0):
            continue
        f_output.write(str(q_num)+" " + str(abs_data[0])+" " + str(abs_data[1])+ "\n")
        # f_output.write(str(abs_data[0])+" ")
        # f_output.write(str(abs_data[1])+ "\n")

f_output.close()
#
# dict1 = {1: 1, 2: 9, 3: 4}
# sorted_tuples = sorted(dict1.items(), key=lambda item: item[1])
# print(sorted_tuples)  # [(1, 1), (3, 4), (2, 9)]
# sorted_dict = {k: v for k, v in sorted_tuples}
#
# print(sorted_dict)  # {1: 1, 3: 4, 2: 9}