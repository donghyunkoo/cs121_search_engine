from collections import defaultdict

from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
import string



def tokenizer(text, remove_stopwords=False):
    stemmer = PorterStemmer()
    try:
        tokens = TweetTokenizer().tokenize(text)
   
        stopwordLst = [line.strip() for line in open("stopwordlist.txt", encoding="utf-8")]

        ans = []

        for token in tokens:
            token = token.lower()

            if (token not in string.punctuation) and (len(token) > 1):
                if (remove_stopwords):
                    if token not in stopwordLst:
                 
                        is_valid = True
                        for char in token:
                            if char not in string.ascii_lowercase + string.punctuation:
                                is_valid = False
                                break

                        if is_valid:
                            stemmed_token = stemmer.stem(token)
                            ans.append(stemmed_token)
                            
                else:
                    is_valid = True
                    for char in token:
                        if char not in string.ascii_lowercase + string.punctuation:
                            is_valid = False
                            break

                    if is_valid:
                        stemmed_token = stemmer.stem(token)
                        ans.append(stemmed_token)
                        


        return ans

    except Exception as e:
        print(e)
        return []



def computeTokenFrequency(tokens):
    count_dict = defaultdict(int)

    for token in tokens:
        count_dict[token] += 1

    return count_dict

