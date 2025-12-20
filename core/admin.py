from django.contrib import admin
from .models import Project, User, Comment, UploadedFile

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
    list_display = ('id', 'user', 'project', 'comment')
    search_fields = ("user",)

@admin.register(UploadedFile)
class UploadedAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'original_name')
    search_fields = ('original_name',)