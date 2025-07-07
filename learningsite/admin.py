from django.contrib import admin

# Register your models here.
from .models import Category, Lesson, TestCase, UserLessonProgress

class CategoryAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug':('name',)} #tự động điền slug khi nhập tên danh mục
    list_display = ('name', 'layout', 'status', 'ordering') #các trường hiển thị trong danh sách danh mục khi thêm trên admin site
    list_filter = ['status', 'layout'] #tạo bộ lọc theo các trường trong danh sách danh mục
    search_fields = ['name']


    class Media: #thêm các file js trong static/my_admin/js để slug có thể tự đồng điền cả khi tên danh mục là tiếng việt
        js = (
            'my_admin/js/jquery-3.6.0.min.js', 
            'my_admin/js/slugify.min.js', 
            'my_admin/js/general.js'
        )
class TestCaseInline(admin.TabularInline): #hiển thị và chỉnh sửa testcase dạng bảng (tabular) trực tiếp trong lesson
    model = TestCase #liên kết với model TestCase
    extra = 1 #số lượng dòng trống để thêm mới testcase, ở đây là 1 dòng

class LessonAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug':('name',)} #tự động điền slug khi nhập tên bài học
    list_display = ('name', 'status', 'category', 'ordering') #các trường hiển thị trong danh sách danh mục khi thêm trên admin site
    list_filter = ['status', 'category'] #tạo bộ lọc theo các trường trong danh sách danh mục
    search_fields = ['name']
    inlines = [TestCaseInline] #hiển thị và chỉnh sửa testcase trực tiếp trong lesson

    class Media: #thêm các file js trong static/my_admin/js để slug có thể tự đồng điền cả khi tên danh mục là tiếng việt
        js = (
            'my_admin/js/jquery-3.6.0.min.js', 
            'my_admin/js/slugify.min.js', 
            'my_admin/js/general.js'
        )

admin.site.register(Category, CategoryAdmin) #đăng ký model Category với admin site 
admin.site.register(Lesson, LessonAdmin) #đăng ký model Lesson với admin site 
admin.site.register(TestCase) #đăng ký model TestCase với admin site, không cần tùy chỉnh gì vì đã có inline trong LessonAdmin
admin.site.register(UserLessonProgress) #đăng ký model UserLessonProgress với admin site, không cần tùy chỉnh gì vì chỉ dùng để lưu trữ tiến độ học tập của người dùng