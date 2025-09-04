from django.contrib import admin

from core.models import AttrDefinitionModel
from .models import Level1Category, Category, Content


@admin.register(Level1Category)
class Level1CategoryAdmin(admin.ModelAdmin):
    """一级分类的管理界面配置"""
    list_display = ('code', 'name', 'description', 'create_time', 'update_time')
    search_fields = ('code', 'name', 'description')
    ordering = ('code',)
    list_per_page = 20

    fieldsets = (
        ('基本信息', {
            'fields': ('code', 'name', 'description')
        }),
        ('元数据', {
            'fields': ('create_time', 'update_time'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('code', 'name', 'create_time', 'update_time')
    
    # 禁止删除一级分类
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """分类的管理界面配置"""
    list_display = ('code', 'name', 'description', 'level1', 'definition', 'create_time', 'update_time')
    list_filter = ('level1',)
    search_fields = ('code', 'name', 'description')
    ordering = ('code',)
    list_per_page = 20
    autocomplete_fields = ('level1', 'definition')

    fieldsets = (
        ('基本信息', {
            'fields': ('code', 'name', 'description')
        }),
        ('关联信息', {
            'fields': ('level1', 'definition')
        }),
        ('审计数据', {
            'fields': ('create_time', 'update_time'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('code', 'name', 'level1', 'create_time', 'update_time')
    attr_feild_map = dict()
    

       
    # 禁止删除分类
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """内容的管理界面配置"""
    list_display = ('id', 'code', 'title', 'category', 'document_type', 'state', 'create_time', 'update_time')
    list_filter = ('category', 'document_type', 'state')
    search_fields = ('code', 'title', 'abstract', 'summary', 'keyword')
    attr_feild_map = dict()
    
    ordering = ('-create_time',)
    list_per_page = 20
    autocomplete_fields = ('category',)

    fieldsets = [
        ('基本信息', {
            'fields': ('code', 'title', 'document_type', 'state')
        }),
        ('关联与文件', {
            'fields': ('category', 'file', 'web_url')
        }),
        ('内容详情', {
            'fields': ('abstract', 'summary', 'keyword')
        }),
        ('元数据', {
            'fields': ('create_time', 'update_time'),
            'classes': ('collapse',),
        }),
    ]
    readonly_fields = ('create_time', 'update_time')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for key, field in form.base_fields.items():
            label = self.attr_feild_map.get(key)
            if label:
                field.label = label
        return form
    
    def get_object(self, request, object_id, from_field=None):
        if len(self.fieldsets) > 4:
            self.fieldsets.pop()
        obj = super().get_object(request, object_id, from_field)
        definition_id = obj.category.definition_id
        attr_set = AttrDefinitionModel.objects.filter(model_id=definition_id)

        ext_fields = []
        for attr in attr_set:
            ext_fields.append(attr.attr_id)
            self.attr_feild_map[attr.attr_id] = f'{attr.attr_name}[{attr.attr_type}]'
        
        self.fieldsets.append(('扩展信息', {
            'fields': ext_fields,
            
        }))

        return obj

    # 自定义状态列的显示
    def get_state_display(self, obj):
        return dict(obj._meta.get_field('state').flatchoices).get(obj.state, obj.state)
    get_state_display.short_description = '状态'