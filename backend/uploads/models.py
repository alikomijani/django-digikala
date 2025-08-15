from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class HasImagesMixin:
    """Mixin to attach images via GenericForeignKey"""

    @property
    def default_image(self):
        content_type = ContentType.objects.get_for_model(self)
        return Image.objects.filter(
            content_type=content_type, object_id=self.id, is_default=True
        ).first()

    @property
    def all_images(self):
        content_type = ContentType.objects.get_for_model(self)
        return Image.objects.filter(content_type=content_type, object_id=self.id)


class Image(models.Model):
    """Generic image model that can be used by any model"""

    alt = models.CharField(_("Alternative Text"), max_length=100)
    image = models.ImageField(_("Image"), upload_to="images/")
    is_default = models.BooleanField(_("Is default image?"), default=False)

    # Generic foreign key to associate with any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.alt} - {self.content_object}"
