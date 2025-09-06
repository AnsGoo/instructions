from django.contrib import admin
from core.models import AttrDefinitionModel, ModelDefinitionModel
from core.admin import AttrDefinitionModelAdmin, ModelDefinitonModelAdmin

def register_admin(ext_model):
    setattr(admin.site, 'ext_model', ext_model)
    admin.site.register(AttrDefinitionModel, AttrDefinitionModelAdmin)
    admin.site.register(ModelDefinitionModel, ModelDefinitonModelAdmin)