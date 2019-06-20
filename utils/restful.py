from django.http import JsonResponse

class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500

def result(code=HttpCode.ok,message="",data=None,kwargs=None):
    json_dict = {"code":code,"message":message,"data":data}
    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)

def ok():
    return result()

def params_error(message="",data=None):
    return result(HttpCode.paramserror,message,data)

def unauth(message="",data=None):
    return result(HttpCode.unauth,message,data)

def method_error(message="",data=None):
    return result(HttpCode.methoderror,message,data)

def server_error(message="",data=None):
    return result(HttpCode.servererror,message,data)