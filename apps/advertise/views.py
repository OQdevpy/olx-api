from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from .models import *
from .serializers import *
from django.db.models import Q
from django.db.models.functions import Now
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# from apps.accounts.UserPermission import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django.conf import settings
# import stripe
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()
# stripe.api_key = settings.STRIPE_SECRET_KEY

class AdvertisesListView(APIView):
    def get(self, request):
        advertises = Advertise.objects.filter(Q (expiration_date__gt = Now())).order_by('-is_active').values()
        serializer = AdvertiseSerializer(advertises, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class AdvertiseCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AdvertiseSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            print(user)
            serializer.save(owner = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdvertisePkView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, id):
        try:
            return Advertise.objects.get(id=id)
        except Advertise.DoesNotExist:
            return Http404

    def get(self, request, id):
        obj = self.get_object(id)
        serializer = AdvertiseSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        obj = self.get_object(id)
        serializer = AdvertiseSerializer(obj, data=request.data)
        if request.user == obj.owner:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request, id):
        obj = self.get_object(id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAdvertisesView(APIView):
    
    def get(self, request, user_id):
        user = User.objects.get(pk = user_id)
        user_advertises = Advertise.objects.all().filter(owner = user)
        serializer = AdvertiseSerializer(user_advertises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAdvertiseDetatilView(APIView):
    def get(self, request, user_id, ad_id):
        user = User.objects.get(pk = user_id)
        user_advertises = Advertise.objects.all().filter(owner = user).filter(id = ad_id)
        serializer = AdvertiseSerializer(user_advertises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StripeCheckoutView(APIView):
    def post(self, request, *args, **kwargs):
        adv_id = self.kwargs["pk"]
        adv = Advertise.objects.get(id = adv_id)
        try:
            adv = Advertise.objects.get(id = adv_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency':'usd',
                             'unit_amount': 50 * 100,
                             'product_data':{
                                 'name':adv.description,

                             }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "product_id":adv.id
                },
                mode='payment',
                success_url=settings.SITE_URL + '?success=true',
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_SECRET_WEBHOOK)
    
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        adv_id = session['metadata']['product_id']
        adv = Advertise.objects.get(id=adv_id)
        adv.is_active = True
        adv.expiration_date = date.today() + timedelta(days=62)
        adv.save()

    return Response(status=200)