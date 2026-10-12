from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    # فروشگاه مشتری
    path('', views.StoreHomeView, name='store_home'),
    path('product/<int:product_id>/', views.ProductDetailView, name='product_detail'),
    path('cart/', views.CartView, name='cart'),
    path('cart/add/', views.AddToCartView, name='add_to_cart'),
    path('cart/item/<int:item_id>/update/', views.UpdateCartItemView, name='update_cart_item'),
    path('cart/item/<int:item_id>/remove/', views.RemoveCartItemView, name='remove_cart_item'),
    path('checkout/', views.CheckoutView, name='checkout'),
    path('checkout/submit/', views.SubmitCheckoutView, name='submit_checkout'),
    path('payment/callback/', views.PaymentCallbackView, name='payment_callback'),
    path('payment/result/<int:order_id>/', views.PaymentResultView, name='payment_result'),
    path('orders/', views.OrderHistoryView, name='order_history'),
    path('orders/<int:order_id>/', views.OrderDetailView, name='order_detail'),
    path('orders/<int:order_id>/retry-payment/', views.RetryPaymentView, name='retry_payment'),

    # پنل مدیریت فروشگاه
    path('manage/categories/', views.ManageCategoryListView, name='manage_category_list'),
    path('manage/categories/new/', views.ManageCategoryFormView, name='manage_category_new'),
    path('manage/categories/<int:category_id>/edit/', views.ManageCategoryFormView, name='manage_category_edit'),
    path('manage/categories/<int:category_id>/delete/', views.ManageCategoryDeleteView, name='manage_category_delete'),
    path('manage/products/', views.ManageProductListView, name='manage_product_list'),
    path('manage/products/new/', views.ManageProductFormView, name='manage_product_new'),
    path('manage/products/<int:product_id>/edit/', views.ManageProductFormView, name='manage_product_edit'),
    path('manage/products/<int:product_id>/delete/', views.ManageProductDeleteView, name='manage_product_delete'),
    path('manage/products/<int:product_id>/toggle/', views.ManageProductToggleView, name='manage_product_toggle'),
    path('manage/orders/', views.ManageOrderListView, name='manage_order_list'),
    path('manage/orders/<int:order_id>/', views.ManageOrderDetailView, name='manage_order_detail'),
    path('manage/orders/<int:order_id>/status/', views.ManageOrderStatusView, name='manage_order_status'),
]
