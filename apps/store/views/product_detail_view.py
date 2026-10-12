from django.shortcuts import render
from store import actions


def ProductDetailView(request, product_id: int):
    """ویوی صفحه جزئیات محصول"""
    data = actions.GetProductDetailAction(product_id)

    if data['status'] == 'error':
        context = {'error_message': data['message']}
        return render(request, 'store/product_not_found.html', context, status=404)

    context = {'product': data['product']}
    return render(request, 'store/product_detail.html', context)
