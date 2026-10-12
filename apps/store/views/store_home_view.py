from django.shortcuts import render
from store import actions


def StoreHomeView(request):
    """ویوی صفحه اصلی فروشگاه (دسته‌بندی‌ها و محصولات منتشرشده)"""
    category_id = request.GET.get('category')
    search = request.GET.get('search', '').strip()

    # فیلتر دسته‌بندی فقط اگر عدد معتبر ارسال شده باشد اعمال می‌شود
    if category_id and category_id.isdigit():
        category_id = int(category_id)
    else:
        category_id = None

    data = actions.GetStoreCatalogAction(
        category_id=category_id, search=search
    )

    context = {
        'categories': data.get('categories', []),
        'products': data.get('products', []),
        'search': search,
        'selected_category_id': category_id,
    }
    return render(request, 'store/store_home.html', context)
