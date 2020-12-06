from rest_framework import serializers

from notion.models import Block, Collection, LayoutPage, Page


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'icon']


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'type', 'data', 'col', 'row']


class LayoutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayoutPage
        fields = ['id', 'title', 'icon', 'block_set']

    block_set = BlockSerializer(many=True, read_only=True)


class CollectionPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'icon', ]

