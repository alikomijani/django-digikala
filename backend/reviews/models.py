from django.db import models

from digikala.mixins import TimeStamp
from .validators import validate_rate
from django.utils.translation import gettext as _
from django.conf import settings

# Create your models here.


class Comment(TimeStamp):
    title = models.CharField(_("Title"), max_length=150)
    text = models.TextField(_("Text"))
    product = models.ForeignKey(
        "products.Product",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    rate = models.PositiveSmallIntegerField(_("Rate"), validators=[validate_rate])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    is_approved = models.BooleanField(_("Is Approved?"), default=False)
    is_unanimous = models.BooleanField(
        _("Is Unanimous?"),
        help_text=_("show comment withoud your information"),
        default=False,
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        indexes = [
            models.Index(fields=["product", "is_approved"]),
        ]

    def __str__(self):
        return f"comment on {self.product.name}"


class Question(TimeStamp):
    text = models.TextField(_("Question"))
    product = models.ForeignKey(
        "products.Product",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="questions",
    )
    is_approved = models.BooleanField(_("Is Approved?"), default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="questions",
    )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product", "is_approved"]),
        ]

    def __str__(self):
        return self.text[:50]


class Answer(TimeStamp):
    text = models.TextField(_("Answer"))
    question = models.ForeignKey(
        "Question",
        verbose_name=_("Question"),
        on_delete=models.CASCADE,
        related_name="answer",
    )
    is_approved = models.BooleanField(_("Is Approved?"), default=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="answers",
    )

    def __str__(self):
        return self.text[:50]
