from products.models import SellerProductPrice


def get_product_last_price_list(id):
    return SellerProductPrice.objects.raw(
        """select * from products_sellerproductprice 
            where product_id = %(id)s
            group by seller_id
            having Max(update_at)""", {"id": id})
