from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegForm,LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Student
from hostel.models import Room
@login_required
def registration(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            # Create the user using the cleaned data from the form
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()  # Save the user to the database
            
            # Now save the registration info to the Student model
            student = form.save(commit=False)
            # Optionally link Student to User if there's a ForeignKey
            student.user = user  # Uncomment if you have a ForeignKey
            student.save()

            return redirect('admission:index') 
    else:
        form = RegForm()

    context = {'form': form}
    return render(request, 'admission/register.html', context)
def LoginView(request):
    page = 'login'
    form = LoginForm()  # Initialize the form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')  # Use cleaned_data
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print('user logged in successfull')
                return redirect('admission:index')  # Ensure redirect is returned
            else:
                form.add_error(None, 'Invalid username or password')  # Add error message
    context = {'page': page, 'form': form}  # Include the form in context
    return render(request, 'admission/login.html', context)  # Pass context
@login_required
def index(request):
    studentcount = Student.objects.count()
    roomcount = Room.objects.count()

    context = {'studentcount':studentcount,'roomcount':roomcount}
    return render(request,'admission/index.html',context)

def LogoutView(request):
    logout(request)
    return redirect('admission:login')

def veiewStudents(request):
    students = Student.objects.all()
    context = {'students':students}
    return render(request,'admission/students.html',context)

def deletestudent(request, pk):
    student = User.objects.get(pk = pk)
    student.delete()
    return redirect('admission:viewstudents')

def updatedetails(request, pk):
    user = User.objects.get(pk = pk)
    student = Student.objects.get(user = user)
    form = RegForm(instance=student)
    if request.method == 'POST':
        form = RegForm(request.POST, instance=student)
        if form.is_valid():
            student.save()
            return redirect('admission:viewstudents')
        else:
            print(form.errors)  # Add this line to debug

    context = {'form':form}
    return render(request,'admission/updatedetails.html',context)