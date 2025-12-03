# core/views.py 
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsTeacherOrAdmin, IsReadOnly
from rest_framework import permissions
# الاستيراد الموحد لجميع النماذج (باستخدام * مناسب هنا)
from .models import * # الاستيراد الموحد لجميع الـ Serializers 
from .serializers import (NotificationSerializer,
    UserRegisterSerializer, UserSerializer, TeacherProfileSerializer, 
    ParentProfileSerializer, StudentProfileSerializer, ClassSerializer, 
    SubjectSerializer, CourseSerializer, AssignmentSerializer, GradeSerializer
)
# ************

class GradeViewSet(viewsets.ModelViewSet):
    # ندمج الصلاحيتين: إما أن تكون مدرساً/مشرفاً، أو مجرد مستخدم مسجل للدخول (للقراءة فقط)
    permission_classes = [IsTeacherOrAdmin | permissions.IsAuthenticated]
    serializer_class = GradeSerializer

    def get_queryset(self):
        user = self.request.user
        # للمدرسين والمشرفين: عرض جميع الدرجات أو درجات دوراته
        if user.is_staff or hasattr(user, 'teacher'):
            if user.is_staff:
                 return Grade.objects.all()
            # المدرس يرى درجات طلابه في الدورات التي يدرسها
            teacher_courses = user.teacher.teaching_courses.all()
            return Grade.objects.filter(assignment__course__in=teacher_courses)

        # للطالب: عرض درجاته فقط
        elif hasattr(user, 'student'):
            return Grade.objects.filter(student=user.student)

        # لولي الأمر: عرض درجات أبنائه فقط
        elif hasattr(user, 'parentprofile'):
            children_students = user.parentprofile.children.all()
            return Grade.objects.filter(student__in=children_students)
        
        # لغير ذلك (مجرد مستخدم مسجل): لا يرى شيئاً
        return Grade.objects.none()

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]



class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrAdmin] # بقيت صلاحيات التعديل للمدرس/المشرف فقط

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        
        # المدرس يرى الدورات التي يدرسها فقط
        if hasattr(user, 'teacher'):
            return Course.objects.filter(teacher=user.teacher)
            
        # غير المدرسين والمشرفين لا يحتاجون لرؤية جميع الدورات (يمكن تعديلها لاحقاً)
        return Course.objects.none()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    # يجب أن يكون مسموحاً للجميع بالتسجيل
    permission_classes = () 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serializer.data,
            "message": "تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول."
        }, status=status.HTTP_201_CREATED)
# 2. عرض الملف الشخصي (Profile View)
# ----------------------------------------
class ProfileView(APIView):
    # يتطلب مصادقة (JWT)
    permission_classes = (IsAuthenticated,) 

    def get(self, request, *args, **kwargs):
        # المستخدم الذي تم التحقق من هويته عبر JWT موجود في request.user
        user = request.user
        profile_data = {}
        role = None

        # 1. التحقق من نوع الملف الشخصي وتطبيق Serializer المناسب
        
        try:
            # ملف الأستاذ
            teacher_profile = user.teacher
            serializer = TeacherProfileSerializer(teacher_profile)
            role = 'teacher'
        except Teacher.DoesNotExist:
            try:
                # ملف ولي الأمر
                parent_profile = user.parentprofile
                serializer = ParentProfileSerializer(parent_profile)
                role = 'parent'
            except ParentProfile.DoesNotExist:
                try:
                    # ملف الطالب
                    student_profile = user.student
                    serializer = StudentProfileSerializer(student_profile)
                    role = 'student'
                except Student.DoesNotExist:
                    # إذا لم يكن له أي ملف شخصي (مشكلة في البيانات، أو مستخدم عادي)
                    return Response({
                        "message": "لا يوجد ملف شخصي مرتبط بهذا المستخدم.",
                        "user_id": user.id
                    }, status=status.HTTP_404_NOT_FOUND)
        
        profile_data = serializer.data
        
        # 2. بناء الاستجابة النهائية
        return Response({
            "status": "success",
            "role": role,
            "profile": profile_data
        }, status=status.HTTP_200_OK)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    # الإشعارات للقراءة فقط للمستخدمين العاديين، ويتم إنشاؤها عبر المشرف/المدرس/النظام
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        # كل مستخدم يرى إشعاراته فقط
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # للتأكد من ربط الإشعار بالمستخدم أثناء الإنشاء عبر API
        # (يمكن لاحقاً منع الإنشاء إلا للمشرفين إذا كانت الإشعارات تولد فقط من النظام)
        if self.request.user.is_staff or hasattr(self.request.user, 'teacher'):
            serializer.save()
        # نتركها فارغة هنا، حيث سيتم توليد الإشعارات عبر الـ signals وليس عبر واجهة API مباشرة في معظم الحالات.

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    # نسمح بالقراءة للمستخدمين العاديين، والتعديل/الإضافة للمدرس/المشرف
    permission_classes = [IsTeacherOrAdmin | permissions.IsAuthenticated]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        user = self.request.user
        
        # المشرف يرى جميع الواجبات
        if user.is_staff:
            return Assignment.objects.all()
            
        # المدرس يرى واجبات دوراته
        if hasattr(user, 'teacher'):
            teacher_courses = user.teacher.teaching_courses.all()
            return Assignment.objects.filter(course__in=teacher_courses)

        # الطالب يرى الواجبات لدورات صفه
        if hasattr(user, 'student'):
            student_class = user.student.class_ref
            return Assignment.objects.filter(course__class_level=student_class)
            
        return Assignment.objects.none()