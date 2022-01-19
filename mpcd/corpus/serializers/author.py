from ..models import Author
from rest_framework import serializers


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class AuthorListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        authors = [Author(**item) for item in validated_data]
        return Author.objects.bulk_create(authors)

    def update(self, instance, validated_data):

        # Maps for id->instance and id->data item.
        author_mapping = {author.id: author for author in instance}
        data_mapping = {item['id']: item for item in validated_data}

        logger.error('LIST validated_data: {}'.format(validated_data))

        # Perform creations and updates.
        ret = []
        for author_id, data in data_mapping.items():
            author = author_mapping.get(author_id, None)
            if author is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(author, data))

        # Perform deletions.
        for author_id, author in author_mapping.items():
            if author_id not in data_mapping:
                author.delete()

        return ret


class AuthorSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(format='hex')

    def create(self, validated_data):
        logger.error('OBJECT create validated_data: {}'.format(validated_data))
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        logger.error('OBJECT update validated_data: {}'.format(validated_data))
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

    class Meta:
        model = Author
        fields = ['id', 'name', 'last_name']
        list_serializer_class = AuthorListSerializer
        validators = []

    @classmethod
    def many_init(cls, *args, **kwargs):
            # Instantiate the child serializer.
            kwargs['child'] = cls()
            # Instantiate the parent list serializer.
            return AuthorListSerializer(*args, **kwargs)
