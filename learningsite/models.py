from django.db import models
from tinymce.models import HTMLField #thư viện để tạo trường nhập liệu cho bài học, có thể định dạng văn bản như in đậm, in nghiêng, gạch chân,... giống như word
from django.core.exceptions import ValidationError #thư viện để kiểm tra dữ liệu nhập vào có hợp lệ hay không
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User #thư viện để tạo form đăng ký người dùng
# Create your models here.

class CreateUserForm(UserCreationForm): #tạo lại form đăng ký người dùng, kế thừa từ UserCreationForm
    class Meta:
        model = User 
        fields = ['username', 'email', 'first_name','last_name', 'password1', 'password2']
    
    def clean_email(self): #trong from đăng ký, kiểm tra email đã được sử dụng hay chưa
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email này đã được sử dụng.")
        return email
    
    def __init__(self, *args, **kwargs): #khởi tạo lại form, để có thể gắn class và placeholder cho từng trường
        super(CreateUserForm, self).__init__(*args, **kwargs)
        
        # Gắn class và placeholder cho từng trường
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

class Category(models.Model): #danh mục các bài học (VD: Lập trình C, Lập trình Python,...)
    
    LAYOUT_CHOICE = (
        ('grid', 'Grid'),
        ('list', 'List'),
    )
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/categories', blank=True, null=True) #hình ảnh đại diện cho danh mục này
    description = models.TextField(max_length=300, blank=True, default="")  # Thêm trường mô tả ngắn
    layout = models.CharField(max_length=100, choices= LAYOUT_CHOICE, default='grid') #kiểu hiển thị của danh mục này là grid(lưới) hay list
    status = models.CharField(max_length=100, choices= STATUS_CHOICE, default='draft') #trạng thái của danh mục này là hiển thị hay chỉ là nháp (draft)
    ordering = models.IntegerField(default=0) #thứ tự hiển thị của danh mục này trên trang chủ

    def __str__(self):
        return self.name
    
    def clean(self):
    # Kiểm tra trùng ordering (trừ chính nó khi update), để đảm bảo ordering các category sẽ không được chọn trùng nhau
        if Category.objects.filter(ordering=self.ordering).exclude(pk=self.pk).exists():
            raise ValidationError({'ordering': 'Ordering already exists.'})
    
    class Meta:
        ordering = ['ordering']

class Lesson(models.Model): #các bài học trong danh mục (VD: Danh mục Lập trình C có Bài 1: Intro, Bài 2: Biến,...)
  
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    LESSON_TYPE_CHOICES = [
        ('theory', 'Lý thuyết'),
        ('exercise', 'Bài tập'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.CharField(max_length=100, choices= STATUS_CHOICE, default='draft') #trạng thái của danh mục này là hiển thị hay chỉ là nháp (draft)
    ordering = models.IntegerField(default=0) #thứ tự hiển thị của danh mục này trên trang chủ
    publish_date = models.DateTimeField() #ngày giờ xuất bản bài học này, có thể đặt để đến 1 ngày sẽ published 
    content = HTMLField() #nội dung bài học này, có thể định dạng văn bản như in đậm, in nghiêng, gạch chân,... giống như word
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='lessons') #khóa ngoại đến danh mục của bài học này
    lesson_type = models.CharField(
        max_length = 10,
        choices= LESSON_TYPE_CHOICES,
        default='theory' #mặc định là lý thuyết, có thể là bài tập
    )
    def __str__(self):
        return self.name
    
    def clean(self):
    # Kiểm tra lesson có bị trùng ordering trong cùng category (trừ chính nó khi update), để đảm bảo ordering các bài sẽ không được chọn trùng nhau
        if Lesson.objects.filter(category=self.category, ordering=self.ordering).exclude(pk=self.pk).exists():
            raise ValidationError({'ordering': 'Ordering already exists.'})
    
    class Meta:
        ordering = ['ordering']

class UserLessonProgress(models.Model): #model này không cần chỉnh sửa gì, chỉ dùng để lưu trữ tiến độ học tập của người dùng
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson', 'is_completed') 

class TestCase(models.Model): #lesson lý thuyết thì không có testcase, lesson bài tập thì có 
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='testcases')
    input_data = models.TextField(blank=True) #dữ liệu kiểm tra của bài tập này, có thể để trống nếu không có dữ liệu kiểm tra
    expected_output = models.TextField() #đầu ra mong đợi của bài tập này
    ordering = models.IntegerField(default=0) #thứ tự hiển thị của testcase này trong bài tập

    def __str__(self):
        return f"{self.lesson.name} - Test Case {self.ordering}"
    
    class Meta:
        ordering = ['ordering']