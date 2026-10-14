from django.urls import path
from tags import views

app_name = 'tags'

urlpatterns = [
    path('', views.ManageTagListView, name='manage_tag_list'),
    path('new/', views.ManageTagFormView, name='manage_tag_new'),
    path('<int:tag_id>/edit/', views.ManageTagFormView, name='manage_tag_edit'),
    path('<int:tag_id>/delete/', views.ManageTagDeleteView, name='manage_tag_delete'),
]
