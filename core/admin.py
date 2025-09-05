from django.contrib import admin
from django import forms

from .models import MetadataModel
from .models import AttrDefinitionModel, ModelDefinitionModel
from django.db import connection
# 创建自定义表单，将attr_id字段的组件类型改为Select组件
class AttrDefinitionModelForm(forms.ModelForm):
    fields = MetadataModel._meta.get_fields()
    ATTR_TYPE_CHOICES = []
    # 定义attr1-attr30的选项
    for field in fields:
        if field.name.startswith('attr'):
            ATTR_TYPE_CHOICES.append((field.name, f'{field.verbose_name}-{field.db_type(connection)}'))
    
    # 将attr_id字段设置为Select组件
    attr_id = forms.ChoiceField(
        choices=ATTR_TYPE_CHOICES,
        required=True,
        label='属性ID',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = AttrDefinitionModel
        fields = '__all__'

class AttrDefinitionInline(admin.TabularInline):
    model = AttrDefinitionModel
    extra = 0
    fields = ('attr_type', 'attr_name', 'attr_id')
    readonly_fields=('attr_type', 'attr_name', 'attr_id')

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ModelDefinitionModel)
class ModelDefinitonModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'description')
    list_filter = ('name', 'code')
    search_fields = ('name', 'code')
    fields = ('name', 'code', 'description')
    list_display_links = ( 'name', 'code')
    ordering = ('id',)
    list_per_page = 20
    inlines = [AttrDefinitionInline]
    readonly_fields = ('create_time', 'update_time','name','code')


    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AttrDefinitionModel)
class AttrDefinitionModelAdmin(admin.ModelAdmin):
    """属性定义模型的管理界面配置"""
    form = AttrDefinitionModelForm  # 使用自定义表单
    list_display = ('id', 'attr_type', 'attr_name', 'attr_id', 'create_time', 'update_time')
    list_filter = ('attr_type',)
    search_fields = ('attr_name', 'attr_id')
    ordering = ('id',)
    list_per_page = 20

    fieldsets = (
        ('基本信息', {
            'fields': ('attr_type', 'attr_name', 'attr_id','model','attr_description')
        }),
        ('元数据', {
            'fields': ('create_time', 'update_time'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('create_time', 'update_time')
