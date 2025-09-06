from typing import Dict, Any
from django.db import models
from django.utils import timezone
from instructions.settings import AUTH_USER_MODEL


class BaseManger(models.Manager):

    def delete(self):
        return super().update(is_delete=True, delete_at=timezone.now())
    
    def _chain(self):
        return super()._chain().filter(is_delete=False)

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)

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
        return 1

        
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



class MetadataManger(BaseManger):

    def create(self, **kwargs):
        self.transform(kwargs)
        return super().create(**kwargs)

    def update(self, **kwargs):
        self.transform(kwargs)
        return super().update(**kwargs)

    def transform(self, data:Dict[str, Any]):
        ext_fields = data.pop('ext_fields', [])
        for field in ext_fields:
            attr_name = field.attr_name
            if attr_name in data:
                value = data.pop(attr_name)
                data.setdefault(field.attr_id, value)
        return data


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

    objects = MetadataManger()

    class Meta:
        abstract = True
        verbose_name = '元数据模型'
        verbose_name_plural = '元数据模型'
    
    @classmethod
    def get_ext_prefix(cls):
        """获取扩展字段的前缀"""
        return 'attr'


    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        update_field_list = []
        ext_fields = self.get_extended_field_definitions()
        if update_fields is not None:
            for field_name in update_fields:
                field_def = ext_fields.get(field_name, None)
                if field_def:
                    update_field_list.append(field_def.attr_id)
                else:
                    update_field_list.append(field_name)
        else:
            update_field_list = None
                
        return super().save(*args, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_field_list)

    __model_id = None


    __attr_definition_cache:Dict[str, Any] = dict()

    @classmethod
    def set_model_id(model_id):
        self.__model_id = model_id

    @property
    def model_id(self):
        """
        获取模型ID，如果实例已保存则调用实例方法，否则使用类级别的ID
        """
        try:
            if not self.__model_id:
                self.__model_id = self.get_instance_model_id()
            
            return self.__model_id
        except Exception:
            # 如果出现异常，返回类级别的model_id
            return self.__model_id

    @model_id.setter
    def model_id(self, model_id):
        self.__model_id = model_id
        self.__get_attr_definition_map()

        
    def __get_attr_definition_map(self):
        """
        获取属性定义映射，用于代理模式
        返回格式: {attr_name: attr_id}
        """
        # 避免循环引用：使用try-except捕获可能的递归错误
        try:
            
            if len(self.__attr_definition_cache.keys()) == 0:
                # 获取与该模型关联的所有属性定义
                attr_definitions = AttrDefinitionModel.objects.filter(model_id=self.model_id).all()
                for attr_def in attr_definitions:
                    self.__attr_definition_cache.setdefault(attr_def.attr_name, {
                        'attr_name': attr_def.attr_name,
                        'attr_id': attr_def.attr_id,
                        'attr_description': attr_def.attr_description,
                        'attr_label': attr_def.attr_label
                    })
            
            return self.__attr_definition_cache
        except RecursionError:
            # 如果发生递归错误，返回空字典
            return {}
        
    def get_instance_model_id(self):
        """
        获取模型定义，由子类实现
        """
        raise NotImplementedError("子类必须实现get_instance_model_id方法")


    def __getattr__(self,name):
        if self.__attr_definition_cache.get(name) is not None:
            atrr = self.__attr_definition_cache.get(name)['attr_id']
            return self.__getattr__(atrr)
        else:
            return super().__getattr__(name)

    def __setattr__(self, name, value) -> None:
        if self.__attr_definition_cache.get(name) is not None:
            atrr = self.__attr_definition_cache.get(name)['attr_id']
            return self.__setattr__(atrr, value)
        return super().__setattr__(name, value)

    def get_extended_field_definitions(self):
        """
        获取所有扩展字段的定义元数据
        返回格式: {field_label: {attr_name, attr_id, attr_description}}
        """
       
        if len(self.__attr_definition_cache.keys()) > 0:
            return self.__attr_definition_cache
        else:
            return self.__get_attr_definition_map()


class AttrDefinitionModel(BaseModel):
    class Meta:
        db_table = 'attr_define'
        verbose_name = '属性定义'
        verbose_name_plural = '属性定义'
        unique_together = ('model', 'attr_id')

    attr_name = models.CharField(max_length=255, verbose_name='属性名称')
    attr_id = models.CharField(max_length=255,verbose_name='属性ID')
    attr_description = models.CharField(max_length=255, verbose_name='属性描述', null=True, blank=True)
    attr_label = models.CharField(max_length=255, verbose_name='属性标签')
    model = models.ForeignKey(ModelDefinitionModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='模型', related_name='%(class)s_model')
    
    def __str__(self) -> str:
        return f'{self.attr_label}[{self.attr_name}]'