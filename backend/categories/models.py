from django.db import models
from django.utils.translation import gettext_lazy as _

from uploads.models import HasImagesMixin


# ---------- Brand ----------
class Brand(models.Model, HasImagesMixin):
    name = models.CharField(_("Name"), max_length=150)
    en_name = models.CharField(_("English Name"), max_length=150)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name


# ---------- Category Manager & QuerySet ----------
class CategoryQuerySet(models.QuerySet):
    def with_children(self):
        return self.prefetch_related("children")

    def root(self):
        return self.filter(parent__isnull=True)

    def active(self):
        return self.filter(is_active=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def with_children(self):
        return self.get_queryset().with_children()

    def root(self):
        return self.get_queryset().root()

    def active(self):
        return self.get_queryset().active()


# ---------- Category ----------
class Category(models.Model, HasImagesMixin):
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    description = models.TextField(_("Description"), blank=True)
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent Category"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    # --- Hierarchy Helpers ---
    def get_hierarchy(self):
        """List from root to current category"""
        hierarchy = []
        current = self
        while current:
            hierarchy.append(current)
            current = current.parent
        return list(reversed(hierarchy))

    def get_hierarchy_names(self):
        return [c.name for c in self.get_hierarchy()]

    def get_hierarchy_slugs(self):
        return [c.slug for c in self.get_hierarchy()]

    def get_breadcrumb_path(self, separator=" > "):
        return separator.join(self.get_hierarchy_names())

    # --- Recursive Child Fetch ---
    def get_all_children(self):
        """All descendants (active only)"""
        descendants = []

        def collect(node):
            for child in node.children.filter(is_active=True):
                descendants.append(child)
                collect(child)

        collect(self)
        return descendants

    def get_all_children_ids(self):
        return [c.id for c in self.get_all_children()]


class CategoryAttribute(models.Model):
    category = models.ForeignKey(
        "Category",
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        related_name="category_attributes",
    )
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), max_length=50)  # useful for frontend form keys
    data_type = models.CharField(
        max_length=50,
        choices=[
            ("text", "Text"),
            ("number", "Number"),
            ("boolean", "Boolean"),
            ("select", "Select"),
        ],
    )
    is_required = models.BooleanField(default=False)
    options = models.JSONField(blank=True, null=True)  # for select-type attributes

    class Meta:
        unique_together = ["category", "slug"]
