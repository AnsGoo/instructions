from django.contrib import admin
from .models import ConcreteExtModel
from ext_model.register import register_admin

# Register your models here.


@admin.register(ConcreteExtModel)
class ContentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'description')
    list_filter = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('id',)
    actions = ['delete_selected']


def get_ext_model(site: admin.AdminSite):
    return ConcreteExtModel


register_admin(get_ext_model)
