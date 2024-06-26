from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handle_validation_error,
        "AuthenticationFailed": _handle_authentication_failed,
        "PermissionDenied": _handle_permission_denied,
    }
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_validation_error(exc, context, response):
    response = exception_handler(exc, context)
    errors = as_serializer_error(exc)

    if response is not None:
        response.data = {"status_code": response.status_code, "errors": []}
        make_pretty_error(response.data, errors)
    return response


def _handle_authentication_failed(exc, context, response):
    if response is not None:
        response.data = {
            "status_code": response.status_code,
            "errors": [
                {
                    "error": "authentication_failed",
                    "message": str(exc),
                }
            ],
        }

    return response


def _handle_permission_denied(exc, context, response):
    if response is not None:
        response.data = {"detail": str(exc)}

    return response


def make_pretty_error(data, errors):
    for error in errors:
        if isinstance(errors[error], dict) and len(errors[error]) >= 1:
            for er in errors[error]:
                make_pretty_error(data, {er: errors[error][er]})
        elif isinstance(errors[error], list) and isinstance(errors[error][0], ErrorDetail) and len(errors[error]) == 1:
            data["errors"].append({"error": f"{error}_{errors[error][0].code}", "message": errors[error][0]})
        elif isinstance(errors[error][0], dict) and len(errors[error]) >= 1:
            for er in errors[error]:
                make_pretty_error(data, er)
        else:
            if isinstance(errors[error], list):
                for er in errors[error]:
                    data["errors"].append({"error": f"{error}_{er.code}", "message": er})
            else:
                data["errors"].append({"error": f"{error}_{errors[error].code}", "message": errors[error]})
