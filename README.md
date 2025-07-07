# 🧠 CodeZilla-LearningSite

An AI-powered web-based programming learning platform built with **Django**, supporting three user roles:  
👤 **Administrators**, 🎓 **Learners**, and 👀 **Visitors**.

---

## 🚀 Features

### 👑 1. Administrator (Admin)
Admins have full control over the system:
- 🔐 Log in with admin privileges.
- 📚 Manage courses (add, update, delete).
- 📄 Manage lessons and 🧪 test cases.
- 👥 Manage user accounts.

### 👤 2. Guest Users
Unauthenticated users (guests) can:
- 📝 Register for a new account.
- 🔍 Search and view available courses and lesson lists.

### 🎓 3. Learners
Registered users can:
- 🔐 Log in, reset/change password, and view personal profile.
- 📘 Search and access courses and lessons.
- 🤖 Ask lesson-related questions to an AI chatbot for quick explanations.
- 💻 Write, run, and submit code to get real-time evaluation feedback.

### ⚙️ 4. System Requirements (Non-Functional)
- ⚡ Fast and accurate code execution/submission processing.
- 🔐 Secure handling of user data and learning results.
- 🤖 Smooth chatbot response with minimal delay.
- 🖥️ Clean, intuitive, and beginner-friendly interface.

---

## 📸 Screenshots

[Home Page] ![image](https://github.com/user-attachments/assets/26a63741-1de4-496d-a7b7-2913fd34273c)

[Search Page] ![image](https://github.com/user-attachments/assets/a89c9e72-c700-46f1-99d8-8fb1cb74aa5a)

[Sign up Page] ![image](https://github.com/user-attachments/assets/024e45f6-80c4-4fff-8c08-9173653140ea)

[Login Page] ![image](https://github.com/user-attachments/assets/61b2e9c9-8782-432c-a480-6cd333f28cf0)

[Password Reset Page] ![image](https://github.com/user-attachments/assets/944fa3ac-9cb8-4eb0-9bd9-c58f81f3a346)

[An email containing the link has been sent when reset password] ![image](https://github.com/user-attachments/assets/1f257772-cedb-4ae7-8452-4611f42b4c63)

[User Information Page] ![image](https://github.com/user-attachments/assets/a62c788d-3788-46ce-8de5-eab3cf708071)

[Password change Page] ![image](https://github.com/user-attachments/assets/736ec5ef-aa51-40c9-b16f-0f9cb35a4e4e)

[List Exercise Page] ![image](https://github.com/user-attachments/assets/1427835f-0db7-414b-862a-4c327edc4922)

[Exercise Page] ![image](https://github.com/user-attachments/assets/e0d23bdb-33bd-44f8-a52e-cebf86f225ce)
![image](https://github.com/user-attachments/assets/12a3011f-fcc5-4f94-ba90-b3fef33a7ae8)

[submission and a correct solution] ![image](https://github.com/user-attachments/assets/efd6fde5-8e9f-43ee-84bd-4a1ef0387390)
[submission and a fail solution] ![image](https://github.com/user-attachments/assets/ee7a322c-8c69-4a98-9bdc-323a9f75ef4f)

[Ask AI Assistant] ![image](https://github.com/user-attachments/assets/33b321b7-dd3c-4c1d-bec7-05ffbf202ffa)

---

## 🛠️ Getting Started

### 📦 Prerequisites

#### 💻 1. Visual Studio Code
- Version: **1.101.2** or later

#### 🐍 2. Python
- Version: **3.11.4** or later

#### 🌐 3. Django
- Version: **5.1.7** or later

#### 📚 4. Python Libraries

- Install via pip:

```bash
pip install django==5.1.7 tinymce openai==0.28 python-dotenv
```
##### Includes:

- 📝 tinymce – for rich text input

- 🤖 openai – to call OpenRouter API (v0.28)

- 🔐 python-dotenv – load environment variables from .env file

#### 🐳 5. Docker (for secure code execution)
- Docker Desktop for Windows (version **28.1.1** or later)

- Build Docker image:

```bash
docker build -t python-runner .
```
Run this in the folder where Dockerfile is located.

---
## ⚡ Quick Setup
### ⬇️ 1. Clone the Repository
```bash
git clone https://github.com/Zank4/CodeZilla-LearningSite.git
cd CodeZilla-LearningSite
```
### 🔑 2. Configure API Key
- Get a free API Key from OpenRouter.ai

- Recommended model: deepseek/deepseek-r1-0528-qwen3-8b:free

- In the root directory (where manage.py is), create a file named .env with:

```ini
OPENROUTER_API_KEY="your_api_key_here"
```
### 🗃️ 3. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```
### 👤 4. Create Admin User
```bash
python manage.py createsuperuser
```
### ▶️ 5. Run the Web Application
- Make sure Docker Desktop is running

- Start the server:

```bash
python manage.py runserver
Then visit: http://127.0.0.1:8000
```
---
## 📖 Documentation Reference
- 📚 CS50 Web Programming with Python and JavaScript: https://cs50.harvard.edu/web/

---
## 📬 Contact
- If you have questions or want to contribute:

- 📧 Email: huuvan877@gmail.com
