from django.contrib import admin
from .models import AttrDefinitionModel


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
