from django.core.management.base import BaseCommand
import json
import os
from content.models import Category, Level1Category
from core.models import AttrDefinitionModel

class Command(BaseCommand):
    help = '导入分类数据并自动生成关联的定义对象'

    def add_arguments(self, parser):
        # 添加fixture文件路径参数
        parser.add_argument('fixture_path', nargs='?', type=str, help='fixture文件路径')

    def handle(self, *args, **options):
        # 获取fixture文件路径
        fixture_path = options['fixture_path']
        
        # 如果未提供路径，使用默认路径
        if not fixture_path:
            fixture_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                'content', 'fixtures', 'category_fixture.json'
            )
            self.stdout.write(f"未指定fixture文件路径，使用默认路径: {fixture_path}")
        
        # 检查文件是否存在
        if not os.path.exists(fixture_path):
            self.stderr.write(f"错误: 找不到fixture文件 {fixture_path}")
            return
        
        self.stdout.write(f"开始导入分类数据并自动生成定义对象...")
        self.stdout.write(f"使用fixture文件: {fixture_path}")
        
        try:
            # 读取fixture文件
            with open(fixture_path, 'r', encoding='utf-8') as f:
                fixtures = json.load(f)
            
            # 记录创建的对象数量
            created_definitions = 0
            updated_categories = 0
            
            # 遍历每个category fixture
            for fixture in fixtures:
                if fixture['model'] == 'content.category':
                    fields = fixture['fields']
                    pk = fixture['pk']
                    
                    # 获取或创建Category对象
                    try:
                        category = Category.objects.get(pk=pk)
                        self.stdout.write(f"找到分类 {pk}: {fields['name']}")
                    except Category.DoesNotExist:
                        # 如果不存在，创建新的Category对象
                        level1 = Level1Category.objects.get(pk=fields['level1'])
                        category = Category(
                            pk=pk,
                            code=fields['code'],
                            name=fields['name'],
                            description=fields['description'],
                            level1=level1,
                            # 使用get方法获取is_delete字段，如果不存在则使用默认值False
                            is_delete=fields.get('is_delete', False)
                        )
                        category.save()
                        self.stdout.write(f"创建新分类 {pk}: {fields['name']}")
                    
                    # 检查是否已有关联的definition
                    if not category.definition:
                        # 创建对应的AttrDefinitionModel对象
                        attr_definition = AttrDefinitionModel(
                            attr_type='text',  # 默认使用text类型
                            attr_name=f"分类_{fields['code']}_定义",
                            attr_id=f"category_{fields['code']}",
                            attr_description=f"分类'{fields['name']}'的属性定义"
                        )
                        attr_definition.save()
                        created_definitions += 1
                        
                        # 关联definition到category
                        category.definition = attr_definition
                        category.save()
                        updated_categories += 1
                        self.stdout.write(f"  ✅ 为分类 {fields['name']} 创建并关联了定义对象")
                    else:
                        self.stdout.write(f"  分类 {fields['name']} 已有关联的定义对象")
            
            # 输出统计信息
            self.stdout.write(f"\n导入完成！")
            self.stdout.write(f"- 创建了 {created_definitions} 个定义对象")
            self.stdout.write(f"- 更新了 {updated_categories} 个分类对象")
            self.stdout.write("\n操作完成！")
        except Exception as e:
            self.stderr.write(f"处理过程中发生错误: {str(e)}")