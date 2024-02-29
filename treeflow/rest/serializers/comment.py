from rest_framework import serializers
from treeflow.corpus.models import Comment

#serializer for Comment
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
