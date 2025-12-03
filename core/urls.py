# core/urls.py (للتأكد فقط)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, ProfileView, ClassViewSet, SubjectViewSet, 
    CourseViewSet, AssignmentViewSet, GradeViewSet,NotificationViewSet
) 

router = DefaultRouter()
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'notifications', NotificationViewSet, basename='notification') # المسار الجديد
urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # باقي المسارات التي تستخدم الـ Router
    path('', include(router.urls)),
]