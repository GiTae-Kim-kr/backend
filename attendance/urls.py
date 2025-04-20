from django.urls import path
from .views import RegisterView, LoginView, create_club, get_clubs

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # ✅ 동아리 관련 API 추가
    path('create-club/', create_club, name='create-club'),
    path('clubs/', get_clubs, name='get-clubs'),
]


#엔드포인트 설정