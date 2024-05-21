from django.core.cache import cache
from django.http import JsonResponse

from treeflow.corpus.templatetags.dict_tags import getCustomAlphabeticalOrder
from treeflow.dict.models.lemma import Lemma

# import time


def fetch_alphabet(request):
    usesCache = False
    lemmas = cache.get('lemmas')
 
    if lemmas is None:
       print(f"({__name__}) Cache not available: Querying lemmas from database")
       lemmas = Lemma.objects.values('word')
    else:
        usesCache = True

    processed_data = set()

    # start_time = time.time()

    for item in lemmas:
        if not usesCache:
            if (s := item['word']) != "":
                processed_data.add(s[0])
        else:
            if (s := item.word) != "":
                processed_data.add(s[0])

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"The loop took {elapsed_time} seconds.")

    return JsonResponse({'alphabet': sort(processed_data)})

def sort(data):
    c_order = getCustomAlphabeticalOrder()
    return sorted([x for x in data if x != ""], key=lambda x: c_order.index(x) if x in c_order else len(c_order))



