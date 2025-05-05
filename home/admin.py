from django.contrib import admin
from .models import Quiz, Question, Answer, Marks_Of_User

admin.site.register(Quiz)

class AnswerInLine(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]
    list_display = ('text', 'quiz')  # Display text and quiz in the admin list view

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

admin.site.register(Marks_Of_User)









from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_active', 'is_approved', 'is_superuser']
    list_editable = ['is_approved']  # Allows quick editing from list view
    list_filter = ('role', 'is_active', 'is_approved')  # Add filters
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'full_name', 'is_approved')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
