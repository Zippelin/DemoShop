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
