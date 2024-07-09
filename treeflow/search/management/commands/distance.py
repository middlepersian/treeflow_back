from django.core.management.base import BaseCommand
from treeflow.corpus.models import Section, Token, SectionToken
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import F
from django.contrib.postgres.aggregates import StringAgg
import time
import re
def get_token_indecies(tokens, token) -> list:
    indecies = []
    for i, t in enumerate(tokens):
        if t == token:
            indecies.append(i)
    return indecies

class Command(BaseCommand):
    help = 'Perform a distance search on the database. Takes anchor token, [tokens], direction and distance as arguments.'

    def add_arguments(self, parser):
        # parse list of tokens
        parser.add_argument('anchor_token', type=str, help='The anchor token to search for.')
        parser.add_argument('tokens', nargs='+', type=str, help='The tokens to search for.')
        parser.add_argument('direction', type=str, help='The direction of the search. Can be "before" or "after".')
        parser.add_argument('distance', type=int, help='The distance between the two tokens.')

    def handle(self, *args, **options):
        start = time.time()
        print("start time: ", start)

        anchor_token = options['anchor_token']
        query_tokens = [token for token in options['tokens'] if token != '+']
        distance = options['distance']
        direction = options['direction']

        queryClasses = Q()
        for token in [anchor_token]+query_tokens:
            queryClasses |= Q(token__transcription__icontains=token)
        
        regexClasses = Q()
        for token in query_tokens:
            regexStr = r"("+re.escape(anchor_token)+r")((===\w+)){"+re.escape(str(distance))+r"}===("+re.escape(token)+r")"
            invertedStr = r"("+re.escape(token)+r")((===\w+)){"+re.escape(str(distance))+r"}===("+re.escape(anchor_token)+r")"
            if direction == "after":
                regexClasses &= Q(transcription__regex=regexStr)
            elif direction == "before":
                regexClasses &= Q(transcription__regex=invertedStr)
            else:
                regexClasses &= Q(transcription__regex=regexStr) | Q(transcription__regex=invertedStr)

        #get Sections
        sections = Section.objects.filter(Q(type="sentence")).prefetch_related("tokens").annotate(
            transcription=StringAgg('tokens__transcription', delimiter='===',ordering=('tokens__number_in_sentence'))
        ).filter(regexClasses).distinct()[:20]
        
        results = []
        for candidate in sections:


            tokenList = candidate.transcription.split('===')
            anchor_indecies = get_token_indecies(tokenList, anchor_token)
            query_tokens_indecies = []
            for token in query_tokens:
                query_tokens_indecies += get_token_indecies(tokenList,token)

            for anchor_index in anchor_indecies:
                smallIndex = anchor_index - (distance+1)
                bigIndex = anchor_index + (distance+1)
                if smallIndex < 0 and direction != "after":
                    continue

                if bigIndex >= len(tokenList) and direction != "before":
                    continue
                if smallIndex in query_tokens_indecies or bigIndex in query_tokens_indecies:
                    print(candidate.identifier)
                    result = {
                        "section_id" : candidate.id,
                        "section_identifier" : candidate.identifier,
                        "tokens": candidate.tokens
                    }
                    results.append(result)
                    for i,token in enumerate(tokenList):
                        if smallIndex in query_tokens_indecies and i == smallIndex:
                            print('\033[92m'+token+'\033[0m',end=" ")
                        elif bigIndex in query_tokens_indecies and i == bigIndex:
                            print('\033[92m'+token+'\033[0m',end=" ")
                        elif i == anchor_index:
                            print('\033[4m'+token+'\033[0m',end=" ")
                        else:
                            print(token, end=" ")
        end = time.time()
        print("")
        print("time taken: ", end-start)
        # return results
