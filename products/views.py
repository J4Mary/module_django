from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from products import models, forms
from users import models as users_models


class Homepage(ListView):
    model = models.Product
    template_name = 'products/base.html'

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id', '')
        amount = int(request.POST.get('amount', ''))
        buyer_id = int(request.POST.get('user_id', ''))
        buyer = users_models.User.objects.get(pk=buyer_id)
        product = models.Product.objects.get(pk=product_id)

        product.available -= amount
        buyer.cash -= amount * product.price
        if product.available < amount:
            return render(request, 'products/no_products.html', {'product': product, 'user': buyer})
        elif buyer.cash < amount * product.price:
            return render(request, 'products/no_money.html', {'product': product, 'user': buyer})
        else:
            purchase = models.Purchase(buyer=buyer, product=product, amount=amount)
            buyer.save()
            product.save()
            purchase.save()
            messages.success(request, "The purchase was made!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NewProductView(CreateView):
    model = models.Product
    form_class = forms.ProductForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductEdit(UpdateView):
    model = models.Product
    form_class = forms.ProductForm
    success_url = reverse_lazy('homepage')


class PurchaseList(ListView):
    model = models.Purchase
    template_name = 'products/purchases_list.html'

    def post(self, request, *args, **kwargs):
        purchase_id = request.POST.get('purchase_id', '')
        purchase = models.Purchase.objects.get(pk=purchase_id)
        if purchase.get_time_diff() <= 180:
            refund = models.Refund(purchase=purchase, status=1)
            refund.save()
            purchase.is_active = False
            purchase.save()
            messages.success(request, "The refund was made!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, 'products/refund_warning.html')


class RefundListView(ListView):
    model = models.Refund

    def post(self, request, *args, **kwargs):
        refund_id = request.POST.get('refund_id')
        refund = models.Refund.objects.get(pk=refund_id)
        action = request.POST.get('action')
        if action == 'approve':
            refund.status = 3
            refund.purchase.buyer.cash += refund.purchase.amount * refund.purchase.product.price
            refund.purchase.product.available += refund.purchase.amount
            refund.purchase.buyer.save()
            refund.purchase.product.save()
        elif action == 'decline':
            refund.status = 2
        refund.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
