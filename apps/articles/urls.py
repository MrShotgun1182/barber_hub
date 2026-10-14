from django.urls import path
from articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView, name='article_list'),
    # از str استفاده می‌شود چون مبدل slug حروف فارسی را قبول نمی‌کند
    path('<str:slug>/', views.ArticleDetailView, name='article_detail'),
]
