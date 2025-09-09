from typing import Any

# 使用Django的标准方式获取AUTH_USER_MODEL
from django.conf import settings
from django.db import models
from django.utils import timezone

AUTH_USER_MODEL = settings.AUTH_USER_MODEL


class BaseManger(models.Manager):
    def delete(self):
        return super().update(is_delete=True, delete_at=timezone.now())

    def _chain(self):
        return super()._chain().filter(is_delete=False)

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)

    def update(self, **kwargs):
        if 'is_delete' in kwargs:
            del kwargs['is_delete']
        if 'delete_at' in kwargs:
            del kwargs['delete_at']
        return super().update(**kwargs)

    def all(self):
        return super().all().filter(is_delete=False)


# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    create_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name='创建时间'
    )
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='更新时间'
    )
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='创建用户',
        related_name='%(class)s_create',
    )
    update_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='更新用户',
        related_name='%(class)s_update',
    )
    delete_at = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')

    objects = BaseManger()

    class Meta:
        abstract = True
        ordering = ['id']
        verbose_name = '基础模型'
        verbose_name_plural = '基础模型'

    def __str__(self):
        return str(self.id)

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.delete_at = timezone.now()
        self.save()
        return 1


class BaseManger(models.Manager):
    def delete(self):
        return super().update(is_delete=True, delete_at=timezone.now())

    def _chain(self):
        return super()._chain().filter(is_delete=False)

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)

    def update(self, **kwargs):
        if 'is_delete' in kwargs:
            del kwargs['is_delete']
        if 'delete_at' in kwargs:
            del kwargs['delete_at']
        return super().update(**kwargs)

    def all(self):
        return super().all().filter(is_delete=False)
