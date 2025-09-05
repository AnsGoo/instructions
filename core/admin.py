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
    fields = ('attr_id','attr_name' ,'attr_type', 'attr_label')
    readonly_fields=('attr_id','attr_name', 'attr_type', 'attr_label')

    field_type_map =dict()

    def attr_type(self, obj):
        if len(self.field_type_map.keys()) == 0:
            for field in MetadataModel._meta.get_fields():
                if field.name.startswith('attr'):
                    self.field_type_map[field.name] = f'{field.verbose_name}-{field.db_type(connection)}'
        return self.field_type_map[obj.attr_id]
    
    # 设置自定义字段的verbose_name
    attr_type.short_description = '属性类型'

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

    def get_queryset(self, request):
        # 使用正确的反向关系名称，基于外键字段的related_name设置
        return super().get_queryset(request).prefetch_related('attrdefinitionmodel_model')

@admin.register(AttrDefinitionModel)
class AttrDefinitionModelAdmin(admin.ModelAdmin):
    """属性定义模型的管理界面配置"""
    form = AttrDefinitionModelForm  # 使用自定义表单
    list_display = ('id', 'attr_id','attr_name','attr_label', 'create_time', 'update_time')
    search_fields = ('attr_name', 'attr_id','model__name')
    ordering = ('id',)
    list_per_page = 20

    fieldsets = (
        ('基本信息', {
            'fields': ('attr_name', 'attr_label', 'attr_id','model','attr_description')
        }),
        ('审计信息', {
            'fields': ('create_time', 'update_time','create_user','update_user'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('create_time', 'update_time','create_user','update_user')


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('model')
