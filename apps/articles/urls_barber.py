from django.urls import path
from articles import views

app_name = 'articles_barber'

urlpatterns = [
    path('', views.BarberArticleListView, name='barber_article_list'),
    path('new/', views.BarberArticleFormView, name='barber_article_new'),
    path('<int:article_id>/edit/', views.BarberArticleFormView, name='barber_article_edit'),
    path('<int:article_id>/delete/', views.BarberArticleDeleteView, name='barber_article_delete'),
]
