#sử dụng python 3.11-slim làm base image
FROM python:3.11-slim 

#chỉ định thư mục làm việc
WORKDIR /app
#coppy file run_user_code.py vào thư mục làm việc hiện tại .
COPY run_user_code.py .

#mã CMD để chạy mã Python
CMD ["python", "run_user_code.py"]