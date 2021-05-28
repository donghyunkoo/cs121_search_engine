import os

import re
from bs4 import BeautifulSoup
from urllib.parse import urldefrag

from collections import namedtuple
from collections import defaultdict
import json

import time

from my_tokenizer import tokenizer, computeTokenFrequency


# {token: {document_id: namedtuple(count, title, important_count)}} 
if __name__ == '__main__':
    path = "./DEV"

    # code = code._replace(top = 1)
    # count bold_count heading_count title_count href_count
    DocInfo = namedtuple("DocInfo", "count title anchor important_count checksum")

    # {token: {file_id: {count: 0, title: 0, important_count: 0, checksum: 0}}}    
    index = defaultdict(dict)

    # {file_id: file_name}
    file_indexer = {}

    file_count = 0
    json_count = 0
    file_id = 0

    for root, directory, files in os.walk(path):
        for file_name in files:
           with open(root + "/" + file_name) as f:
               file_id += 1
               file_count += 1

               # print(file_id)
        
               if file_count > 10000:
                   with open(f"./data/data_{json_count}.json", "w") as data:
                       json_count += 1
                       json_object = json.dumps(index, sort_keys=True)
                       json.dump(json_object, data)
                   file_count = 0

               page_json = json.load(f)
       
               url = page_json['url']
               file_indexer[file_id] = urldefrag(url)[0]

               soup = BeautifulSoup(page_json['content'], 'html.parser')
               
               title = file_name.replace(".json", "")
               title_tag_lst = soup.find_all("title")
               anchor_tag_lst = soup.find_all("href")
               important_tag_lst = soup.find_all(re.compile('^(h[1-6]|b|strong)$'))

               # identify title
               title_tokens = []
               for title_tag in title_tag_lst:
                   text = title_tag.get_text()
                   title_tokens = tokenizer(text)
               title_frequency = computeTokenFrequency(title_tokens)

               # identify anchor
               anchor_tokens = []
               for anchor_tag in anchor_tag_lst:
                   text = anchor_tag.get_text()
                   anchor_tokens = tokenizer(text)
               anchor_frequency = computeTokenFrequency(anchor_tokens)
                  
               # identify heading
               important_tokens = []
               for important_tag in important_tag_lst:
                   text = important_tag.get_text()
                   important_tokens = tokenizer(text)
               important_frequency = computeTokenFrequency(important_tokens)       
 
               # tokenize text
               text = soup.get_text()
               tokens = tokenizer(text)
               tokens_frequency = computeTokenFrequency(tokens)

               # calculate checksum
               checksum = sum(ord(i) for i in soup.get_text())

               for token in tokens:
                   curr_page_info = DocInfo(tokens_frequency[token], title_frequency.get(token, 0), anchor_frequency.get(token, 0), important_frequency.get(token, 0), checksum)._asdict()
                   index[token][file_id] = curr_page_info            
               
              
    with open("./data/file_index.json", "w") as file_index:
        json.dump(file_indexer, file_index)
    

    with open("total_files.txt", "w") as total_files:
        total_files.write("Number of Documents: " + str(file_id))


