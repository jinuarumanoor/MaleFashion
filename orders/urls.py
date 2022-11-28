from django.urls import path
from .import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path("cancel_order/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("return_order/<int:order_id>/", views.return_order, name="return_order"),
    path('orderstatus/<int:id>/', views.order_status, name='orderstatus'),
    path("cod/", views.cod, name="cod"),

]