from .models import Pin, UserAdmin, Food, Operation, OperDetail
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


def get_buyer_by_pin(pin):
    return Pin.objects.filter(pin=pin).get()


def get_total_sum_for_products(products):
    total_sum_buyed_products = 0
    for product in products:
        food = Food.objects.get(id=product['id'])
        total_sum_buyed_products += (food.price * product['amount'])
    return total_sum_buyed_products


def determine_DCOP(total_sum_to_pay, paid_money):
    """computates D-debt_sum, C-change_money,
    determines OP-OPER_STATUS"""
    difference_money_operation = total_sum_to_pay - paid_money
    debt_sum = 0
    change_money = 0
    OPER_STATUS = 'NOTACTIVE'
    if difference_money_operation > 0:
        debt_sum = difference_money_operation
        OPER_STATUS = 'ACTIVE'
    elif difference_money_operation < 0:
        change_money = abs(difference_money_operation)
    return debt_sum, change_money, OPER_STATUS


def take_A_note_to_pin_debt(debt_sum, buyer_by_pin):
    buyer_by_pin.debt += debt_sum
    buyer_by_pin.save()


def make_a_operation(data):

    pin = data.pop('pin')
    status = data.pop('status')
    debt_sum = data.pop('debt_sum')
    total_sum = data.pop('total_sum')
    products = data.pop('product')

    operation = Operation.objects.create(pin=pin,
                                         total_sum=total_sum,
                                         debt_sum=debt_sum,
                                         status=status)
    for product in products:
        food_to_oper_detail = Food.objects.get(id=product['id'])
        oper_detail = OperDetail.objects.create(operation=operation,
                                                food=food_to_oper_detail,
                                                amount=product['amount'])
        oper_detail.save()
    return operation


def change_operation_status(pin_instance, paid_sum):
    """Меняет статус неоплаченных операций на NOTACTIVE-Оплачено(Закрыто) у пина"""
    all_active_operation_by_pin = Operation.objects.filter(pin=pin_instance,
                                                           status="ACTIVE").order_by('add_date').all()
    remain_of_paid_sum = paid_sum
    flag = False
    for active_operation in all_active_operation_by_pin:
        remain_of_paid_sum -= active_operation.debt_sum
        if flag:
            break
        if remain_of_paid_sum < 0:
            active_operation.debt_sum = abs(remain_of_paid_sum)
            active_operation.save()
            flag = True
        elif remain_of_paid_sum >= 0:
            active_operation.debt_sum = 0
            active_operation.status = "NOTACTIVE"
            active_operation.save()
        print(remain_of_paid_sum)


def computate_change(pin_instance, payment):
    """Определяет сдачу и меняет у экземпляра ПИН поле долг"""
    change = pin_instance.debt - payment
    if change < 0:
        pin_instance.debt = 0
        change = abs(change)
        pin_instance.save()
    elif change > 0:
        pin_instance.debt = change
        pin_instance.save()
        change = 0
    else:
        pin_instance.debt = 0
        pin_instance.save()
    return change




