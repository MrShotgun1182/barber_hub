from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('admin_panel/', include('admin_panel.urls')),
    path('barber/', include('barbers.urls')),
    path('booking/', include('booking.urls')),
    path('store/', include('store.urls')),
    path('articles/', include('articles.urls')),
    path('barber/articles/', include('articles.urls_barber')),
    path('admin_panel/articles/', include('articles.urls_manager')),
    path('admin_panel/tags/', include('tags.urls')),
    path('', TemplateView.as_view(template_name='core/landing.html'), name='landing'),
]

# ۱. سرو کردن فایل‌های آپلودی (تصاویر محصولات) فقط در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)