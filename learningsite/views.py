from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
import subprocess, tempfile, os
from django.views.decorators.csrf import csrf_protect
import openai
from dotenv import load_dotenv
from django.utils import timezone
from django.views.decorators.http import require_POST

# Create your views here.
def home(request):
    query = request.GET.get('q', '') #lấy giá trị của query từ url, nếu không có thì mặc định là None
    categories = Category.objects.filter(status='published')
    if query: #nếu có giá trị của query thì lọc danh sách category theo tên
        categories = categories.filter(name__icontains=query) #lọc danh sách category theo tên, sử dụng icontains để tìm kiếm không phân biệt chữ hoa chữ thường
    return render(request, "learningsite/home.html", {"categories": categories, "query": query}) #gọi đến home.html và truyền vào biến categories để hiển thị danh sách bài học


def category(request, category_slug): 
    
    category = get_object_or_404(Category,slug=category_slug) #lấy danh mục bài học theo slug

    lessons = Lesson.objects.filter(category=category, status="published") #lấy tất cả các bài học có trạng thái published trong danh mục này, dựa vào khóa ngoại category trong model Lesson có related_name là lessons
    # Nếu user đã đăng nhập thì lấy tiến độ, chưa đăng nhập thì không
    if request.user.is_authenticated:
        completed_ids = list(UserLessonProgress.objects.filter(
            user=request.user, lesson__in=lessons, is_completed=True
        ).values_list('lesson_id', flat=True))
        total = lessons.count()
        completed = len(completed_ids)
        percent = int(completed / total * 100) if total else 0
    else:
        completed_ids = []
        percent = None

    return render(request, "learningsite/category.html", {
        "category": category,
        "lessons": lessons,
        "completed_ids": completed_ids,
        "percent": percent,
    })

def lesson(request, category_slug, lesson_slug):
    if not request.user.is_authenticated: #nếu người dùng chưa đăng nhập thì chuyển hướng về trang đăng nhập
        return redirect(f"{reverse('login')}?next={request.path}") #chuyển hướng về trang đăng nhập, truyền tham số next để lưu url bài học hiện tại đang vào để sau khi đăng nhập sẽ chuyển về lại đúng bài học đó
    #lấy bài học theo slug
    lesson = get_object_or_404(Lesson,slug=lesson_slug, category__slug=category_slug) #lấy bài học theo slug
    category = get_object_or_404(Category,slug=category_slug) #lấy danh mục bài học theo slug
    testcases = lesson.testcases.all() #lấy tất cả các testcase của bài học này, dựa vào khóa ngoại lesson trong model TestCase có related_name là testcases

    #lấy tất cả bài học trong category này, sắp xếp theo ordering
    lessons = Lesson.objects.filter(category=category).order_by('ordering')
    lesson_list = list(lessons) #chuyển queryset thành list để có thể lấy index của bài học này trong danh sách bài học
    lesson_index = lesson_list.index(lesson) #lấy index của bài học này trong danh sách bài học

    #xác định bài học trước và bài học sau
    prev_lesson = lesson_list[lesson_index - 1] if lesson_index > 0 else None #nếu bài học này không phải là bài học đầu tiên thì lấy bài học trước đó, nếu là bài học đầu tiên thì không có bài học trước
    next_lesson = lesson_list[lesson_index + 1] if lesson_index < len(lesson_list) - 1 else None #nếu bài học này không phải là bài học cuối cùng thì lấy bài học sau đó, nếu là bài học cuối cùng thì không có bài học sau 

    
    return render(request, "learningsite/lesson.html",{
        "lesson": lesson,
        "category": category,
        "prev_lesson": prev_lesson,
        "next_lesson": next_lesson,
        "testcases": testcases, #truyền vào biến testcases để dựa vào đó biết bài nào là bài tập(có testcase), bài nào là lý thuyết(không có testcase) để biết hiển thị nút submit code hay không
    })

def register(request):
    form = CreateUserForm() 
    if request.method == "POST":
        form = CreateUserForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Bạn có thể đăng nhập.")
            return redirect('login')
        else:
            # Hiển thị tất cả lỗi chi tiết cho từng trường
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return render(request, "learningsite/register.html", {"form": form})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home') #nếu người dùng đã đăng nhập thì chuyển hướng về trang chủ
    
    next_url = request.GET.get('next') #lấy giá trị của tham số next trong url, nếu không có thì mặc định là None
    
    if request.method == "POST":
        username = request.POST.get('username') #lấy tên đăng nhập từ form
        password = request.POST.get('password') #lấy mật khẩu từ form
        user = authenticate(request, username=username, password=password) #kiểm tra xem tên đăng nhập và mật khẩu có hợp lệ không
        if user is not None: #nếu hợp lệ thì đăng nhập
            login(request, user) #đăng nhập

            if request.POST.get('next'): #nếu đnhap thành công và có tham số next gửi đi thì chuyển hướng về trang bài học trong next đó
                return redirect(request.POST.get('next')) 
            elif next_url: #thêm kiểm tra này tránh TH lỗi ở if đầu tiên, ta vẫn có next_url đã lấy ở trên thanh url 
                return redirect(next_url)
            else:
                return redirect('home') #(ko có tham số next), chuyển hướng về trang chủ
        else:
            messages.info(request, "Tên đăng nhập hoặc mật khẩu không đúng")
            return redirect('login')  
    
    #nếu không phải là POST thì hiển thị form đăng nhập
    return render(request, "learningsite/login.html") #gọi đến login.html

