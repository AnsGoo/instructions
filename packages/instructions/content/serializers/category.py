from rest_framework import serializers

from content.models import Category


class CategorySerializer(serializers.ModelSerializer):
    # 在创建或更新时，需要使用id来关联
    level1_id = serializers.IntegerField(write_only=True)
    definition_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'code',
            'name',
            'description',
            'level1',
            'definition',
            'level1_id',
            'definition_id',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        # 获取关联对象的id
        level1_id = validated_data.pop('level1_id')
        definition_id = validated_data.pop('definition_id', None)

        # 创建Category对象
        category = Category.objects.create(**validated_data)

        # 设置关联
        category.level1_id = level1_id
        if definition_id:
            category.definition_id = definition_id
        category.save()

        return category

    def update(self, instance, validated_data):
        # 更新基本字段
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # 更新关联字段
        if 'level1_id' in validated_data:
            instance.level1_id = validated_data['level1_id']
        if 'definition_id' in validated_data:
            instance.definition_id = validated_data['definition_id']

        instance.save()
        return instance
