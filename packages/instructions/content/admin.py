from dataclasses import field

from django.contrib import admin
from ext_model.admin import AttrDefinitionModelAdmin, ModelDefinitionModelAdmin

from .models import (
    Category,
    Content,
    Document,
    Level1Category,
    MyAttrDefinitionModel,
    MyModelDefinitionModel,
)


def get_ext_model(site: admin.AdminSite):
    return Content


admin.AdminSite.get_ext_model = get_ext_model


@admin.register(Level1Category)
class Level1CategoryAdmin(admin.ModelAdmin):
    """一级分类的管理界面配置"""

    list_display = ('code', 'name', 'description', 'create_time', 'update_time')
    search_fields = ('code', 'name', 'description')
    ordering = ('code',)
    list_per_page = 20
    list_display_links = ('code', 'name')

    fieldsets = (
        ('基本信息', {'fields': ('code', 'name', 'description')}),
        (
            '元数据',
            {
                'fields': ('create_time', 'update_time'),
                'classes': ('collapse',),
            },
        ),
    )
    readonly_fields = ('code', 'name', 'create_time', 'update_time')

    # 禁止删除一级分类
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """分类的管理界面配置"""

    list_display = ('code', 'name', 'description', 'level1')
    list_filter = ('level1',)
    list_display_links = ('code', 'name')
    search_fields = ('code', 'name', 'description')
    ordering = ('code',)
    list_per_page = 20
    autocomplete_fields = ('level1', 'definition')

    fieldsets = (
        ('基本信息', {'fields': ('code', 'name', 'description')}),
        ('关联信息', {'fields': ('level1', 'definition')}),
        (
            '审计数据',
            {
                'fields': ('create_time', 'update_time'),
                'classes': ('collapse',),
            },
        ),
    )
    readonly_fields = ('code', 'name', 'level1', 'create_time', 'update_time')
    attr_feild_map = {}

    # 禁止删除分类
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """内容的管理界面配置"""

    list_display = ('id', 'code', 'title', 'category', 'state', 'create_time', 'update_time')
    list_filter = ('category', 'state')
    search_fields = ('code', 'title', 'abstract', 'summary', 'keyword')
    attr_feild_map = {}
    list_display_links = ('code', 'title')

    ordering = ('-create_time',)
    list_per_page = 20
    autocomplete_fields = ('category',)

    fieldsets = [
        ('基本信息', {'fields': ('code', 'title', 'state')}),
        ('关联与文件', {'fields': ('category', 'web_url')}),
        (
            '内容详情',
            {
                'fields': ('abstract', 'summary', 'keyword'),
                'classes': ('collapse',),
            },
        ),
        (
            '审计信息',
            {
                'fields': ('create_time', 'update_time', 'create_user', 'update_user'),
                'classes': ('collapse',),
            },
        ),
    ]
    readonly_fields = ('create_time', 'update_time', 'create_user', 'update_user')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for key, field in form.base_fields.items():
            label = self.attr_feild_map.get(key)
            if label:
                field.label = label
        return form

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        definition_id = obj.category.definition_id
        attr_set = MyAttrDefinitionModel.objects.filter(model_id=definition_id)

        ext_fields = []
        for attr in attr_set:
            ext_fields.append(attr.attr_id)
            self.attr_feild_map[attr.attr_id] = f'{attr.attr_label}[{attr.attr_name}]'

        for key, value in self.fieldsets:
            print(key)
            if key == '扩展信息':
                self.fieldsets.remove(value)

        self.fieldsets.append(
            (
                '扩展信息',
                {
                    'fields': ext_fields,
                },
            )
        )
        return obj

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user
        return super().save_model(request, obj, form, change)

    # 自定义状态列的显示
    def get_state_display(self, obj):
        return dict(obj._meta.get_field('state').flatchoices).get(obj.state, obj.state)

    get_state_display.short_description = '状态'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """文档的管理界面配置"""

    list_display = ('id', 'name', 'path', 'mime_type', 'size', 'collection', 'order', 'create_time')
    list_filter = ('mime_type', 'collection')
    search_fields = ('name', 'path', 'hex', 'content')
    ordering = ('collection', 'order')
    list_per_page = 20
    autocomplete_fields = ('collection',)

    fieldsets = [
        ('基本信息', {'fields': ('name', 'path', 'mime_type', 'size', 'order', 'hex')}),
        ('关联信息', {'fields': ('collection',)}),
        (
            '内容信息',
            {
                'fields': ('content',),
                'classes': ('collapse',),
            },
        ),
        (
            '审计信息',
            {
                'fields': ('create_time', 'update_time', 'create_user', 'update_user'),
                'classes': ('collapse',),
            },
        ),
    ]
    readonly_fields = ('create_time', 'update_time', 'create_user', 'update_user')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('category ')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(MyModelDefinitionModel)
class MyModelDefinitionModelAdmin(ModelDefinitionModelAdmin):
    def get_list_display(self, request):
        return ('id', 'name', 'code', 'update_user', 'create_time', 'update_time')

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets + (
                (
                    '审计信息',
                    {
                        'fields': ('create_time', 'update_time', 'create_user', 'update_user'),
                        'classes': ('collapse',),
                    },
                ),
            )
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                'name',
                'code',
                'create_time',
                'update_time',
                'create_user',
                'update_user',
            )
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('update_user')


@admin.register(MyAttrDefinitionModel)
class MyAttrDefinitionModelAdmin(AttrDefinitionModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user
        return super().save_model(request, obj, form, change)
