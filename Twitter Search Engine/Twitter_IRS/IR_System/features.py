
import nltk
from nltk.util import ngrams
from nltk.metrics.distance  import edit_distance
#nltk.download('words')
from nltk.corpus import words, wordnet

correct_words = words.words()



def getRefinedQueryJC(query):
    def jaccardCoeff(set1, set2):
        return len(set1.intersection(set2)) / len(set1.union(set2))
    res = []
    query = query.strip().split()
    #print(query)
    for word in query:
        if len(word) > 1:
            temp = [ (jaccardCoeff(set(ngrams(word, 2)), set(ngrams(w, 2))),w) for w in correct_words if w[0]==word[0]]
            res.append(sorted(temp, key = lambda val:val[0])[-1][1])
    #print(res)
    return ' '.join(res).strip()


#print(getRefinedQueryJC("happpy azmaing intelliengt "))


def getRefinedQueryED(query):

    res = []
    query = query.strip().split()
    #print(query)
    for word in query:
        temp = [(edit_distance(word, w),w) for w in correct_words if w[0]==word[0]]
        res.append(sorted(temp, key = lambda val:val[0])[0][1])
    #print(res)
    return ' '.join(res).strip()

#print(getRefinedQueryED("happpy azmaing intelliengt "))

def getRefinedQueryThesauras(query1):
    try:
        query = query1.strip().split()
        #print(query)
        for ind, word in enumerate(query):
            rel = {}
            #print('for - ', word)
            syns = wordnet.synsets(word)
            for syn in syns:
                if syn.lemmas()[0].name() not in rel.keys():
                    rel[syn.lemmas()[0].name()] = wordnet.synset(syn.name()).wup_similarity(wordnet.synset(wordnet.synsets(word)[0].name()))
            #print(rel)
            rel = {k: v for k, v in rel.items() if v is not None}
            bestMatch = max(rel, key= lambda x: rel[x])
            #print(bestMatch)
            if rel[bestMatch]>0.8:
                query[ind] = bestMatch
        #print(query)
        return ' '.join(query).strip()
    except:
        return query1.strip()

#print(getRefinedQueryThesauras("happy program welcome news paper"))
