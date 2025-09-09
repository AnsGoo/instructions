from django.db import models

from instructions.models import BaseModel


class PluginModel(BaseModel):
    SCOPE_CHOICES = [
        ('STORE', 'STORE'),
        ('PARSING', 'PARSING'),
    ]
    name = models.CharField(max_length=255, verbose_name='插件名称')
    description = models.TextField(verbose_name='插件描述')
    code = models.CharField(verbose_name='插件编码', max_length=255)
    scope = models.CharField(max_length=20, verbose_name='插件作用域', choices=SCOPE_CHOICES)
    config = models.JSONField(verbose_name='插件配置')
    status = models.CharField(max_length=20, verbose_name='插件状态', default='active')
    version = models.CharField(max_length=20, verbose_name='插件版本')
    author = models.CharField(max_length=255, verbose_name='插件作者')
    tags = models.CharField(
        max_length=1000, verbose_name='插件标签', default='', help_text='逗号分隔'
    )

    class Meta:
        db_table = 'plugin'
        verbose_name = '插件'
        verbose_name_plural = '插件'
        unique_together = ('code', 'version')
