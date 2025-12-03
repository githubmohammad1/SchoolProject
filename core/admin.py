# core/admin.py
from django.contrib import admin
from .models import Notification
from .models import (
    Class, Subject, Teacher, ParentProfile, Student, 
    Course, Assignment, Grade
)

# ----------------------------------------
# 1. نماذج التعليم الأساسية
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read')
    search_fields = ('user__username', 'title', 'message')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    list_filter = ('year',)
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_religious')
    list_filter = ('is_religious',)
    search_fields = ('name',)
    
# ----------------------------------------
# 2. نماذج المستخدمين (Profiles)
# ----------------------------------------

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'hire_date')
    search_fields = ('user__username', 'specialization')
    raw_id_fields = ('user',) # لتحسين البحث عن المستخدم

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')
    raw_id_fields = ('user',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'class_ref', 'parent')
    list_filter = ('class_ref',)
    search_fields = ('user__username', 'student_id')
    raw_id_fields = ('user', 'class_ref', 'parent') # للتعامل مع المفاتيح الخارجية الكبيرة

# ----------------------------------------
# 3. نماذج الكورسات والواجبات والدرجات
# ----------------------------------------

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'class_level', 'teacher')
    list_filter = ('class_level', 'subject', 'teacher')
    search_fields = ('name', 'subject__name', 'class_level__name')
    raw_id_fields = ('teacher', 'subject', 'class_level')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'max_score', 'due_date')
    list_filter = ('course',)
    search_fields = ('title',)
    raw_id_fields = ('course',)
    date_hierarchy = 'due_date'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'score')
    list_filter = ('assignment', 'student')
    search_fields = ('assignment__title', 'student__user__username')
    raw_id_fields = ('assignment', 'student')