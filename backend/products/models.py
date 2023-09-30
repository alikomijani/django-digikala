
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.conf import settings
from .validators import validate_rate


class Brand(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    en_name = models.CharField(_("English Name"), max_length=150)
    slug = models.SlugField(_("slug"))

    def __str__(self) -> str:
        return self.slug


class MyQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_active=False)


class NoDeleteManager(models.Manager):
    def get_queryset(self):
        return MyQuerySet(self.model, using=self._db)


class Product(models.Model):
    name = models.CharField(_("Persian Name"), max_length=200)
    en_name = models.CharField(_("English Name"), max_length=200)
    description = models.TextField(_("Description"))
    category = models.ForeignKey("Category",
                                 verbose_name=_("Category"),
                                 on_delete=models.RESTRICT
                                 )
    brand = models.ForeignKey("Brand", verbose_name=_("Brand"),
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    sellers = models.ManyToManyField("sellers.Seller",
                                     verbose_name=_("Sellers"),
                                     through='SellerProductPrice')
    is_active = models.BooleanField(_("is active"), default=True)
    objects = NoDeleteManager()
    liked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='liked_products')

    @property
    def default_image(self):
        return self.image_set.filter(is_default=True).first()

    def delete(self, using=None, keep_parents=None):
        self.is_active = False
        self.save()
        return

    @property
    def categories_list(self):
        category_list = []
        current_category = self.category
        while current_category.parent is not None:
            category_list.append(current_category)
            current_category = current_category.parent
        category_list.append(current_category)
        category_list.reverse()
        return category_list

    @property
    def sellers_last_price(self):
        return SellerProductPrice.objects.raw(
            """select * from products_sellerproductprice 
            where product_id = %(id)s
            group by seller_id
            having Max(update_at)""", {"id": self.id})

    @property
    def default_product_seller(self):
        if (self.sellers_last_price):
            return self.sellers_last_price[0]
        return None

    def __str__(self):
        return f"{self.id} {self.name}"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    description = models.TextField(_("Description"))
    icon = models.ImageField(
        _("Icon"), upload_to='category_images', null=True, blank=True)
    image = models.ImageField(
        _("Image"), upload_to='category_images', null=True, blank=True)
    parent = models.ForeignKey("self",
                               verbose_name=_("Parent Category"),
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True
                               )

    @property
    def children(self):
        return self.category_set.all()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.slug


class Comment(models.Model):
    title = models.CharField(_("Title"), max_length=150)
    text = models.TextField(_("Text"))
    product = models.ForeignKey("Product",
                                verbose_name=_("Product"),
                                on_delete=models.CASCADE,
                                )
    rate = models.PositiveSmallIntegerField(
        _("Rate"), validators=[validate_rate])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        null=True,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f'comment on {self.product.name}'

    def to_dict(self):
        return {
            "id": self.id,
            "user": {'id': self.user.id,
                     'first_name': self.user.first_name
                     }if self.user is not None else None,
            "title": self.title,
            "text": self.text,
            "rate": self.rate
        }


class Image(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    alt = models.CharField(_("Alternative Text"), max_length=100)
    product = models.ForeignKey("Product",
                                verbose_name=_("Product"),
                                on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to='products',)
    is_default = models.BooleanField(_("Is default image?"), default=False)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField(_("Question"))
    user_email = models.EmailField(_("Email"), max_length=254)
    product = models.ForeignKey("Product",
                                verbose_name=_("Product"),
                                on_delete=models.CASCADE
                                )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField(_("Answer"))
    question = models.ForeignKey("Question",
                                 verbose_name=_("Question"),
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        return self.text


class ProductOption(models.Model):
    product = models.ForeignKey("Product",
                                verbose_name=_("Product"),
                                on_delete=models.CASCADE,
                                related_name='product_options'
                                )
    name = models.CharField(_("Attribute"), max_length=200)
    value = models.CharField(_("Value"), max_length=200)

    class Meta:
        verbose_name = _("ProductOption")
        verbose_name_plural = _("ProductOptions")

    def __str__(self):
        return f'{self.product.name} {self.name}'


class SellerProductPrice(models.Model):
    product = models.ForeignKey("Product",
                                verbose_name=_("Product"),
                                related_name='seller_prices',
                                on_delete=models.CASCADE
                                )
    seller = models.ForeignKey(
        "sellers.Seller", verbose_name=_("Seller"), on_delete=models.CASCADE)
    price = models.PositiveIntegerField(_("Price"))
    discount = models.PositiveSmallIntegerField(_("Discount"), default=0)
    create_at = models.DateTimeField(
        _("create at"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(
        _("create at"), auto_now=True,)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return int(self.price - (self.discount * self.price / 100))
        return self.price

    class Meta:
        verbose_name = _("Seller Product Price")
        verbose_name_plural = _("Seller Product Prices")
