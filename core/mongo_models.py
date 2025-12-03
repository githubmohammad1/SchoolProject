# core/mongo_models.py

from mongoengine import Document, fields

# تعريف نموذج وثيقة MongoDB (ODM)
class StudentProfile(Document):
    # لا حاجة لـ Primary Key، MongoDB تولده تلقائيًا (_id)

    # مرجع إلى Student SQL (جعل الـ Profile مرتبطاً بطالب SQL)
    # نستخدم حقل CharField لتخزين اسم الطالب أو ID إذا كنا سنستخدم اسم المستخدم كمرجع
    student_name = fields.StringField(required=True, unique=True)
    
    # حقل JSONB مرن لتخزين التفضيلات (لا يتطلب هيكلاً ثابتاً)
    preferences = fields.DictField(default={
        'theme': 'light',
        'notifications': True
    })
    
    # قائمة الأنشطة (مثال: بيانات مصفوفة)
    activities = fields.ListField(fields.StringField())

    # تحديد اسم المجموعة في قاعدة البيانات (اختياري)
    meta = {'collection': 'student_profiles'}

    def __str__(self):
        return f"Profile of {self.student_name}"

# مثال على وثيقة MongoDB الناتجة:
"""
{
  "_id": ObjectId("..."),
  "student_name": "عائشة السعدي",
  "preferences": {
    "theme": "dark",
    "notifications": false,
    "language": "ar"
  },
  "activities": ["Reading", "Sports club"]
}
"""