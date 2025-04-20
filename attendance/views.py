from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ClubSerializer
from .models import Club

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response(serializer.errors, status=400)

# ✅ 새로운 기능 추가 (동아리 생성)
@api_view(['POST'])
def create_club(request):
    data = request.data
    club_name = data.get("name")
    leader_email = data.get("leaderEmail")

    # ✅ leaderEmail을 이용해 CustomUser 인스턴스 찾기
    try:
        leader = User.objects.get(email=leader_email)
    except User.DoesNotExist:
        return Response({"error": "동아리장 정보가 올바르지 않습니다."}, status=400)

    # 그룹 생성
    group, created = Group.objects.get_or_create(name=club_name)

    # 동아리 모델 저장
    club = Club.objects.create(
        name=data.get("name"),
        leader=leader,  # 🔥 leader를 문자열이 아니라 CustomUser 인스턴스로 저장
        advisor=data.get("advisor"),
        max_members=int(data.get("maxMembers", 0)),  # 🔥 maxMembers를 정수로 변환
        current_members=0,
        activity_schedule=data.get("activitySchedule"),
        tags=data.get("tags"),
        description=data.get("description"),
        group=group  # 그룹 연결
    )

    return Response({"success": True, "club_id": club.id}, status=201)

# ✅ 새로운 기능 추가 (동아리 목록 조회)
@api_view(['GET'])
def get_clubs(request):
    clubs = Club.objects.all()
    serializer = ClubSerializer(clubs, many=True)
    return Response(serializer.data)


# API 엔드포인트 구현