# ext_model 测试指南

本指南介绍如何运行和使用`ext_model`基础库的测试工程。

## 测试工程概述

测试工程位于`src/tests/test_base.py`文件中，包含了对`ext_model`基础库中各种模型和功能的全面测试，包括：

- **BaseModel**：测试基础模型的软删除功能、继承功能等
- **ModelDefinitionModel**：测试模型定义的 CRUD 操作
- **AttrDefinitionModel**：测试属性定义的 CRUD 操作和唯一性约束
- **ExtModel**：测试扩展模型的核心功能
- **模型管理器**：测试自定义管理器的行为
- **模型关系**：测试模型定义和属性定义之间的关系

## 运行测试

你可以通过 Django 的测试框架来运行这些测试。以下是运行测试的几种方式：

### 方式 1：使用项目根目录的管理脚本

在项目根目录下执行：

```bash
python -m utils.manage test ext_model
```

### 方式 2：直接使用 Django 的 manage.py

在 instructions 目录下执行：

```bash
cd packages/instructions
python manage.py test ext_model
```

### 方式 3：运行特定的测试用例

如果你只想运行特定的测试用例，可以指定测试方法：

```bash
python -m utils.manage test ext_model_test.tests.test_base.ExtModelTestProject.test_basemodel_soft_delete
```

## 测试用例说明

测试工程中包含以下测试用例：

1. **test_basemodel_soft_delete**：测试 BaseModel 的软删除功能，验证记录被标记为删除但仍保留在数据库中
2. **test_model_definition_crud**：测试 ModelDefinitionModel 的创建、读取、更新和删除操作
3. **test_attr_definition_crud**：测试 AttrDefinitionModel 的创建、读取、更新和删除操作
4. **test_attr_definition_unique_constraint**：测试 AttrDefinitionModel 的(model, attr_id)唯一约束
5. **test_extmodel_functionality**：测试 ExtModel 的核心功能，包括属性代理和模型关联
6. **test_model_manager**：测试自定义的 BaseManger，验证它不会返回已删除的记录
7. **test_base_model_inheritance**：测试 BaseModel 的继承功能，确保子类能正确继承基础字段和方法
8. **test_model_and_attr_relationship**：测试模型定义和属性定义之间的关系

## 测试数据

测试工程会自动创建以下测试数据：

- 一个测试用户
- 一个模型定义
- 两个属性定义

这些数据只在测试过程中存在，不会影响实际的数据库。

## 编写新的测试

如果你需要为`ext_model`添加新的测试，可以在`src/tests.py`文件中扩展`ExtModelTestProject`类，或者创建新的测试类。

### 添加新的测试方法

```python
def test_new_functionality(self):
    """测试新功能的描述"""
    # 测试代码
    # 断言语句
```

## 注意事项

1. 确保在运行测试前已经应用了所有数据库迁移：

   ```bash
   python -m utils.manage migrate
   ```

2. 测试会创建临时的测试数据库，不会影响开发或生产数据库

3. 运行测试时，Django 会自动处理数据库的创建和销毁

4. 如果你修改了模型定义，请确保更新相应的测试用例
