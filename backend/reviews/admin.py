from django.contrib import admin
from reviews.models import Answer, Comment, Question


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "product",
        "user",
        "rate",
        "is_approved",
        "is_unanimous",
        "created_at",
    )
    list_filter = (
        "is_approved",
        "is_unanimous",
        "rate",
        "created_at",
    )
    search_fields = ("title", "text", "product__name", "user__username", "user__email")
    list_editable = ("is_approved",)
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("product", "user")

    fieldsets = (
        ("Comment Details", {"fields": ("title", "text", "rate")}),
        ("Relations", {"fields": ("product", "user")}),
        ("Status", {"fields": ("is_approved", "is_unanimous")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    fields = ("text", "is_approved", "user")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("user",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "text_preview",
        "product",
        "user_email",
        "is_approved",
        "is_answered",
        "created_at",
    )
    list_filter = (
        "is_approved",
        "created_at",
    )
    search_fields = ("text", "product__name", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("product", "user")
    inlines = [AnswerInline]

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_preview.short_description = "Question"

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "User Email"

    def is_answered(self, obj):
        return obj.answer.exists()

    is_answered.boolean = True
    is_answered.short_description = "Answered?"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "text_preview",
        "question_preview",
        "user",
        "is_approved",
        "created_at",
    )
    list_filter = ("is_approved", "created_at")
    search_fields = ("text", "question__text", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("question", "user")

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_preview.short_description = "Answer"

    def question_preview(self, obj):
        text = obj.question.text
        return text[:30] + "..." if len(text) > 30 else text

    question_preview.short_description = "Question"
