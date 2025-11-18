from rest_framework import serializers
from core.models.comment import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate_comment(self, value):
        if len(value.split()) < 5:
            raise serializers.ValidationError("Comment must have at least 5 words.")
        return value

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must have at least 2 characters.")
        return value