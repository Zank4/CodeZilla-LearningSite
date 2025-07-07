"""
URL configuration for MySite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), #route admin phải ở trước các route khác vì nếu không thì django sẽ tìm đến các route khác trước và không tìm thấy admin
    path('', include('learningsite.urls')), #khi chạy localhost:8000 thì django sẽ tìm đến urls.py trong learningsite
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #để có thể hiển thị hình ảnh trong các bài học, cần thêm dòng này để django biết đường dẫn đến thư mục chứa hình ảnh

