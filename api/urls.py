from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name=""),
    path('autocomplete/', views.autocomplete_view, name='autocomplete'),
]
