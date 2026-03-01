from django.contrib import admin, messages
from .models import Starship, Category, PublishStatus
from django.utils.safestring import mark_safe


@admin.register(Starship)
class StarshipAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'title', 'time_create', 'is_published', 'cat', 'brief_info', 'tags_count')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['is_published', 'cat', 'time_create']
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Основные данные", {"fields": ("title", "slug", "cat", "tags", "photo", "photo_preview")}),
        ("Текст", {"fields": ("content",)}),
        ("Публикация", {"fields": ("is_published",)}),
        ("Служебная информация", {"fields": ("time_create", "time_update")}),
    )
    readonly_fields = ['time_create', 'time_update', 'photo_preview']

    @admin.display(description="Фото")
    def photo_preview(self, starship):
        if starship.photo:
            return mark_safe(f"<img src='{starship.photo.url}' width='60' />")
        return "—"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=PublishStatus.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=PublishStatus.DRAFT)
        self.message_user(
            request,
            f"{count} записи(ей) сняты с публикации!",
            messages.WARNING
        )

    @admin.display(description="Тэги (кол-во)")
    def tags_count(self, starship: Starship):
        return starship.tags.count()

    @admin.display(description="Краткое описание")
    def brief_info(self, starship: Starship):
        return f"Описание {len(starship.content)} символов."

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')