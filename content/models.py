from turtle import mode
from django.db import models

from core.models import BaseModel, MetadataModel, ModelDefinitionModel

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
    id = models.AutoField(primary_key=True, verbose_name='ID')
    code = models.CharField(max_length=255, verbose_name='编码')
    title = models.CharField(max_length=255, verbose_name='标题')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类', db_constraint=False)
    file = models.CharField(max_length=600, verbose_name='文件')
    abstract = models.TextField(verbose_name='摘要', null=True, blank=True)
    summary = models.TextField(verbose_name='总结', null=True, blank=True)
    keyword = models.CharField(max_length=1000, verbose_name='关键词', null=True, blank=True)
    web_url = models.CharField(max_length=600, verbose_name='链接', null=True, blank=True)
    document_type = models.CharField(max_length=20, verbose_name='文档类型')
    state = models.CharField(max_length=20, verbose_name='状态', choices=[('draft', '草稿'),('published', '已发布'),('archived', '已归档')], default='draft')
    
    class Meta:
        verbose_name = '内容'
        verbose_name_plural = '内容'
    
     
    def __str__(self):
       return self.title