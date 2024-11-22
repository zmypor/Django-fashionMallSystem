<div align="center">
<h1>Django-fashionMallSystem</h1>

</div>

## Project introduction

The Django-fashionMallsystem is a Django-based shopping system, which relies on Django framework system as its backend. This project includes traditional Django Web application using Django and Rest API using Django REST framework (DRF), integrates Django's traditional template system and slightly adopts the front-end and back-end separation architecture.



## Installation

```python
pip install fashionMall
```

## Configuration

## Introducing URL into the project's urls.py

Introduce the following statement at the end of the project's urls.py

```python
# Congifuration at the time of development
from Django-fashionMallSystem.conf.develop import *

# Or

# Congifuration at the time of deployment
from Django-fashionMallSystem.conf.production import *
```

Special note: This project has been customized the default admin configuration. It is necessary to comment out the default admin configuration in the INSTALLED_APPS configuration!

```
INSTALLED_APPS = [
    # 'django.contrib.admin',
]
```

## Introducing URL into the project's urls.py

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # fashionMall的全部url
    path('', include("fashionMall.urls")),
    # Static file configuration at the time of development
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
```

## Data migration

```python
python manage.py makemigrations
python manage.py migrate
```

## Initialize necessary data

```python
python manage.py initdata
```

## Deployment

There are various deployment methods, and as a package file, this project will not determine your participation in the deployment process. You can deploy your project according to your own project requirements and Django's official documentation!

If asynchronous ASGI is used for deployment during the deployment process, there may be asynchronous security class errors such as' SynchronousOnlyOperation '. According to the prompts and solutions provided in the official documentation of Django, the following code can be configured in the project's settings. py to solve the problem:

```python
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
```


