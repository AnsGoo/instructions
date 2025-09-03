#!/usr/bin/env python3
from content.models import Category

# 获取所有Category数据
categories = Category.objects.all()

print(f"Category总数: {len(categories)}")
print("Category列表:")
for cat in categories:
    print(f"- ID: {cat.id}, Code: {cat.code}, Name: {cat.name}")

# 检查是否还有Level1Category数据
from content.models import Level1Category
level1_categories = Level1Category.objects.all()
print(f"\nLevel1Category总数: {len(level1_categories)}")
for l1 in level1_categories:
    print(f"- ID: {l1.id}, Code: {l1.code}, Name: {l1.name}")