import json
from math import log


with open("total_files.txt") as total:
    totalDocs = int(total.readline().split()[-1])


def tfidf(termFreq, docFreq):
    global totalDocs
    return (1 + log(termFreq, 10)) * log(totalDocs / docFreq, 10)



# {token: byte_location}
byte_dict = {}


index0 = open("./data/partial_index0.txt")
index1 = open("./data/partial_index1.txt")
index2 = open("./data/partial_index2.txt")
index3 = open("./data/partial_index3.txt")
index4 = open("./data/partial_index4.txt")

nextLine_0 = next(index0, '')
nextLine_1 = next(index1, '')
nextLine_2 = next(index2, '')
nextLine_3 = next(index3, '')
nextLine_4 = next(index4, '')


files = [index0, index1, index2, index3, index4]
currLines = [nextLine_0, nextLine_1, nextLine_2, nextLine_3, nextLine_4]


with open("final_index.txt", "w") as f:
    while any(currLines):

        # find the smallest token
        smallestToken_line = min([currLine for currLine in currLines if currLine], key=lambda x: x.split()[0])
        smallest_token = smallestToken_line.split()[0]
        # print(smallest_token)


        update_file = []
        posting = [smallest_token]
        docIds = []            

        for index_file, currLine in enumerate(currLines):
            parsed_line = currLine.strip().split()
            # print(parsed_line)
            token = parsed_line[0]
            documents = parsed_line[1:]
            
            # if the token is the smallest then index it 
            if token == smallest_token:
                docIds.extend(documents)
                update_file.append(index_file)

        
        # token docId:count:title:important_count:anchor:checksum:tfidf docId:count:bold:title:important_count:anchor:checksum:tfidf
  
        # sort the documents by id
        docCount = len(set(docIds))
        docIds = list(map(lambda x: x + ":" + str(tfidf(int(x.split(":")[1]), docCount)), docIds)) 
        docIds.sort(key=lambda x: int(x.split(":")[0]))


        # prepare to write string into file
        posting.extend(docIds)
        smallestToken_line = ' '.join(posting) + "\n"


        # record the byte location and write to file     
        byte_dict[smallest_token] = f.tell()
        f.write(smallestToken_line)        


        # find the next lines of the files whose tokens were the smallest for this round
        for need_update in update_file:
           currLines[need_update] = next(files[need_update], "")


with open("byte_dict.json", "w") as byte:
    json.dump(byte_dict, byte)
     
