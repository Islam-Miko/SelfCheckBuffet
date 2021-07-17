from .models import Pin, UserAdmin
from .exceptions import PhonePass, NoInDb

def create_pin(request_data):
    phone = request_data.get('phone')
    if phone is None:
        raise PhonePass
    pin = phone[4:]
    while True:
        pins_in_PinModel = Pin.objects.filter(pin=pin).last()
        # комбинация filter и last применнена для обхода try-except блока
        # filter возвращает queryset(В Pin модели пины уникальны.), а last последний объект.
        # get при не нахождении выбрасывает ошибку DoesNotExist, которую нужно отлавливать
        # и отрабатывать отдельно
        if pins_in_PinModel:
            pin = str(int(pins_in_PinModel.pin)+1).zfill(6)
        else:
            break
    request_data['pin'] = pin
    return request_data




def get_userAdmin(data):
    """Ищет в экземплярах UserAdmin по Номеру и Пину"""
    user_admin = UserAdmin.objects.filter(phone=data['phone'], pin=data['pin']).get()
    return user_admin


def check_in_DB(phone):
    user_admin = UserAdmin.objects.filter(phone=phone).last()
    if not user_admin:
        raise NoInDb





