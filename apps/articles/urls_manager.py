from django.urls import path
from articles import views

app_name = 'articles_manager'

urlpatterns = [
    path('', views.ManageArticleListView, name='manage_article_list'),
    path('new/', views.ManageArticleFormView, name='manage_article_new'),
    path('<int:article_id>/edit/', views.ManageArticleFormView, name='manage_article_edit'),
    path('<int:article_id>/delete/', views.ManageArticleDeleteView, name='manage_article_delete'),
    path('<int:article_id>/moderate/', views.ModerateArticleView, name='moderate_article'),
    path('<int:article_id>/featured/', views.ManageArticleFeaturedToggleView, name='toggle_article_featured'),
]
