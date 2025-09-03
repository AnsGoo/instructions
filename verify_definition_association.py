#!/usr/bin/env python
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instructions.settings')

import django
django.setup()

from content.models import Category
from core.models import AttrDefinitionModel


def verify_definition_association():
    """验证Category对象的definition字段是否正确关联"""
    print("开始验证分类与定义对象的关联...")
    
    # 获取所有Category对象
    categories = Category.objects.all()
    total_categories = categories.count()
    
    # 统计有关联definition的Category数量
    categories_with_definition = categories.filter(definition__isnull=False).count()
    
    # 输出统计信息
    print(f"\n验证结果:")
    print(f"- 总分类数量: {total_categories}")
    print(f"- 有关联定义的分类数量: {categories_with_definition}")
    
    # 检查是否所有Category都有关联的definition
    if categories_with_definition == total_categories:
        print("✅ 所有分类都已成功关联定义对象！")
    else:
        print("❌ 警告：有部分分类未关联定义对象！")
        # 列出未关联定义的分类
        categories_without_definition = categories.filter(definition__isnull=True)
        print("\n未关联定义的分类:")
        for category in categories_without_definition:
            print(f"- {category.id}: {category.name} (code: {category.code})")
    
    # 检查定义对象是否正确创建
    attr_definitions = AttrDefinitionModel.objects.filter(attr_id__startswith='category_')
    print(f"\n找到的分类相关定义对象数量: {attr_definitions.count()}")
    
    # 打印前5个关联示例
    print("\n前5个分类与定义的关联示例:")
    for i, category in enumerate(categories[:5]):
        if category.definition:
            print(f"{i+1}. 分类: {category.name} (code: {category.code})")
            print(f"   关联的定义: {category.definition.attr_name} (id: {category.definition.id})")
            print(f"   定义描述: {category.definition.attr_description}")
            print()


if __name__ == '__main__':
    verify_definition_association()
    print("\n验证完成！")