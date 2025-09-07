from django.contrib import admin

from core.admin import AttrDefinitionModelAdmin, ModelDefinitonModelAdmin
from core.models import AttrDefinitionModel, ModelDefinitionModel


def register_admin(get_ext_model):
    def get_my_ext_model(self):
        return get_ext_model(self)

    admin.AdminSite.get_ext_model = get_my_ext_model
    admin.site.register(AttrDefinitionModel, AttrDefinitionModelAdmin)
    admin.site.register(ModelDefinitionModel, ModelDefinitonModelAdmin)
