import uuid
from functools import partial

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.managers import InheritanceManager


class Page(models.Model):
    class PageType(models.TextChoices):
        LAYOUT = 'LAYOUT', _('Layout')
        COLLECTION = 'COLLECTION', _('Collection')

    objects = InheritanceManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    icon = models.CharField(max_length=200,null=True,blank=True)

    title = models.TextField(default='Untitled')
    parent = models.ForeignKey('self', null=True,blank=True, on_delete=models.CASCADE)
    # type = models.CharField(max_length=50, choices=PageType.choices)
    wide = models.BooleanField(default=False)


class LayoutPage(Page):
    # type = models.CharField(max_length=50, default=Page.PageType.LAYOUT.value,choices=Page.PageType.choices)

    pass


class Block(models.Model):
    class BlockType(models.TextChoices):
        TEXT = 'TEXT', _('Text')
        LINK = 'LINK', _('Link')
        H1 = 'H1', _('Heading 1')
        H2 = 'H2', _('Heading 1')
        H3 = 'H3', _('Heading 1')
        BULLETED_LIST = 'BULLETED_LIST', _('Bulleted list')
        NUMBERED_LIST = 'NUMBERED_LIST', _('Numbered list')
        TOGGLE = 'TOGGLE', _('Toggle')
        QUOTE = 'QUOTE', _('Quote')
        DIVIDER = 'DIVIDER', _('Divider')
        CALL_OUT = 'CALL_OUT', _('Call Out')
        EMBED = 'EMBED', _('Embed')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, choices=BlockType.choices)
    data = models.JSONField(null=True)
    page = models.ForeignKey(LayoutPage, on_delete=models.CASCADE)
    col = models.IntegerField(default=1,null=False)
    row = models.IntegerField(default=1)


class Collection(models.Model):
    # type = models.CharField(max_length=50, default=Page.PageType.COLLECTION.value,choices=Page.PageType.choices)
    pass


class CollectionView(models.Model):
    class ViewType(models.TextChoices):
        TABLE = 'TALBE', _('Table')
        BOARD = 'BOARD', _('Board')
        TIMELINE = 'TIMELINE', _('Timeline')
        LIST = 'LIST', _('List')
        CALENDAR = 'CALENDAR', _('Calendar')
        GALLERY = 'GALLERY', _('Gallery')

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=ViewType.choices,default=ViewType.TABLE.value)
    data = models.JSONField(default=dict)


class CollectionProperty(models.Model):
    page = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default='Column',blank=True)
    data = models.JSONField(default=dict)


class PageProperty(models.Model):
    type = models.ForeignKey(CollectionProperty, on_delete=models.CASCADE)
    page = models.ForeignKey(LayoutPage, on_delete=models.CASCADE)
    data = models.JSONField(default=partial(dict,value=''))
