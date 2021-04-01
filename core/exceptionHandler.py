from django.http import Http404
from rest_framework.views import exception_handler, set_rollback
from rest_framework.response import Response
from core.exceptions import FormValidationError


def api_exception_handler(exc, context):
    if not isinstance(exc, Http404):
        if hasattr(exc,'default_code') and exc.default_code == 'invalid' and exc.status_code == 400:
            detail_list = []
            for name in exc.detail:
                try:
                    detail_list.append(exc.detail[name][0])
                except:
                    for second_name in exc.detail[name]:
                        detail_list.append(exc.detail[name][second_name][0])
            new_exec = FormValidationError(detail_list)
            response = set_form_error_response(new_exec)
            response.data['code'] = FormValidationError.default_code
        else:
            response = exception_handler(exc, context)
            if response is not None and 'detail' in response.data and 'code' not in response.data:
                response.data['code'] = exc.get_codes()
    else:
        response = exception_handler(exc, context)
    return response


def set_form_error_response(exc):
            headers = {}
            if getattr(exc, 'auth_header', None):
                headers['WWW-Authenticate'] = exc.auth_header
            if getattr(exc, 'wait', None):
                headers['Retry-After'] = '%d' % exc.wait
            data = {'detail': exc.detail}
            set_rollback()
            return Response(data, status=exc.status_code, headers=headers)

