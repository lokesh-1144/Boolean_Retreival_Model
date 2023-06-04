'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math
from collections import OrderedDict

class Node:

    def __init__(self, value=None, next=None, tf_idf=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.tf_idf = 0
        self.tf = 0
        self.skip = None


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None
        self.post_with_skips = OrderedDict({})

    def traverse_list(self):
        traversal = []
        traversal_tfidf = []
        if self.start_node is None:
            return
        else:
            
            head = self.start_node
            while(head!=None):
                traversal.append(head.value)
                traversal_tfidf.append(head.tf_idf)
                head = head.next
            
            return traversal, traversal_tfidf

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            head = self.start_node
            if(head.next == None):
               traversal.append(head.value)
               return traversal 
          
            while(head.skip!=None):
                    traversal.append(head.value)
                    head = head.skip
            traversal.append(head.value)

            return traversal

    def add_skip_connections(self):
        count = 0
        n_skips = math.floor(math.sqrt(self.length))
        
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1
        if(self.start_node == None):
            return

        head = self.start_node


        i = 0
        j = 0
        skip_n = head
        # self.n_skips = self.n_skips+1
        if(head.next == None):
            self.n_skips = self.n_skips+1
            return
            
        while(head!=None):
            n = round(math.sqrt(self.length),0)
            if(n_skips!=0 and (j-i)%(n)==0 and j!=0):
                count = count + 1
                skip_n.skip = head
                skip_n = head
                self.n_skips = self.n_skips+1
                i = j
            j  = j+1
            head = head.next
            if(count == n_skips):
                break
    

    def insert_at_end(self, value, co):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
             implemented. """
        self.length = self.length + 1
        if (self.start_node == None):
            sn = Node() 
            sn.value = value
            sn.next  = self.end_node
            # sn.tf_idf = 0 
            sn.tf = co    
            self.start_node = sn
            return 
        
        
        head = self.start_node
        
        
        new_node = Node()
        new_node.value = value
        # new_node.tf_idf = 0
        new_node.tf = co
        new_node.next = None

        
        if(head.value == value):
            self.length = self.length - 1
            return
        if(value < head.value):
            new_node.next = head
            self.start_node = new_node
            return

        prev = head                               
        while (head.next!= None):
            prev = head
            head = head.next 
            if (value == prev.value or value == head.value):
                self.length = self.length - 1
                return         
            if(value < head.value and  value > prev.value):
                break
            prev = head

        new_node.next = prev.next         
        prev.next = new_node
        
        

