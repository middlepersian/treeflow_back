from re import A
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
        author_data = validated_data.pop('authors', None)
        title_data = validated_data.pop('title')
        year_data = validated_data.pop('year')

        bibentry_instance, bibentry_created = BibEntry.objects.get_or_create(
            title=title_data, year=year_data, **validated_data)

        if author_data:
            for author in author_data:
                auth, auth_created = Author.objects.get_or_create(**author)
                bibentry_instance.authors.add(auth)

        return bibentry_instance

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)

        auths = validated_data.pop('authors')
        logger.error('auths: {} {}'.format(type(auths), auths))

        #auths = instance.authors.update(authors)
        #instance.authors = instance.authors.set(auths)
        '''

        for author in authors:
            if author.get('id', None):
                author_instance, author_created = Author.objects.get_or_create(id=author['id'])
                # the ID exists, so we update the author
                if not author_created:
                    author_instance.name = author.get('name', author_instance.name)
                    author_instance.last_name = author.get('last_name', author_instance.last_name)
                    author_instance.save()
                    instance.authors.add(author_instance)
                else:
                    # the ID does not exist, so we create the author
                    logger.error('author:{}'.format(author))
                    author_instance = Author.objects.create(**author)
                    instance.authors.add(author_instance)
        '''

        instance.save()

        return instance

    class Meta:
        model = BibEntry
        fields = ['id', 'authors', 'title', 'year']
        validators = []
