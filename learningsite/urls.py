from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'), #đường dẫn đến trang đăng ký
    path('login/', views.loginPage, name='login'), #đường dẫn đến trang đăng nhập
    path('logout/', views.logoutPage, name='logout'), #đường dẫn đến trang đăng xuất
    path('profile/', views.profile, name='profile'), #đường dẫn đến trang cá nhân
    path('password_change/', views.password_change, name='password_change'), #đường dẫn đến trang đổi mật khẩu
    path('run_code', views.run_code, name='run_code'), #API nhận code và trả về kết quả chạy code

    #các đường dẫn đến các trang liên quan đến việc quên mật khẩu, các views trong phần đổi mk này đã được django cung cấp sẵn
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='learningsite/password_reset.html'), name='password_reset'), #trang nhập email để gửi link reset mật khẩu
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='learningsite/password_reset_done.html'), name='password_reset_done'), #trang thông báo đã gửi link reset mật khẩu
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='learningsite/password_reset_confirm.html'), name='password_reset_confirm'), #trang nhập mật khẩu mới
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='learningsite/password_reset_complete.html'), name='password_reset_complete'), #trang thông báo đã đổi mật khẩu thành công

    path('tinymce/', include('tinymce.urls')), #thêm đường dẫn đến thư viện tinymce
    path('<slug:category_slug>/', views.category, name = 'category'), #đường dẫn đến danh mục bài học khi người dùng click vào 1 danh mục nào đó trên trang chủ
    path('<slug:category_slug>/<slug:lesson_slug>/', views.lesson, name='lesson'), #đường dẫn đến bài học khi người dùng click vào 1 bài học nào đó trong danh mục
    path('<slug:category_slug>/<slug:lesson_slug>/check/', views.check_lesson, name='check_lesson'), #đường dẫn đến trang kiểm tra bài tập khi người dùng click vào nút "Submit"
    path('<slug:category_slug>/<slug:lesson_slug>/ask_ai/', views.ask_ai, name='ask_ai'), #đường dẫn đến trang hỏi AI khi người dùng click vào nút "Ask AI"
    path('<slug:category_slug>/<slug:lesson_slug>/mark_completed/', views.mark_lesson_completed, name='mark_lesson_completed') #đường dẫn đến views đánh dấu bài học đã hoàn thành khi người dùng click vào nút "Đã đọc xong""
]