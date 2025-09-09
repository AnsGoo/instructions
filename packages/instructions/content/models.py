from django.db import models
from ext_model.models import AttrDefinitionModel, ExtModel, ModelDefinitionModel

from instructions.models import BaseModel


class MyExtModel(ExtModel, BaseModel):
    pass


class MyModelDefinitionModel(ModelDefinitionModel, BaseModel):
    class Meta:
        verbose_name = '模型定义'
        verbose_name_plural = '模型定义'

    @classmethod
    def get_child_model(cls):
        return MyAttrDefinitionModel


class MyAttrDefinitionModel(AttrDefinitionModel, BaseModel):
    model = models.ForeignKey(
        MyModelDefinitionModel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='模型',
        db_constraint=False,
    )

    class Meta(AttrDefinitionModel.Meta):
        verbose_name = '属性定义'
        verbose_name_plural = '属性定义'


class Level1Category(BaseModel):
    code = models.CharField(max_length=255, verbose_name='代码', unique=True)
    name = models.CharField(max_length=255, verbose_name='名称')
    description = models.TextField(verbose_name='描述')

    def get_ext_definition_model(self):
        return MyModelDefinitionModel

    class Meta:
        verbose_name = '一级分类'
        verbose_name_plural = '一级分类'

    def __str__(self):
        return self.name + ' - ' + self.code


class Category(BaseModel):
    code = models.CharField(max_length=255, verbose_name='代码', unique=True)
    name = models.CharField(max_length=255, verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    definition = models.OneToOneField(
        MyModelDefinitionModel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='定义',
        db_constraint=False,
    )
    level1 = models.ForeignKey(
        Level1Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='一级分类',
        db_constraint=False,
    )

    def get_ext_definition_model(self):
        return MyModelDefinitionModel

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name + ' - ' + self.code


class Content(ExtModel, BaseModel):
    code = models.CharField(max_length=255, verbose_name='编码')
    title = models.CharField(max_length=255, verbose_name='标题')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name='分类', db_constraint=False
    )
    abstract = models.TextField(verbose_name='摘要', null=True, blank=True)
    summary = models.TextField(verbose_name='总结', null=True, blank=True)
    keyword = models.CharField(max_length=1000, verbose_name='关键词', null=True, blank=True)
    web_url = models.CharField(max_length=600, verbose_name='链接', null=True, blank=True)
    state = models.CharField(
        max_length=20,
        verbose_name='状态',
        choices=[('draft', '草稿'), ('published', '已发布'), ('archived', '已归档')],
        default='draft',
    )
    thumbnail = models.CharField(max_length=600, verbose_name='缩略图', null=True, blank=True)
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

    def get_ext_definition_model(self):
        return MyModelDefinitionModel

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

    def get_ext_model_id(self):
        """
        获取实例关联的模型定义ID
        """
        if self.category and self.category.definition:
            return self.category.definition_id
        return None


class Document(BaseModel):
    CONTENT_TYPE_CHOICES = [('TEXT', 'TEXT'), ('MARKDOWN', 'MD'), ('CSV', 'CSV'), ('JSON', 'JSON')]
    name = models.CharField(max_length=255, verbose_name='名称')
    path = models.CharField(max_length=600, verbose_name='路径')
    size = models.IntegerField(verbose_name='大小')
    mime_type = models.CharField(max_length=20, verbose_name='类型')
    order = models.IntegerField(verbose_name='顺序')
    hex = models.CharField(max_length=255, verbose_name='哈希值', unique=True)
    collection = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='集合')
    content = models.TextField(verbose_name='内容', null=True, blank=True)
    thumbnail = models.CharField(max_length=255, verbose_name='缩略图', null=True, blank=True)
    content_type = models.CharField(
        max_length=20, verbose_name='内容类型', null=True, blank=True, choices=CONTENT_TYPE_CHOICES
    )

    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档'
        ordering = ('order',)
        unique_together = ('collection', 'hex')

    def __str__(self):
        return self.name + ' - ' + self.path
