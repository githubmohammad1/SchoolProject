# core/permissions.py

from rest_framework import permissions
from .models import Teacher # يجب استيراد نموذج المعلم للتحقق من وجود ملفه الشخصي

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    تسمح بالوصول (إنشاء، تعديل، حذف) فقط إذا كان المستخدم:
    1. مشرفاً (is_staff) في Django Admin.
    2. أو مدرساً (لديه ملف شخصي Teacher مرتبط بحسابه).
    """

    # لا نحتاج لـ has_object_permission لأن الصلاحية تطبق على مستوى القائمة/الإجراء (View level)

    def has_permission(self, request, view):
        # 1. يجب أن يكون المستخدم مسجلاً دخوله ومصدقاً عليه (مفروضة بواسطة IsAuthenticated)
        if not request.user.is_authenticated:
            return False
            
        # 2. السماح للمشرفين (Admins) بالوصول دائماً
        if request.user.is_staff:
            return True
        
        # 3. التحقق مما إذا كان المستخدم مدرساً
        try:
            # إذا كان ملف Teacher موجوداً للمستخدم، فإنه مدرس
            return request.user.teacher is not None 
        except Teacher.DoesNotExist:
            # إذا لم يكن لديه ملف Teacher، فليس مدرساً
            return False
        
        # 4. منع أي مستخدم آخر (طالب، ولي أمر)
        return False
class IsReadOnly(permissions.BasePermission):
    """
    يسمح بأي طلب GET, HEAD, OPTIONS (قراءة فقط).
    """
    def has_permission(self, request, view):
        # القراءة مسموحة للجميع
        if request.method in permissions.SAFE_METHODS:
            return True
        # الكتابة غير مسموحة إلا إذا سمح بها منطق ViewSet
        return False
class IsTeacherOrGuidance(permissions.BasePermission):
    """
    يسمح بالوصول إذا كان المستخدم معلمًا أو موجهًا طلابيًا (لتسجيل السلوك).
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_staff:
            return True

        try:
            # التحقق إذا كان User لديه ملف Teacher
            if hasattr(user, 'teacher'):
                # يسمح لجميع المعلمين بتسجيل السلوك (لأنهم يراقبون الفصل)
                return True
            return False
        except:
            return False

class IsSchoolAdministrator(permissions.BasePermission):
    """
    يسمح بالوصول إذا كان المستخدم مشرفًا أو مديرًا أو أمين سر.
    يستخدم لإدارة SchoolInfo وأنواع التقييمات/السلوكيات.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_staff:
            return True
            
        try:
            # يجب أن يكون لديه ملف معلم مع دور إداري
            teacher_profile = user.teacher
            return teacher_profile.is_principal or teacher_profile.is_secretary
        except:
            return False