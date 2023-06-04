'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList,Node
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

import json
# if you are using python 3, you should 
import urllib.request

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()
        self.no_doc = 0

    def _merge(self, p1, p2,p1_tf_idf, p2_tf_idf):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        li = []
        li_tf_idf = []
        n = len(p1)
        m = len(p2)
        i = 0
        j = 0
        count = 0
        while(i<n and j<m):
            if(p1[i] == p2[j]):
                count = count +1
                li.append(p1[i])
                max_tf = 0
                if(p1_tf_idf[i] > p2_tf_idf[j]):
                     max_tf =  p1_tf_idf[i]
                else:
                     max_tf =  p2_tf_idf[j]
                li_tf_idf.append(max_tf) 
                i = i+1
                j = j+1
            elif (p1[i] < p2[j]):
                count = count + 1
                i = i+1
            else:
                j = j+1
                count = count+1
        return li,count,li_tf_idf
    
    def _merge_skip(self, p1, p2 ):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        li = LinkedList()
        
       
        count = 0
        while(p1!=None and p2!=None):
            if(p1.value == p2.value):
                count = count +1
                nn = Node()
                nn.value = p1.value
                max_tf_idf = 0
                if(p1.tf_idf > p2.tf_idf):
                     max_tf_idf =  p1.tf_idf
                else:
                     max_tf_idf =  p2.tf_idf

                nn.tf_idf = max_tf_idf
               

                if(li.start_node == None):
                    li.start_node = nn
                    li.length = li.length+1

                    p1 = p1.next
                    p2 = p2.next
                    continue

                head =  li.start_node
                while(head.next!=None):
                    head = head.next
                li.length = li.length+1
                head.next = nn   
                p1 = p1.next
                p2 = p2.next
            elif (p1.value < p2.value):
                if (p1.skip != None and (p1.skip.value <= p2.value)):

                    
                    while (p1.skip != None and (p1.skip.value <= p2.value)):
                        p1 = p1.skip
                        count = count + 1
                else:
                        count = count + 1
                        p1 = p1.next
            else:
                if (p2.skip !=None and (p2.skip.value <= p1.value )):
                    while (p2.skip != None and (p2.skip.value <= p1.value)):
                            p2 = p2.skip
                            count = count + 1
                else:
                        count = count + 1
                        p2 = p2.next
        # print (li.traverse_list())
        li.add_skip_connections()            
        return li,count

    def _daat_and(self, term_li):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        tf_idf_dict = OrderedDict({})
        pl = self._get_postings(term_li[0])
        res,res_tf_idf = pl.traverse_list()
        res_cmp = 0
        for term in term_li[1:]:
            ll = self._get_postings(term)
            li,li_tfidf = ll.traverse_list()

            res,c,res_tf_idf = self._merge(res, li,res_tf_idf,li_tfidf)
            res_cmp = res_cmp + c
        i = 0
        for doc in res:
           tf_idf_dict[doc] = res_tf_idf[i]
           i = i+1

        return res,res_cmp,tf_idf_dict

    def _daat_and_skip(self,term_li):
        res = self._get_postings(term_li[0])
        res_cmp =0
        tf_idf_dict = OrderedDict({})
        for term in term_li[1:]:
            ll = self._get_postings(term)
            res,c = self._merge_skip(res.start_node, ll.start_node)
            res_cmp = res_cmp + c
        res, res_tf_idf = res.traverse_list()
        i = 0
        for doc in res:
           tf_idf_dict[doc] = res_tf_idf[i]
           i = i+1
        return res,res_cmp,tf_idf_dict
        

    def _get_postings(self,term):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        inv = self.indexer.get_index()
        return inv.get(term)

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        # with open(corpus, 'r',encoding="utf8") as fp:
        #     for line in tqdm(fp.readlines()):
        #         self.no_doc = self.no_doc + 1
        #         doc_id, document = self.preprocessor.get_doc_id(line)
        #         tokenized_document = self.preprocessor.tokenizer(document)
        #         # print (type(tokenized_document))              
        #         self.indexer.generate_inverted_index(doc_id, tokenized_document)
        #         # dic = self.indexer.get_index()
        #         # print(dic)

        
 
# import urllib2


        with open(corpus, 'r',encoding="utf-8") as fp:
        # change the url according to your own corename and query
          
            outfn = 'output_bm25.txt'
            doc_id = '004'
       
            text = "Wegen Flüchtlingskrise\: Angela Merkel stürzt in Umfragen"
            
            # text = text.encode('utf8')
            inurl = 'http://34.125.12.134:8983/solr/IRP3BM5_1/select?q=text_en:'+text+', text_ru:'+text+', text_de:'+text+'&fl=id%2Cscore&wt=json&indent=true&rows=20'

            # inurl = inurl.encode('utf-8')

            inurl = inurl.replace(' ','%20')

        # change query id and IRModel name accordingly
            qid = doc_id
            IRModel='bm25' #either bm25 or vsm
            outf = open(outfn, 'a+')
# if you're using python 3, you should use
            data = urllib.request.urlopen(inurl)

            docs = json.load(data)['response']['docs']
# the ranking should start from 1 and increase
            rank = 1
            for doc in docs:
                outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
                rank += 1
            outf.close()
        
       
       
        # self.indexer.sort_terms()
        # self.indexer.add_skip_connections()
        # inv = self.indexer.get_index()
    
      
        # self.indexer.calculate_tf_idf(self.no_doc)

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores.
                IMP"""
            input_term_arr = self.preprocessor.tokenizer(query)
            inv = self.indexer.get_index()

            # raise NotImplementedError
            sort_len_pl = OrderedDict({})  

            for term in input_term_arr:
                postings, skip_postings = None, None



                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                  implemented."""
                
                ll = inv.get(term)
                sort_len_pl[term] = ll.length
                postings,tf_idf = ll.traverse_list()
                skip_postings = ll.traverse_skips()
                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings
            

            sort_len_pl = dict(sorted(sort_len_pl.items(), key = lambda item: item[1]))
            
            term_li = list(sort_len_pl.keys())

            
            

            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            #daatAnd
            and_op_no_score_no_skip, and_comparisons_no_skip, daat_idf_dict = self._daat_and(term_li)
            and_results_cnt_no_skip = len(and_op_no_score_no_skip)

            #daatAndSkip
            and_op_no_score_skip, and_comparisons_skip, daat_skip_idf_dict  = self._daat_and_skip(term_li)
            and_results_cnt_skip = len(and_op_no_score_skip)


            #daatAndTfIdf
            daat_idf_dict = dict(sorted(daat_idf_dict.items(), key = lambda item: item[1],reverse=True))
            and_op_no_score_no_skip_sorted = list(daat_idf_dict.keys())
            and_results_cnt_no_skip_sorted  = and_results_cnt_no_skip
            and_comparisons_no_skip_sorted  = and_comparisons_no_skip

            #daatAndSkipTfIdf

            daat_skip_idf_dict = dict(sorted(daat_skip_idf_dict.items(), key = lambda item: item[1],reverse=True))
            and_op_no_score_skip_sorted = list(daat_skip_idf_dict.keys())
            and_results_cnt_skip_sorted  = and_results_cnt_skip
            and_comparisons_skip_sorted  = and_comparisons_skip


            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)
    


    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")

    argv = parser.parse_args()

    # corpus = argv.corpus
    corpus = "D:\Fall-Sem2\IR\Project2\CSE_4535_Fall_2021\project2\queries.txt"
   
    # output_location = argv.output_location
  
    # username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)
    
    # app.run(host="0.0.0.0", port=9999)
