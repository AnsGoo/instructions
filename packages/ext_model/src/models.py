from typing import Any

from django.db import models


class ModelDefinitionModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='模型名称', null=True, blank=True)
    code = models.CharField(max_length=255, verbose_name='模型类型', null=True, blank=True)
    description = models.CharField(max_length=255, verbose_name='模型描述', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.code + '-' + self.name


class ExtModelManger(models.Manager):
    def create(self, **kwargs):
        self.transform(kwargs)
        return super().create(**kwargs)

    def update(self, **kwargs):
        self.transform(kwargs)
        return super().update(**kwargs)

    def transform(self, data: dict[str, Any]):
        ext_fields = data.pop('ext_fields', [])
        for field in ext_fields:
            attr_name = field.attr_name
            if attr_name in data:
                value = data.pop(attr_name)
                data.setdefault(field.attr_id, value)
        return data


class ExtModel(models.Model):
    objects = ExtModelManger()

    class Meta:
        abstract = True
        verbose_name = '元数据模型'
        verbose_name_plural = '元数据模型'
        abstract = True

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        update_field_list = []
        ext_fields = self.get_ext_field_definitions()
        if update_fields is not None:
            for field_name in update_fields:
                field_def = ext_fields.get(field_name, None)
                if field_def:
                    update_field_list.append(field_def.attr_id)
                else:
                    update_field_list.append(field_name)
        else:
            update_field_list = None

        return super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_field_list,
        )

    __model_id = None
    __attr_definition_cache: dict[str, Any] = {}  # 使用空字典字面量代替dict()

    @classmethod
    def get_ext_prefix(cls):
        """获取扩展字段的前缀"""
        return 'attr'

    @property
    def model_id(self):
        """
        获取模型ID，如果实例已保存则调用实例方法，否则使用类级别的ID
        """
        try:
            if not self.__model_id:
                self.__model_id = self.get_ext_model_id()

            return self.__model_id
        except Exception:
            # 如果出现异常，返回类级别的model_id
            return self.__model_id

    @model_id.setter
    def model_id(self, model_id):
        self.__model_id = model_id
        self.__get_attr_definition_map()

    def get_ext_definition_model(self):
        raise NotImplementedError('子类必须实现get_ext_definition_model方法')

    def __get_attr_definition_map(self):
        """
        获取属性定义映射，用于代理模式
        返回格式: {attr_name: attr_id}
        """
        # 避免循环引用：使用try-except捕获可能的递归错误
        try:
            if len(self.__attr_definition_cache.keys()) == 0:
                # 获取与该模型关联的所有属性定义
                DefinitionModel = self.get_ext_definition_model()
                AttrModel = DefinitionModel.get_child_model()
                attr_definitions = AttrModel.objects.filter(model_id=self.model_id).all()

                for attr_def in attr_definitions:
                    self.__attr_definition_cache.setdefault(
                        attr_def.attr_name,
                        {
                            'attr_name': attr_def.attr_name,
                            'attr_id': attr_def.attr_id,
                            'attr_description': attr_def.attr_description,
                            'attr_label': attr_def.attr_label,
                        },
                    )

            return self.__attr_definition_cache
        except RecursionError:
            # 如果发生递归错误，返回空字典
            return {}

    def get_ext_model_id(self):
        """
        获取模型定义，由子类实现
        """
        raise NotImplementedError('子类必须实现get_ext_model_id方法')

    def get_ext_field_definitions(self):
        """
        获取所有扩展字段的定义元数据
        返回格式: {field_label: {attr_name, attr_id, attr_description}}
        """

        if len(self.__attr_definition_cache.keys()) > 0:
            return self.__attr_definition_cache
        else:
            return self.__get_attr_definition_map()

    def update_ext_fields(self, data: dict[str, Any]):
        """
        更新扩展字段
        """
        definitions = self.get_ext_field_definitions()
        for key, value in data.items():
            if key in definitions:
                field = definitions.get(key)
                setattr(self, field['attr_id'], value)
            else:
                setattr(self, key, value)
        return self


class AttrDefinitionModel(models.Model):
    attr_name = models.CharField(max_length=255, verbose_name='属性名称')
    attr_id = models.CharField(max_length=255, verbose_name='属性ID')
    attr_description = models.CharField(
        max_length=255, verbose_name='属性描述', null=True, blank=True
    )
    attr_label = models.CharField(max_length=255, verbose_name='属性标签')
    model = models.ForeignKey(
        ModelDefinitionModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='模型',
    )

    class Meta:
        abstract = True
        unique_together = ('model', 'attr_id')

    def __str__(self) -> str:
        return f'{self.attr_label}[{self.attr_name}]'

    # 为了确保子类能够正确继承Meta属性，提供一个类方法
    @classmethod
    def get_meta_options(cls):
        """获取Meta选项，便于子类继承"""
        return {
            'unique_together': cls._meta.unique_together,
        }
