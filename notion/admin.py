from django.contrib import admin

# Register your models here.
from notion.models import Block, Collection, CollectionProperty, CollectionView, LayoutPage, Page, PageProperty

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    model = Page

class BlockInlineAdmin(admin.TabularInline):
    model = Block

class PagePropertyInlineAdmin(admin.TabularInline):
    model = PageProperty

@admin.register(LayoutPage)
class LayoutPageAdmin(admin.ModelAdmin):
    model = LayoutPage

    inlines = (BlockInlineAdmin,PagePropertyInlineAdmin)


class CollectionViewInlineAdmin(admin.TabularInline):
    model = CollectionView

class CollectionPropertyInlineAdmin(admin.TabularInline):
    model = CollectionProperty

@admin.register(Collection)
class CollectionPageAdmin(admin.ModelAdmin):
    model = Collection

    inlines = (CollectionPropertyInlineAdmin,CollectionViewInlineAdmin,)

