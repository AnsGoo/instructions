from django.contrib import admin
from .models import AttrDefinitionModel, ModelDefinitionModel

class AttrDefinitionInline(admin.TabularInline):
    model = AttrDefinitionModel
    extra = 0
    fields = ('attr_type', 'attr_name', 'attr_id')
    readonly_fields=('attr_type', 'attr_name', 'attr_id')

    def has_add_permission(self, request, obj):
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
    ordering = ('id',)
    list_per_page = 20
    inlines = [AttrDefinitionInline]
    readonly_fields = ('create_time', 'update_time','name','code')


    def has_add_permission(self, request, obj):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AttrDefinitionModel)
class AttrDefinitionModelAdmin(admin.ModelAdmin):
    """属性定义模型的管理界面配置"""
    list_display = ('id', 'attr_type', 'attr_name', 'attr_id', 'create_time', 'update_time')
    list_filter = ('attr_type',)
    search_fields = ('attr_name', 'attr_id')
    ordering = ('id',)
    list_per_page = 20

    fieldsets = (
        ('基本信息', {
            'fields': ('attr_type', 'attr_name', 'attr_id')
        }),
        ('元数据', {
            'fields': ('create_time', 'update_time'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('create_time', 'update_time')
