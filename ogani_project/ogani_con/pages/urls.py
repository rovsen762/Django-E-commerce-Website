from django.urls import path
from . import views
from pages.views import IndexView, ContactView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
