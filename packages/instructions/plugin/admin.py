from django.contrib import admin

from plugin.models import PluginModel

# Register your models here.


@admin.register(PluginModel)
class PluginModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'scope', 'config', 'status', 'version', 'author', 'tags')
    list_filter = ('name', 'code', 'scope', 'status')
    search_fields = ('name', 'code', 'scope', 'status')
    ordering = ('id',)
    actions = ['delete_selected']
    readonly_fields = ('create_time', 'update_time', 'create_user', 'update_user')
    fieldsets = (
        (
            '基本信息',
            {'fields': ('name', 'code', 'scope', 'config', 'status', 'version', 'author', 'tags')},
        ),
        ('审计信息', {'fields': ('create_time', 'update_time', 'create_user', 'update_user')}),
    )
