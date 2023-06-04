'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
        text = text.lower()
        text = re.sub("[^a-z0-9]"," ",text)
        text = text.strip()
        text = " ".join(text.split())
        tokens = text.split()
        sw = self.stop_words
        tok_af_stop = [t for t in tokens if t not in sw]
        tok_af_stem = [self.ps.stem(t) for t in tok_af_stop]
        return tok_af_stem



        
        
        
