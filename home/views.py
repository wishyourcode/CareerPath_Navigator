from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm, CustomUserCreationForm
from django.forms import inlineformset_factory
from .models import Question, Answer, CustomUser
from django.contrib import messages
from .forms import RejectionForm
from .models import Quiz
from django.views.decorators.http import require_http_methods
from .forms import CareerForm
import joblib
import pandas as pd
import os
from django.conf import settings

def home(request):
    return render(request, 'home.html')
def dashboard(request):
    return render(request, 'home/dashboard.html')

def about_us(request):
    return render(request, 'about.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def explore(request):
    return render(request, 'explore.html')
def Collage(request):
    return render(request, 'Collage.html')

def Consult(request):
    return render(request, 'consult.html')

def index(request):
    quiz = Quiz.objects.all()
    para = {'quiz': quiz}
    return render(request, "home/index.html", para)

@login_required(login_url='/login')
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "home/quiz.html", {'quiz': quiz})

def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

def save_quiz_view(request, myid):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken', None)

        for k in data_.keys():
            print('key: ', k)
            try:
                question = Question.objects.get(text=k)
                questions.append(question)
            except Question.DoesNotExist:
                continue

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected:
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})

        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)

        return JsonResponse({'passed': True, 'score': score, 'marks': marks})

    return JsonResponse({'passed': False, 'error': 'Not an AJAX request.'}, status=400)


def Logout(request):
    logout(request)
    return render(request, "home/home.html")


@login_required(login_url='/login')
def add_quiz(request):
    quizzes = Quiz.objects.all()
    if request.method == "POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save()
            return render(request, "home/add_quiz.html", {
                'form': QuizForm(),  # Return empty form for new entries
                'success': True,
                'quiz_id': quiz.id,
                'obj': quiz,  # Keeping your original obj if needed elsewhere
                'quizzes': quizzes  # Include quizzes in success response
            })
    else:
        form = QuizForm()
    
    return render(request, "home/add_quiz.html", {
        'form': form,
        'success': False,
        'quizzes': quizzes  # Include quizzes in initial response
    })
@login_required(login_url='/login')
def confirm_delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'home/confirm_delete_quiz.html', {'quiz': quiz})
@login_required(login_url='/login')
def delete_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.delete()
        return redirect('add_quiz')  # Redirect to the add_quiz page after deletion
    return redirect('home/confirm_quiz_delete', quiz_id=quiz_id)
@login_required(login_url='/login')
def add_question(request):
    questions = Question.objects.all().order_by('-id')
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_question')
    else:
        form = QuestionForm()
    return render(request, "home/add_question.html", {'form': form, 'questions': questions})
@login_required(login_url='/login')
def delete_question(request, myid):
    question = get_object_or_404(Question, id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('/add_question')
    return render(request, "home/delete_question.html", {'question': question})


@login_required(login_url='/login')
def add_options(request, myid):
    question = get_object_or_404(Question, id=myid)
    AnswerFormSet = inlineformset_factory(
        Question, 
        Answer, 
        fields=('text', 'correct')
    )
    
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, instance=question)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.question = question  # Ensure relationship is set
                instance.save()
            alert = True
            return render(request, "home/add_options.html", {
                'alert': alert,
                'question': question,
                'formset': AnswerFormSet(instance=question)  # Return fresh formset
            })
    else:
        formset = AnswerFormSet(instance=question)
    
    return render(request, "home/add_options.html", {
        'formset': formset,
        'question': question
    })
def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "home/results.html", {'marks': marks})

