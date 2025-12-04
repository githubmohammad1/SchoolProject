# core/urls.py (للتأكد فقط)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'notifications', NotificationViewSet, basename='notification') # المسار الجديد
# 2. نماذج الإدارة والسلوك الجديدة
router.register(r'school-info', SchoolInfoViewSet) # معلومات المدرسة الرسمية
router.register(r'assessment-types', AssessmentTypeViewSet) # أنواع التقييمات (مذاكرة، امتحان)
router.register(r'behavior-types', BehaviorTypeViewSet) # أنواع السلوك (إيجابي/سلبي)
router.register(r'behavior-records', BehaviorRecordViewSet, basename='behavior-record') # سجلات سلوك الطالب
urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('reports/student-list-docx/', export_student_list_docx, name='export_student_list_docx'),
    # باقي المسارات التي تستخدم الـ Router
    path('', include(router.urls)),
]