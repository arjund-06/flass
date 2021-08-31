from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import *
import random
# Create your views here.


def dashboard(request):
    current_user = request.user
    if(current_user is None and current_user != "admin"):
        return redirect("/login")
    if current_user.is_authenticated == False:
        return redirect("/login")

    user_data = getUserType(current_user)

    subjects = []
    if user_data[1] == "teacher":
        sub_arr = Teacher_Subject.objects.filter(
            teacher_id=user_data[0].teacher_id)
    elif user_data[1] == "student":
        sub_arr = Student_Subject.objects.filter(
            student_id=user_data[0].student_id)

    for i in sub_arr:
        print(i.subject_id)
        subjects.append(Subjects.objects.get(subject_id=i.subject_id))

    context = {
        'subjects': subjects,
    }
    return render(request, "dashboard.html", context)


def addSubject(request):
    current_user = request.user
    if(current_user is None and current_user != "admin"):
        return redirect("/login")
    if current_user.is_authenticated == False:
        return redirect("/login")

    user_data = getUserType(current_user)

    if request.method == "POST":
        sub_name = request.POST['sub_name']
        subject_id = request.POST['subject_id']
        enroll_id = makeRandom()
        picture = request.FILES['picture']

        newSubject = Subjects(
            subject_name=sub_name,
            subject_id=subject_id,
            enroll_id=enroll_id,
            picture=picture,

        )
        newSubject.save()

        newTeacherSub = Teacher_Subject(
            teacher_id=user_data[0].teacher_id,
            subject_id=subject_id,
        )
        newTeacherSub.save()
        print("SUCCESS IN ADD SUB")

        return redirect("/")

    context = {
        'user_info': user_data[0],
    }
    return render(request, "addSubject.html", context)


def joinClass(request):
    message = ""
    alert_type = ""
    current_user = request.user
    print(current_user)
    if(current_user is None and current_user != "admin"):
        return redirect("/login")
    if current_user.is_authenticated == False:
        return redirect("/login")

    user_data = getUserType(current_user)

    if(user_data[1] != "student"):
        return redirect("/")

    if(request.method == "POST"):
        enroll_id = request.POST['enroll_id']
        try:
            subject_to_join = Subjects.objects.get(enroll_id=enroll_id)
            join = True
        except:
            join = False
            message = "Invalid Enroll Id. Please try again"
            alert_type = "danger"
            subject_to_join = None

        if(subject_to_join != None):
            try:
                stu_sub = Student_Subject.objects.get(subject_id=subject_to_join.subject_id)
                if(stu_sub.student_id == user_data[0].student_id):
                    message = "You are already in this subject"
                    alert_type = "danger"
                    join = False
            except:
                None

        if(join):
            newStudentSub = Student_Subject(
                subject_id=subject_to_join.subject_id,
                student_id=user_data[0].student_id,
            )
            newStudentSub.save()

            #checking for existing assignments
            assignments = Assignment.objects.filter(subject_id = subject_to_join.subject_id)
            if(len(assignments) > 0):
                for assignment in assignments:
                    newAssignmentStudent = Assignment_Student(
                        student_id= user_data[0].student_id,
                        assignment_id=assignment.assignment_id,
                        status= "Not Submitted",
                        marks= "0",
                    )
                    newAssignmentStudent.save()

            redirect_string = "subject/" + str(subject_to_join.subject_id)
            return redirect(redirect_string)

    context = {
        'message': message,
        'alert_type': alert_type,
    }
    return render(request, "joinClass.html")


