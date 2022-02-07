from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import os
import numpy as np
import pandas as pd

from .system import System



def home(request):

    try:
        print(request.POST['query'])

    except:
        pass

    return render(request, 'queries/home.html')

def queries(request, q):

    # Calling the IR System

    BASE_DIR = Path(__file__).resolve().parent.parent
    DOCUMENTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'dataset.txt')
    FREQUENCY_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'frequency-index.txt')
    TFIDF_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'tf-idf-index.txt')
    TEST_QUERY_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'test-run-50.xml')
    RESULTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'results.txt')



    system = System(DOCUMENTS_PATH, FREQUENCY_IDX_PATH, TFIDF_IDX_PATH, False)
    q = system.test_system_with_stringQueries("myrun", q, RESULTS_PATH , 0, 0.7, 100)


    try:
        # loading results.txt
        results = pd.read_csv(RESULTS_PATH, sep=" ", header=None)
        results.columns = ["QUERY_ID", "Q", "DOCUMENT_ID", "RANK", "SCORE", "RUN_NAME"]
        results = results[["QUERY_ID", "DOCUMENT_ID", "RANK"]]

        # loading trec-microblog11.txt
        documents = pd.read_csv(DOCUMENTS_PATH, sep="\t", header=None)
        documents.columns = ["DOCUMENT_ID", "DOCUMENT"]
        documents.index = pd.Index(documents.DOCUMENT_ID.values)

        # initializing constants
        NUM_QUERIES = results.QUERY_ID.max()
        MAX_RANK = results.RANK.max()

        # extracting only  the query 1
        results_1 = results.groupby(by="QUERY_ID").get_group(1)
        results_1.index = pd.Index(range(len(results_1)))

        # extracting ranked documents
        ranked_documents = documents.loc[results_1.DOCUMENT_ID]
        ranked_documents.index = pd.Index(range(len(ranked_documents)))
        ranked_documents["RANK"] = range(1, len(ranked_documents)+1)

    except:
        ranked_documents = pd.DataFrame({'DOCUMENT': ["No results found."]})




    context = {'query': q, 'ranked_documents': ranked_documents}

    return render(request, 'queries/queries.html', context)


def jaccard_distance_queries(request, q):

    # Calling the IR System

    BASE_DIR = Path(__file__).resolve().parent.parent
    DOCUMENTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'dataset.txt')
    FREQUENCY_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'frequency-index.txt')
    TFIDF_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'tf-idf-index.txt')
    TEST_QUERY_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'test-run-50.xml')
    RESULTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'results.txt')



    system = System(DOCUMENTS_PATH, FREQUENCY_IDX_PATH, TFIDF_IDX_PATH, False)
    q = system.test_system_with_stringQueries("myrun", q, RESULTS_PATH , 1, 0.7, 100)


    try:
        # loading results.txt
        results = pd.read_csv(RESULTS_PATH, sep=" ", header=None)
        results.columns = ["QUERY_ID", "Q", "DOCUMENT_ID", "RANK", "SCORE", "RUN_NAME"]
        results = results[["QUERY_ID", "DOCUMENT_ID", "RANK"]]

        # loading trec-microblog11.txt
        documents = pd.read_csv(DOCUMENTS_PATH, sep="\t", header=None)
        documents.columns = ["DOCUMENT_ID", "DOCUMENT"]
        documents.index = pd.Index(documents.DOCUMENT_ID.values)

        # initializing constants
        NUM_QUERIES = results.QUERY_ID.max()
        MAX_RANK = results.RANK.max()

        # extracting only  the query 1
        results_1 = results.groupby(by="QUERY_ID").get_group(1)
        results_1.index = pd.Index(range(len(results_1)))

        # extracting ranked documents
        ranked_documents = documents.loc[results_1.DOCUMENT_ID]
        ranked_documents.index = pd.Index(range(len(ranked_documents)))
        ranked_documents["RANK"] = range(1, len(ranked_documents)+1)

    except:
        ranked_documents = pd.DataFrame({'DOCUMENT': ["No results found."]})




    context = {'query': q, 'ranked_documents': ranked_documents}

    return render(request, 'queries/queries.html', context)

