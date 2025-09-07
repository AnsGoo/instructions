# Django Fixture 使用说明

本目录包含Django项目的fixture数据文件，用于批量导入数据到数据库。

## 已创建的fixture文件

- `level1_fixture.json` - 一级分类数据，适用于`Level1Category`模型

## 如何使用fixture文件

在项目根目录下运行以下命令加载数据：

```bash
python manage.py loaddata content/fixtures/level1_fixture.json
```

## 注意事项

1. 请确保在运行此命令前，数据库已正确配置且`Level1Category`模型已通过migrate命令创建对应的数据库表
2. 如果遇到"No fixture named 'content/fixtures/level1_fixture' found"错误，请检查文件路径是否正确
3. 若需要重新加载数据，可以先删除现有数据再执行加载命令

## 原始数据

原始数据文件 `level1.json` 已保留，供参考