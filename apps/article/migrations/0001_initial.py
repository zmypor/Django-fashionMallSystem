# Generated by Django 4.2.4 on 2024-01-21 11:20

from django.db import migrations, models
import django.db.models.deletion
import tinymce.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fashionMallArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='描述')),
                ('keywords', models.CharField(blank=True, default='', max_length=150, verbose_name='关键词')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='排序')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.fashionMallarticlecategory', verbose_name='父类')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='fashionMallArticleTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='fashionMallArticleContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='描述')),
                ('keywords', models.CharField(blank=True, default='', max_length=150, verbose_name='关键词')),
                ('content', tinymce.fields.TinyMCEField(verbose_name='内容')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '草稿'), (1, '发布')], default=1, verbose_name='状态')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.fashionMallarticlecategory', verbose_name='分类')),
                ('tags', models.ManyToManyField(blank=True, to='article.fashionMallarticletags', verbose_name='标签')),
            ],
            options={
                'verbose_name': '文章内容',
                'verbose_name_plural': '文章内容',
                'ordering': ['-pub_date'],
            },
        ),
    ]
