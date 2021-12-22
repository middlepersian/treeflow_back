from rest_framework import serializers
from .author import AuthorSerializer
from ..models import BibEntry, Author


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class BibEntrySerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True, partial=True, required=False)

    def create(self, validated_data):
        author_data = validated_data.pop('authors')
        title_data = validated_data.pop('title')
        year_data = validated_data.pop('year')

        bibentry_instance, bibentry_created = BibEntry.objects.get_or_create(title=title_data, year=year_data)

        if not bibentry_created:
            logger.error('bibentry does not exist')
            loan_word_instance = BibEntry.objects.create(**validated_data)

        for author in author_data:
            auth, auth_created = Author.objects.get_or_create(**author)

            if not auth_created:
                logger.error('author does not exist')
                bibentry_instance.authors.add(auth)

        return bibentry_instance

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)

        authors_data = validated_data.pop('authors')

        for author in authors_data:
            instance.authors.update(**author)

        instance.save()

        return instance

    class Meta:
        model = BibEntry
        fields = ['authors', 'title', 'year']
