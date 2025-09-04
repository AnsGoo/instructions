from django.contrib.admin.actions import delete_selected
from django.db import models
from django.utils import timezone
from instructions.settings import AUTH_USER_MODEL


class BaseManger(models.Manager):

    def delete(self):
        return super().update(is_delete=True, delete_at=timezone.now())
    
    def _chain(self):
        return super()._chain().filter(is_delete=False)

    def update(self, **kwargs):
        del kwargs['is_delete']
        return super().update(**kwargs)
        
# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['id']
        verbose_name = '基础模型'
        verbose_name_plural = '基础模型'
    id = models.AutoField(primary_key=True, verbose_name='ID')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建用户', related_name='%(class)s_create')
    update_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='更新用户', related_name='%(class)s_update')
    delete_at = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')

    objects = BaseManger()

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.delete_at = timezone.now()
        self.save()

        
    def __str__(self):
        return str(self.id)



class ModelDefinitionModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name='模型名称', null=True, blank=True)
    code = models.CharField(max_length=255, verbose_name='模型类型', null=True, blank=True)
    description = models.CharField(max_length=255, verbose_name='模型描述', null=True, blank=True)

    class Meta:
        db_table = 'attr_model'
        verbose_name = '模型定义'
        verbose_name_plural = '模型定义'

    def __str__(self):
        return self.code +'-'+ self.name

class MetadataModel(BaseModel):
    attr1 = models.CharField(max_length=255, verbose_name='属性1', null=True, blank=True)
    attr2 = models.CharField(max_length=255, verbose_name='属性2', null=True, blank=True)
    attr3 = models.CharField(max_length=255, verbose_name='属性3', null=True, blank=True)
    attr4 = models.CharField(max_length=255, verbose_name='属性4', null=True, blank=True)
    attr5 = models.CharField(max_length=255, verbose_name='属性5', null=True, blank=True)
    attr6 = models.CharField(max_length=255, verbose_name='属性6', null=True, blank=True)
    attr7 = models.CharField(max_length=255, verbose_name='属性7', null=True, blank=True)
    attr8 = models.CharField(max_length=255, verbose_name='属性8', null=True, blank=True)
    attr9 = models.CharField(max_length=255, verbose_name='属性9', null=True, blank=True)
    attr10 = models.CharField(max_length=6000, verbose_name='属性10', null=True, blank=True)     
    attr11 = models.CharField(max_length=6000, verbose_name='属性11', null=True, blank=True)
    attr12 = models.CharField(max_length=6000, verbose_name='属性12', null=True, blank=True)
    attr13 = models.CharField(max_length=6000, verbose_name='属性13', null=True, blank=True)
    attr14 = models.CharField(max_length=6000, verbose_name='属性14', null=True, blank=True)
    attr15 = models.CharField(max_length=6000, verbose_name='属性15', null=True, blank=True)
    attr16 = models.CharField(max_length=6000, verbose_name='属性16', null=True, blank=True)
    attr17 = models.CharField(max_length=6000, verbose_name='属性17', null=True, blank=True)
    attr18 = models.CharField(max_length=6000, verbose_name='属性18', null=True, blank=True)
    attr19 = models.CharField(verbose_name='属性19', null=True, blank=True)
    attr20 = models.TextField(verbose_name='属性20', null=True, blank=True)
    attr21 = models.TextField(verbose_name='属性21', null=True, blank=True)
    attr22 = models.TextField(verbose_name='属性22', null=True, blank=True)
    attr23 = models.TextField(verbose_name='属性23', null=True, blank=True)
    attr24 = models.TextField(verbose_name='属性24', null=True, blank=True)
    attr25 = models.JSONField(verbose_name='属性25', null=True, blank=True)
    attr26 = models.JSONField(verbose_name='属性26', null=True, blank=True)
    attr27 = models.JSONField(verbose_name='属性27', null=True, blank=True)
    attr28 = models.JSONField(verbose_name='属性28', null=True, blank=True)
    attr29 = models.JSONField(verbose_name='属性29', null=True, blank=True)
    attr30 = models.JSONField(verbose_name='属性30', null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = '元数据模型'
        verbose_name_plural = '元数据模型'


class AttrDefinitionModel(BaseModel):
    class Meta:
        db_table = 'attr_define'
        verbose_name = '属性定义'
        verbose_name_plural = '属性定义'

    attr_choices= [('text', '文本'),('json', 'JSON'),('number', '数字'),('date', '日期'),('time', '时间')]
    attr_type = models.CharField(max_length=255, verbose_name='属性类型',choices=attr_choices, default='text')
    attr_name = models.CharField(max_length=255, verbose_name='属性名称')
    attr_id = models.CharField(max_length=255,verbose_name='属性ID')
    attr_description = models.TextField(verbose_name='属性描述', null=True, blank=True)
    model = models.ForeignKey(ModelDefinitionModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='模型', related_name='%(class)s_model')
    
