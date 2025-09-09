import json
import os

from django.core.management.base import BaseCommand

from content.models import MyModelDefinitionModel


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
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                ),
                'content',
                'fixtures',
                'data.json',
            )
            self.stdout.write(f'未指定fixture文件路径，使用默认路径: {fixture_path}')

        # 检查文件是否存在
        if not os.path.exists(fixture_path):
            self.stderr.write(f'错误: 找不到fixture文件 {fixture_path}')
            return

        self.stdout.write('开始导入分类数据并自动生成定义对象...')
        self.stdout.write(f'使用fixture文件: {fixture_path}')

        try:
            # 读取fixture文件
            with open(fixture_path, encoding='utf-8') as f:
                fixtures = json.load(f)

            # 记录创建的对象数量
            created_definitions = 0

            # 遍历每个category fixture
            for fixture in fixtures:
                fields = fixture['fields']
                pk = fixture['pk']

                # 获取或创建Category对象
                attr_definition = MyModelDefinitionModel(
                    id=pk,
                    name=fields['name'],
                    code=fields['code'],
                    description=fields['description'],
                )
                attr_definition.save()
                created_definitions += 1
                self.stdout.write(f'  ✅ 为分类 {fields["name"]} 创建并关联了定义对象')

            # 输出统计信息
            self.stdout.write('\n导入完成！')
            self.stdout.write(f'- 创建了 {created_definitions} 个定义对象')
            self.stdout.write('\n操作完成！')
        except Exception as e:
            self.stderr.write(f'处理过程中发生错误: {str(e)}')
