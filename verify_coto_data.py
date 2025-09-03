import os
import django

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instructions.settings')
django.setup()

from content.models import Category

# 验证导入的Category数据
print("验证Category数据：")
categories = Category.objects.all()
print(f"Category总数: {categories.count()}")

# 打印前5条数据进行验证
print("\n前5条Category数据：")
for cat in categories[:5]:
    print(f"ID: {cat.id}, Code: {cat.code}, Name: {cat.name}, Level1 ID: {cat.level1_id}")

# 验证特定code的存在
print("\n验证特定code的存在：")
sample_codes = ['0101', '0105', '0110', '0117']
for code in sample_codes:
    exists = Category.objects.filter(code=code).exists()
    print(f"Code {code} 存在: {exists}")

print("\n数据验证完成！")