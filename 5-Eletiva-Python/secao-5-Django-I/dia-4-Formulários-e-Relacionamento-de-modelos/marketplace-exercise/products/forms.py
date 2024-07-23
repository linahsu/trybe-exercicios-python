from django import forms
from products.models import Order


class CreateProductForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Nome do produto",
    )
    description = forms.TextInput(label="Descrição do produto")
    price = forms.FloatField(label="Preço R$:")


class CreateSellerForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField()


class CreateBuyerForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField()


class CreateOrderForm(forms.Form):
    class Meta:
        model = Order
        fields = "__all__"
