from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout,authenticate,get_user_model
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.http import JsonResponse,HttpResponse
from utils import restful
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.core.cache import cache


User = get_user_model()

@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)

                return restful.ok()
            else:
                return restful.unauth("No entry")
        else:
            return restful.params_error("Params wrong")
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

def image_captcha(request):
    text, image = Captcha.gene_code()
    #流的形式返回
    out = BytesIO()
    image.save(out,'png')
    #将文件指针移动到最开始位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()

    #字典型
    cache.set(text.lower(),text.lower(),5*60);

    return response

@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.params_error(message=form.get_errors())


