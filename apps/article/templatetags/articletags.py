

from django.template import Library
from fashionMall.apps.article.models import (
    fashionMallArticleCategory, fashionMallArticleContent,
    fashionMallArticleTags
)

register = Library()


@register.inclusion_tag('article/sidebar/category.html', takes_context=True)
def sidebar_category(context):
    """ 文章分类 """
    object = context.get('object')
    category_list = fashionMallArticleCategory.objects.exclude(parent__isnull=False)
    return {
        'category_list': category_list,
        'object': object
    }


@register.inclusion_tag('article/sidebar/archiving.html', takes_context=True)
def sidebar_archiving(context):
    """ 文章归档 """
    dates = fashionMallArticleContent.objects.dates(field_name="add_date", kind="month")
    return {
        'dates':dates,
        'month': context.get('month')
    }


@register.inclusion_tag('article/sidebar/tags.html')
def sidebar_tags():
    """ 标签 """
    return {
        'tags': fashionMallArticleTags.objects.all(),
        'colors': [
            'is-white', 'is-black', 'is-light', 'is-dark', 
            'is-primary', 'is-info', 'is-success', 'is-warning', 'is-danger'
        ],
    }