from django.contrib import admin
from .models import UserProfile, Show, Episode, Subscription, NotificationLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'sms_notifications_enabled', 'created_at')
    search_fields = ('user__username', 'phone_number')


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_active', 'last_checked_at', 'created_at')
    search_fields = ('title', 'rss_url')
    list_filter = ('is_active',)


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('show', 'title', 'published_at', 'is_downloaded')
    search_fields = ('title', 'guid')
    list_filter = ('show', 'is_downloaded')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'created_at')
    search_fields = ('user__username', 'show__title')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'episode', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'episode__title')
