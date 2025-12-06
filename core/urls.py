# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# 1. النماذج البسيطة (التي ما زالت تستخدم queryset=... في views.py)
# لا تحتاج basename لأنها تملك queryset ثابت
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)

# 2. النماذج المخصصة (التي تستخدم get_queryset)
# يجب إضافة basename هنا إجبارياً
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'notifications', NotificationViewSet, basename='notification')

# 3. نماذج الإدارة والسلوك
router.register(r'school-info', SchoolInfoViewSet)
router.register(r'assessment-types', AssessmentTypeViewSet)
router.register(r'behavior-types', BehaviorTypeViewSet)
router.register(r'behavior-records', BehaviorRecordViewSet, basename='behavior-record')
router.register(r'students', StudentViewSet, basename='student')
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('reports/student-list-docx/', export_student_list_docx, name='export_student_list_docx'),
    
    path('', include(router.urls)),
]