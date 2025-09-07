from django.contrib import admin
from django import forms

from .models import AttrDefinitionModel
from django.db import connection
from django.core.exceptions import ValidationError

class AttrDefinitionInline(admin.TabularInline):
    model = AttrDefinitionModel
    extra = 0
    fields = ('attr_id','attr_name' ,'attr_type', 'attr_label')
    readonly_fields=('attr_id','attr_name', 'attr_type', 'attr_label')

    field_type_map = dict()

    def attr_type(self, obj):
        ext_model = self.admin_site.get_ext_model()
        prefix = ext_model.get_ext_prefix()
        if len(self.field_type_map.keys()) == 0:
            for field in ext_model._meta.get_fields():
                if field.name.startswith(prefix):
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


# @admin.register(ModelDefinitionModel)
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

# @admin.register(AttrDefinitionModel)
class AttrDefinitionModelAdmin(admin.ModelAdmin):
    """属性定义模型的管理界面配置"""
    list_display = ('id', 'attr_id','attr_name','attr_label', 'create_time', 'update_time')
    search_fields = ('attr_name', 'attr_id','model__name')
    ordering = ('id',)
    list_per_page = 20
    list_display_links=('attr_name','attr_id')

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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'attr_id' not in form.base_fields:
            return form
        cur_model_id = request.POST.get('model')
        all_attrname_set = set()
        exists_attrid_set = set()
        if cur_model_id:
            exits_attr_queryset = self.model.objects.filter(model_id=cur_model_id).values_list('attr_name','attr_id')
            if exits_attr_queryset.exists():
                for attr_name, attr_id in exits_attr_queryset:
                    all_attrname_set.add(attr_name)
                    exists_attrid_set.add(attr_id)
        ext_model = self.admin_site.get_ext_model()
        fields = ext_model._meta.get_fields()

        for field in fields:
            all_attrname_set.add(field.name)

        def ConflictValidator(value):
            if value in all_attrname_set:
                raise ValidationError(message=f'属性{value}已存在', code='attr_conflict')

        def UsedAttrValidator(value):
            if value in exists_attrid_set:
                raise ValidationError(message=f'属性{value}已被使用', code='attr_used')
            return value
        
        form.base_fields['attr_name'].validators.append(ConflictValidator)
        form.base_fields['attr_id'].validators.append(UsedAttrValidator)

        prefix = ext_model.get_ext_prefix()
        ATTR_TYPE_CHOICES = []
        print(form.base_fields['attr_id'])
        for field in fields:
            if field.name.startswith(prefix):
                ATTR_TYPE_CHOICES.append((field.name, f'{field.verbose_name}-{field.db_type(connection)}'))
        form.base_fields['attr_id'].widget= forms.Select(attrs={'class': 'form-control'}, choices=ATTR_TYPE_CHOICES)
        return form

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('model')


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('attr_id','model')
        return self.readonly_fields
