from django.forms import ModelForm

from products import models


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ('name', 'description', 'price', 'available')


class PurchaseForm(ModelForm):
    class Meta:
        model = models.Purchase
        fields = ('buyer', 'product', 'amount')


class RefundForm(ModelForm):
    class Meta:
        model = models.Refund
        fields = ('purchase', 'status')
