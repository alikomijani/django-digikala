from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.conf import settings
from sellers.models import SellerProductPrice
from uploads.models import Image


class MyQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_active=False)

    def active(self):
        return self.filter(is_active=True)


class NoDeleteManager(models.Manager):
    def get_queryset(self):
        return MyQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Product(models.Model):
    name = models.CharField(_("Persian Name"), max_length=200, db_index=True)
    en_name = models.CharField(_("English Name"), max_length=200)
    description = models.TextField(_("Description"))
    category = models.ForeignKey(
        "categories.Category",
        verbose_name=_("Category"),
        on_delete=models.RESTRICT,
        related_name="products",
    )
    brand = models.ForeignKey(
        "categories.Brand",
        verbose_name=_("Brand"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    sellers = models.ManyToManyField(
        "sellers.Seller",
        verbose_name=_("Sellers"),
        through="sellers.SellerProductPrice",
        related_name="products",
    )
    is_active = models.BooleanField(_("is active"), default=True)

    objects = NoDeleteManager()

    liked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProductLike",
        related_name="liked_products",
        blank=True,
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["brand", "is_active"]),
        ]

    @property
    def default_image(self):
        """Get the default image for this product"""
        content_type = ContentType.objects.get_for_model(self)
        return Image.objects.filter(
            content_type=content_type, object_id=self.id, is_default=True
        ).first()

    @property
    def all_images(self):
        """Get all images for this product"""
        content_type = ContentType.objects.get_for_model(self)
        return Image.objects.filter(
            content_type=content_type, object_id=self.id
        ).order_by("-is_default", "created_at")

    def delete(self, using=None, keep_parents=None):
        self.is_active = False
        self.save()
        return

    @property
    def categories_list(self):
        """Get category hierarchy for this product"""
        return self.category.get_hierarchy()

    @property
    def category_breadcrumb(self):
        """Get category breadcrumb path"""
        return self.category.get_breadcrumb_path()

    def get_latest_seller_prices(self):
        """Get latest price for each seller using Django ORM"""
        from django.db.models import OuterRef, Subquery

        # Subquery to get the latest update_at for each seller
        latest_prices = (
            SellerProductPrice.objects.filter(product=self, seller=OuterRef("seller"))
            .order_by("-update_at")
            .values("id")[:1]
        )

        # Get the actual SellerProductPrice objects
        return SellerProductPrice.objects.filter(
            id__in=Subquery(latest_prices)
        ).select_related("seller")

    @property
    def sellers_last_price(self):
        """Get latest price for each seller - works across all databases"""
        return self.get_latest_seller_prices()

    def get_latest_seller_prices_alternative(self):
        """Alternative method using window functions (PostgreSQL, MySQL 8.0+, SQLite 3.25+)"""
        from django.db.models import Window, F
        from django.db.models.functions import RowNumber

        return (
            SellerProductPrice.objects.filter(product=self)
            .annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=["seller"],
                    order_by=F("update_at").desc(),
                )
            )
            .filter(row_number=1)
            .select_related("seller")
        )

    def get_latest_seller_prices_raw_sqlite(self):
        """Raw SQL version that works specifically with SQLite"""
        return SellerProductPrice.objects.raw(
            """
            SELECT * FROM products_sellerproductprice p1
            WHERE p1.product_id = %s
            AND p1.update_at = (
                SELECT MAX(p2.update_at) 
                FROM products_sellerproductprice p2 
                WHERE p2.product_id = p1.product_id 
                AND p2.seller_id = p1.seller_id
            )
        """,
            [self.id],
        )

    def get_latest_seller_prices_raw_universal(self):
        """Raw SQL that works across most databases"""
        from django.db import connection

        if "sqlite" in connection.vendor:
            # SQLite version
            query = """
                SELECT * FROM products_sellerproductprice p1
                WHERE p1.product_id = %s
                AND p1.update_at = (
                    SELECT MAX(p2.update_at) 
                    FROM products_sellerproductprice p2 
                    WHERE p2.product_id = p1.product_id 
                    AND p2.seller_id = p1.seller_id
                )
                ORDER BY p1.seller_id
            """
        else:
            # PostgreSQL, MySQL, etc.
            query = """
                SELECT DISTINCT ON (seller_id) *
                FROM products_sellerproductprice
                WHERE product_id = %s
                ORDER BY seller_id, update_at DESC
            """

        return SellerProductPrice.objects.raw(query, [self.id])

    @property
    def default_product_seller(self):
        latest_prices = self.sellers_last_price
        if latest_prices:
            return latest_prices[0]
        return None

    @property
    def min_price(self):
        """Get minimum price among all sellers"""
        latest_prices = self.sellers_last_price
        if latest_prices:
            return min(price.discounted_price for price in latest_prices)
        return None

    @property
    def max_price(self):
        """Get maximum price among all sellers"""
        latest_prices = self.sellers_last_price
        if latest_prices:
            return max(price.discounted_price for price in latest_prices)
        return None

    def __str__(self):
        return f"{self.id} {self.name}"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class ProductLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")
        indexes = [
            models.Index(fields=["product", "user"]),
        ]


class ProductOption(models.Model):
    product = models.ForeignKey(
        "Product",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="product_options",
    )
    attribute = models.ForeignKey(
        "categories.CategoryAttribute", on_delete=models.CASCADE
    )

    value = models.CharField(_("Value"), max_length=200)

    class Meta:
        verbose_name = _("ProductOption")
        verbose_name_plural = _("ProductOptions")
        unique_together = ["product", "attribute"]
        indexes = [
            models.Index(fields=["attribute", "value"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
