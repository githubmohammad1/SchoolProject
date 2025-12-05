# SchoolProject/urls.py

from django.contrib import admin
from django.urls import path, include 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="School API",
      default_version='v1',
      description="توثيق نظام إدارة المدرسة",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/core/', include('core.urls')),


    path('admin/', admin.site.urls),

    # توجيه كل المسارات التي تبدأ بـ 'results/' إلى ملف urls الخاص بـ 'core'
    # path('results/', include('core.urls')), 
]