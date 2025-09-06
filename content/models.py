from enum import unique
from operator import index
from tabnanny import verbose
from turtle import mode
from django.db import models

from core.models import BaseModel, MetadataModel, ModelDefinitionModel, AttrDefinitionModel

# Create your models here.


class Level1Category(BaseModel):
    code = models.CharField(max_length=255, verbose_name='代码', unique=True)
    name = models.CharField(max_length=255, verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    class Meta:
        verbose_name = '一级分类'
        verbose_name_plural = '一级分类'
    
    def __str__(self):
        return self.name + ' - ' + self.code

class Category(BaseModel):

    code = models.CharField(max_length=255, verbose_name='代码', unique=True)
    name = models.CharField(max_length=255, verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    definition = models.OneToOneField(ModelDefinitionModel, on_delete=models.SET_NULL, null=True, verbose_name='定义', db_constraint=False)
    level1 = models.ForeignKey(Level1Category, on_delete=models.SET_NULL, null=True, verbose_name='一级分类', db_constraint=False)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
    
    def __str__(self):
        return self.name + ' - ' + self.code 


class Content(MetadataModel):
    code = models.CharField(max_length=255, verbose_name='编码')
    title = models.CharField(max_length=255, verbose_name='标题')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类', db_constraint=False)
    abstract = models.TextField(verbose_name='摘要', null=True, blank=True)
    summary = models.TextField(verbose_name='总结', null=True, blank=True)
    keyword = models.CharField(max_length=1000, verbose_name='关键词', null=True, blank=True)
    web_url = models.CharField(max_length=600, verbose_name='链接', null=True, blank=True)
    state = models.CharField(max_length=20, verbose_name='状态', choices=[('draft', '草稿'),('published', '已发布'),('archived', '已归档')], default='draft')
    
    class Meta:
        verbose_name = '内容'
        verbose_name_plural = '内容'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['title']),
            models.Index(fields=['category']),
            models.Index(fields=['state']),
        ]
     
    def __str__(self):
       return self.title


    def get_instance_model_id(self):
        """
        获取实例关联的模型定义ID
        """
        if self.category and self.category.definition:
            return self.category.definition_id
        return None
    
class Document(BaseModel):
    name = models.CharField(max_length=255, verbose_name='名称')
    path = models.CharField(max_length=600, verbose_name='路径')
    size = models.IntegerField(verbose_name='大小')
    type = models.CharField(max_length=20, verbose_name='类型')
    order = models.IntegerField(verbose_name='顺序')
    hex = models.CharField(max_length=255, verbose_name='哈希值',unique=True)
    collection = models.ForeignKey(Content, on_delete=models.CASCADE,verbose_name='集合')
    content = models.TextField(verbose_name='内容', null=True, blank=True)
    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档'
        ordering = ('order',)
        unique_together = ('collection', 'hex')
    
    def __str__(self):
        return self.name + ' - ' + self.path