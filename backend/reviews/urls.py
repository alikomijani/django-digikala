from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"questions", QuestionViewSet, basename="question")
router.register(
    r"answers", AnswerViewSet, basename="answer"
)  # create/update/delete only

urlpatterns = router.urls
