from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from user.views import authenticate
from user.views import User
import simplejson
import datetime
from .models import Post, Content
import math

@authenticate
def pub(request: HttpRequest):
    post = Post()   # 新增
    content = Content() # 新增
    try:
        payload = simplejson.loads(request.body)
        post.title = payload['title']
        post.author = User(id=request.user.id)  # 注入指定id的用户对象
        post.postdate = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8)))

        post.save() # 获得一个post id

        content.content = payload['content']
        content.post = post
        content.save()

        return JsonResponse({'post_id':post.id})
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def get(request: HttpRequest, id):
    try:
        id = int(id)
        post = Post.objects.get(pk=id)
        if post:
            return JsonResponse({
                'post':{
                    'post_id': post.id,
                    'title': post.title,
                    'author': post.author.name,
                    'author_id': post.author_id, # post.author.id
                    'postdate': post.postdate.timestamp(),
                    'content': post.content.content
                }
            })
        # get 方法保证必须只有一条记录，否则抛异常
    except Exception as e:
        print(e)
        return HttpResponseNotFound()

def validate(d:dict, name:str, type_func, default, validate_func):
    try:    # 页码
        result = type_func(d.get(name, default))
        result = validate_func(result, default)
    except:
        result = default
    return result


def getall(request: HttpRequest):
    # 页码
    page = validate(request.GET, 'page', int, 1, lambda x,y: x if x>0 else y)
    # 注意，这个数据不要轻易让浏览器改变，如果允许改变，一定要控制范围
    size = validate(request.GET, 'size', int, 20, lambda x,y: x if x>0 and x<101 else y)


    try:
        # 按id倒排
        start = (page -1) * size
        posts = Post.objects.order_by('-id')
        count = posts.count()
        posts = posts[start:start + size]

        return JsonResponse({
            'posts':[
                {
                    'post_id': post.id,
                    'title': post.title,
                } for post in posts
            ],
            'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages': math.ceil(count / size)
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()