def showSubject(request, path_sub_id):
    current_user = request.user
    if(current_user is None and current_user != "admin"):
        return redirect("/login")
    if current_user.is_authenticated == False:
        return redirect("/login")

    # data for the subject page
    subject_data = Subjects.objects.get(subject_id=path_sub_id)
    teacher_sub_rel = Teacher_Subject.objects.get(
        subject_id=subject_data.subject_id)
    teacher_data = Teacher.objects.get(teacher_id=teacher_sub_rel.teacher_id)

    # data to check if user is in the class or not
    user_data = getUserType(current_user)
    if(user_data[1] == "student"):
        student_sub_rel = Student_Subject.objects.filter(
            subject_id=path_sub_id).filter(student_id=user_data[0].student_id)
        if(len(student_sub_rel) > 0):
            verified = True
        else:
            verified = False
        
        assignments = []
        if(verified):
            student_asi_rel = Assignment_Student.objects.filter(student_id = user_data[0].student_id)
            for student_asi in student_asi_rel:
                assignment = Assignment.objects.get(assignment_id = student_asi.assignment_id)
                if(assignment.subject_id == path_sub_id and assignment.assignment_type == "Asi"):
                    assignments.append(assignment)
    else:
        teacher_sub_rel_verify = Teacher_Subject.objects.filter(
            subject_id=path_sub_id).filter(teacher_id=user_data[0].teacher_id)
        if(len(teacher_sub_rel_verify) > 0):
            verified = True
        else:
            verified = False
        assignments = []

    context = {
        'subject': subject_data,
        'teacher': teacher_data,
        'verified': verified,
        'user_type': user_data[1],
        'assignments': assignments,
    }
    return render(request, "subject.html", context)


def addAssignment(request, path_sub_id):
    current_user = request.user
    if(current_user is None and current_user != "admin"):
        return redirect("/login")
    if current_user.is_authenticated == False:
        return redirect("/login")

    user_data = getUserType(current_user)

    if(user_data[1] != "teacher"):
        return redirect("/")

    if request.method == "POST":
        assignment_title = request.POST['assignment_title']
        assignment_id = makeRandom()

        newAssignment = Assignment(
            assignment_id=assignment_id,
            assignment_title=assignment_title,
            assignment_type="Asi",
            teacher_id=user_data[0].teacher_id,
            subject_id=path_sub_id,
        )
        newAssignment.save()

        student_sub_rel = Student_Subject.objects.filter(subject_id = path_sub_id)
        if(len(student_sub_rel) > 0):
            for stu in student_sub_rel:
                newAssignmentStudent = Assignment_Student(
                    student_id= stu.student_id,
                    assignment_id= assignment_id,
                    status= "Not Submitted",
                    marks= "0",
                )
                newAssignmentStudent.save()
        redirect_string = "/subject/" + str(path_sub_id)
        return redirect(redirect_string)
    
    context = {
        'path_sub_id': path_sub_id
    }
    return render(request, "addAssignment.html", context)


def handleTeacherSignup(request):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect("/")
    message = ""
    alert_type = ""
    valid = True

    if request.method == "POST":
        name = request.POST['name']
        teacher_id = request.POST['teacher_id']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        try:
            teacher = Teacher.objects.get(email=email)
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
                teacher_id=teacher_id,
                email=email,
                name=name,
                phone=phone,
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
        name = request.POST['name']
        email = request.POST['email']
        student_id = request.POST['student_id']
        dob = request.POST['dob']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        try:
            student = Student.objects.get(email=email)
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
                student_id=student_id,
                email=email,
                name=name,
                dob=dob,
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
        email = request.POST['email']
        password = request.POST['password']

        try:
            login_user = Teacher.objects.get(email=email)
        except:
            login_user = None

        if(login_user is None):
            try:
                login_user = Student.objects.get(email=email)
            except:
                login_user = None

        if login_user is not None:
            username = login_user.name
            user = authenticate(username=username, password=password)

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
            data = Student.objects.get(email=current_user.email)
            user_type = "student"
            return [data, user_type]
        except:
            data = Teacher.objects.get(email=current_user.email)
            user_type = "teacher"
            return [data, user_type]


def makeRandom():
    res = ""
    rand = random.randint(97, 122)
    res = res + str(chr(rand))
    rand = random.randint(97, 122)
    res = res + str(chr(rand))
    res = res + str(random.randint(0, 9))
    rand = random.randint(97, 122)
    res = res + str(chr(rand))
    res = res + str(random.randint(0, 9))
    rand = random.randint(97, 122)
    res = res + str(chr(rand))
    return res
