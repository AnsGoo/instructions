from ext_model.models import ExtModel, ModelDefinitionModel
from django.db import models


class ConcreteExtModel(ExtModel):
    """测试用的具体ExtModel子类"""

    name = models.CharField(max_length=255, verbose_name='测试属性1', null=True, blank=True)
    code = models.CharField(max_length=255, verbose_name='测试属性2', null=True, blank=True)
    description = models.CharField(max_length=255, verbose_name='测试属性3', null=True, blank=True)
    attr1 = models.CharField(max_length=255, verbose_name='测试属性1', null=True, blank=True)
    attr2 = models.IntegerField(verbose_name='测试属性2', null=True, blank=True)
    attr3 = models.FloatField(verbose_name='测试属性3', null=True, blank=True)
    attr4 = models.DateField(verbose_name='测试属性4', null=True, blank=True)
    attr5 = models.TextField(verbose_name='测试属性5', null=True, blank=True)
    attr6 = models.JSONField(max_length=255, verbose_name='测试属性6', null=True, blank=True)
    attr7 = models.TimeField(verbose_name='测试属性7', null=True, blank=True)
    attr8 = models.EmailField(max_length=255, verbose_name='测试属性8', null=True, blank=True)
    attr9 = models.URLField(max_length=255, verbose_name='测试属性9', null=True, blank=True)
    attr10 = models.BooleanField(
        max_length=255, verbose_name='测试属性10', null=True, blank=True, default=False
    )
    attr11 = models.BigIntegerField(verbose_name='测试属性11', null=True, blank=True)
    attr12 = models.SmallIntegerField(verbose_name='测试属性12', null=True, blank=True)
    attr13 = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='测试属性13', null=True, blank=True
    )
    attr14 = models.DurationField(verbose_name='测试属性14', null=True, blank=True)
    attr15 = models.DateTimeField(verbose_name='测试属性15', null=True, blank=True)
    attr16 = models.UUIDField(verbose_name='测试属性16', null=True, blank=True)
    definition = models.ForeignKey(
        ModelDefinitionModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='模型定义',
    )

    model_id = None

    def get_instance_model_id(self):
        """实现必要的抽象方法"""
        if self.model_id:
            return self.model_id
        elif self.definition:
            return self.definition.id
        return None
