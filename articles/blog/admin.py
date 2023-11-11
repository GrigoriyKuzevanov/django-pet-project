from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from .models import Post, Category, TagPost


class AuthorFilter(admin.SimpleListFilter):
    """
    класс пользовательского поля для фильтрации
    """
    title = 'Статус автора'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('has author', 'Есть автор'),
            ('has not author', 'Автор не указан')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'has author':
            return queryset.filter(author__isnull=False)
        elif self.value() == 'has not author':
            return queryset.filter(author__isnull=True)


@admin.register(Post)                   # то же, что и admin.site.register(Post, PostAdmin)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'slug', 'category', 'tags')   # поля, которые отражаются при редактировании поста в админпанели
    # readonly_fields = ('slug', )    # поля только для чтения (поле slug формируется автоматически при сохранении поста)
    prepopulated_fields = {'slug': ('title', )} # автозаполнение поля slug на основе других полей (title)
    filter_horizontal = ('tags', )  # настройка видежета редактирования тэгов
    list_display = ('title', 'time_create', 'is_published', 'category', 'brief_info')   # поля, которые отображаются в админпанели для модели Post
    list_display_links = ('title',)    # поля, являются ссылками на редактирвование отдельной записи
    ordering = ('-time_create', 'title')     # поля для сортировки (при совпадении 'time_create', сортировка по 'title')
    list_editable = ('is_published',)    # поля с возможностью редактирования (не может быть одновременно ссылкой)
    list_per_page = 10  # пагинация отображения на странице
    actions = ('set_published', 'set_draft')   # действия на странице отображения в админпанели
    search_fields = ('title', 'category__name')  # список полей для панели поиска
    list_filter = (AuthorFilter, 'category__name', 'is_published')    # поля для фильтрации

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


@admin.register(TagPost)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', )
    prepopulated_fields = {'slug': ('tag', )}
