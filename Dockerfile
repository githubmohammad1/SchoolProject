# 1. المرحلة الأساسية: استخدام صورة Python الرسمية
FROM python:3.11-slim

# 2. تعيين متغير البيئة الذي يمنع Python من كتابة ملفات بايت كود
ENV PYTHONDONTWRITEBYTECODE 1
# 3. تعيين متغير البيئة الذي يضمن توجيه مخرجات Python مباشرة إلى الطرفية/السجلات
ENV PYTHONUNBUFFERED 1

# 4. تعيين مجلد العمل داخل الحاوية
WORKDIR /usr/src/app

# 5. نسخ ملف المتطلبات أولاً (لتحسين التخزين المؤقت لـ Docker)
COPY requirements.txt .

# 6. تثبيت الاعتماديات
# سنثبت psycopg2-binary للاتصال بـ PostgreSQL و djangorestframework للحاجة المستقبلية
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 7. نسخ باقي كود التطبيق إلى مجلد العمل
COPY . .

# 8. تعريف المنفذ الذي سيستمع إليه الخادم
EXPOSE 8000

# 9. الأمر الافتراضي الذي سيتم تشغيله عند بدء الحاوية
# سيتم استبدال هذا الأمر لاحقاً بملف shell عند النشر الفعلي
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]