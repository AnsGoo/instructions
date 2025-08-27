from django.db import models

# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True
        db_table = 'base_model'
        ordering = ['id']
        verbose_name = '基础模型'
        verbose_name_plural = '基础模型'
    id = models.AutoField(primary_key=True, verbose_name='ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建用户')
    update_user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='更新用户')
    delete_at = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """恢复已删除的对象"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()
    
    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)
    
    def get_queryset(self):
        # 重写基础查询集
        return super().get_queryset().filter(is_deleted=False)
    def all(self):
        return super().get_queryset()
   
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs).filter(is_deleted=False)
    def exclude(self, *args, **kwargs):
        return super().exclude(*args, **kwargs).filter(is_deleted=False)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs).filter(is_deleted=False)
    def first(self):
        return super().first().filter(is_deleted=False)
    def last(self):
        return super().last().filter(is_deleted=False)
    def count(self):
        return super().count().filter(is_deleted=False)
    def exists(self):
        return super().exists().filter(is_deleted=False)    
    def values(self, *args, **kwargs):
        return super().values(*args, **kwargs).filter(is_deleted=False)
    def values_list(self, *args, **kwargs):
        return super().values_list(*args, **kwargs).filter(is_deleted=False)
    def annotate(self, *args, **kwargs):
        return super().annotate(*args, **kwargs).filter(is_deleted=False)
    def order_by(self, *args, **kwargs):
        return super().order_by(*args, **kwargs).filter(is_deleted=False)
    def distinct(self, *args, **kwargs):
        return super().distinct(*args, **kwargs).filter(is_deleted=False)
    def __str__(self):
        return str(self.id)


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
    attr10 = models.CharField(max_length=255, verbose_name='属性10', null=True, blank=True)     
    attr11 = models.CharField(max_length=255, verbose_name='属性11', null=True, blank=True)
    attr12 = models.CharField(max_length=255, verbose_name='属性12', null=True, blank=True)
    attr13 = models.CharField(max_length=255, verbose_name='属性13', null=True, blank=True)
    attr14 = models.CharField(max_length=255, verbose_name='属性14', null=True, blank=True)
    attr15 = models.CharField(max_length=255, verbose_name='属性15', null=True, blank=True)
    attr16 = models.CharField(max_length=255, verbose_name='属性16', null=True, blank=True)
    attr17 = models.CharField(max_length=255, verbose_name='属性17', null=True, blank=True)
    attr18 = models.CharField(max_length=255, verbose_name='属性18', null=True, blank=True)
    attr19 = models.CharField(max_length=255, verbose_name='属性19', null=True, blank=True)
    attr20 = models.CharField(max_length=255, verbose_name='属性20', null=True, blank=True)
    attr21 = models.CharField(max_length=255, verbose_name='属性21', null=True, blank=True)
    attr22 = models.CharField(max_length=255, verbose_name='属性22', null=True, blank=True)
    attr23 = models.CharField(max_length=255, verbose_name='属性23', null=True, blank=True)
    attr24 = models.CharField(max_length=255, verbose_name='属性24', null=True, blank=True)
    attr25 = models.CharField(max_length=255, verbose_name='属性25', null=True, blank=True)
    attr26 = models.CharField(max_length=255, verbose_name='属性26', null=True, blank=True)
    attr27 = models.CharField(max_length=255, verbose_name='属性27', null=True, blank=True)
    attr28 = models.CharField(max_length=255, verbose_name='属性28', null=True, blank=True)
    attr29 = models.CharField(max_length=255, verbose_name='属性29', null=True, blank=True)
    attr30 = models.CharField(max_length=255, verbose_name='属性30', null=True, blank=True)

    class Meta:
        db_table = 'metadata_model'
        verbose_name = '元数据模型'
        verbose_name_plural = '元数据模型'


class EntityDefine(BaseModel):
    class Meta:
        db_table = 'entity_define'
        verbose_name = '实体定义'
        verbose_name_plural = '实体定义'
    entity_type = models.CharField(max_length=255, verbose_name='实体类型')
    entity_name = models.CharField(max_length=255, verbose_name='实体名称')
    entity_description = models.TextField(verbose_name='实体描述', null=True, blank=True)
    entity_fields = models.JSONField(verbose_name='实体字段', null=True, blank=True)
    entity_type = models.CharField(max_length=255, verbose_name='实体类型')