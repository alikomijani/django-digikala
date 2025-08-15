from rest_framework import serializers
from .models import Comment, Question, Answer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("user", "is_approved")


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ("user", "is_approved")


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # <- nested answers

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ("user", "is_approved")
