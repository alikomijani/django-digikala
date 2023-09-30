
from django import forms

from products.models import Comment


# class ProductCommentForm(forms.Form):
#     user_email = forms.EmailField(
#         required=True, label='ایمیل', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     title = forms.CharField(max_length=150, label='عنوان', widget=forms.TextInput(
#         attrs={'class': 'form-control'}))
#     text = forms.CharField(widget=forms.Textarea(
#         attrs={'class': 'form-control'}), label='متن نظر', )
#     rate = forms.IntegerField(max_value=5, min_value=1, label='امتیاز',
#                               widget=forms.TextInput(attrs={'class': 'form-control'}))
#     product_id = forms.IntegerField(widget=forms.HiddenInput())

#     def clean_product_id(self):
#         product_id = self.cleaned_data['product_id']
#         query = Product.objects.filter(pk=product_id)
#         if not query.exists():
#             raise ValidationError({"password": "the product id is invalid"})
#         return product_id

class ProductCommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user',)
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "text": forms.Textarea(attrs={'class': 'form-control', }),
            "rate": forms.NumberInput(attrs={'class': 'form-control'}),
            "product": forms.HiddenInput(),
        }
        labels = {
            "title": "عنوان",
            "text": "متن",
            "rate":  "امتیاز",
        }

    def save(self, commit: bool = ...):
        return super().save(commit)
