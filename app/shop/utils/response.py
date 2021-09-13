from django.http import JsonResponse

C_WRONG_FILE = 1
C_WRONG_COMPANY_EMPLOYEE = 2
C_NO_INPUT_FILE = 3
C_UNKNOWN = 4
C_NOT_PROVIDER = 5
C_NOT_CUSTOMER = 6

__error_messages = {
    C_WRONG_FILE: 'wrong file format',
    C_WRONG_COMPANY_EMPLOYEE: 'you must be employee for that company to import data',
    C_NO_INPUT_FILE: 'need file for import',
    C_UNKNOWN: 'Unknown Errors',
    C_NOT_PROVIDER: 'You must be provider for that',
    C_NOT_CUSTOMER: 'You must be customer for that',
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
