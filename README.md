<div align="center">

![baykeshop](https://www.bayke.shop/static/img/logo.png)

<h1>Django-fashionMallSystem</h1>

</div>

## Project introduction

The Django-fashionMallsystem is a Django-based shopping system, which relies on Django framework system as its backend. This project includes traditional Django Web application using Django and Rest API using Django REST framework (DRF), integrates Django's traditional template system and slightly adopts the front-end and back-end separation architecture.！



## Installation

```python
pip install fashionMall
```

## Congifuration

在项目settings.py中的最后引入

```python
# Congifuration at the time of development
from Django-fashionMallSystem.conf.develop import *

# Or

# Congifuration at the time of deployment
from Django-fashionMallSystem.conf.production import *
```

特别说明：本项目覆盖了默认的admin进行了定制，需要将INSTALLED_APPS配置中默认的admin配置注释掉!

```
INSTALLED_APPS = [
    # 'django.contrib.admin',
]
```

## 项目urls.py中引入url

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # baykeshop的全部url
    path('', include("baykeshop.urls")),
    # 开发时静态文件配置
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
```

## Data migration

```python
python manage.py makemigrations
python manage.py migrate
```

## 初始化必要数据

```python
python manage.py initdata
```

## 部署

部署方式多种多样，本项目作为一个包文件，将不会决定参与到你的部署过程当中，你可以根据你自身项目的需求以及django的官方文档来部署你的项目！

在部署过程中如果采用异步asgi的方式部署，可能会有异步安全类错误 `SynchronousOnlyOperation`，根据django官方文档给的提示和解决方案是在项目的settings.py中配置如下代码即可解决：

```python
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
```


