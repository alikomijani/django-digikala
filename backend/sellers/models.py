from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
# Create your models here.


class Seller(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(_("slug"), unique=True, db_index=True)

    class Meta:
        verbose_name = _("Seller")
        verbose_name_plural = _("Sellers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("seller_detail", kwargs={"slug": self.slug})


class SellerProductPrice(models.Model):
    product = models.ForeignKey(
        "products.Product",
        verbose_name=_("Product"),
        related_name="seller_prices",
        on_delete=models.CASCADE,
    )
    seller = models.ForeignKey(
        "Seller",
        verbose_name=_("Seller"),
        on_delete=models.CASCADE,
        related_name="product_prices",
    )
    price = models.PositiveIntegerField(_("Price"))
    discount = models.PositiveSmallIntegerField(_("Discount"), default=0)
    stock_quantity = models.PositiveIntegerField(_("Stock Quantity"), default=0)
    is_available = models.BooleanField(_("Is Available"), default=True)

    create_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Updated at"), auto_now=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return int(self.price - (self.discount * self.price / 100))
        return self.price

    @property
    def discount_amount(self):
        if self.discount > 0:
            return int(self.discount * self.price / 100)
        return 0

    class Meta:
        verbose_name = _("Seller Product Price")
        verbose_name_plural = _("Seller Product Prices")
        ordering = ["-update_at"]
        indexes = [
            models.Index(fields=["product", "seller", "-update_at"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.seller} - {self.discounted_price}"
