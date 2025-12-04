# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# -----------------
# 1. نماذج التعليم والمناهج (نضع Class و Subject هنا أولاً لأنها أساسية)
# -----------------

class Class(models.Model):
    name = models.CharField(max_length=50) # مثال: الخامس أ
    year = models.IntegerField(default=2025)
    
    class Meta:
        verbose_name_plural = "Classes"
        unique_together = ('name', 'year')
        
    def __str__(self):
        return f"{self.name} ({self.year})"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_religious = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.name

# -----------------
# 2. نماذج المستخدمين (Profiles)
# -----------------
class AssessmentType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نوع التقييم")
    weight_percentage = models.DecimalField(max_digits=5, decimal_places=2, 
                                            default=0.00, verbose_name="الوزن النسبي في المعدل العام للمادة")

    def __str__(self):
        return self.name
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    specialization = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    is_principal = models.BooleanField(default=False, verbose_name="مدير المدرسة")
    is_secretary = models.BooleanField(default=False, verbose_name="أمين السر")
    is_guidance_counselor = models.BooleanField(default=False, verbose_name="موجه طلابي")

    def __str__(self):
        return f"Teacher: {self.user.username}"
class Assignment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    due_date = models.DateTimeField() 
    created_at = models.DateTimeField(auto_now_add=True)
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.SET_NULL, null=True, 
                                        verbose_name="تصنيف التقييم")

    def __str__(self):
        return f"{self.title} ({self.course.name})"
class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # جعل unique=False والسماح بالـ blank/null
    phone_number = models.CharField(max_length=15, unique=False, blank=True, null=True) 
    
    def __str__(self):
        return f"Parent: {self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    # حقل class_ref أصبح صحيحاً الآن
    class_ref = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='students_in_class')
    
    # جعل parent يقبل Null/Blank
    parent = models.ForeignKey(ParentProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"Student: {self.user.username} ({self.student_id})"
        
# -----------------
# 3. نموذج الدورة التدريبية (Course)
# -----------------
class SchoolInfo(models.Model):
    principal_name = models.CharField(max_length=100, verbose_name="اسم المدير")
    secretary_name = models.CharField(max_length=100, verbose_name="اسم أمين السر")
    # يمكن إضافة المزيد من التفاصيل (العنوان، الشعار، إلخ)

    class Meta:
        verbose_name = "معلومات المدرسة"
        verbose_name_plural = "معلومات المدرسة"
class Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='teaching_courses')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_level = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True) 
    
    class Meta:
        unique_together = ('subject', 'class_level', 'teacher') 
        
    def __str__(self):
        return f"{self.subject.name} لـ {self.class_level.name}"
class Grade(models.Model):
    # الدرجة مرتبطة بواجب محدد
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='grades')
    
    # الدرجة مرتبطة بطالب محدد
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='grades')
    
    # الدرجة التي حصل عليها الطالب
    score = models.DecimalField(max_digits=5, decimal_places=2)
    
    # ملاحظات المدرس على الدرجة/الواجب
    feedback = models.TextField(blank=True)
    
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # لا يمكن للطالب أن يحصل على أكثر من درجة واحدة لنفس الواجب
        unique_together = ('assignment', 'student') 
        
    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}: {self.score}"

# -----------------
# 4. إدارة Signals (لإبقاء الكود نظيفاً)
# -----------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        pass # نستخدم منطق الإنشاء المخصص في UserRegisterSerializer

from django.contrib.auth import get_user_model
User = get_user_model()
class Notification(models.Model):
    """
    نموذج لتمثيل الإشعارات المرسلة إلى مستخدم محدد.
    """
    # المستلم: نربط الإشعار بنموذج المستخدم الأساسي
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications', 
        verbose_name="المستلم"
    )
    
    # محتوى الإشعار
    title = models.CharField(max_length=255, verbose_name="العنوان")
    message = models.TextField(verbose_name="الرسالة")
    
    # رابط اختياري للعنصر المرتبط (مثل الواجب أو الدرجة)
    link = models.URLField(max_length=255, blank=True, null=True, verbose_name="الرابط المرتبط")
    
    # حالة الإشعار
    is_read = models.BooleanField(default=False, verbose_name="مقروء")
    
    # بيانات وصفية
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    # نوع الإشعار (مفيد للواجهة الأمامية لتغيير الأيقونات)
    NOTIFICATION_CHOICES = (
        ('ASSIGNMENT', 'واجب جديد'),
        ('GRADE', 'درجة جديدة'),
        ('ANNOUNCEMENT', 'إعلان عام'),
        ('ALERT', 'تنبيه'),
    )
    type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_CHOICES, 
        default='ANNOUNCEMENT', 
        verbose_name="النوع"
    )
    
    class Meta:
        # نرتب الإشعارات من الأحدث إلى الأقدم
        ordering = ('-created_at',)
        verbose_name = "إشعار"
        verbose_name_plural = "إشعارات"

    def __str__(self):
        return f"الإشعار لـ {self.user.username}: {self.title}"


class BehaviorType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="نوع السلوك")
    is_positive = models.BooleanField(default=False, verbose_name="إيجابي؟")
    points = models.IntegerField(default=1, verbose_name="النقاط المكتسبة/المفقودة")
    
    def __str__(self):
        return f"[{'✅' if self.is_positive else '❌'}] {self.name}"

class BehaviorRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='behavior_records', verbose_name="الطالب")
    behavior_type = models.ForeignKey(BehaviorType, on_delete=models.PROTECT, verbose_name="نوع السلوك")
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="سجله المدرس")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    
    # لسهولة التقرير
    points_change = models.IntegerField(editable=False, verbose_name="تغيير النقاط") 
    
    def save(self, *args, **kwargs):
        # حفظ قيمة النقاط بناءً على نوع السلوك
        self.points_change = self.behavior_type.points if self.behavior_type.is_positive else -self.behavior_type.points
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.username} - {self.behavior_type.name}"