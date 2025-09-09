from django.contrib import admin
from ext_model.admin import AttrDefinitionModelAdmin, ModelDefinitionModelAdmin

from .models import ConcreteExtModel, MyAttrDefinitionModel, MyModelDefinitionModel


def get_ext_model(site: admin.AdminSite):
    return ConcreteExtModel


admin.AdminSite.get_ext_model = get_ext_model


@admin.register(ConcreteExtModel)
class ContentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'description')
    list_filter = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('id',)
    actions = ['delete_selected']


@admin.register(MyModelDefinitionModel)
class MyModelDefinitionModelAdmin(ModelDefinitionModelAdmin):
    pass


@admin.register(MyAttrDefinitionModel)
class MyAttrDefinitionModelAdmin(AttrDefinitionModelAdmin):
    pass
