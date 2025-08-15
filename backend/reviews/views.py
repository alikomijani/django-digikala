from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Question, Answer
from .serializers import CommentSerializer, QuestionSerializer, AnswerSerializer
from digikala.paginators import BasePaginatedViewSet


class CommentViewSet(BasePaginatedViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.all().order_by("-created_at")
        return Comment.objects.filter(is_approved=True).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionViewSet(BasePaginatedViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Question.objects.all().order_by("-created_at")
        return Question.objects.filter(is_approved=True).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Used only for create/update/delete.
    Read happens via QuestionSerializer.nested answers.
    """

    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
