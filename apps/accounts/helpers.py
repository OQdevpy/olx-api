import requests
import random
from django.conf import settings
def send_otp_to_phone(number):
    try:
        otp = random.randint(1000, 9999)
        url = f"https://2factor.in/API/V1/{settings.API_KEY}/SMS/{number}/{otp}"
        print(url)
        response = requests.get(url)
        return otp
    except Exception as e:
        print("xato")
        return None