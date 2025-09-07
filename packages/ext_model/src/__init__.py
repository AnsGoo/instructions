"""ext_model包初始化文件"""
# 导入ext_model的主要模型和类
def __getattr__(name):
    # 延迟导入，避免循环导入问题
    if name == 'BaseModel':
        from .models import BaseModel
        return BaseModel
    if name == 'ModelDefinitionModel':
        from .models import ModelDefinitionModel
        return ModelDefinitionModel
    if name == 'AttrDefinitionModel':
        from .models import AttrDefinitionModel
        return AttrDefinitionModel
    if name == 'ExtModel':
        from .models import ExtModel
        return ExtModel
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ['BaseModel', 'ModelDefinitionModel', 'AttrDefinitionModel', 'ExtModel']
