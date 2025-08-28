from turtle import title
from django.db import models
from django.utils.autoreload import file_changed

# Create your models here.


class Category(BaseModel):
    code=models.CharField(max_length=255, verbose_name='代码')
    name=models.CharField(max_length=255, verbose_name='名称')
    description=models.TextField(verbose_name='描述')
    domai
    class Meta:
        db_table = 'category'   
        verbose_name = '分类'
        verbose_name_plural = '分类'
    
    def __str__(self):
        return self.name + ' - ' + self.code 
    

class Content(MetadataModel):
    class Meta:
        db_table = 'content'
        verbose_name = '内容'
        verbose_name_plural = '内容'
    
    code = models.CharField(max_length=255, verbose_name='代码')
    title = models.CharField(max_length=255, verbose_name='标题')
    md_content = models.TextField(verbose_name='内容')
    origin_content = models.TextField(verbose_name='原始内容')
    file = models.FileField(verbose_name='文件', upload_to='content/', null=True, blank=True)