def logoutPage(request):
    logout(request) #đăng xuất
    return redirect('home') #chuyển hướng về trang chủ

@login_required #yêu cầu người dùng phải đăng nhập mới có thể truy cập vào trang này
def profile(request):
    return render(request, "learningsite/profile.html", {"user": request.user}) #gọi đến profile.html, truyền vào biến user để hiển thị thông tin người dùng

@login_required #yêu cầu người dùng phải đăng nhập mới có thể truy cập vào trang này
def password_change(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user #lấy thông tin người dùng hiện tại
        if not user.check_password(current_password):
            messages.error(request, "Mật khẩu hiện tại không đúng")
        elif new_password != confirm_password:
            messages.error(request, "Mật khẩu mới và xác nhận mật khẩu không khớp")
        else:
            user.set_password(new_password) #đặt lại mật khẩu mới cho user
            user.save() #lưu lại
            update_session_auth_hash(request, user) #cập nhật session auth hash để không bị đăng xuất khi đổi mật khẩu
            messages.success(request, "Đổi mật khẩu thành công")
            
    return render(request, "learningsite/password_change.html")

#hàm chạy để cho code vào docker và chạy đảm bảo an toàn
def run_code_in_docker(code, input_data=""):
    with tempfile.TemporaryDirectory() as tmpdir: #tạo thư mục tạm thời để lưu code, sau khi chạy xong sẽ tự động xóa thư mục này
        code_path = os.path.join(tmpdir, "main.py") #tạo đường dẫn đến file code trong thư mục tạm thời
        with open(code_path, "w", encoding="utf-8") as f: #mở file code để ghi
            f.write(code)

        try:
            result = subprocess.run(
                [
                    "docker", "run", "--rm", "-i",
                    "--network", "none", # không cho phép kết nối mạng,
                    "--memory", "128m", #giới hạn bộ nhớ RAM 128MB
                    "--cpus", "0.5", #giới hạn chỉ dùng 0.5 CPU core tránh lạm dụng máy chủ
                    "-v", f"{code_path}:/app/main.py", #gắn file code vào docker
                    "python-runner" # tên image docker đã build sẵn
                ],
                input = input_data.encode(), #chuyển input_data thành bytes để đưa vào stdin của docker
                stdout = subprocess.PIPE, #lấy đầu ra chuẩn của docker
                stderr = subprocess.STDOUT, #lấy lỗi của docker nếu có và gộp chung vào stdout để xử lí 1 stdout gồm cả kết quả và lỗi
                timeout = 5 #thời gian chạy tối đa là 5 giây, tránh lạm dụng máy chủ
            )
            return result.stdout.decode() #trả về kết quả stdout của docker sau khi chạy code, decode để chuyển từ bytes sang string
        except subprocess.TimeoutExpired:
            return "Quá thời gian thực thi!"
        except Exception as e:
            return f"Lỗi: {e}"

# API để nhận code từ người dùng và trả về kết quả chạy code, sử dụng hàm run_code_in_docker để chạy code trong docker
@csrf_protect 
def run_code(request): 
    if request.method == "POST":
        code = request.POST.get('code', "")
        input_data = request.POST.get('input', "") #lấy dữ liệu đầu vào từ form, nếu không có thì mặc định là rỗng
        output = run_code_in_docker(code, input_data) #gọi hàm run_code_in_docker để chạy code trong docker, truyền vào code và input_data
        return JsonResponse({"output": output}) #trả về kết quả chạy code dưới dạng JSON, lưu vào biến output
    return JsonResponse({"output": "chỉ hỗ trợ POST request!"}) #nếu method khác post (vd người dùng truy cập trực tiếp đường dẫn /run_code tức là đang dùng GET thì sẽ báo lỗi này)


def check_lesson(request, category_slug, lesson_slug): #chạy code trong bài tập với các test case sẵn có
    if request.method == "POST":
        lesson = get_object_or_404(Lesson, slug=lesson_slug, category__slug=category_slug)
        code = request.POST.get('code', '')
        test_cases = lesson.testcases.all()
        all_passed = True
        results = []
        for test_case in test_cases:
            # Làm sạch input trong testcase: loại bỏ khoảng trắng đầu/cuối mỗi dòng và bỏ dòng trống
            cleaned_input = "\n".join(
                [line.strip() for line in test_case.input_data.strip().splitlines() if line.strip() != ""]
            )
            output = run_code_in_docker(code, cleaned_input).strip() #output của user
            expected = test_case.expected_output #output mong đợi từ testcase

            # So sánh từng dòng ouput của học sinh với ouput của testcase, loại bỏ khoảng trắng thừa
            output_lines = [line.strip() for line in output.strip().splitlines() if line.strip() != ""]
            expected_lines = [line.strip() for line in expected.strip().splitlines() if line.strip() != ""]
            passed = output_lines == expected_lines 

            if not passed:
                all_passed = False
            results.append({
                'input': test_case.input_data,
                'expected': test_case.expected_output,
                'actual': output,
                'passed': passed
            })
        # Format kết quả
        result_html = "<div class='mb-2'>"
        if all_passed:
            result_html += "<h5 class='text-success'>Chúc mừng! Bài làm của bạn đã đúng!</h5>"
            UserLessonProgress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={'is_completed': True, 'completed_at': timezone.now()} #cập nhật tiến độ học tập của người dùng, đánh dấu là đã hoàn thành bài tập này
            )
        else:
            result_html += "<h5 class='text-danger'>Bài làm chưa đúng. Chi tiết test case:</h5>"
        for index, result in enumerate(results, 1):
            result_html += f"<div class='mb-2'><strong>Test case #{index}:</strong> "
            if result['passed']:
                result_html += "<span class='text-success'>Đúng</span><br>"
            else:
                result_html += f"<span class='text-danger'>Sai</span><br>"
                result_html += f"Input: {result['input']}<br>"
                result_html += f"Expected output: {result['expected']}<br>"
                result_html += f"Your output: {result['actual']}"
            result_html += "</div>"
        result_html += "</div>"
        return JsonResponse({"result": result_html})
    return JsonResponse({"result": "Chỉ hỗ trợ POST request!"})

