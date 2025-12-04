# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Grade, BehaviorRecord, Notification, Student

# -----------------------------------------------------
# 1. إشعار عند تسجيل درجة جديدة (Grade)
# -----------------------------------------------------

@receiver(post_save, sender=Grade)
def create_grade_notification(sender, instance, created, **kwargs):
    """
    يتم تشغيل هذه الإشارة بعد حفظ كائن Grade (درجة) جديد أو تحديثه.
    """
    if created or instance.pk is not None:
        student = instance.student
        assignment_title = instance.assignment.title
        score = instance.score
        
        title = f"نتيجة تقييم: {assignment_title}"
        message = f"تم تسجيل درجتك {score} في تقييم {assignment_title}."
        
        # 1. إشعار للطالب نفسه
        Notification.objects.create(
            user=student.user,
            title=title,
            message=message,
            type='GRADE'
        )
        
        # 2. إشعار لولي الأمر (إن وجد)
        if student.parent:
            Notification.objects.create(
                user=student.parent.user,
                title=f"نتيجة ابنك: {assignment_title}",
                message=f"تم تسجيل درجة {score} لابنك/ابنتك في تقييم {assignment_title}.",
                type='GRADE'
            )

# -----------------------------------------------------
# 2. إشعار عند تسجيل سلوك جديد (BehaviorRecord)
# -----------------------------------------------------

@receiver(post_save, sender=BehaviorRecord)
def create_behavior_notification(sender, instance, created, **kwargs):
    """
    يتم تشغيل هذه الإشارة بعد حفظ سلوك جديد.
    """
    if created or instance.pk is not None:
        student = instance.student
        behavior_type = instance.behavior_type
        
        action = "إيجابي" if behavior_type.is_positive else "سلبي"
        points = abs(instance.points_change)

        title = f"تحديث سلوكي: {action}"
        message = f"تم تسجيل ملاحظة سلوكية ({behavior_type.name}) للطالب. تغيير النقاط: {points}."
        
        # 1. إشعار للطالب نفسه (إيجابي أو سلبي)
        Notification.objects.create(
            user=student.user,
            title=title,
            message=message,
            type='ALERT'
        )
        
        # 2. إشعار لولي الأمر
        if student.parent:
            Notification.objects.create(
                user=student.parent.user,
                title=f"سجل سلوك لابنك: {action}",
                message=f"تم تسجيل ملاحظة ({behavior_type.name}) لابنك/ابنتك. يرجى المتابعة.",
                type='ALERT'
            )