def edit_distance_queries(request, q):

    # Calling the IR System

    BASE_DIR = Path(__file__).resolve().parent.parent
    DOCUMENTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'dataset.txt')
    FREQUENCY_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'frequency-index.txt')
    TFIDF_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'tf-idf-index.txt')
    TEST_QUERY_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'test-run-50.xml')
    RESULTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'results.txt')



    system = System(DOCUMENTS_PATH, FREQUENCY_IDX_PATH, TFIDF_IDX_PATH, False)
    q = system.test_system_with_stringQueries("myrun", q, RESULTS_PATH , 2, 0.7, 100)


    try:
        # loading results.txt
        results = pd.read_csv(RESULTS_PATH, sep=" ", header=None)
        results.columns = ["QUERY_ID", "Q", "DOCUMENT_ID", "RANK", "SCORE", "RUN_NAME"]
        results = results[["QUERY_ID", "DOCUMENT_ID", "RANK"]]

        # loading trec-microblog11.txt
        documents = pd.read_csv(DOCUMENTS_PATH, sep="\t", header=None)
        documents.columns = ["DOCUMENT_ID", "DOCUMENT"]
        documents.index = pd.Index(documents.DOCUMENT_ID.values)

        # initializing constants
        NUM_QUERIES = results.QUERY_ID.max()
        MAX_RANK = results.RANK.max()

        # extracting only  the query 1
        results_1 = results.groupby(by="QUERY_ID").get_group(1)
        results_1.index = pd.Index(range(len(results_1)))

        # extracting ranked documents
        ranked_documents = documents.loc[results_1.DOCUMENT_ID]
        ranked_documents.index = pd.Index(range(len(ranked_documents)))
        ranked_documents["RANK"] = range(1, len(ranked_documents)+1)

    except:
        ranked_documents = pd.DataFrame({'DOCUMENT': ["No results found."]})




    context = {'query': q, 'ranked_documents': ranked_documents}

    return render(request, 'queries/queries.html', context)

def thesauras_queries(request, q):

    # Calling the IR System

    BASE_DIR = Path(__file__).resolve().parent.parent
    DOCUMENTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'dataset.txt')
    FREQUENCY_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'frequency-index.txt')
    TFIDF_IDX_PATH = os.path.join(BASE_DIR, 'IR_System', 'index', 'tf-idf-index.txt')
    TEST_QUERY_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'test-run-50.xml')
    RESULTS_PATH = os.path.join(BASE_DIR, 'IR_System', 'data', 'results.txt')



    system = System(DOCUMENTS_PATH, FREQUENCY_IDX_PATH, TFIDF_IDX_PATH, False)
    q = system.test_system_with_stringQueries("myrun", q, RESULTS_PATH , 3, 0.7, 100)


    try:
        # loading results.txt
        results = pd.read_csv(RESULTS_PATH, sep=" ", header=None)
        results.columns = ["QUERY_ID", "Q", "DOCUMENT_ID", "RANK", "SCORE", "RUN_NAME"]
        results = results[["QUERY_ID", "DOCUMENT_ID", "RANK"]]

        # loading trec-microblog11.txt
        documents = pd.read_csv(DOCUMENTS_PATH, sep="\t", header=None)
        documents.columns = ["DOCUMENT_ID", "DOCUMENT"]
        documents.index = pd.Index(documents.DOCUMENT_ID.values)

        # initializing constants
        NUM_QUERIES = results.QUERY_ID.max()
        MAX_RANK = results.RANK.max()

        # extracting only  the query 1
        results_1 = results.groupby(by="QUERY_ID").get_group(1)
        results_1.index = pd.Index(range(len(results_1)))

        # extracting ranked documents
        ranked_documents = documents.loc[results_1.DOCUMENT_ID]
        ranked_documents.index = pd.Index(range(len(ranked_documents)))
        ranked_documents["RANK"] = range(1, len(ranked_documents)+1)

    except:
        ranked_documents = pd.DataFrame({'DOCUMENT': ["No results found."]})




    context = {'query': q, 'ranked_documents': ranked_documents}

    return render(request, 'queries/queries.html', context)
