from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import *
# Create your views here.


def dashboard(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect("/login")
    
    user_data = getUserType(current_user)

    if user_data[1] == "teacher":
        print("teach")

    subjects = Subjects.objects.all()

    context = {
        'subjects': subjects,
        }
    return render(request, "dashboard.html", context)

def addSubject(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect("/login")
    
    user_data = getUserType(current_user)
    if(user_data[1] != "teacher"):
        return redirect("/")
    
    if request.method == "POST":
        sub_name= request.POST['sub_name']
        subject_id= request.POST['subject_id']
        enroll_id= "abcdefg"

        newSubject = Subjects(
            subject_name = sub_name,
            subject_id = subject_id,
            enroll_id = enroll_id,
        )
        newSubject.save()

        newTeacherSub = Teacher_Subject(
            teacher_id = user_data[0].teacher_id,
            subject_id = subject_id,
        )
        newTeacherSub.save()
        print("SUCCESS IN ADD SUB")

        return redirect("/")
    
    context = {
        'user_info': user_data[0],
    } 
    return render(request, "addSubject.html", context)

def handleTeacherSignup(request):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect("/")
    message = ""
    alert_type = ""
    valid = True

    if request.method == "POST":
        name= request.POST['name']
        teacher_id= request.POST['teacher_id']
        email= request.POST['email']
        phone= request.POST['phone']
        password1= request.POST['password1']
        password2= request.POST['password2']

        try:
            teacher = Teacher.objects.get(email = email)
        except:
            teacher = None
        # about
        if password1 != password2:
            valid = False
            message = "Passwords do not match"
            alert_type = "danger"

        if teacher is not None:
            valid = False
            message = "User already exists with this email address"
            alert_type = "danger"

        if valid == True:
            newUser = User.objects.create_user(name, email, password1)
            newUser.save()

            newTeacher = Teacher(
                teacher_id = teacher_id,
                email = email,
                name = name,
                phone = phone,
                )
            newTeacher.save()
            return redirect("/")

    context = {
        'message': message,
        'alert_type': alert_type
    }
    return render(request, "teacherSignup.html", context)

def handleStudentSignup(request):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect("/")
    message = ""
    alert_type = ""
    valid = True

    if request.method == "POST":
        name= request.POST['name']
        email= request.POST['email']
        student_id= request.POST['student_id']
        dob= request.POST['dob']
        password1= request.POST['password1']
        password2= request.POST['password2']

        try:
            student = Student.objects.get(email = email)
        except:
            student = None
        # about
        if password1 != password2:
            valid = False
            message = "Passwords do not match"
            alert_type = "danger"

        if student is not None:
            valid = False
            message = "User already exists with this email address"
            alert_type = "danger"

        if valid == True:
            newUser = User.objects.create_user(name, email, password1)
            newUser.save()

            newStudent = Student(
                student_id = student_id,
                email = email,
                name = name,
                dob = dob,
                )
            newStudent.save()
            return redirect("/")

    context = {
        'message': message,
        'alert_type': alert_type
    }
    return render(request, "studentSignup.html", context)

def handleLogin(request):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect("/")
    message = ""
    alert_type = ""

    if request.method == "POST":
        email= request.POST['email']
        password= request.POST['password']

        try:
            login_user = Teacher.objects.get(email = email)
        except:
            login_user = None
        
        if(login_user is None):
            try:
                login_user = Student.objects.get(email = email)
            except:
                login_user = None

        if login_user is not None:
            username = login_user.name
            user = authenticate(username = username,password = password)

            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                message = "Email or password is wrong"
                alert_type = "danger"
        
        if login_user is None:
            message = "User does exist. Please sign up"
            alert_type = "danger"

    context = {
        'message': message,
        'alert-type': alert_type
    }
    return render(request, 'login.html', context)

def handleLogout(request):
    current_user = request.user
    logout(request)
    return redirect("/login")

def getUserType(current_user):
    if current_user is not None:
        try:
            data = Student.objects.get(email = current_user.email)
            user_type = "student"
            return [data, user_type]
        except:
            data = Teacher.objects.get(email = current_user.email)
            user_type = "teacher"
            return [data, user_type]