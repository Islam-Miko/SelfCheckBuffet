from .models import Pin, UserAdmin
from .exceptions import PhonePass

def create_pin(request_data):
    phone = request_data.get('phone')
    if phone is None:
        raise PhonePass
    pin = phone[4:]
    pins_in_PinModel = Pin.objects.filter(pin=pin).last()
    if pins_in_PinModel:
        request_data['pin'] = phone[3:]
        return request_data
    else:
        request_data['pin'] = phone[4:]
        return request_data



def get_userAdmin(data):
    user_admin = UserAdmin.objects.filter(phone=data['userPhone']).last()
    return user_admin

