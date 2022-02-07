
'''
Group Members:
    Harshith Jupuru (S20190010072) , Sree Nithish B (S20190010166) , Logu R (S20190010___)

'''

from .indexing import Indexer
from .preprocessor import Preprocessor
from .query import Query
from xml.etree import ElementTree
import re
from pathlib import Path
import os
from .features import getRefinedQueryJC, getRefinedQueryED, getRefinedQueryThesauras

class System:
    def __init__(self, corpus_path, freq_index_path, tf_idf_index_path, create_index=False):
        '''
        Sets up the system for testing by parsing the corpus with the Preprocessor and creating the two indexes with the Indexer.
        If the indexes have already been created and written to a file, it is possible to read them in instead of recreating them to save time.
        :param corpus_path: the path to the file containing the corpus of words.
        :param freq_index_path: the path to the file to save/load the frequency index
        :param tf_idf_index_path: the path to the file to save/load the tf-idf index
        :param create_index: if True, creates the frequency index and tf-idf index and writes them to the specified path.  Otherwise, loads them from a file at the specified path.
        '''
        self.preprocessor = Preprocessor(corpus_path);
        self.corpus = {}
        # if create_index, then run the create_indexes, otherwise, load them from their already existing file locations
        if create_index:
            print ("Creating frequency and tf_idf_indexes.")
            self.corpus = self.preprocessor.parse_corpus()  # {docId:content in docId(which is a string), docId:content(string),...}    Ex: corpus[DocId]:"Content in Doc1"
            tokens = self.preprocessor.create_tokens(self.corpus)   # all unique tokens from all the documents, dtype = Set() Ex: ("all", "unique", "words",...)
            c_counter = self.preprocessor.create_corpus_counter(self.corpus)    # {docId1:{"term1inDoc1":freq, "term2inDoc1":freq,...}, docId2:{"term1inDoc2":freq, "term2inDoc2":freq,...}}  corupus_counter[doc_id] = {"fifa": 2, "world": 1, "cup": 1}.
            self.indexer = Indexer(c_counter, tokens)   # Create an instance of Indexer class
            # Uncomment and run with create_index set to True if you would like to see the results using the
            # different, but faster optimized algorithm for indexing
            # self.frequency_index = self.indexer.create_frequency_index_optimized()
            self.frequency_index = self.indexer.create_frequency_index()    # {"token1":{docId:freq, ...}, "token2":{docId:freq,...}, ....} i.e, {"Index1/token1":{docId1:freqOfToken1InDoc1, docId2:freqOfToken1InDoc2,...}, "Index2/token2":{docId1:freqOfToken2InDoc1, docId2:freqOfToken2InDoc2,...},...}
            # print(self.frequency_index)
            self.indexer.index_to_file(self.frequency_index, freq_index_path)   #saves the idf into the file in given location
            #len(self.frequency_index) gives number of unique tokens in doc collection but not no of docs. We need to use len(self.corpus) for corpus size.
            self.tf_idf_index = self.indexer.create_tf_idf_index(self.frequency_index, len(self.corpus))   # {"token1":{docId:tfIdf_weight, ...}, "token2":{docId:tfIdf_weight,...}, ....}
            self.indexer.index_to_file(self.tf_idf_index, tf_idf_index_path)
        else:
            print ("Loading frequency and tf_idf indexes.")
            self.corpus = self.preprocessor.parse_corpus(True)
            self.indexer = Indexer()
            self.frequency_index = self.indexer.load_index(freq_index_path)
            self.tf_idf_index = self.indexer.load_index(tf_idf_index_path)
        self.query = Query(self.frequency_index, self.tf_idf_index, self.corpus)


    def test_system(self, run_name, query_path, results_path):
        '''
        Tests the system by running all the queries, saving the results to a file.  Formats the file output to match expected format for use with trec_eval
        :param run_name: a name for the current run, used to distinguish results
        :param query_path: the path to the file containing the queries
        :param results_path: the desired path to save the results file in
        '''
        query_tree = ElementTree.parse(query_path)
        print ("Testing system on queries.")
        with open(results_path, 'wb') as f:
            for child in query_tree.getroot():
                qid_re = re.compile("\d{3}")
                qid = int(qid_re.search(child[0].text).group(0))
                query_results = self.query.execute_query(child[1].text)
                for i in range(len(query_results)):
                    if i >= 100:
                        break
                    print_out = str(qid) + " " + "Q0" + " " + str(query_results[i].get("id")) + " " + str(i + 1) + " " + \
                                str(query_results[i].get("score")) + " " + run_name + "\n"

                    f.write(print_out.encode('ascii'))
        print("Query results saved to", results_path)


    def test_system_with_stringQueries(self, run_name, query, results_path, feature_Id, threshold, maxDocs):
        if feature_Id>0:
            query_results_original_list = self.query.execute_query(query)
            query_results_original = {}
            query_results_refined = {}
            for i in query_results_original_list:
                query_results_original.update({i.get('id'):i.get('score')})

            if feature_Id==1:
                query = getRefinedQueryJC(query)    # Jaccard distance
            elif feature_Id==2:
                query = getRefinedQueryED(query)    # edit distance
            elif feature_Id==3:
                query = getRefinedQueryThesauras(query) # Thesauras
            print(query)
            query_results_refined_list = self.query.execute_query(query)
            for i in query_results_refined_list:
                query_results_refined.update({i.get('id'):i.get('score')})

            for key in query_results_refined.keys():
                if (key in query_results_original.keys()) and (query_results_original[key] < query_results_refined[key]):
                    query_results_original[key] = query_results_refined[key]
                elif query_results_refined[key] >= threshold:
                    query_results_original[key] = query_results_refined[key]
            query_results = []
            for key, val in query_results_original.items():
                query_results.append({'id':key, 'score':val})
            query_results = sorted(query_results, key=lambda doc: doc["score"], reverse=True)

        else:
            query_results = self.query.execute_query(query)
            print(query)
        with open(results_path, 'wb') as f:
            for i in range(len(query_results)):
                if i>=maxDocs or query_results[i].get("score")<threshold:
                    break
                print_out = str(1) + " " + "Q0" + " " + str(query_results[i].get("id")) + " " + str(i + 1) + " " + \
                            str(query_results[i].get("score")) + " " + run_name + "\n"
                f.write(print_out.encode('ascii'))
        print("Query results saved to", results_path)
        return query


# Paths to create Indexing

# BASE_DIR = Path(__file__).resolve().parent.parent
# DOCUMENTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'dataset.txt')
# FREQUENCY_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'frequency-index.txt')
# TFIDF_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'tf-idf-index.txt')
# TEST_QUERY_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'test-run-50.xml')
# RESULTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'results.txt')


# system = System("data/trec-microblog11.txt", "index/frequency-index.txt", "index/tf-idf-index.txt", False)
# system.test_system("myrun", "data/topics_mb1-50.xml", "data/results1withoutIndexing.txt")


# To create Indexed again
# system = System("data/trec-microblog11.txt", "index/frequency-index-new-1WithIndexing.txt", "index/tf-idf-index-new-1WithIndexing.txt", True)
# system.test_system("myRun", "data/topics_MB1-50.xml", "data/results-new-1WithIndexing.txt")


# sys = System("data/trec-microblog11.txt", "index/frequency-index-new-1WithIndexing.txt", "index/tf-idf-index-new-1WithIndexing.txt", False)
# sys.test_system_with_stringQueries("myrun", "BBC job lost", "data/testingRes1.txt" , 3, 0.7, 100)
