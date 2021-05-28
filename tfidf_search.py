# ideas: similar docs, word positions (need to reindex everything), stopword ratio


import json
from my_tokenizer import tokenizer

from collections import defaultdict

from math import log

from time import time

def tfidf_search(query):
        results = []
        with open("total_files.txt") as total:
                totalDocs = int(total.readline().split()[-1])


        # open required files
        with open("byte_dict.json") as byte_file:
                byte_dict = json.load(byte_file)


        with open("./data/file_index.json") as fileName_file:
                file_dict = json.load(fileName_file)
        index_txt = open("final_index.txt")


        with open("folder_index.json") as url:
                url_dict = json.load(url)

        # see if we have the tokens in index
        try:    
                allStopwords = False
                start = time()
                with_stopwords = set(tokenizer(query, remove_stopwords=False))
                without_stopwords = set(tokenizer(query, remove_stopwords=True))

                if (len(without_stopwords))/len(with_stopwords)<=0.2:
                        conditions = with_stopwords
                        allStopwords = True
                else:
                        conditions = without_stopwords
                #conditions = with_stopwords if len(with_stopwords) <= 2 or (len(without_stopwords)) / len(with_stopwords) == 0 else without_stopwords

                # {docId: [checksum, tfidf_score]}
                retrieved_docs = defaultdict(list)
                for condition in conditions:
                        index_txt.seek(byte_dict[condition])

                        # token docId:bfjslkf docId:fkdsjfkasj
                        line = index_txt.readline().rstrip().split()

                        docs = line[1:]
                        doc_count = 0

                        for doc in docs:
                                parsed_doc = doc.split(":")

                                docId = parsed_doc[0]
                                title = 1.15 ** int(parsed_doc[-5])
                                anchor = 1.05 ** int(parsed_doc[-4])
                                important_count = 1.025 ** int(parsed_doc[-3])
                                checksum = int(parsed_doc[-2])
                                tfidf_score = float(parsed_doc[-1])
                        
                                if not retrieved_docs[docId]:
                                        retrieved_docs[docId].extend([checksum, tfidf_score])
                                else:
                                        retrieved_docs[docId][1] += tfidf_score * title * anchor * important_count

                                doc_count+=1
                                if allStopwords and doc_count >= 20000:
                                        break

        # return error message if tokens are not found in index
        except Exception as e:
                print(e)
                print("Query is not in Index")
        

        # if tokens are found in index then find the intersection
        else:
                # {docId: url}
                printed = 0
                curr_checksum = None
                for docId, [checksum, tfidf] in sorted(retrieved_docs.items(), key=lambda x: x[1][1], reverse=True): 
                        if (curr_checksum is None or curr_checksum != checksum) and (file_dict[docId] not in results):
                                results.append(file_dict[docId])
                                curr_checkum = checksum
                                printed += 1

                        if printed >= 5:
                                break

        # close resource
        index_txt.close()
        print(time()-start)

        return results



if __name__=="__main__":
        print(tfidf_search("master of software engineering"))
        print(tfidf_search("to be or not to be"))
        print(tfidf_search("machine learning"))
        print(tfidf_search("christina lopez"))