# core/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
# استيراد جميع النماذج التي سيتم استخدامها في Serializers
from .models import Teacher, ParentProfile, Student, Subject, Class, Course, Grade,Assignment, Notification
# سنضيف Assignment و Grade لاحقًا في Sprint 3

# ----------------------------------------
# I. السيريلايزرات الأساسية للمستخدمين (Registration & Profile Display)
# ----------------------------------------
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user', 'created_at') # لا يسمح للمستخدم بتحديد المستخدم وتاريخ الانشاء يدويا
class UserSerializer(serializers.ModelSerializer):
    """Serializer أساسي لعرض بيانات المستخدم (الاسم، البريد)"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer لإنشاء مستخدم جديد (Registration)"""
    role = serializers.CharField(write_only=True, required=True) 
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'first_name', 'last_name')

    def validate_role(self, value):
        valid_roles = ['teacher', 'parent', 'student']
        if value.lower() not in valid_roles:
            raise serializers.ValidationError("الدور يجب أن يكون 'teacher', 'parent', أو 'student'.")
        return value.lower()

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        
        # إنشاء مستخدم Django وتجزئة كلمة المرور
        user = User.objects.create_user(password=password, **validated_data)
        
        # إنشاء الملف الشخصي المرتبط بناءً على الدور
        if role == 'teacher':
            Teacher.objects.create(user=user)
        elif role == 'parent':
            ParentProfile.objects.create(user=user)
        elif role == 'student':
            Student.objects.create(user=user, student_id=user.username) 

        return user
    
# ----------------------------------------
# II. سيريلايزرات الـ Profiles (لعرض /api/core/profile/)
# ----------------------------------------

class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'specialization', 'hire_date') 
        
class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    # يمكن إضافة الأبناء لاحقًا هنا عبر علاقة Foreign Key
    
    class Meta:
        model = ParentProfile
        fields = ('id', 'user', 'phone_number')

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    # عرض اسم الصف عبر علاقة المفتاح الخارجي
    class_name = serializers.CharField(source='class_ref.name', read_only=True) 
    
    class Meta:
        model = Student
        # أضفنا class_ref و class_name (للعرض)
        fields = ('id', 'user', 'student_id', 'class_ref', 'class_name')
        # جعل المفتاح الخارجي (class_ref) للقراءة فقط في العرض
        extra_kwargs = {'class_ref': {'read_only': True}} 

# ----------------------------------------
# III. سيريلايزرات إدارة الكيانات (Admin/Teacher Only)
# ----------------------------------------

class ClassSerializer(serializers.ModelSerializer):
    """لإدارة الصفوف (إنشاء، عرض، تحديث)"""
    class Meta:
        model = Class
        fields = ('id', 'name', 'year')

class SubjectSerializer(serializers.ModelSerializer):
    """لإدارة المواد"""
    class Meta:
        model = Subject
        fields = ('id', 'name', 'is_religious')
class GradeSerializer(serializers.ModelSerializer):
    """لإدارة إدخال درجات الطلاب"""
    # لعرض اسم الطالب والواجب بدلاً من الـ ID
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = Grade
        fields = ('id', 'assignment', 'assignment_title', 'student', 'student_name', 
                  'score', 'feedback', 'graded_at')
        extra_kwargs = {
            'assignment': {'write_only': True},
            'student': {'write_only': True},
            'graded_at': {'read_only': True}
        } 

class AssignmentSerializer(serializers.ModelSerializer):
    """لإدارة الواجبات والامتحانات"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Assignment
        # تأكد من أن جميع الحقول متطابقة مع نموذج Assignment في models.py
        fields = ('id', 'course', 'course_name', 'title', 'description', 'max_score', 'due_date', 'created_at')
        extra_kwargs = {
            'course': {'write_only': True},
            'created_at': {'read_only': True}
        }

class CourseSerializer(serializers.ModelSerializer):
    """لإدارة الدورات التدريبية (ربط المدرس بالصف والمادة)"""
    # حقول للقراءة فقط لعرض تفاصيل بدلاً من المفاتيح الخارجية
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_level.name', read_only=True)
    teacher_username = serializers.CharField(source='teacher.user.username', read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'subject', 'class_level', 'teacher', 
                  'subject_name', 'class_name', 'teacher_username')
        # التأكد من أن حقول المفاتيح الخارجية تقبل الإرسال في طلب POST/PUT
        extra_kwargs = {
            'subject': {'write_only': True},
            'class_level': {'write_only': True},
            'teacher': {'write_only': True},
        }