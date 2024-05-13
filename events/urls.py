from django.urls import path
from events import views

urlpatterns = [
    path('user',
         views.userForm.as_view(),
         name='user'),
]
