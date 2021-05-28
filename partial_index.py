# turn the json file into text file -> partial_index.py
# merge the text together and create byte_dict -> merge_index.py
# implement boolean search -> search.py

import json
import os


path = "./data"
partial_index_count = 0


for root, directory, files in os.walk(path):
    for file_name in files: 
        if "data_" in file_name:
            print(file_name)

    
            # token   doc:frequency:bold doc:frequency:bold
            # token2  doc:frequency:bold
            with open(f"./data/partial_index{partial_index_count}.txt", "w") as f:
                partial_index_count += 1

                with open(root + "/" + file_name) as index:
                    final_index = json.loads(json.load(index))
  
                for token, doc_info_dict in final_index.items():
                    # print(token)

                    total_string = ""
                    total_string += f"{token}"

                    for doc, markup_dict in doc_info_dict.items():
                        total_string += f" {doc}:{markup_dict['count']}:{markup_dict['title']}:{markup_dict['anchor']}:{markup_dict['important_count']}:{markup_dict['checksum']}"

                    total_string += "\n"

                    f.write(total_string)


              
