from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Quiz(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    number_of_questions = models.IntegerField(default=1)
    time = models.IntegerField(help_text="Duration of the quiz in minutes", default=1)  # Changed to minutes
    
    def __str__(self):
        return self.name

    def get_questions(self):
        return self.question_set.all()

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.TextField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Question: {self.question.text}, Answer: {self.text}, Correct: {self.correct}"

class Marks_Of_User(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()
    
    def __str__(self):
        return str(self.quiz)

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)  # Faculty approval status
    rejection_reason = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Auto-approve non-faculty users
        if self.role != 'faculty':
            self.is_approved = True
        super().save(*args, **kwargs)