def delete_result(request, myid):
    marks = get_object_or_404(Marks_Of_User, id=myid)
    if request.method == "POST":
        marks.delete()
        return redirect('results')
    return render(request, "home/delete_result.html", {'marks': marks})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Handle faculty approval
            if user.role == 'faculty':
                user.is_active = False
                user.is_approved = False
                user.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'requires_approval': True,
                        'message': "Your account has been created but requires admin approval."
                    })
                messages.info(request, "Your account requires admin approval.")
            
            # Handle admin creation restriction
            elif user.role == 'admin' and not request.user.is_superuser:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': "Only superusers can create admin accounts."
                    })
                messages.error(request, "Only superusers can create admin accounts.")
                return redirect('signup')
            
            user.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': "Account created successfully!"
                })
            
            messages.success(request, "Account created successfully.")
            return redirect('login')
        
        # Form is invalid
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data()
            })
        
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'home/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Faculty approval check (added to your existing code)
            if user.role == 'faculty' and not user.is_approved:
                if hasattr(user, 'rejection_reason') and user.rejection_reason:
                    messages.error(request, 
                        f"Your faculty account was rejected. Reason: {user.rejection_reason}"
                    )
                else:
                    messages.error(request, "Your faculty account is not yet approved.")
                return redirect('login')
            
            # Your existing active check
            if user.role == 'faculty' and not user.is_active:
                messages.error(request, "Your faculty account is not yet approved.")
                return redirect('login')
            
            # Your existing successful login
            login(request, user)
            return redirect('index')
            
        else:
            # Your existing invalid credentials handling
            messages.error(request, "Invalid credentials.")
            return redirect('login')
    
    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login')
def clear_success_message(request):
    if request.method == 'POST':
        # Clear all messages
        storage = messages.get_messages(request)
        storage.used = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
@login_required(login_url='/login')
def pending_approvals(request):
    pending = CustomUser.objects.filter(role='faculty', is_approved=False,rejection_reason__isnull=True)
    return render(request, 'home/pending_approvals.html', {
        'pending_faculty': pending,
        'pending_count': pending.count()
    })
@login_required(login_url='/login')
def approve_faculty(request, user_id):
    faculty = get_object_or_404(CustomUser, id=user_id, role='faculty', is_approved=False)
    faculty.is_approved = True
    faculty.is_active = True # Activate the user account
    faculty.rejection_reason = None  
    faculty.save()
    messages.success(request, f"Approved faculty member: {faculty.full_name}")
    return redirect('pending_approvals')
@login_required(login_url='/login')
def reject_faculty(request, user_id):
    faculty = get_object_or_404(CustomUser, id=user_id, role='faculty', is_approved=False)
    
    if request.method == 'POST':
        form = RejectionForm(request.POST)
        if form.is_valid():
            faculty.rejection_reason = form.cleaned_data['reason']
            faculty.is_approved = False  # Explicitly set to False
            faculty.save()
            faculty.delete()
            messages.warning(request, f"Rejected faculty application for {faculty.full_name}")
            return redirect('pending_approvals')
    else:
        form = RejectionForm()
    
    return render(request, 'home/reject_faculty.html', {
        'faculty': faculty,
        'form': form
    })
@login_required(login_url='/login')
def approved_faculty(request):
    # Filter for approved faculty members (role='faculty' and is_approved=True)
    approved_faculty = CustomUser.objects.filter(
        role='faculty', 
        is_approved=True
    ).order_by('-date_joined')
    
    context = {
        'approved_faculty': approved_faculty
    }
    return render(request, 'home/approved_faculty.html', context)
@login_required(login_url='/login')
def delete_faculty(request, faculty_id):
    faculty = get_object_or_404(CustomUser, id=faculty_id, role='faculty')
    
    if request.method == 'POST':
        username = faculty.username
        faculty.delete()
        messages.success(request, f'Faculty member {username} has been deleted successfully.')
        return redirect('approved_faculty')
    
    context = {'faculty': faculty}
    return render(request, 'home/confirm_delete.html', context)


@login_required(login_url='/login')
def student_list_view(request):
    # Only show students (role='student') who are active
    students = CustomUser.objects.filter(role='student', is_active=True).order_by('date_joined')
    return render(request, 'home/student_list.html', {'students': students})


