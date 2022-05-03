from django.urls import path
from .views import MainView, ProductlistView,ProductDetailView

urlpatterns = [
    path('', MainView.as_view()),
    path('/list', ProductlistView.as_view()),
    path('/details/<int:product_id>', ProductDetailView.as_view())
]
