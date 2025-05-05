from django import forms
from .models import Quiz, Question, Answer
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'desc', 'number_of_questions', 'time')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'quiz')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'role', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RejectionForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter reason for rejection...',
            'class': 'form-control'
        }),
        required=True
    )
class CareerForm(forms.Form):
    # Basic Fields
    class10 = forms.IntegerField(label="Class 10 Marks", required=True)
    class11 = forms.IntegerField(label="Class 11 Marks", required=True)

    # Stream Choices
    STREAM_CHOICES = [
        ('Science-Maths', 'Science (Maths)'),
        ('Science-Bio', 'Science (Biology)'),
        ('Commerce', 'Commerce'),
        ('Arts', 'Arts'),
    ]
    stream = forms.ChoiceField(choices=STREAM_CHOICES, label="Stream", required=True)

    # Interest Choices
    INTEREST_CHOICES = [
    ("Engineering", "Engineering"),
    ("Medical", "Medical"),
    ("Accountant", "Accountant"),
    ("Design", "Design"),
    ("Teaching", "Teaching"),
    ("Law", "Law"),
    ("Civil Services", "Civil Services"),
    ("Research", "Research"),
]
    interest = forms.ChoiceField(choices=INTEREST_CHOICES, label="Interest", required=True)

    # Subject Fields (all subjects initially, but some will be hidden based on stream selection)
    physics = forms.FloatField(label="Physics", required=False)
    chemistry = forms.FloatField(label="Chemistry", required=False)
    maths = forms.FloatField(label="Maths", required=False)
    biology = forms.FloatField(label="Biology", required=False)
    english = forms.FloatField(label="English", required=False)
    accountancy = forms.FloatField(label="Accountancy", required=False)
    business_studies = forms.FloatField(label="Business Studies", required=False)
    economics = forms.FloatField(label="Economics", required=False)
    history = forms.FloatField(label="History", required=False)
    geography = forms.FloatField(label="Geography", required=False)
    political_science = forms.FloatField(label="Political Science", required=False)
    sociology = forms.FloatField(label="Sociology", required=False)
    psychology = forms.FloatField(label="Psychology", required=False)

    def clean(self):
        cleaned_data = super().clean()
        # You can add any additional form validation here if needed
        return cleaned_data
