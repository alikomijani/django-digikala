from django import forms


class ProductCommentForm(forms.Form):
    user_email = forms.EmailField(required=True)
    title = forms.CharField(max_length=150)
    text = forms.CharField()
    rate = forms.IntegerField(max_value=5, min_value=1)
    product_id = forms.IntegerField()
