from rest_framework import serializers

from content.models import Content

from .category import CategorySerializer


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

    def update(self, instance, validated_data: dict):
        # 更新基本字段
        instance.code = validated_data.pop('code', instance.code)
        instance.title = validated_data.pop('title', instance.title)
        instance.abstract = validated_data.pop('abstract', instance.abstract)
        instance.summary = validated_data.pop('summary', instance.summary)
        instance.keyword = validated_data.pop('keyword', instance.keyword)
        instance.web_url = validated_data.pop('web_url', instance.web_url)
        validated_data.pop('category_id', None)
        validated_data.pop('definition_id', None)
        instance.update_ext_fields(validated_data)
        instance.save()
        return instance
