from rest_framework import serializers

from core.models import ModelDefinitionModel

from .models import Category, Content, Level1Category


class Level1CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Level1Category
        fields = ['id', 'code', 'name', 'description']


class ModelDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelDefinitionModel
        fields = ['id', 'name', 'code', 'description']


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


class ContentSerializer(serializers.ModelSerializer):
    # 嵌套序列化器，用于显示关联的分类信息
    category = CategorySerializer(read_only=True)

    # 在创建或更新时，需要使用id来关联
    category_id = serializers.IntegerField(read_only=True, required=False, allow_null=True)

    class Meta:
        model = Content
        fields = [
            'id',
            'code',
            'title',
            'category',
            'abstract',
            'summary',
            'keyword',
            'web_url',
            'state',
            'category_id',
            'create_time',
            'update_time',
            'create_user',
            'update_user',
        ]
        read_only_fields = [
            'id',
            'create_time',
            'update_time',
            'create_user',
            'update_user',
            'state',
            'category_id',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        views_kwargs = self.context.get('view').kwargs
        ext_fields = views_kwargs.get('ext_fields')
        for attr in ext_fields:
            self.fields[attr.attr_name] = serializers.ModelField(
                model_field=self.Meta.model._meta.get_field(attr.attr_id)
            )
            self.fields[attr.attr_name].label = attr.attr_label

    def create(self, validated_data):
        # 获取关联对象的id
        category_id = validated_data.pop('category_id', None)
        definition_id = validated_data.pop('definition_id', None)
        # 创建Content对象
        content = Content.objects.create(**validated_data)
        content.model_id = definition_id

        # 设置关联
        if category_id:
            content.category_id = category_id
        content.save()

        return content

    def update(self, instance, validated_data):
        # 更新基本字段
        instance.code = validated_data.get('code', instance.code)
        instance.title = validated_data.get('title', instance.title)
        instance.abstract = validated_data.get('abstract', instance.abstract)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.keyword = validated_data.get('keyword', instance.keyword)
        instance.web_url = validated_data.get('web_url', instance.web_url)
        validated_data.pop('category_id', None)
        validated_data.pop('definition_id', None)

        instance.save()
        return instance
