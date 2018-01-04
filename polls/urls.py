from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:thing_id>/', views.detail, name='detail'),
    path('vote/', views.vote, name='vote'),
    path('new/', views.new, name='new'),
    path('thingslist/', views.ThingsListView.as_view(), name='thingslist'),
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
]
