from rest_framework import serializers

from accounts.models import User
from .models import Comment, Product


class CommentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    text = serializers.CharField()
    rate = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Comment

    def create(self, validated_data):
        return super().create(validated_data)
