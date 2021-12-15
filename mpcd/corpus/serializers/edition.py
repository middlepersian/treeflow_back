from ..models import Edition, BibEntry, Author, TextSigle, Codex
from rest_framework import serializers
from app_backend.mpcd.corpus.serializers.author import AuthorSerializer
from app_backend.mpcd.corpus.serializers.bibliography import BibEntrySerializer
from app_backend.mpcd.corpus.serializers.sigle import TextSigleSerializer

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class EditionSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(many=True, partial=True)
    references = BibEntrySerializer(many=True, partial=True)
    text_sigle = TextSigleSerializer(partial=True)

    def create(self, validated_data):

        authors_data = validated_data.pop('authors')
        references_data = validated_data.pop('references')
        text_sigle_data = validated_data.pop('text_sigle')

        text_sigle_instance, text_sigle_created = TextSigle.objects.get_or_create(**text_sigle_data)
        edition_instance, edition_created = Edition.objects.get_or_create(**validated_data,text_sigle=text_sigle_instance)

        for author_data in authors_data:
            author_instance, author_created = Author.objects.get_or_create(**author_data)
            edition_instance.authors.add(author_instance)

        for reference in references_data:
            bib_entry_instance, bib_entry_created = BibEntry.objects.get_or_create(**reference)
            edition_instance.references.add(bib_entry_instance)

        return edition_instance

    def update(self, instance, validated_data):    


        text_sigle_data = validated_data.pop('text_sigle')
        text_sigle = instance.text_sigle
        text_sigle.name = text_sigle_data.get('sigle', text_sigle.sigle)
        text_sigle.slug = text_sigle_data.get('genre', text_sigle.genre)
        text_sigle.save()

        authors_data = validated_data.pop('authors')
        references_data = validated_data.pop('references')

        if authors_data:
            logger.error('UPDATE {}'.format(authors_data))
            for author in authors_data:
                instance.authors.get_or_create(**author)
        else:
            for author in authors_data:
                instance.authors.create(**author)
       
        
        if references_data:
            logger.error('UPDATE {}'.format(references_data))
            for reference in references_data:
                instance.references.get_or_create(**reference)
        else:
            for reference in references_data:
                instance.references.create(**reference)    

        instance.save()                     

        return instance


    class Meta:
        model = Edition
        fields = ['id', 'name', 'author', 'references', 'text_sigle', 'description']