from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Club

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'student_id', 'department', 'phone')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'student_id', 'department', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            student_id=validated_data['student_id'],
            department=validated_data['department'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        return user

class ClubSerializer(serializers.ModelSerializer):
    leader_name = serializers.SerializerMethodField()  # 🔥 동아리장 이름 필드 추가

    class Meta:
        model = Club
        fields = ["id", "name", "leader_name", "advisor", "max_members", "current_members", "activity_schedule", "tags", "description"]

    def get_leader_name(self, obj):
        return obj.leader.name if obj.leader else "Unknown"  # 🔥 leader 객체에서 이름 가져오기