# đánh dấu bài học lý thuyết đã hoàn thành khi user click nút đã đọc xong, sử dụng model UserLessonProgress để lưu trữ tiến độ học tập của người dùng
@require_POST
@login_required
def mark_lesson_completed(request, category_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug, category__slug=category_slug)
    UserLessonProgress.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'is_completed': True, 'completed_at': timezone.now()}
    )
    return JsonResponse({'success': True})

#xử lý câu hỏi của người dùng gửi lên AI, sử dụng OpenRouter (model DeepSeek) để trả lời câu hỏi liên quan đến bài học
def ask_ai(request, category_slug, lesson_slug):
    if request.method == "POST": 
        question = request.POST.get("question", "")
        code = request.POST.get("code", "")
        #lesson = get_object_or_404(Lesson, slug=lesson_slug, category__slug=category_slug)

        # Pre-prompt: Cài đặt ngữ cảnh, vai trò, giới hạn AI chỉ trả lời về lập trình: lý thuyết, code, lỗi, ví dụ...
        pre_prompt = (
            "Bạn là trợ lý AI chuyên về lập trình. " #kỹ thuật role based prompt (định nghĩa vai trò của AI, tạo context chuyên môn)
            #instructions following để hướng dẫn AI trả lời câu hỏi của người dùng
            "NHIỆM VỤ:\n"
            "1. Chỉ trả lời các câu hỏi liên quan đến lập trình, các câu hỏi không liên quan bạn sẽ trả lời bằng 1 câu: 'Tôi chỉ trả lời các câu hỏi liên quan tới lập trình'. " #fine-tuning AI để chỉ trả lời các câu hỏi liên quan đến lập trình
            "2. Nếu người dùng hỏi về lý thuyết, khái niệm lập trình, hãy trả lời rõ ràng, chi tiết, kèm ví dụ code Python minh họa. "
            "3. Nếu người dùng hỏi về đánh giá code, hãy phân tích, đánh giá code của người dùng và giải thích rõ ràng. "
            "4. Nếu người dùng hỏi về cách làm bài tập, hãy hướng dẫn từng bước, giải thích rõ ràng, ngắn gọn và cung cấp ví dụ code Python. "
            "5. Nếu người dùng hỏi về lỗi, hãy chỉ ra lỗi và gợi ý sửa. "
            "Phong cách trả lời: Sử dụng ngôn ngữ tiếng Việt, rõ ràng, ngắn gọn, dễ hiểu. "
        )

        # Tạo prompt cho AI, context injection để AI hiểu rõ bài tập và code của người dùng
        full_prompt = f"{pre_prompt}\n\nCode của người dùng:\n{code}\n\nCâu hỏi của người dùng: {question}"

        # Cấu hình OpenRouter 
        load_dotenv() # Tải biến môi trường từ file .env ở thư mục gốc
        openai.api_key = os.environ.get("OPENROUTER_API_KEY") #lấy API key từ biến môi trường OPENROUTER_API_KEY ở file .env
        openai.api_base = "https://openrouter.ai/api/v1"

        response = openai.ChatCompletion.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",  #Sử dụng model DeepSeek chat trên OpenRouter
            messages=[
                {"role": "system", "content": pre_prompt},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=600, #kiểm soát độ dài câu trả lời của AI, tránh quá dài 
            temperature=0.7, #temperature control cân bằng giữa tính sáng tạo và chính xác của câu trả lời
        )
        answer = response.choices[0].message.content.strip()
        return JsonResponse({"answer": answer})
    return JsonResponse({"answer": "Chỉ hỗ trợ POST request!"})