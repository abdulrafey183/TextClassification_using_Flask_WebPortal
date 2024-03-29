import numpy as np
from collections import Counter
import csv, pickle, os
from nltk.corpus import stopwords
from flask import current_app as app 

class_arr = np.array([
    "purpose", 
    "craftsmanship", 
    "aesthetic",
    "none"
])
index = {
    "purpose"      : [1, 0, 0, 0], 
    "craftsmanship": [0, 1, 0, 0],  
    "aesthetic"    : [0, 0, 1, 0],
    "none"         : [0, 0, 0, 1]        
}

#############       DATA PRE-PROCESSING FUNCTIONS       #############   

def load_data(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            temp = row
            break
        
        if row[0].lower() != 'labels' or row[1].lower() != 'sentences':            
            print("ERROR: PLZ NAME THE FIRST ROW 'labels' and 'sentences'")
            return
                
        df = pd.read_csv(path)    
        return df


def count_words(features):
    counter = Counter()
    maximum = 0
    
    for sentence in features:
        maximum = max(maximum, len(sentence))
        
        for word in sentence: 
            counter[word] += 1
            
    return maximum, counter


def filter_func(temp):
    
    stop = set(stopwords.words("english"))
    
    temp = temp.lower()
    temp = temp.split()
    temp = [
        element
        for element in temp
        if element not in stop
    ]
    return temp

filter_func = np.vectorize(filter_func, otypes=[list])    


def shuffle(features, labels):
    
    assert labels.shape[0] == features.shape[0]

    idx = np.arange(labels.shape[0])
    np.random.shuffle(idx)
    
    return features[idx], labels[idx]


def onehot_encode_labels(labels):
    
    return np.array([
        index[e] 
        for e in labels
    ])


def decode_onehot_labels(class_idx):
    
    return class_arr[class_idx] 


#############       LOAD FUNCTIONS      #############

def load_tokenizer():

    with open('application/static/Pickles/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    return tokenizer


def load_classColors():

    with open('application/static/Pickles/class_colors.pickle', 'rb') as handle:
        class_colors = pickle.load(handle)

    return class_colors


#############       SAVE FUNCTIONS      #############

def save_tokenizer(tokenizer):

    with open('application/static/Pickles/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_classColors(new_purpose, new_craftsmaship, new_aesthetic, new_none):
    class_colors = {'purpose': new_purpose, 'craftsmaship': new_craftsmaship, 'aesthetic': new_aesthetic, 'none':new_none}

    #Overwriting Previous Colors File
    with open('application/static/Pickles/class_colors.pickle', 'wb') as handle:
        pickle.dump(class_colors, handle, protocol=pickle.HIGHEST_PROTOCOL)


#############       BIN FUNCTIONS      #############


def appendTSVtoBin(labels, sentences):

    with open('application/bin/output2.tsv', 'a', newline="") as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t')

        for i in zip(labels, sentences):
            tsv_writer.writerow([i[0], i[1]])
            print(i[0], i[1])

def loadTSVfromBin():

    with open('application/bin/output2.tsv', 'r') as tsv_file:

        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        
        try:
            data = [ (row[1], row[0]) for row in tsv_reader ]

        except IndexError as ie:
            print(ie)
            data = []
            
        
    return data

def clearBin():

    with open('application/bin/output2.tsv', 'wt') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t')

    return


#############       OTHER FUNCTIONS      #############

def singlefile(file):

    list = os.listdir("application/static/File_Upload_Folder/")
    for i in list:
        os.remove("application/static/File_Upload_Folder/"+i)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], "uploaded.tsv"))

def roundoff(arr):

    arr = np.max(arr, axis= 1)
    arr = arr * 100
    arr = np.around(arr, decimals= 3)

    return arr