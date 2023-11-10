from django.contrib import admin, messages
from .models import Post, Category

@admin.register(Post)                   # то же, что и admin.site.register(Post, PostAdmin)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'category', 'brief_info')   # поля, которые отображаются в админпанели для модели Post
    list_display_links = ('title',)    # поля, являются ссылками на редактирвование отдельной записи
    ordering = ('-time_create', 'title')     # поля для сортировки (при совпадении 'time_create', сортировка по 'title')
    list_editable = ('is_published',)    # поля с возможностью редактирования (не может быть одновременно ссылкой)
    list_per_page = 10  # пагинация отображения на странице
    actions = ('set_published', 'set_draft')   # действия на странице отображения в админпанели

    @admin.display(description='Краткое описание', ordering='content')      # название пользовательского поля для отображения в админпанели
    def brief_info(self, post: Post):
        """
        пользовательское поле, которое возвращает строку с длиной символов
        в поле content модели Post
        """
        return f'Длина статьи - {len(post.content)} символов'
    
    @admin.action(description='Опубликовать выбранные посты')
    def set_published(self, request, queryset):
        """
        пользовательское действие, меняет статус выбранных постов
        на "опубликовано"
        """
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано постов: {count}')  # сообщение для пользователя

    @admin.action(description='Снять с публикации выбранные посты')
    def set_draft(self, request, queryset):
        """
        пользовательское действие, меняет статус выбранных постов
        на "черновик"
        """
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f'Снято с публикации  постов: {count}', messages.WARNING)  # сообщение для пользователя


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
# admin.site.register(Post, PostAdmin)

