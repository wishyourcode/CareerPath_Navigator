from django.contrib import admin
from django.urls import path, include 
from django.urls import path
from . import views
from home.views import pending_approvals, approve_faculty, reject_faculty
from home import views 
from django.conf import settings
from django.conf.urls.static import static
from contact import views as contact_views
urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', contact_views.contact_view, name='contact'),
    path('success/', contact_views.success_view, name='success'),
    path('explore/',views.explore, name= "explore"),
    path('dashboard/',views.dashboard, name= "dashboard"),
    path('Collage/',views.Collage, name= "Collage"),
    path('Consult/',views.Consult, name= "Consult"),
    path("index/", views.index, name="index"),
    path("index/<int:myid>/", views.quiz, name="quiz"), 
    path('index/<int:myid>/data/', views.quiz_data_view, name='quiz-data'),
    path('index/<int:myid>/save/', views.save_quiz_view, name='quiz-save'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('add_quiz/delete/<int:quiz_id>/confirm/', views.confirm_delete_quiz, name='confirm_quiz_delete'),
    path('add_quiz/delete/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('add_question/', views.add_question, name='add_question'),  
    path('add_options/<int:myid>/', views.add_options, name='add_options'), 
    path('results/', views.results, name='results'),    
    path('delete_question/<int:myid>/', views.delete_question, name='delete_question'),  
    path('delete_result/<int:myid>/', views.delete_result, name='delete_result'),
    path('clear-success-message/', views.clear_success_message, name='clear_success_message'),
    path('pending_approvals/', views.pending_approvals, name='pending_approvals'),
    path('approve/<int:user_id>/', views.approve_faculty, name='approve_faculty'),
    path('reject/<int:user_id>/', views.reject_faculty, name='reject_faculty'),
    path('approved-faculty/', views.approved_faculty, name='approved_faculty'),
    path('delete-faculty/<int:faculty_id>/', views.delete_faculty, name='delete_faculty'),
    path('students/', views.student_list_view, name='student_list'),
    path('students/<int:student_id>/confirm-delete/', views.confirm_student_delete_view, name='confirm_student_delete'),
    path('students/<int:student_id>/delete/', views.delete_student_view, name='delete_student'),
    path('career/', views.career_predict, name='career_predict')
]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
