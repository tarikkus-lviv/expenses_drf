"""JSON helper functions"""
import json
from django.http import HttpResponse


def JsonResponse(data=None, message=None, status=200):
    resp = dict()
    if message:
        resp['message'] = message
    if data:
        resp.update(data)
    return HttpResponse(json.dumps(resp, sort_keys=True), status=status,
                        content_type='application/json'
                        )


def JsonError(errors, status=400):
    if type(errors) == type(str()):
        data = {'error': errors}
    else:
        for key, value in errors.items():
            if type(value) == type(list()):
                errors.update({key: value[0]})
        data = errors
    return HttpResponse(json.dumps(data, sort_keys=True), status=status,
                        content_type='application/json')


# For backwards compatibility purposes
JSONResponse = JsonResponse
JSONError = JsonError
