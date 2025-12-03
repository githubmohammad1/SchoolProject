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