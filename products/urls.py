from django.urls import include, path

from products import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('products/new', views.NewProductView.as_view(), name='new_product'),
    path('products/<int:pk>/edit', views.ProductEdit.as_view(), name='product_edit'),
    path('purchases/', views.PurchaseList.as_view(), name='all_purchases'),
    path('refunds/', views.RefundListView.as_view(), name='all_refunds'),
]