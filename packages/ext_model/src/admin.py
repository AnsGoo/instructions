from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import connection

from .models import AttrDefinitionModel


class AttrDefinitionInline(admin.TabularInline):
    model = AttrDefinitionModel

    def __init__(self, parent_model, admin_site):
        self.model = parent_model.get_child_model()
        super().__init__(parent_model, admin_site)

    extra = 0
    fields = ('attr_id', 'attr_name', 'attr_type', 'attr_label')
    readonly_fields = ('attr_id', 'attr_name', 'attr_type', 'attr_label')

    field_type_map = {}

    def attr_type(self, obj):
        if not hasattr(self.admin_site, 'get_ext_model'):
            raise Exception('AdminSite must implement get_ext_model')
        ext_model = self.admin_site.get_ext_model()
        prefix = ext_model.get_ext_prefix()
        if len(self.field_type_map.keys()) == 0:
            for field in ext_model._meta.get_fields():
                if field.name.startswith(prefix):
                    self.field_type_map[field.name] = (
                        f'{field.verbose_name}-{field.db_type(connection)}'
                    )
        return self.field_type_map[obj.attr_id]

    # 设置自定义字段的verbose_name
    attr_type.short_description = '属性类型'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ModelDefinitionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'description')
    list_filter = ('name', 'code')
    search_fields = ('name', 'code')
    list_display_links = ('name', 'code')
    ordering = ('id',)
    list_per_page = 20
    inlines = [AttrDefinitionInline]
    fieldsets = (('基本信息', {'fields': ('name', 'code', 'description')}),)


class ConflictValidator:
    all_attrname_set: set[str]

    def __init__(self, all_attrname_set: set[str]) -> None:
        super().__init__()
        self.all_attrname_set = all_attrname_set

    def validate(self, value):
        if value in self.all_attrname_set:
            raise ValidationError(message=f'属性{value}已存在', code='attr_conflict')


class UsedAttrValidator:
    exists_attrid_set: set[str]

    def __init__(self, exists_attrid_set: set[str]) -> None:
        super().__init__()
        self.exists_attrid_set = exists_attrid_set

    def validate(self, value):
        if value in self.exists_attrid_set:
            raise ValidationError(message=f'属性{value}已被使用', code='attr_used')


class AttrDefinitionModelAdmin(admin.ModelAdmin):
    """属性定义模型的管理界面配置"""

    list_display = ('id', 'attr_id', 'attr_name', 'attr_label')
    search_fields = ('attr_name', 'attr_id', 'model__name')
    ordering = ('id',)
    list_per_page = 20
    list_display_links = ('attr_name', 'attr_id')

    fieldsets = [
        (
            '基本信息',
            {'fields': ('attr_name', 'attr_label', 'attr_id', 'model', 'attr_description')},
        )
    ]

    def get_ext_attr(self, model_id: str, attr_name_set: set[str], attr_id_set: set[str]):
        exits_attr_queryset = self.model.objects.filter(model_id=model_id).values_list(
            'attr_name', 'attr_id'
        )
        if exits_attr_queryset.exists():
            for attr_name, attr_id in exits_attr_queryset:
                attr_name_set.add(attr_name)
                attr_id_set.add(attr_id)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'attr_id' not in form.base_fields:
            return form
        cur_model_id: str = request.POST.get('model')
        all_attrname_set = set[str]()
        exists_attrid_set = set[str]()
        if cur_model_id:
            self.get_ext_attr(cur_model_id, all_attrname_set, exists_attrid_set)
        if not hasattr(self.admin_site, 'get_ext_model'):
            raise Exception('AdminSite must implement get_ext_model')
        ext_model = self.admin_site.get_ext_model()
        fields = ext_model._meta.get_fields()

        for field in fields:
            all_attrname_set.add(field.name)

        attrname_validator = ConflictValidator(all_attrname_set)
        form.base_fields['attr_name'].validators.append(attrname_validator.validate)
        used_attr_validator = UsedAttrValidator(exists_attrid_set)
        form.base_fields['attr_id'].validators.append(used_attr_validator.validate)

        prefix = ext_model.get_ext_prefix()
        ATTR_TYPE_CHOICES = []
        for field in fields:
            if field.name.startswith(prefix):
                ATTR_TYPE_CHOICES.append(
                    (field.name, f'{field.verbose_name}-{field.db_type(connection)}')
                )
        form.base_fields['attr_id'].widget = forms.Select(
            attrs={'class': 'form-control'}, choices=ATTR_TYPE_CHOICES
        )
        return form

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('model')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('attr_id', 'model')
        return self.readonly_fields
