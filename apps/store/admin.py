from django.contrib import admin
from store import models as store_models


@admin.register(store_models.CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = store_models.ProductImageModel
    extra = 0


@admin.register(store_models.ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_published', 'is_orderable', 'is_deleted')
    list_filter = ('is_published', 'is_orderable', 'is_deleted', 'category')
    search_fields = ('title',)
    inlines = (ProductImageInline,)


class CartItemInline(admin.TabularInline):
    model = store_models.CartItemModel
    extra = 0


@admin.register(store_models.CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'updated_at')
    search_fields = ('customer__user__username', 'customer__user__phone_number')
    inlines = (CartItemInline,)


class OrderItemInline(admin.TabularInline):
    model = store_models.OrderItemModel
    extra = 0
    readonly_fields = ('product', 'product_title', 'unit_price', 'quantity', 'line_total')


@admin.register(store_models.OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'total_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_number', 'customer__user__username', 'customer__user__phone_number')
    inlines = (OrderItemInline,)


@admin.register(store_models.PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'ref_id', 'created_at', 'verified_at')
    list_filter = ('status', 'gateway')
    search_fields = ('authority', 'ref_id', 'order__order_number')
    # authority و ref_id کلیدهای یکتایی هستند و نباید دستی ویرایش شوند
    readonly_fields = ('authority', 'ref_id', 'gateway_code', 'verified_at')
