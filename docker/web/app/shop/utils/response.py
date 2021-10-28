from django.http import JsonResponse

C_WRONG_FILE = 1
C_WRONG_COMPANY_EMPLOYEE = 2
C_NO_INPUT_FILE = 3
C_UNKNOWN = 4
C_NOT_PROVIDER = 5
C_NOT_CUSTOMER = 6
C_API_EXCEPTION = 7
C_PRICE_WRONG = 8
C_QUANTITY_WRONG = 9
C_USER_NOT_IN_COMPANY = 10
C_QUANTITY_THRESHOLD = 11
C_WRONG_REQUEST = 12
C_METHOD_NOT_ALLOWED = 13

__error_messages = {
    C_WRONG_FILE: 'wrong file format',
    C_WRONG_COMPANY_EMPLOYEE: 'you must be employee for that company to import data',
    C_NO_INPUT_FILE: 'need file for import',
    C_UNKNOWN: 'Unknown Errors',
    C_NOT_PROVIDER: 'You must be provider for that',
    C_NOT_CUSTOMER: 'You must be customer for that',
    C_API_EXCEPTION: 'API fields error',
    C_PRICE_WRONG: 'Price should be positive and above zero',
    C_QUANTITY_WRONG: 'Quantity should be positive and above zero',
    C_USER_NOT_IN_COMPANY: 'User must be part of company',
    C_QUANTITY_THRESHOLD: 'Quantity should be equal or bellow target item',
    C_WRONG_REQUEST: 'Wrong data in request',
    C_METHOD_NOT_ALLOWED: 'Method not allowed here.'
}


def response(status=True, errors=None, data=None):
    if errors:
        status = False
        return JsonResponse({
            'Status': status,
            'Errors': __error_messages[errors],
        })
    else:
        return JsonResponse({
            'Status': status,
            'Data': data
        })


def get_error_message(code=C_UNKNOWN):
    return __error_messages[code]


def get_mail_text_on_order_creation(order_url, order_number, last_name, first_name):
    return f'Уважаемый {last_name} {first_name} !!\n' \
           f'Спасибо за Ваш заказ !!\n' \
           f'Номер оформленного заказа: {order_number}\n' \
           f'Проследить за выполнение заказа можно по ссылке:\n' \
           f'{order_url}', f'Оформлен заказ {order_number}'


def get_mail_text_on_sing_up(user_mail):
    return f'Спасибо за регистрацию на сайте Дипломной работы Нетологии\n' \
           f'Это письмо было автоматически сгенерировано на адрес {user_mail}\n', \
           f'Регистрация на сайте Дипломной работы Нетологии завершена.'
