from django.contrib import admin
from .models import Project, User, Comment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
    search_fields = ('title',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ("username",)

@admin.register(Comment)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment')
    search_fields = ("name",)