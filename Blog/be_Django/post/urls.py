from django.conf.urls import url
from .views import pub, get, getall

urlpatterns = [
    url(r'^pub$', pub),
    url(r'^(\d+)$', get),   # 给get传入一个参数str类型
    url(r'^$', getall)
]
