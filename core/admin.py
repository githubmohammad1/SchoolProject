from django.contrib import admin
from .models import *

# ----------------------------------------
# 1. نماذج التعليم الأساسية
# ----------------------------------------

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ('principal_name', 'secretary_name')
    # لا داعي للفلاتر هنا لأنها غالباً سجل واحد

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

@admin.register(AssessmentType)
class AssessmentTypeAdmin(admin.ModelAdmin):
    # أضفنا الوزن النسبي ليظهر في القائمة
    list_display = ('name', 'weight_percentage') 
    search_fields = ('name',)

# ----------------------------------------
# 2. نماذج المستخدمين (Profiles)
# ----------------------------------------

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    # أضفنا الصلاحيات (مدير، أمين سر...) لتراها مباشرة
    list_display = ('user', 'specialization', 'is_principal', 'is_secretary', 'is_guidance_counselor', 'hire_date')
    list_filter = ('is_principal', 'is_secretary', 'is_guidance_counselor')
    search_fields = ('user__username', 'user__first_name', 'specialization')
    raw_id_fields = ('user',)

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')
    raw_id_fields = ('user',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # أضفنا تاريخ الميلاد للقائمة
    list_display = ('user', 'student_id', 'class_ref', 'parent', 'date_of_birth')
    list_filter = ('class_ref',)
    search_fields = ('user__username', 'user__first_name', 'student_id')
    raw_id_fields = ('user', 'class_ref', 'parent')

# ----------------------------------------
# 3. نماذج الكورسات والواجبات والدرجات
# ----------------------------------------

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'class_level', 'teacher')
    list_filter = ('class_level', 'subject', 'teacher')
    search_fields = ('name', 'subject__name', 'class_level__name', 'teacher__user__username')
    raw_id_fields = ('teacher', 'subject', 'class_level')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    # أضفنا نوع التقييم (مذاكرة/امتحان) للعرض
    list_display = ('title', 'course', 'assessment_type', 'max_score', 'due_date')
    list_filter = ('course__class_level', 'assessment_type')
    search_fields = ('title', 'course__name')
    raw_id_fields = ('course', 'assessment_type')
    date_hierarchy = 'due_date'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'score', 'graded_at')
    list_filter = ('assignment__course', 'assignment')
    search_fields = ('student__user__username', 'assignment__title')
    raw_id_fields = ('assignment', 'student')

# ----------------------------------------
# 4. السلوك والإشعارات
# ----------------------------------------

@admin.register(BehaviorType)
class BehaviorTypeAdmin(admin.ModelAdmin):
    # أضفنا هل هو إيجابي أم لا، وعدد النقاط
    list_display = ('name', 'is_positive', 'points')
    list_filter = ('is_positive',)
    search_fields = ('name',)

@admin.register(BehaviorRecord)
class BehaviorRecordAdmin(admin.ModelAdmin):
    # تصحيح اسم الحقل: في الموديل اسمه date وليس date_recorded
    # وأضفنا points_change لنرى كم خصم/أضيف للطالب
    list_display = ('student', 'behavior_type', 'points_change', 'recorded_by', 'date')
    list_filter = ('behavior_type', 'date')
    search_fields = ('student__user__username', 'recorded_by__user__username')
    raw_id_fields = ('student', 'behavior_type', 'recorded_by')
    date_hierarchy = 'date'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read')
    search_fields = ('user__username', 'title', 'message')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)

# ملاحظة: قمت بحذف AssessmentRecord لأنه غير موجود في ملف models.py الذي أنشأناه
# (الدرجات يتم التعامل معها في Grade)