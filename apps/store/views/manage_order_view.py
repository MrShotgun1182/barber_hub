from django.contrib import messages
from django.shortcuts import redirect, render
from store import actions


def _IsManager(request) -> bool:
    """بررسی دسترسی مدیر فروشگاه"""
    return request.user.is_authenticated and (
        request.user.role == 'MANAGER'
        or request.user.is_staff
        or request.user.is_superuser
    )


def ManageOrderListView(request):
    """ویوی لیست سفارش‌های فروشگاه در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    status = request.GET.get('status') or None
    data = actions.GetManageOrdersAction(status=status)

    context = {
        'orders': data.get('orders', []),
        'selected_status': status or '',
        'status_choices': [
            ('', 'همه'),
            ('PENDING_PAYMENT', 'در انتظار پرداخت'),
            ('PLACED', 'ثبت‌شده'),
            ('VIEWED', 'بررسی‌شده'),
            ('READY_FOR_PICKUP', 'آماده تحویل'),
            ('DELIVERED', 'تحویل‌شده'),
            ('CANCELLED', 'لغوشده'),
        ],
    }
    return render(request, 'store/manager/order_list.html', context)


def ManageOrderDetailView(request, order_id: int):
    """ویوی جزئیات سفارش در پنل مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    data = actions.GetOrderByIdAction(order_id)
    if data['status'] == 'error':
        messages.error(request, data['message'])
        return redirect('store:manage_order_list')

    context = {'order': data['order']}
    return render(request, 'store/manager/order_detail.html', context)


def ManageOrderStatusView(request, order_id: int):
    """ویوی تغییر وضعیت سفارش توسط مدیر"""
    if not _IsManager(request):
        return redirect('admin_panel:admin_login')

    if request.method == 'POST':
        new_status = request.POST.get('status', '')
        data = actions.UpdateOrderStatusAction(order_id, new_status)
        if data['status'] == 'success':
            messages.success(request, data['message'])
        else:
            messages.error(request, data['message'])
    return redirect('store:manage_order_detail', order_id=order_id)
