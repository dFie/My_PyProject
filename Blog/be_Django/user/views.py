from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseBadRequest
import simplejson
from .models import User
from django.conf import settings
import bcrypt
import jwt
import datetime


AUTH_EXPIRE = 8 * 60 * 60  # 8小时过期

def gen_token(user_id):
    """生成token"""
    return jwt.encode({     # 增加时间戳，判断是否重发token或者重新登录
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE  # 要取整
    }, settings.SECRET_KEY, 'HS256').decode()   # 字符串


# 注册函数
def reg(request:HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        # 有任何异常，都返回400，如果保存数据出错，则向外抛出异常
        email = payload['email']
        query = User.objects.filter(email=email)
        if query:
            return HttpResponseBadRequest() # 这里返回实例，这不是异常类

        name = payload['name']
        password = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())

        user = User()
        user.email = email
        user.name = name
        user.password = password

        try:
            user.save()
            return JsonResponse({'token': gen_token(user.id)})  # 如果正常，返回json数据
        except:
            raise   # 没有值代表最近的那个异常
    except Exception as e:  # 有任何异常，都返回
        print(e)
        return HttpResponseBadRequest()  # 这里返回实例，这不是异常类

# 登录
def login(request:HttpRequest):
    payload = simplejson.loads(request.body)    # 获取登录信息数据
    try:
        email = payload['email']
        user = User.objects.filter(email=email).get()   # 返回符合条件的数据

        if bcrypt.checkpw(payload['password'].encode(), user.password.encode()):
            # 验证通过
            token = gen_token(user.id)
            res = JsonResponse({
                'user': {
                        'user_id': user.id,
                        'name': user.name,
                        'email': user.email},
                'token': token
            })
            res.set_cookie('Jwt', token)    # 演示如何 set  cookie
            return res
        else:
            return HttpResponseBadRequest()

    except Exception as e:  # 有任何异常，都返回
        print(e)
        return HttpResponseBadRequest()     # 这里返回实例，这不是异常类

# 认证
def authenticate(view):
    def wrapper(request:HttpRequest):
        # 自定义header jwt
        payload = request.META.get('HTTP_JWT')  # 会被加前缀HTTP_且全大写
        if not payload:   # None没拿到，认证失败
            return HttpResponse(status=401)
        try:    # 解码，同时验证过期时间
            payload = jwt.decode(payload, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            return HttpResponse(status=401)

        try:
            user_id = payload.get('user_id', -1)
            user = User.objects.filter(pk=user_id).get()
            request.user = user # 如果正确，则注入user
        except Exception as e:
            print(e)
            return HttpResponse(status=401)

        ret = view(request) # 调用视图函数
        # 特别注意view调用的时候，里面也有返回异常
        return ret
    return wrapper