def confirm_student_delete_view(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id, role='student')
    return render(request, 'home/student_confirm_delete.html', {'student': student})

@require_http_methods(["DELETE"])
def delete_student_view(request, student_id):
    if not request.user.is_staff and not request.user.is_superuser:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        messages.error(request, "Permission denied")
        return redirect('student_list')
    student = get_object_or_404(CustomUser, id=student_id, role='student')
    student.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Student deleted successfully'})
    
    messages.success(request, "Student deleted successfully")
    return redirect('student_list')


def load_ml_assets():
    try:
        model_path = os.path.join(settings.BASE_DIR, 'ml_model', 'career_model.pkl')
        scaler_path = os.path.join(settings.BASE_DIR, 'ml_model', 'scaler.pkl')
        encoders_path = os.path.join(settings.BASE_DIR, 'ml_model', 'label_encoders.pkl')

        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        label_encoders = joblib.load(encoders_path)

        return model, scaler, label_encoders, None
    except Exception as e:
        return None, None, None, f"Error loading ML assets: {str(e)}"
def career_predict(request):
    prediction = None
    form_errors = None
    model, scaler, label_encoders, load_error = load_ml_assets()

    if load_error:
        form_errors = [load_error]
    
    if request.method == "POST":
        form = CareerForm(request.POST)
        if form.is_valid() and model:
            try:
                data = form.cleaned_data
                stream = data['stream']
                interest = data['interest']

                row = {
                    'Class10%': data['class10'],
                    'Class11%': data['class11'],
                    'Stream': label_encoders['Stream'].transform([stream])[0],
                    'Interest': label_encoders['Interest'].transform([interest])[0],
                }

                subject_map = {
                    "Physics": data.get("physics", 0),
                    "Chemistry": data.get("chemistry", 0),
                    "Maths": data.get("maths", 0),
                    "Biology": data.get("biology", 0),
                    "English": data.get("english", 0),
                    "Accountancy": data.get("accountancy", 0),
                    "Business Studies": data.get("business_studies", 0),
                    "Economics": data.get("economics", 0),
                    "History": data.get("history", 0),
                    "Geography": data.get("geography", 0),
                    "Political Science": data.get("political_science", 0),
                    "Sociology": data.get("sociology", 0),
                    "Psychology": data.get("psychology", 0),
                }

                stream_subjects = {
                    "Science-Maths": ["Physics", "Chemistry", "Maths", "English"],
                    "Science-Bio": ["Physics", "Chemistry", "Biology", "English"],
                    "Commerce": ["Accountancy", "Business Studies", "Economics", "English"],
                    "Arts": ["History", "Geography", "Political Science", "Sociology", "Psychology", "English"]
                }

                for subject in stream_subjects.get(stream, []):
                    row[subject] = subject_map.get(subject, 0)

                input_df = pd.DataFrame([row])
                expected_columns = [
                    'Class10%', 'Class11%', 'English',
                    'Accountancy', 'Business Studies', 'Economics',
                    'Physics', 'Chemistry', 'Maths', 'Biology',
                    'History', 'Geography', 'Political Science', 'Sociology', 'Psychology',
                    'Stream', 'Interest'
                ]

                # Fill missing columns with 0
                for col in expected_columns:
                    if col not in input_df.columns:
                        input_df[col] = 0.0

                # Reorder columns to match training order exactly
                input_df = input_df[expected_columns]

                input_scaled = scaler.transform(input_df)
                pred = model.predict(input_scaled)[0]
                prediction = label_encoders['PredictedCareer'].inverse_transform([pred])[0]

            except Exception as e:
                form_errors = [f"Prediction error: {str(e)}"]
        else:
            form_errors = ["Form is invalid or model failed to load."]
            print("Form errors:", form.errors)
    else:
        form = CareerForm()

    return render(request, "home/career_form.html", {
        "form": form,
        "prediction": prediction,
        "form_errors": form_errors
    })
