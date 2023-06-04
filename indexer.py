'''
@author: Sougata Saha
Institute: University at Buffalo
'''


from linkedlist import LinkedList,Node
from collections import OrderedDict, deque


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        # self.docid_doc = OrderedDict({})
        # self.tf_idf = OrderedDict({})

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        # self.docid_doc[doc_id] = tokenized_document
        for t in tokenized_document:
            co = tokenized_document.count(t)
            co = co/len(tokenized_document)
            self.add_to_index(t, doc_id, co)
        

    def add_to_index(self, term_, doc_id_,co):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented.
            Implemented"""
      
        if (self.inverted_index.get(term_,False) == False):
            self.inverted_index[term_] =  LinkedList()
        ll = self.inverted_index.get(term_)
        ll.insert_at_end(doc_id_,co)

         

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
      
        for term, llist in self.inverted_index.items():
            llist.add_skip_connections()


    def calculate_tf_idf(self, N):
        for term, llist in self.inverted_index.items():
            pl_n = llist.length
            llist.idf = N/pl_n
        for term, llist in self.inverted_index.items():
            head = llist.start_node
            while(head!=None):
                head.tf_idf = llist.idf*head.tf
                head = head.next
        
        
        

