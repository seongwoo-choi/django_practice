from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
    # django.contrib.auth 앱의 LoginView 클래스를 활용 했으므로 별도의 views.py 파일 수정이 필요 없다!
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]