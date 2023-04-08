from django.urls import path
from .views import *

urlpatterns = [
    path('', AdvertisesListView.as_view(), name = 'ListAdvertise'),
    path('create/', AdvertiseCreateView.as_view(), name = 'CreateAdvertise'),
    path('advertise/<str:id>/', AdvertisePkView.as_view(), name = 'PkAdvertise'),
    path('user_advertise/<str:user_id>/', UserAdvertisesView.as_view(), name = 'UserAdvertise'),
    path('user_advertise/<str:user_id>/<str:ad_id>/', UserAdvertiseDetatilView.as_view(), name = 'UserAdvertiseDetatil'),
    path('payment/<str:pk>', StripeCheckoutView.as_view()),
    path('webhook/', stripe_webhook_view, name='webhook')


]