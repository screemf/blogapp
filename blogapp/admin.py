from django.contrib import admin
from . models import Post,Author


# Register your models here.
#admin.site.register(Post)
#admin.site.register(Author)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','views_count')
    list_filter = ('is_published',)
    search_fields = ('title',)
    actions = ['make_published','make_unpublished']

    @admin.action(description='Опубликовать выбранные посты')
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Отменить выбранные публикиации')
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)



admin.site.register(Author)
