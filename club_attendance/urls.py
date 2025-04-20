from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('attendance.urls')),  # attendance 앱의 URL 경로 포함
]
